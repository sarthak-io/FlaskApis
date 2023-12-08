import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename  # Add this line
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime, timedelta
app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("imagedata-cb-firebase-adminsdk-eg04o-d94f0ee134.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'imagedata-cb.appspot.com'})

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def get_download_url(file, file_name):
    # Assuming the images are stored in Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(file_name)

    # Convert file data to bytes
    file_data = io.BytesIO(file.read())

    # Upload the file using upload_from_file
    blob.upload_from_file(file_data, content_type=file.content_type)
    expiration_time = datetime.utcnow() + timedelta(days=30)
    expiration_timestamp = int(expiration_time.timestamp())

    download_url = blob.generate_signed_url(expiration=expiration_timestamp)

    return download_url

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        images = {}
        for key, file in request.files.items():
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                download_url = get_download_url(file, filename)
                images[key] = download_url
        return jsonify(images), 200
    except Exception as e:
        print(f"Error uploading image: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
