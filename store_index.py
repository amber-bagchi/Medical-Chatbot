from src.helper import load_pdf, text_splitter, download_hugging_face_embedding, batch_upsert
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

#print(PINECONE_API_KEY)

#calling the data extraction function and storing it in extracted_data
extracted_data = load_pdf("data/")

#Calling the chunks function to create chunks of extracted data and store it in text_chunks 
text_chunks = text_splitter(extracted_data)

embeddings = download_hugging_face_embedding()


pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "mchatbot" # index name created in pinecone

index = pc.Index('mchatbot')

# Extract text content from document objects
texts = [doc.page_content for doc in text_chunks]

# Convert text data into embeddings
embedding_vectors = embeddings.embed_documents(texts)

#function for converting the vectors into pinecone input format like id and value
vectors_to_upsert = [
    {"id": str(i), "values": vector, "metadata": {"text": texts[i]}}
    for i, vector in enumerate(embedding_vectors)
]

# Upsert the vectors into Pinecone index in batches
batch_upsert(index, vectors_to_upsert, batch_size=50)


