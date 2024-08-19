# 🩺 End-to-End Medical Chatbot using Llama3
Welcome to the End-to-End Medical Chatbot using Llama3 project! This project showcases a comprehensive medical chatbot built using advanced technologies to assist users with medical inquiries.

## 📋 Project Overview
This chatbot leverages the power of the Llama3 model from Hugging Face to provide intelligent and context-aware responses. It integrates with Pinecone for vector database operations and is developed using Flask for a seamless web interface.

## 🚀 How to Run
Follow these steps to get the project up and running on your local machine:

### 1️⃣ Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/amber-bagchi/Medical-Chatbot.git
```
```bash
cd End-to-End-Medical-Chatbot-using-Llama3

```

### 2️⃣ Create and Activate a Conda Environment
Create a Conda environment with Python 3.8:
```bash
conda create -n mchatbot python=3.8 -y
```
```bash
conda activate mchatbot
```

### 3️⃣ Install Requirements
Install the necessary packages:
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a .env file in the root directory and add your Pinecone credentials:
```bash
PINECONE_API_KEY=your_pinecone_api_key
```
```bash
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

### 5️⃣ Authenticate and Initialize the Hugging Face Llama Model
- Retrieve API Key: Ensure your Hugging Face API key is stored in your environment variables.
- Authenticate with Hugging Face: Use the login(KEY) function to authenticate your session.
- Initialize the Language Model: Configure the Llama model meta-llama/Meta-Llama-3-8B-Instruct with a temperature setting of 0.5.

### 6️⃣ Run the Application
First, run the script to store the index:
```bash
python store_index.py
```
```bash
python app.py
```
### 🛠 Tech Stack
- Python
- LangChain
- Flask
- Hugging Face Hub
- Pinecone

## 📸 Screenshots

Here is a screenshot of the application:

![mchatb](https://github.com/user-attachments/assets/8b81760c-f299-4637-9c6f-e0745b55a595)

## License

This project is licensed under the MIT License. See the LICENSE
[MIT](https://choosealicense.com/licenses/mit/) file for more details.
