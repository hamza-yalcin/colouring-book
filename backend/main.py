from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import io
import numpy as np
import cv2


app = Flask(__name__)
CORS(app)

def convert_to_coloring_image(image, threshold=100):
    image_np = np.array(image)

    # Convert to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, threshold1=threshold, threshold2=threshold * 2)

    # Invert colors for a white background and black edges
    inverted_edges = cv2.bitwise_not(edges)

    # Remove small noise using morphological opening
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # Adjust kernel size if needed
    cleaned_edges = cv2.morphologyEx(inverted_edges, cv2.MORPH_OPEN, kernel)

    # Convert back to a PIL image
    coloring_image = Image.fromarray(cleaned_edges)

    return coloring_image



@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error: image not uploaded'}), 400
    
    uploadedFile = request.files['image']
    try:
        image = Image.open(uploadedFile.stream)
    except Exception as e:
        return jsonify({'error': 'failed to process image'}), 400

    threshold = int(request.args.get('threshold', 100))

    coloringImage = convert_to_coloring_image(image, threshold)

     # Save to an in-memory file to send as a response
    img_io = io.BytesIO()
    coloringImage.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)