from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Testing purposes
from routes.main import get_translation
from routes.main import get_current_datetime

# Register routes
from routes.main import main as main_blueprint

app.register_blueprint(main_blueprint)