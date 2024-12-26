from dotenv import load_dotenv 
import os

load_dotenv("E:/UdacityProject/FullStackWeb/Capstone/.env") 
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
DATABASE_URL = os.getenv("DATABASE_URL")