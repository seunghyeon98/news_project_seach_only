import requests
from dotenv import load_dotenv
import os
load_dotenv()


url = "https://api.deepl.com/v2/translate"
params = {
    "auth_key": os.getenv('DEEPL_API_KEY') ,
    "text": "Hello, world!",
    "source_lang": "EN",
    "target_lang": "KO"
}

response = requests.post(url, data=params)
print(response.json())