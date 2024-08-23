from flask import Flask, render_template,jsonify,request
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



app = Flask(__name__)

load_dotenv()  

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

embeddings = download_hugging_face_embedding()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "mchatbot" # index name created in pinecone

index = pc.Index('mchatbot')

# Define the Pinecone vector store for Langchain
docsearch = PineconeVectorStore(index=index, embedding=embeddings, text_key="text")

PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs={"prompt": PROMPT}


KEY=os.getenv("HUGGINGFACE_API_KEY")

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
    return cleaned_text


# Define the index route to serve the chat HTML page
@app.route("/")
def index():
    return render_template('chat.html')

# Define the chat route to handle POST requests
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    result = qa({"query": msg})
    answer = clean_response(result["result"])
    print("Response:", answer)
    return str(answer)

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)