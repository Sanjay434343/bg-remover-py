from flask import Flask, request, send_file, flash, redirect, url_for, render_template
from rembg import remove
from PIL import Image
import os
import tempfile

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_background', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            flash('No image provided')
            return redirect(url_for('index'))

        input_image = request.files['image']
        
        # Create a temporary directory to store the uploaded image
        temp_dir = tempfile.mkdtemp()
        input_image_path = os.path.join(temp_dir, 'input_image.jpg')
        input_image.save(input_image_path)

        output_image_path = os.path.join(temp_dir, 'output.png')
        input_image = Image.open(input_image_path)
        output_image = remove(input_image)
        output_image.save(output_image_path)

        # Send the output image file as an attachment for download
        return send_file(output_image_path, as_attachment=True)

    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
