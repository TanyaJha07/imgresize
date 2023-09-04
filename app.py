import os
from flask import Flask, request, render_template, send_from_directory
from PIL import Image

app = Flask(__name__)

# Define the upload and resized image directories
UPLOAD_FOLDER = 'uploads'
RESIZED_FOLDER = 'resized'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESIZED_FOLDER'] = RESIZED_FOLDER

# Function to resize an image
def resize_image(input_path, output_path, size):
    try:
        image = Image.open(input_path)
        image.thumbnail(size)
        image.save(output_path)
        return True
    except Exception as e:
        print(f"Error resizing image: {str(e)}")
        return False

# Route to upload and resize an image
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    width = request.form.get('width')
    height = request.form.get('height')

    if not width or not height:
        return "Please provide both width (x) and height (y) dimensions"
    
    try:
        width = int(width)
        height = int(height)
        if width <= 0 or height <= 0:
            return "Width (x) and height (y) dimensions must be positive integers"
    except ValueError:
        return "Width (x) and height (y) dimensions must be valid integers"

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Resize the uploaded image and save it to the resized folder
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['RESIZED_FOLDER'], filename)
        resize_image(input_path, output_path, (width, height))
        
        return send_from_directory(app.config['RESIZED_FOLDER'], filename)

# Route to display the resized image
@app.route('/resized/<filename>')
def resized_file(filename):
    return send_from_directory(app.config['RESIZED_FOLDER'], filename)

# Route to the upload form
@app.route('/')
def index():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
