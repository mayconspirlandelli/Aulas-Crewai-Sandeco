from dotenv import load_dotenv
import os

load_dotenv()  # carrega variáveis do .env

print("API KEY:", os.getenv("GOOGLE_API_KEY"))
