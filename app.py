from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
from routes.main import main as main_blueprint

app.register_blueprint(main_blueprint)