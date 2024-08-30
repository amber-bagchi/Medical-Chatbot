from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone
from pymongo import MongoClient
from bson.objectid import ObjectId
import os



class AppointmentManager:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def close(self):
        self.client.close()

    def check_availability(self, doctor_name, desired_time):
        doctor = self.db.doctors.find_one({"doctor_name": doctor_name})
        if not doctor:
            return False, "Doctor not found."
        
        # Check if an appointment already exists for the desired time
        existing_appointment = self.db.appointments.find_one({
            "doctor_id": doctor["_id"],
            "appointment_time": desired_time
        })
        
        if existing_appointment:
            return False, "The desired time is not available. Please choose another time."
        
        return True, None

    def book_appointment(self, doctor_name, patient_name, desired_time):
        is_available, message = self.check_availability(doctor_name, desired_time)
        if not is_available:
            return message
        
        doctor = self.db.doctors.find_one({"doctor_name": doctor_name})
        
        # Create a new appointment
        self.db.appointments.insert_one({
            "doctor_id": doctor["_id"],
            "patient_name": patient_name,
            "appointment_time": desired_time,
            "appointment_status": "confirmed"
        })
        
        return f"Your appointment is confirmed with {doctor_name} at {desired_time}."

mongo_uri = os.getenv("MONGO_URI")
mongo_db = "medical_db"
appointment_manager = AppointmentManager(mongo_uri, mongo_db)



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