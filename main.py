from distutils.log import debug
from flask import Flask, request, render_template, url_for
from werkzeug.utils import redirect, secure_filename
from color_detector import main as get_color_data
import json
import ast
import os


<<<<<<< HEAD
UPLOAD_FOLDER = r".\static\user_images"
=======
UPLOAD_FOLDER = "static/user_images"
>>>>>>> af9ab4828d008a94ec5ec7810f56d2ddd5754d19
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# --------------------- Globals


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ app.route("/image-colors", methods=["POST"])
def get_image_colors():
    color_data = []
    file_name = ""
    user_image_file = request.files["userImage"]
    if allowed_file(user_image_file.filename):
        file_name = secure_filename(user_image_file.filename)
        user_image_file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], file_name))
    color_data = get_color_data(os.path.join(
        app.config['UPLOAD_FOLDER'], file_name))
    return redirect(url_for("color_extract_interface", file_name=file_name, color_data=color_data))


@ app.route("/")
def home():
    sample_color_data = {}
<<<<<<< HEAD
    with open(r".\json\samples_data.json", encoding="UTF-8") as f:
=======
    with open("json/samples_data.json", encoding="UTF-8") as f:
>>>>>>> af9ab4828d008a94ec5ec7810f56d2ddd5754d19
        sample_color_data = json.load(fp=f)
    return render_template("index.html", color_data=sample_color_data)


@ app.route("/extract/", methods=["GET", "POST"])
def color_extract_interface():
    try:
        color_data = ast.literal_eval(request.args.get("color_data"))
        file_name = request.args.get("file_name")
    except:
        color_data = {}
        file_name = ""
    print(color_data, file_name, type(color_data))
    return render_template("color_extract.html", color_data=color_data, file_name=file_name)


if __name__ == "__main__":
    app.run(debug=True)
