from flask import Flask, render_template, jsonify, request, send_file
from src.helper import download_hugging_face_embedding
from langchain.vectorstores import Pinecone
from pinecone import Pinecone
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain.vectorstores import Pinecone as LangchainPinecone
import os
import re
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub import login  
from src.prompt import *
from dotenv import load_dotenv
from text_to_speech import text_to_speech
from src.helper import appointment_manager
from database_neo4j import db_manager
from database_neo4j import HospitalDatabaseManager


app = Flask(__name__)

load_dotenv()  

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

embeddings = download_hugging_face_embedding()

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "mchatbot" # index name created in pinecone

index = pc.Index('mchatbot')

# Define the Pinecone vector store for Langchain
docsearch = PineconeVectorStore(index=index, embedding=embeddings, text_key="text")

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

KEY = os.getenv("HUGGINGFACE_API_KEY")

login(KEY)
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    temperature=0.6,
    max_tokens=150,             
    token=KEY
)

# Initialize the RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs
)

import re

def clean_response(text):
    # Remove disclaimers or repetitive content
    text = re.sub(r'(?i)if you don\'t know the answer,.*', '', text)
    text = re.sub(r'(?i)please note that this information.*', '', text)
    
    # Remove any content after specific phrases like "Note:", "Best regards,", or "[Your Name]"
    text = re.split(r"(Note:|Best regards,|\[Your Name\])", text)[0]

    # Remove duplicate sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    seen = set()
    cleaned_sentences = []
    for sentence in sentences:
        if sentence.strip() and sentence not in seen:
            cleaned_sentences.append(sentence.strip())
            seen.add(sentence.strip())
    
    cleaned_text = ' '.join(cleaned_sentences).strip()

    # Add the disclaimer about consulting a doctor
    disclaimer = "Please remember, while I strive to provide accurate and helpful advice, it's important to consult with a healthcare professional before starting any medication. Your health and safety are my top priorities!"
    cleaned_text += disclaimer

    return cleaned_text

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"].lower()  # Convert to lowercase for easier matching
    response_text = ""
    
    # Determine if the user's query is about hospital services or doctors
    if "services" in msg:
        response_text = db_manager.get_services_info()
    elif "doctors" in msg or "doctor" in msg:
        response_text = db_manager.get_doctors_info()
    else:
        # If not a direct request for hospital info, query the LLM
        result = qa({"query": msg})
        response_text = clean_response(result["result"])
    
    # Generate the audio response
    audio_file = text_to_speech(response_text)
    audio_url = f"/audio/{os.path.basename(audio_file)}"
    
    return jsonify({"text": response_text, "audio": audio_url})

@app.route('/audio/<filename>', methods=["GET"])
def get_audio(filename):
    audio_path = os.path.join("audio", filename)  # Assume the audio files are stored in the 'audio' directory
    return send_file(audio_path, mimetype="audio/mpeg")


@app.route("/book_appointment", methods=["POST"])
def book_appointment():
    doctor_name = request.form["doctor_name"]
    patient_name = request.form["patient_name"]
    desired_time = request.form["desired_time"]
    
    # Convert desired_time to proper format (ISODate)
    response = appointment_manager.book_appointment(doctor_name, patient_name, desired_time)
    
    return jsonify({"text": response})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
