from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import os
import shutil


openai_api_key = "sk-proj-2AEe3BQClelVFDeE5kIvT3BlbkFJ1WE6IKEN5bJbHqIoe1iJ" 
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

CHROMA_PATH = "chroma"
DATA_PATH = "data/Files"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1300,
        chunk_overlap=300,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    
    # Get paths of files added to the database
    added_files = [os.path.join(CHROMA_PATH, file_name) for file_name in os.listdir(CHROMA_PATH)]
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}. Files added: {added_files}")
    return f"Saved {len(chunks)} chunks to {CHROMA_PATH}. Files added: {added_files}"



if __name__ == "__main__":
    main()
