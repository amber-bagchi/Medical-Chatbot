End-to-end-Medical-Chatbot-using-Llama3
How to run?
STEPS:
Clone the repository

Project repo: https://github.com/
STEP 01- Create a conda environment after opening the repository
conda create -n mchatbot python=3.8 -y
conda activate mchatbot
STEP 02- install the requirements
pip install -r requirements.txt
Create a .env file in the root directory and add your Pinecone credentials as follows:
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


##Authenticate and Initialize the Hugging Face Llama Model
To set up the medical chatbot, you need to authenticate with Hugging Face and initialize the language model. Follow these steps:

Retrieve API Key:

The Hugging Face API key is securely retrieved from your environment variables using os.getenv("HUGGINGFACE_API_KEY"). Make sure the API key is stored in your environment variables.
Authenticate with Hugging Face:

Use the login(KEY) function to authenticate your session with Hugging Face. This allows you to access and use various models hosted on the platform.
Initialize the Language Model:

The code initializes the Llama model using HuggingFaceEndpoint. The model specified is meta-llama/Meta-Llama-3-8B-Instruct, which is configured with a temperature setting of 0.5 to control the variability of the generated responses.
The token=KEY parameter ensures that your API requests are authenticated.
Ensure that your environment is set up with the necessary API key and that the model is correctly initialized for the chatbot to generate meaningful responses.


# run the following command
python store_index.py
# Finally run the following command
python app.py
Now,

open up localhost:
Techstack Used:
Python
LangChain
Flask
Hugging Face Hub
Pinecone
