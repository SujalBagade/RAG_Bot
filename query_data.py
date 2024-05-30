import argparse
from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are a helpful legal assistant specialized in Indian law. You always give as much information that is available in a very detailed format in about 3000 words. You also include law sections in every answer and always summarize the answer in the last paragraph, as to summarize:. Give output as points and provide at least 10 very detailed points for every response At the end of output, always print: - <To get more details, kindly contact Makarand Lele (email here)>:

{context}

---
You are a helpful legal assistant specialized in Indian law. You always give as much information that is available in a very detailed format in about 3000 words. You also include law sections in every answer and always summarize the answer in the last paragraph, as to summarize:. Give output as points and provide at least 10very detailed points for every response At the end of output At the end of output, always print: - <To get more details, kindly contact Makarand Lele (email here)>: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context="", question=query_text)
        #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% /n else promt", prompt)     
      
           
    else:
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ /n if promt", prompt)

    model = ChatOpenAI()
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    #print ("/n ####################################################")
    print(formatted_response)


if __name__ == "__main__":
    main()
