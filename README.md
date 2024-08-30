
# 🩺 End-to-End Medical Chatbot with Voice Assistant using Llama3
Welcome to the End-to-End Medical Chatbot using Llama3 project! This project showcases a comprehensive medical chatbot built using advanced technologies to assist users with medical inquiries. It also includes a Voice Assistant for voice interaction and now features an appointment booking system.

## 📋 Project Overview
This chatbot leverages the power of the Llama3 model from Hugging Face to provide intelligent and context-aware responses. It integrates with Pinecone for vector database operations and MongoDB for appointment booking. Developed using Flask, it offers a seamless and interactive web interface.

## 🎯 Features
 - 🧠 LLM-Powered Responses: The chatbot uses an advanced language model to understand and respond to user queries.
 - 🎤 Voice Input: Interact with the bot using your voice for a more accessible experience.
- ⚡ Real-Time Responses: Get instant answers to your questions without delay.
- 💬 Interactive UI: Enjoy a visually appealing and easy-to-navigate interface.
- 📅 Appointment Booking: Users can book medical appointments, which are stored in MongoDB.

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
Create a .env file in the root directory and add your credentials:

```bash
PINECONE_API_KEY=your_pinecone_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
MONGO_URI=your_mongodb_connection_uri
```
### 5️⃣ Authenticate and Initialize the Hugging Face Llama Model
#### - Retrieve API Key: Ensure your Hugging Face API key is stored in your environment variables.
#### - Authenticate with Hugging Face: Use the login(KEY) function to authenticate your session.
#### - Initialize the Language Model: Configure the Llama model meta-llama/Meta-Llama-3-8B-Instruct with a temperature setting of 0.5.

  
### 6️⃣ Set Up MongoDB for Appointment Booking
Ensure MongoDB is running and accessible. The application uses MongoDB to store appointment details.

### 7️⃣ Run the Application

#### First, run the script to store the index:

```bash
python store_index.py
```

#### Then, run the Flask application:

```bash
python app.py
```

## 🛠 Tech Stack
- Python
- LangChain
- Flask
- Hugging Face Hub
- Pinecone
- MongoDB

## 🤝 Contributing
Feel free to fork this repository, make improvements, and submit pull requests. Your contributions are always welcome!

## 📸 Video
Here is a video of the application:

![Screenshot 2024-08-30 021320](https://github.com/user-attachments/assets/045999f7-1bce-4b36-a360-349c1cafbd43)



## License
This project is licensed under the MIT License. See the LICENSE MIT file for more details
