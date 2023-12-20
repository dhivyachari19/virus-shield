# group-project-readme


VirusShield allows you to upload a file (of a specified type) to be detected for malware. VirusShield uses a CNN and SVM model to accomplish this.

## Dependencies

There is a `requirements.txt` file in the main directory which includes the following dependencies:

```
flask==3.0.0
numpy==1.26.2
joblib==1.3.2
werkzeug==3.0.1
scikit-learn==1.2.2
pygments==2.17.2
pillow==10.1.0
pandas==2.1.3
tensorflow==2.15.0
matplotlib==3.8.2
```

Run the command `pip install -r requirements.txt` in your terminal and all the packages with the included versions (latest as of 12/4/23) listed in the `requirements.txt` file will be installed. It is recommended that this be done in a virtual environment. Note that the Python version expected by the Flask application is 3.10. An environment can be created using the following command line `conda create --name VIRTUAL_ENV_NAME python=3.10`.

## Web Server/Technical Architecture

The backend utilizes a thorough training process that is outlined in Abien Fred M. Agarap's paper "Towards Building an Intelligent Anti-Malware System: A Deep Learning Approach using Support Vector Machine (SVM) for Malware Classification", which will be linked below. Virus Shield's unique method of classifying based off of a trained SVM and CNN increased accuracy significantly and can classify over 25 different types of malware. The paper is linked below.

**In order to generate a classification without errors, the file `cnn_model.h5` needs to be added to the "models" subdirectory.** To access and download this file, go to the following link: https://drive.google.com/file/d/1q3DOqOYJRtmLwihADN5yMIHGQwyuYAkr/view?usp=sharing.

To access the Virus Shield website from a development server, run the command `flask run` in the terminal to generate the URL of the server. The route of the command to be executed, which is  `/upload` in this case, should be added to the end of the provided URL (ex: if the link generated is http://127.0.0.1:5000, the final link to be submitted in a web browser would be http://127.0.0.1:5000/upload). From there, the UI should be fairly intuitive; select and upload the file, and click the button that says "Click here to reveal results!" to view the classification of malware. The file uploaded should have one of the following extensions: `{'py', 'c', 'cpp', 'h', 'cc'}`. The HTTP requests being sent to the Flask server from the website can be seen in the terminal as requests are made.

## Project Members

- Ally & Dhivya: Frontend (HTML, CSS, Javascript, Python)
- Aayush & Abhived: Backend (Python, Tensorflow, matplotlib, numpy, pandas)
- All: Flask server, research & project planning (Python, numpy, keras, flask, Postman - testing)

## References 
https://arxiv.org/abs/1801.00318


