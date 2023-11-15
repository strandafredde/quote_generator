from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# Set the template folder explicitly
template_folder = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=template_folder)

@app.route('/')
def index():
    # Picsum Photos API URL
    api_url = 'https://picsum.photos/800/600'
    
    # Directly use the URL from the API
    image_url = api_url

    return render_template('index.html', image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
