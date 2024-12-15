from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageFilter, ImageOps
import io

app = Flask(__name__)
CORS(app)

def convert_to_coloring_image(image):
    # convert to grayscale
    grayImage = ImageOps.grayscale(image)
    # apply edge detection
    edges = grayImage.filter(ImageFilter.FIND_EDGES)
    # invert colors for coloring book effect
    coloringImage = ImageOps.invert(edges)
    return coloringImage


@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error: image not uploaded'}), 400
    
    uploadedFile = request.files['image']
    image = Image.open(uploadedFile.stream)

    coloringImage = convert_to_coloring_image(image)

     # Save to an in-memory file to send as a response
    img_io = io.BytesIO()
    coloringImage.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)