from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone

#functions for extracting the data
def load_pdf(data):
    loader = DirectoryLoader(data,
                             glob="*.pdf",
                             loader_cls=PyPDFLoader)
    
    documents = loader.load()

    return documents

#function for creating the chuncks of the extracting data
def text_splitter(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks

#function for downloading the Hugging Face Embeddging Model
def download_hugging_face_embedding():
    embeddings = SentenceTransformerEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

# Function to upsert vectors in batches
def batch_upsert(index, vectors, batch_size=100):
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)