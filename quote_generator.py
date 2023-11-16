from flask import Flask, render_template
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import base64
import os
from pyofwar import pow

app = Flask(__name__)

# Set the template folder explicitly
template_folder = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=template_folder)


def img_with_quote():
    quote = pow.quote_random(2, False)
    api_url = 'https://picsum.photos/800/600'
    response = requests.get(api_url)

    # Open the image using PIL
    image = Image.open(BytesIO(response.content))

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Use a default font and size
    font = ImageFont.truetype("arial.ttf", 15)

    # Calculate text position
    text_bbox = draw.textbbox((0, 0), quote, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_position = ((image.width - text_width) // 2, (image.height - text_height) // 2)

    # Add the quote to the image
    draw.text(text_position, quote, font=font, fill=(255, 255, 255))

    # Save the modified image back to BytesIO
    modified_image_data = BytesIO()
    image.save(modified_image_data, format='JPEG')

    # Encode the image data as base64
    encoded_image_data = base64.b64encode(modified_image_data.getvalue()).decode('utf-8')

    return encoded_image_data


@app.route('/')
def index():
    return render_template('index.html', image_data=img_with_quote())


if __name__ == '__main__':
    app.run(debug=True)
