from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

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
        input_image_path = 'input_image.jpg'  # Temporarily save the uploaded image
        input_image.save(input_image_path)

        output_image_path = 'output.png'  # Save the output with a transparent background

        input_image = Image.open(input_image_path)
        output_image = remove(input_image)

        # Save the output image with transparent background
        output_image.save(output_image_path)

        # Delete the temporary input image
        os.remove(input_image_path)

        return send_file(output_image_path, mimetype='image/png')

    except Exception as e:
        print(f"Error: {e}")  # Print the error to the console
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
