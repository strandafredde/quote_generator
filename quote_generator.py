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


def draw_text_wrapped(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        # Check the width of the line with the new word
        test_line = current_line + ' ' + word
        bbox = draw.textbbox((0, 0), test_line, font=font)

        # If the line exceeds the maximum width, start a new line
        if bbox[2] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    # Add the last line
    lines.append(current_line)

    return lines


def img_with_quote():
    quote = pow.quote_random(2, False)
    api_url = 'https://picsum.photos/800/600'
    response = requests.get(api_url)

    # Open the image using PIL
    image = Image.open(BytesIO(response.content))

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Use a default font size
    font_size = 35

    # Load a default font with the initial font size
    font = ImageFont.truetype("arial.ttf", font_size)

    # Define a maximum width for the text (adjust as needed)
    max_text_width = 0.8 * image.width

    # Get the wrapped lines of text
    lines = draw_text_wrapped(draw, quote, font, max_text_width)

    # Calculate text position
    text_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines)
    text_position = ((image.width - max_text_width) // 2, (image.height - text_height) // 2)

    # Draw each line of text
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]
        draw.text((text_position[0], text_position[1]), line, font=font, fill=(255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0))
        text_position = (text_position[0], text_position[1] + line_height)

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
