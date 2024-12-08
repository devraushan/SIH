# app.py
import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_cors import CORS
import requests
from PIL import Image, ImageDraw
import numpy as np
import uuid
import imghdr  # For image type validation

app = Flask(__name__)
CORS(app)
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
            return jsonify({"error":"no file part found"})
            # return render_template('index.html', error='No file part')
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error":"no file selected"})
            # return render_template('index.html', error='No selected file')
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({"error":"invalid file type"})
            # return render_template('index.html', error='Invalid file type. Please upload an image.')
        
        # Generate unique filename
        filename = str(uuid.uuid4())+'_'+".jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Validate the image
            if not validate_image(filepath):
                os.remove(filepath)  # Remove invalid file
                return jsonify({"error":"invalid image file"})
                # return render_template('index.html', error='Invalid image file')
            
            # Perform segmentation
            original_image, segmented_image, pixel_count = segment_image(filepath)
            
            # Save output images
            original_path = os.path.join(OUTPUT_FOLDER, f'original_{filename}')
            segmented_path = os.path.join(OUTPUT_FOLDER, f'segmented_{filename}')
            
            # Ensure the image is saved in a standard format
            original_image.convert('RGB').save(original_path, 'JPEG')
            segmented_image.convert('RGB').save(segmented_path, 'JPEG')
            
            res_data = {
                "original_image":"outputs/original_"+filename,
                "segamented_image":"outputs/segamented_"+filename,
                "pixel_count":pixel_count
            }
            return jsonify(res_data)
            # return render_template('result.html', 
            #                        original_image=f'outputs/original_{filename}', 
            #                        segmented_image=f'outputs/segmented_{filename}',
            #                        pixel_count=pixel_count)
            
        
        except Exception as e:
            # Remove temporary file
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error":str(e)})
            # return render_template('index.html', error=f'Processing error: {str(e)}')
    
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




















# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import requests
# import os
# import re

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all origins

# # Upload folders
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Roboflow API configuration
# API_KEY = "msvaHK2lfsfvfg0VAKWZ"
# PROJECT_ID = "project-r-5e4dz"
# MODEL_VERSION = "1"
# API_URL = f"https://detect.roboflow.com/{PROJECT_ID}/{MODEL_VERSION}?api_key={API_KEY}"

# def sanitize_filename(filename):
#     """Sanitize filename to avoid path traversal"""
#     return re.sub(r'[^\w\-_\.]', '_', filename)

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400

#     file = request.files['file']
#     if not file:
#         return jsonify({'error': 'No file uploaded'}), 400

#     filename = sanitize_filename(file.filename)
#     file_path = os.path.join(UPLOAD_FOLDER, filename)
#     try:
#         file.save(file_path)
#         print(f"File saved at: {file_path}")  # Log the file path

#         # Send to Roboflow API
#         with open(file_path, 'rb') as img:
#             response = requests.post(API_URL, files={"file": img})

#         if response.status_code != 200:
#             print(f"Roboflow API Error: {response.status_code} - {response.text}")  # Log Roboflow error
#             return jsonify({'error': 'Failed to process image with Roboflow'}), 500

#         result = response.json()

#         # Log the API response to understand its structure
#         print(f"Roboflow API response: {result}")

#         # Extract segmented image URL
#         segmented_image_url = None
#         if 'predictions' in result and len(result['predictions']) > 0:
#             segmented_image_url = result['predictions'][0].get('image', None)

#         if not segmented_image_url:
#             return jsonify({'error': 'Segmented image URL not found in API response'}), 500

#         return jsonify({
#             'original_image': filename,
#             'segmented_image': segmented_image_url
#         }), 200

#     except Exception as e:
#         print(f"Error processing image: {str(e)}")  # Log the error
#         return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# @app.route('/uploads/<filename>')
# def serve_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

# if __name__ == '__main__':
#     app.run(debug=True)















# # app.py
# import os
# from flask import Flask, render_template, request, send_from_directory
# import requests
# from PIL import Image, ImageDraw
# import numpy as np
# import uuid
# import imghdr  # For image type validation

# app = Flask(__name__)

# # Ensure upload and output directories exist
# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'outputs'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # Allowed image types
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

# # Roboflow API configuration
# API_KEY = "msvaHK2lfsfvfg0VAKWZ"
# PROJECT_ID = "project-r-5e4dz"
# MODEL_VERSION = "1"
# API_URL = f"https://detect.roboflow.com/{PROJECT_ID}/{MODEL_VERSION}?api_key={API_KEY}"

# def allowed_file(filename):
#     """Check if the file has an allowed image extension"""
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def validate_image(filepath):
#     """Validate that the file is actually an image"""
#     try:
#         # Attempt to open the image and verify its type
#         with Image.open(filepath) as img:
#             img.verify()  # Verify that it's a valid image
        
#         # Double-check the image type
#         image_type = imghdr.what(filepath)
#         if not image_type:
#             raise ValueError("Could not determine image type")
        
#         return True
#     except Exception as e:
#         print(f"Image validation error: {e}")
#         return False
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return render_template('index.html', error='No file part')
        
#         file = request.files['file']
        
#         if file.filename == '':
#             return render_template('index.html', error='No selected file')
        
#         # Check file extension
#         if not allowed_file(file.filename):
#             return render_template('index.html', error='Invalid file type. Please upload an image.')
        
#         # Generate unique filename
#         filename = str(uuid.uuid4()) + '_' + file.filename
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         file.save(filepath)
        
#         try:
#             # Validate the image
#             if not validate_image(filepath):
#                 os.remove(filepath)  # Remove invalid file
#                 return render_template('index.html', error='Invalid image file')
            
#             # Perform segmentation
#             original_image, segmented_image, pixel_count = segment_image(filepath)
            
#             # Save output images
#             original_path = os.path.join(OUTPUT_FOLDER, f'original_{filename}')
#             segmented_path = os.path.join(OUTPUT_FOLDER, f'segmented_{filename}')
            
#             # Ensure the image is saved in a standard format
#             original_image.convert('RGB').save(original_path, 'JPEG')
#             segmented_image.convert('RGB').save(segmented_path, 'JPEG')
            
#             return render_template('result.html', 
#                                    original_image=f'outputs/original_{filename}', 
#                                    segmented_image=f'outputs/segmented_{filename}',
#                                    pixel_count=pixel_count)
        
#         except Exception as e:
#             # Remove temporary file
#             if os.path.exists(filepath):
#                 os.remove(filepath)
#             return render_template('index.html', error=f'Processing error: {str(e)}')
    
#     return render_template('index.html')



# def segment_image(image_path, max_size=1024):
#     """
#     Segment image with optional resizing to handle large images
#     """
#     # Open the original image
#     original_image = Image.open(image_path).convert("RGBA")
    
#     # Resize image if too large to prevent API issues
#     width, height = original_image.size
#     if max(width, height) > max_size:
#         # Calculate new size while maintaining aspect ratio
#         if width > height:
#             new_width = max_size
#             new_height = int(height * (max_size / width))
#         else:
#             new_height = max_size
#             new_width = int(width * (max_size / height))
        
#         original_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    
#     # Upload to Roboflow and get predictions
#     with open(image_path, "rb") as img_file:
#         response = requests.post(API_URL, files={"file": img_file})
    
#     if response.status_code != 200:
#         raise Exception(f"Failed to get predictions: {response.status_code}")
    
#     predictions = response.json()
    
#     # Create overlay and mask
#     overlay = Image.new("RGBA", original_image.size, (0, 0, 0, 0))
#     draw_overlay = ImageDraw.Draw(overlay)
    
#     mask = Image.new("L", original_image.size, 0)
#     draw_mask = ImageDraw.Draw(mask)
    
#     # Draw segmentation
#     for prediction in predictions["predictions"]:
#         points = prediction.get("points", [])
#         if points:
#             polygon = [(point["x"], point["y"]) for point in points]
#             draw_overlay.polygon(polygon, fill=(255, 0, 0, 100))
#             draw_mask.polygon(polygon, fill=255)
    
#     # Combine original with overlay
#     segmented_image = Image.alpha_composite(original_image, overlay)
    
#     # Count segmented pixels
#     mask_array = np.array(mask)
#     pixel_count = np.count_nonzero(mask_array)
    
#     return original_image, segmented_image, pixel_count

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

# # @app.route('/outputs/<filename>')
# # def output_file(filename):
# #     return send_from_directory(OUTPUT_FOLDER, filename)


# @app.route('/outputs/<filename>')
# def output_file(filename):
#     return send_from_directory(OUTPUT_FOLDER, filename)


# if __name__ == '__main__':
#     app.run(debug=True)
















# import os
# from flask import Flask, render_template, request, send_from_directory, url_for
# import requests
# from PIL import Image, ImageDraw
# import numpy as np
# import uuid
# import imghdr
# import re

# app = Flask(_name_)

# # Ensure upload and output directories exist
# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'outputs'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # Allowed image types
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

# # Roboflow API configuration
# API_KEY = "msvaHK2lfsfvfg0VAKWZ"
# PROJECT_ID = "project-r-5e4dz"
# MODEL_VERSION = "1"
# API_URL = f"https://detect.roboflow.com/{PROJECT_ID}/{MODEL_VERSION}?api_key={API_KEY}"

# def allowed_file(filename):
#     """Check if the file has an allowed image extension"""
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def sanitize_filename(filename):
#     """Sanitize filename to remove path separators and invalid characters"""
#     filename = filename.replace('/', '').replace('\\', '')
#     filename = re.sub(r'[^a-zA-Z0-9.-]', '', filename)
#     return filename

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return render_template('index.html', error='No file part')
        
#         files = request.files.getlist('file')
        
#         if not files:
#             return render_template('index.html', error='No selected files')

#         results = []
        
#         for file in files:
#             if file.filename == '':
#                 continue
            
#             if not allowed_file(file.filename):
#                 continue
            
#             try:
#                 # Create unique filename only (no separate folder for each upload)
#                 safe_filename = sanitize_filename(file.filename)
#                 unique_filename = f"{str(uuid.uuid4())}_{safe_filename}"
                
#                 # Save file directly in uploads folder
#                 filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
#                 file.save(filepath)
                
#                 # Process the image
#                 original_image, segmented_image, pixel_count = segment_image(filepath)
                
#                 # Save segmented image
#                 output_filename = f"{str(uuid.uuid4())}_segmented.png"
#                 output_filepath = os.path.join(OUTPUT_FOLDER, output_filename)
#                 segmented_image.save(output_filepath)

#                 # Store results with simplified paths
#                 results.append({
#                     "filename": unique_filename,
#                     "original_image_url": url_for('uploaded_file', filename=unique_filename),
#                     "segmented_image": output_filename,
#                     "pixel_count": pixel_count
#                 })
#             except Exception as e:
#                 results.append({
#                     "filename": file.filename,
#                     "error": str(e)
#                 })

#         return render_template('result.html', results=results)
    
#     return render_template('index.html')

# def segment_image(image_path, max_size=1024):
#     """Segment image with optional resizing to handle large images"""
#     original_image = Image.open(image_path).convert("RGBA")
    
#     width, height = original_image.size
#     if max(width, height) > max_size:
#         if width > height:
#             new_width = max_size
#             new_height = int(height * (max_size / width))
#         else:
#             new_height = max_size
#             new_width = int(width * (max_size / height))
        
#         original_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    
#     with open(image_path, "rb") as img_file:
#         response = requests.post(API_URL, files={"file": img_file})
    
#     if response.status_code != 200:
#         raise Exception(f"Failed to get predictions: {response.status_code}")
    
#     predictions = response.json()
    
#     overlay = Image.new("RGBA", original_image.size, (0, 0, 0, 0))
#     draw_overlay = ImageDraw.Draw(overlay)
    
#     mask = Image.new("L", original_image.size, 0)
#     draw_mask = ImageDraw.Draw(mask)
    
#     for prediction in predictions["predictions"]:
#         points = prediction.get("points", [])
#         if points:
#             polygon = [(point["x"], point["y"]) for point in points]
#             draw_overlay.polygon(polygon, fill=(255, 0, 0, 100))
#             draw_mask.polygon(polygon, fill=255)
    
#     segmented_image = Image.alpha_composite(original_image, overlay)
    
#     mask_array = np.array(mask)
#     pixel_count = np.count_nonzero(mask_array)
    
#     return original_image, segmented_image, pixel_count

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     """Serve uploaded files directly from uploads folder"""
#     return send_from_directory(UPLOAD_FOLDER, filename)

# @app.route('/outputs/<filename>')
# def output_file(filename):
#     return send_from_directory(OUTPUT_FOLDER, filename)

# if _name_ == '_main_':
#     app.run(debug=True)











# import os
# from flask import Flask, render_template, request, send_from_directory, url_for, jsonify
# import requests
# from PIL import Image, ImageDraw
# import numpy as np
# import uuid
# import imghdr
# import re

# app = Flask(__name__)

# # Ensure upload and output directories exist
# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'outputs'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # Allowed image types
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

# # Roboflow API configuration
# API_KEY = "msvaHK2lfsfvfg0VAKWZ"
# PROJECT_ID = "project-r-5e4dz"
# MODEL_VERSION = "1"
# API_URL = f"https://detect.roboflow.com/{PROJECT_ID}/{MODEL_VERSION}?api_key={API_KEY}"

# def allowed_file(filename):
#     """Check if the file has an allowed image extension."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def sanitize_filename(filename):
#     """Sanitize filename to remove path separators and invalid characters."""
#     filename = filename.replace('/', '').replace('\\', '')
#     filename = re.sub(r'[^a-zA-Z0-9.-]', '', filename)
#     return filename

# @app.route('/', methods=['POST'])
# def process_image():
#     """Process uploaded image and return results."""
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files['file']
#     if not allowed_file(file.filename):
#         return jsonify({"error": "Invalid file type"}), 400

#     try:
#         # Save the uploaded file
#         safe_filename = sanitize_filename(file.filename)
#         unique_filename = f"{uuid.uuid4()}_{safe_filename}"
#         file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
#         file.save(file_path)

#         # Segment the image
#         segmented_image, pixel_count = segment_image(file_path)
#         output_filename = f"{uuid.uuid4()}_segmented.png"
#         output_path = os.path.join(OUTPUT_FOLDER, output_filename)
#         segmented_image.save(output_path)

#         # Return response
#         return jsonify({
#             "original_image_url": url_for('uploaded_file', filename=unique_filename),
#             "segmented_image_url": url_for('output_file', filename=output_filename),
#             "pixel_count": pixel_count,
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def segment_image(image_path, max_size=1024):
#     """Segment image and return the processed image and pixel count."""
#     original_image = Image.open(image_path).convert("RGBA")

#     # Resize the image if it exceeds max_size
#     width, height = original_image.size
#     if max(width, height) > max_size:
#         if width > height:
#             new_width = max_size
#             new_height = int(height * (max_size / width))
#         else:
#             new_height = max_size
#             new_width = int(width * (max_size / height))
#         original_image = original_image.resize((new_width, new_height), Image.LANCZOS)

#     # Send the image to Roboflow API
#     with open(image_path, "rb") as img_file:
#         response = requests.post(API_URL, files={"file": img_file})

#     if response.status_code != 200:
#         raise Exception(f"Failed to get predictions: {response.status_code}")

#     predictions = response.json()

#     # Create an overlay for the segmented image
#     overlay = Image.new("RGBA", original_image.size, (0, 0, 0, 0))
#     draw_overlay = ImageDraw.Draw(overlay)

#     mask = Image.new("L", original_image.size, 0)
#     draw_mask = ImageDraw.Draw(mask)

#     # Draw predictions on the overlay
#     for prediction in predictions["predictions"]:
#         points = prediction.get("points", [])
#         if points:
#             polygon = [(point["x"], point["y"]) for point in points]
#             draw_overlay.polygon(polygon, fill=(255, 0, 0, 100))  # Red with transparency
#             draw_mask.polygon(polygon, fill=255)  # White for segmentation mask

#     # Combine the original image with the overlay
#     segmented_image = Image.alpha_composite(original_image, overlay)

#     # Count the segmented pixels
#     mask_array = np.array(mask)
#     pixel_count = np.count_nonzero(mask_array)

#     return segmented_image, pixel_count

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     """Serve uploaded files."""
#     return send_from_directory(UPLOAD_FOLDER, filename)

# @app.route('/outputs/<filename>')
# def output_file(filename):
#     """Serve segmented output files."""
#     return send_from_directory(OUTPUT_FOLDER, filename)

# if __name__ == '__main__':
#     app.run(debug=True)








# from flask import Flask, request, jsonify
# import os
# import uuid
# from PIL import Image
# import numpy as np
# import requests

# app = Flask(__name__)

# # Ensure upload and output directories exist
# UPLOAD_FOLDER = 'uploads'
# OUTPUT_FOLDER = 'outputs'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# # Allowed image types
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

# # Roboflow API configuration
# API_KEY = "msvaHK2lfsfvfg0VAKWZ"
# PROJECT_ID = "project-r-5e4dz"
# MODEL_VERSION = "1"
# API_URL = f"https://detect.roboflow.com/{PROJECT_ID}/{MODEL_VERSION}?api_key={API_KEY}"

# def allowed_file(filename):
#     """Check if the file has an allowed image extension"""
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     # Check file extension
#     if not allowed_file(file.filename):
#         return jsonify({'error': 'Invalid file type'}), 400
    
#     # Generate unique filename
#     filename = str(uuid.uuid4()) + '_' + file.filename
#     filepath = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(filepath)
    
#     try:
#         # Validate and segment image (implement your segmentation logic)
#         original_image, segmented_image, pixel_count = segment_image(filepath)
        
#         original_path = os.path.join(OUTPUT_FOLDER, f'original_{filename}')
#         segmented_path = os.path.join(OUTPUT_FOLDER, f'segmented_{filename}')
        
#         original_image.convert('RGB').save(original_path, 'JPEG')
#         segmented_image.convert('RGB').save(segmented_path, 'JPEG')
        
#         return jsonify({
#             'original_image': f'/outputs/original_{filename}', 
#             'segmented_image': f'/outputs/segmented_{filename}',
#             'pixel_count': pixel_count
#         }), 200
    
#     except Exception as e:
#         if os.path.exists(filepath):
#             os.remove(filepath)
#         return jsonify({'error': str(e)}), 500

# def segment_image(image_path):
#     # Implement your image segmentation logic here.
#     # Placeholder for original and segmented images.
#     original_image = Image.open(image_path)
#     segmented_image = original_image  # Replace with actual segmentation logic.
#     pixel_count = np.count_nonzero(np.array(original_image))  # Placeholder logic.
    
#     return original_image, segmented_image, pixel_count

# if __name__ == '__main__':
#     app.run(debug=True)