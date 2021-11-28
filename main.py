from flask import Flask, request, render_template, url_for
from werkzeug.utils import redirect, secure_filename
from color_detector import main as get_color_data
import json
import os


UPLOAD_FOLDER = r"static\user_images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# --------------------- Globals
color_data = []
filename = ""


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ app.route("/image-colors", methods=["POST"])
def get_image_colors():
    global color_data, filename
    color_data = []
    filename = ""
    user_image_file = request.files["userImage"]
    if allowed_file(user_image_file.filename):
        filename = secure_filename(user_image_file.filename)
        user_image_file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
    color_data = get_color_data(os.path.join(
        app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for("color_extract_interface"))


@ app.route("/")
def home():
    sample_color_data = {}
    with open(r"json\samples_data.json", encoding="UTF-8") as f:
        sample_color_data = json.load(fp=f)
    return render_template("index.html", color_data=sample_color_data)


@ app.route("/extract/", methods=["GET", "POST"])
def color_extract_interface():
    global color_data
    return render_template("color_extract.html", color_data=color_data, file_name=filename)


if __name__ == "__main__":
    app.run()
