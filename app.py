from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
import pandas as pd
from datetime import datetime
import csv
from werkzeug.utils import secure_filename
from create_database import main as create_db_main
from convert import convert_all_pdfs_to_md


CHROMA_PATH = "chroma"
CSV_FILE_PATH = "query_responses.csv"  # Path to the CSV file for storing query responses
DATA_PATH = "data/Files"
PROMPT_TEMPLATE = """
You are a helpful legal assistant specialized in Indian law. You always give as much information that is available in a very detailed format in about 3000 words. Give output as points and provide at least 15-20 very detailed points for every response:

Referring to: {context}

---
Answer
{component}: {question} 
{other}

Display answer in proper markdown format in very detailed points in about 100-150 words each and summarize the answer in the last paragraph with heading: In summary, Also include all relevant law sections separately with proper MD formatting. 
"""

app = Flask(__name__)
CORS(app)

def save_to_csv(query, response):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    data = {"Timestamp": timestamp, "Query": query, "Response": response}

    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Timestamp", "Query", "Response"])
            writer.writeheader()
            writer.writerow(data)
    else:
        with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Timestamp", "Query", "Response"])
            writer.writerow(data)

@app.route("/query", methods=["POST"])
def query():
    query_text = request.json["query_text"]
    component = request.json["component"]
    other = request.json["other"]

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context="", question=query_text, component=component, other=other)
    else:
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text, component=component, other=other)

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    save_to_csv(query_text, response_text)  # Save query and response to CSV file

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = {"response": response_text, "sources": sources}
    return jsonify(formatted_response)

@app.route("/create_database", methods=["POST"])
def database():
    r = create_db_main()  # Call the create_database function
    print(r)
    return jsonify({"message": "Database Created Successfully !!! "})

# Route to list file names in the /data/input_pdf folder
@app.route("/list_files", methods=["GET"])
def list_files():
    input_pdf_dir = "data/Files"
    file_names = os.listdir(input_pdf_dir)
    return jsonify({"files": file_names})

# Route to delete multiple files from the /data/Files directory
@app.route("/delete_files", methods=["DELETE"])
def delete_files():
    # Get the list of file names from the request JSON data
    file_names = request.json.get("file_names", [])

    deleted_files = []
    not_found_files = []

    # Loop through each file name and attempt deletion
    for file_name in file_names:
        file_path = os.path.join("data/Files", file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            deleted_files.append(file_name)
        else:
            not_found_files.append(file_name)

    response_message = {
        "deleted_files": deleted_files,
        "not_found_files": not_found_files
    }

    return jsonify(response_message)

# Route to display stored queries along with responses
@app.route("/display_queries", methods=["GET"])
def display_queries():
    if os.path.exists(CSV_FILE_PATH):
        df = pd.read_csv(CSV_FILE_PATH)
        data = df.to_dict(orient="records")
    else:
        data = []

    return jsonify(data)

UPLOAD_FOLDER = 'data/input_pdf'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'files[]' not in request.files:
        return jsonify({"error": "No files part"})

    files = request.files.getlist('files[]')

    if not files:
        return jsonify({"error": "No selected files"})

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return jsonify({"error": "File upload failed or invalid file format"})

    return jsonify({"message": f"{len(files)} files uploaded successfully"})


@app.route('/pdf/<path:filename>', methods=['GET'])
def download_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/list_pdfs', methods=['GET'])
def list_pdfs():
    pdf_files = []
    pdf_dir = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_files.append(filename)
    return jsonify({"pdf_files": pdf_files})

@app.route('/convert_pdf_to_md', methods=['POST'])
def convert_pdf_to_md():
    input_directory = app.config['UPLOAD_FOLDER']
    output_directory = DATA_PATH
    convert_all_pdfs_to_md(input_directory, output_directory)
    return jsonify({"message": "PDFs converted to Markdown successfully"})



if __name__ == "__main__":
    app.run(debug=True)
