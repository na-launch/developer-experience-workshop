from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Blueprint, jsonify, request, abort, Response, render_template
import json
import os
import requests
import random


DEFAULT_COUNTRY_CODE = "en"     # HINT: The easter egg will ask you to change this

main = Blueprint('main', __name__)

def get_translation(country_code):
    try:
        with open("translations.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        translations = data.get("translations", {})
        translation = translations.get(country_code.upper())
        if not translation:
            raise Exception("Translation not found for the specified country code.")
        return translation
    except Exception as e:
        raise e

def get_current_datetime():
        # Set timezone to New York
        timeByZone = datetime.now(ZoneInfo("America/New_York"))
        # Format the time as "HH:MM MM/DD/YYYY"
        return timeByZone.strftime("%H:%M %m/%d/%Y")


# OPTIONAL: Python version older than 3.9 you can use pytz
# import pytz
# def get_current_datetime():
#     # Set timezone to New York
#     tz = pytz.timezone("America/New_York")
#     new_york_time = datetime.now(tz)
#     # Format the time as "HH:MM MM/DD/YYYY"
#     return new_york_time.strftime("%H:%M %m/%d/%Y")

@main.route("/api/health", methods=["GET"])
def health():
    try:
        return "OK", 200
    except Exception:
        return "Service Unhealthy", 500

@main.route("/api/admin")
def admin_panel():    
    if request.args.get("password") == "opensesame":        
        response = requests.get(os.getenv("ADMIN"))
        if response.ok:
            data = json.loads(response.text)
            pretty_json = json.dumps(data, indent=4)
            
            # Wrap in <pre> so the browser displays newlines and spacing
            return f"<pre>{pretty_json}</pre>"
        else:
            abort(500, description="There was a problem calling the API, please review your parameters")
    return abort(403, description="Forbidden")

@main.route("/api/version", methods=["GET"])
def version():
    return "0.0.1", 200

@main.route("/", methods=["GET"])
def index():
    try:
        translation = get_translation(DEFAULT_COUNTRY_CODE).lower()
        current_time = get_current_datetime()
    except Exception as e:
        abort(500, description=str(e))
    return render_template("index.html", 
                           greeting=translation, 
                           current_time=current_time)



#--------------------#
#    BONUS METHODS   #
#--------------------#

@main.route("/api/query", methods=["GET"])
def query_greeting():
    '''
    Route added for /api/query - this will find the country based on a query string of the country code
    '''
    # Get the country code from the query parameter
    country_code = request.args.get("countryCode")
    if not country_code:
        abort(400, description="The query parameter 'countryCode' is required.")
    try:
        # Get the greeting based on the provided country code
        translation = get_translation(country_code)
        current_time = get_current_datetime()
        return Response(f"{translation} @ {current_time}", mimetype='text/plain')
    except Exception as e:
        abort(500, description=str(e))



@main.route("/api/query", methods=["POST"])
def query_greeting_post():
    """
    Works the same as the GET version of /api/query but accepts data via POST.
    It first checks if the request content type is JSON, otherwise it falls back to form data.

    Examples:
    curl -X POST -H "Content-Type: application/json" -d '{"countryCode": "en"}' http://localhost:5000/api/query
    curl -X POST -d "countryCode=en" http://localhost:5000/api/query

    """
    if request.is_json:
        data = request.get_json()
        country_code = data.get("countryCode")
    else:
        country_code = request.form.get("countryCode")

    if not country_code:
        abort(400, description="The parameter 'countryCode' is required in the POST data.")

    try:
        translation = get_translation(country_code)
        current_time = get_current_datetime()
        return Response(f"{translation} @ {current_time}", mimetype='text/plain')
    except Exception as e:
        abort(500, description=str(e))


@main.route("/api/magic8", methods=["GET"])
def magic8():
    """
    Returns a random country greeting.
    Reads all translations from the JSON file, picks one random key,
    and returns the corresponding greeting with its country code in plain text.
    """
    try:
        with open("translations.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        translations = data.get("translations", {})
        if not translations:
            abort(500, description="No translations available.")
        # Randomly select a country code and its greeting
        random_country_code = random.choice(list(translations.keys()))
        random_greeting = translations[random_country_code]
        # Return the greeting in plain text, similar to /api/query
        return Response(f"{random_greeting} (Country: {random_country_code})", mimetype="text/plain")
    except Exception as e:
        abort(500, description=str(e))