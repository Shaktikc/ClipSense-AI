from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.environ["API_KEY"]
MODEL_NAME = "mistral-large-latest"