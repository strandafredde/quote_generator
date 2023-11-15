import requests
from flask import Flask, render_template
from pyofwar import pow
img = requests.get("https://picsum.photos/800/600")

app = Flask(__name__)
@app.route("/")
def index():
    
    return "deez"


app.run(debug=True)
# print("Sun Tzu once said...")
# print(pow.quote_random(1, False))