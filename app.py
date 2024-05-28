from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from rembg import remove
from PIL import Image
import os

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
        input_image_path = 'static/input_image.jpg'
        input_image.save(input_image_path)

        output_image_path = 'static/output.png'
        input_image = Image.open(input_image_path)
        output_image = remove(input_image)
        output_image.save(output_image_path)
        os.remove(input_image_path)

        return render_template('result.html', before_image=input_image_path, after_image=output_image_path)

    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
