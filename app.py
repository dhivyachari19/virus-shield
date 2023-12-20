import os
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
import tensorflow as tf
from keras.models import load_model
from joblib import load
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import ImageFormatter
from PIL import Image
from werkzeug.utils import secure_filename
from pygments import highlight

# Flask documentation on file uploads: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'py', 'c', 'cpp', 'h', 'cc'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.environ.get("SECRET_KEY", None)

malware_labels = {
    0: 'Adialer.C',
    1: 'Agent.FYI',
    2: 'Allaple.A',
    3: 'Allaple.L',
    4: 'Alueron.gen!J',
    5: 'Autorun.K',
    6: 'C2LOP.P',
    7: 'C2LOP.gen!g',
    8: 'Dialplatform.B',
    9: 'Dontovo.A',
    10: 'Fakerean',
    11: 'Instantaccess',
    12: 'Lolyda.AA1',
    13: 'Lolyda.AA2',
    14: 'Lolyda.AA3',
    15: 'Lolyda.AT',
    16: 'Malex.gen!J',
    17: 'Obfuscator.AD',
    18: 'Rbot!gen',
    19: 'Skintrim.N',
    20: 'Swizzor.gen!E',
    21: 'Swizzor.gen!I',
    22: 'VB.AT',
    23: 'Wintrim.BX',
    24: 'Yuner.A'
}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    upload_state = "No file has been uploaded yet."
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as saved_file:
                file_contents = saved_file.read()
                print(f"Contents of {filename}:\n{file_contents}")
            
            upload_state = classify()
    return render_template('index.html', my_string = upload_state)

def preprocess_image(file):
    # Load the saved StandardScaler
    scaler = load('models/scaler.joblib')

    # Get file path
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploaded_files', filename)

    # Read the binary data from the file
    with open(file_path, 'rb') as binary_file:
        binary_data = binary_file.read()

    # Convert binary data to a numpy array of uint8 (8-bit unsigned integers)
    # The length of the array is determined by the size of the binary file
    # Each byte in the file corresponds to a pixel value in the range 0-255
    img_array = np.frombuffer(binary_data, dtype=np.uint8)

    # Resize the flat array to a 32x32 matrix and handle cases where the binary file is too small or too large
    try:
        img_matrix = np.resize(img_array, (32, 32))
    except ValueError as e:  # Handle resizing error
        # Log error and return None or handle it appropriately
        print(f"Error resizing image array: {e}")
        return None

    # Flatten the 32x32 matrix to a 1x1024 array
    img_flatten = img_matrix.flatten()
    
    # Save the 32x32 image for inspection
    processed_image_path = os.path.join('processed-images', os.path.splitext(filename)[0] + '_processed.png')
    Image.fromarray(img_matrix).save(processed_image_path)
    print(f"Processed image saved to: {processed_image_path}")

    # Standardize the image data using the loaded scaler
    standardized_data = scaler.transform([img_flatten])

    return standardized_data.reshape(-1, 32, 32, 1)  # Reshape for CNN input

def classify():
    # If the user does not select a file, the browser might
    # submit an empty file part without a filename.
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    # load models
    svm_model_path = "models/svm_model.joblib"
    svm_model = load(svm_model_path)
    cnn_model_path = "models/cnn_model.h5"
    cnn_model = load_model(cnn_model_path)

    # preprocess image
    preprocessed_image = preprocess_image(file)

    # extract features from CNN
    cnn_features = cnn_model.predict(preprocessed_image)

    # use SVM to make prediction based on extracted features
    predicted_label = svm_model.predict(cnn_features)
    #predicted_label = "1" # for testing purposes: should return 'Agent.FYI'

    # return updated upload state w/ predicted classification label
    upload_state = "The predicted label is: " + malware_labels[int(predicted_label)]
    return upload_state


if __name__ == '__main__':
   app.run(debug=True)