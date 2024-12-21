from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageFilter, ImageOps
import io
import numpy as np

app = Flask(__name__)
CORS(app)

def convert_to_coloring_image(image, threshold=50):
    # convert to grayscale
    grayImage = ImageOps.grayscale(image)
    # apply edge detection
    edges = grayImage.filter(ImageFilter.FIND_EDGES)
    np_edges = np.array(edges) # convert to numpy array

    # threshold for enhancing dark lines on image
    np_edges = np.where(np_edges < threshold, 0, 255).astype(np.uint8) # make dark areas black, rest white

    # invert colors for coloring book effect
    coloringImage = Image.fromarray(255 - np_edges)
    return coloringImage


@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error: image not uploaded'}), 400
    
    uploadedFile = request.files['image']
    try:
        image = Image.open(uploadedFile.stream)
    except Exception as e:
        return jsonify({'error': 'failed to process image'}), 400

    threshold = int(request.args.get('threshold', 50))

    coloringImage = convert_to_coloring_image(image, threshold)

     # Save to an in-memory file to send as a response
    img_io = io.BytesIO()
    coloringImage.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)