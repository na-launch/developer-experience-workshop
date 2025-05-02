from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def hello():
    country = os.environ.get('countryCode')
    if country and len(country) == 2:
        translation = translations.get(country.upper())
        if translation:
            return translation
        else:
            return "Translation not available for this country.", 404
    return "Hello World!"


translations = {
    "EN": "Hello World!",
    "SP": "¡Hola Mundo!",
    "FR": "Bonjour le monde!",
    "DE": "Hallo Welt!",
    "IT": "Ciao Mondo!",
    "SW": "Hej världen!"
}

if __name__ == "__main__":
    app.run(debug=True)