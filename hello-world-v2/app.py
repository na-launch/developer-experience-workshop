from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Dictionaries for greetings and corresponding flag image URLs.
translations = {
    "EN": "Hello World!",
    "SP": "¡Hola Mundo!",
    "FR": "Bonjour le monde!",
    "DE": "Hallo Welt!",
    "IT": "Ciao Mondo!",
    "SW": "Hej världen!"
}

# Updated flags dictionary: using US flag for EN.
flags = {
    "EN": "https://flagcdn.com/w320/us.png",   # American flag for English
    "SP": "https://flagcdn.com/w320/es.png",     # Spanish flag
    "FR": "https://flagcdn.com/w320/fr.png",     # French flag
    "DE": "https://flagcdn.com/w320/de.png",     # German flag
    "IT": "https://flagcdn.com/w320/it.png",     # Italian flag
    "SW": "https://flagcdn.com/w320/se.png",     # Swedish flag (adjust if needed)
}

@app.route("/")
def hello():
    # Read the country code from the environment variable.
    country = os.environ.get("countryCode", "EN").upper()

    # Lookup greeting and flag based on the country code.
    greeting = translations.get(country, "Hello World!")
    flag_url = flags.get(country, flags.get("EN"))

    # HTML template that displays the greeting and flag.
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Hello World!</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
          body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f4; }
          h1 { font-size: 2.5em; color: #333; }
          .flag { vertical-align: middle; width: 80px; margin-left: 20px; border: 1px solid #ccc; }
      </style>
    </head>
    <body>
      <h1>
        {{ greeting }}
        <img class="flag" src="{{ flag_url }}" alt="Flag of {{ country }}">
      </h1>
    </body>
    </html>
    """
    return render_template_string(html_template, greeting=greeting, flag_url=flag_url, country=country)

if __name__ == "__main__":
    app.run(debug=True)