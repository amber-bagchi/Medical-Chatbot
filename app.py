from flask import Flask, render_template,jsonify,request
from src.helper import download_hugging_face_embedding
from langchain.vectorstores import Pinecone
from pinecone import Pinecone
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain.vectorstores import Pinecone as LangchainPinecone
import os
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub import login  
from src.prompt import *
from dotenv import load_dotenv



app = Flask(__name__)

load_dotenv()  

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

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

llm =HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    temperature= 0.5,
    token=KEY
)

qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080, debug=True)