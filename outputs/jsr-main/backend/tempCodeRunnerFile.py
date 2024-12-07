# app.py
import os
from flask import Flask, render_template, request, send_from_directory
import requests
from PIL import Image, ImageDraw
import numpy as np
import uuid
import imghdr  # For image type validation

app = Flask(__name__)

# Ensure upload and output directories exist
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Allowed image types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

# Roboflow API configuration
API_KEY = "msvaHK2lfsfvfg0VAKWZ"
PROJECT_ID = "project-r-5e4dz"
MODEL_VERSION = "1"
API_URL = f"https://detect.roboflow.com/{PROJECT_ID}/{MODEL_VERSION}?api_key={API_KEY}"

def allowed_file(filename):
    """Check if the file has an allowed image extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(filepath):
    """Validate that the file is actually an image"""
    try:
        # Attempt to open the image and verify its type
        with Image.open(filepath) as img:
            img.verify()  # Verify that it's a valid image
        
        # Double-check the image type
        image_type = imghdr.what(filepath)
        if not image_type:
            raise ValueError("Could not determine image type")
        
        return True
    except Exception as e:
        print(f"Image validation error: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        
        # Check file extension
        if not allowed_file(file.filename):
            return render_template('index.html', error='Invalid file type. Please upload an image.')
        
        # Generate unique filename
        filename = str(uuid.uuid4()) + '_' + file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Validate the image
            if not validate_image(filepath):
                os.remove(filepath)  # Remove invalid file
                return render_template('index.html', error='Invalid image file')
            
            # Perform segmentation
            original_image, segmented_image, pixel_count = segment_image(filepath)
            
            # Save output images
            original_path = os.path.join(OUTPUT_FOLDER, f'original_{filename}')
            segmented_path = os.path.join(OUTPUT_FOLDER, f'segmented_{filename}')
            
            # Ensure the image is saved in a standard format
            original_image.convert('RGB').save(original_path, 'JPEG')
            segmented_image.convert('RGB').save(segmented_path, 'JPEG')
            
            return render_template('result.html', 
                                   original_image=f'outputs/original_{filename}', 
                                   segmented_image=f'outputs/segmented_{filename}',
                                   pixel_count=pixel_count)
        
        except Exception as e:
            # Remove temporary file
            if os.path.exists(filepath):
                os.remove(filepath)
            return render_template('index.html', error=f'Processing error: {str(e)}')
    
    return render_template('index.html')

def segment_image(image_path, max_size=1024):
    """
    Segment image with optional resizing to handle large images
    """
    # Open the original image
    original_image = Image.open(image_path).convert("RGBA")
    
    # Resize image if too large to prevent API issues
    width, height = original_image.size
    if max(width, height) > max_size:
        # Calculate new size while maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        
        original_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    
    # Upload to Roboflow and get predictions
    with open(image_path, "rb") as img_file:
        response = requests.post(API_URL, files={"file": img_file})
    
    if response.status_code != 200:
        raise Exception(f"Failed to get predictions: {response.status_code}")
    
    predictions = response.json()
    
    # Create overlay and mask
    overlay = Image.new("RGBA", original_image.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    mask = Image.new("L", original_image.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    
    # Draw segmentation
    for prediction in predictions["predictions"]:
        points = prediction.get("points", [])
        if points:
            polygon = [(point["x"], point["y"]) for point in points]
            draw_overlay.polygon(polygon, fill=(255, 0, 0, 100))
            draw_mask.polygon(polygon, fill=255)
    
    # Combine original with overlay
    segmented_image = Image.alpha_composite(original_image, overlay)
    
    # Count segmented pixels
    mask_array = np.array(mask)
    pixel_count = np.count_nonzero(mask_array)
    
    return original_image, segmented_image, pixel_count

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/outputs/<filename>')
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
