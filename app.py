import os
import re
import qrcode
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Sanitize function for filenames
def sanitize_filename(data):
    # Replace all invalid characters with underscores
    return re.sub(r'[^a-zA-Z0-9]', '_', data)

def generate_qr_code(data, save_dir):
    # Sanitize the input data to create a valid file name
    sanitized_data = sanitize_filename(data)
    
    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Define the file path using sanitized data
    file_path = os.path.join(save_dir, f"{sanitized_data}.png")
    
    # Generate the QR code and save it
    img = qrcode.make(data)
    img.save(file_path)
    return file_path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # Get the data from the form
    data = request.form.get("data")

    # Path where the QR code will be saved
    save_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'qr_codes')

    # Generate QR code and get the file path
    file_path = generate_qr_code(data, save_dir)

    # Send the generated QR code file to the user
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
