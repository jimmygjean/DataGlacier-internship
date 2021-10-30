
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.preprocessing.image import load_img, img_to_array
from utils.helper_functions import allowed_file


UPLOAD_FOLDER = 'images'
model = VGG16()

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def predict():
    """The user is provided with an interface where
    they can upload an image. After submission,
    a deep learning model is used to make a prediction
    of what the image could be. The result is then sent to
    the user.
    """
    if request.method == 'GET':
        out_message = None
    elif request.method == 'POST':
        # get file
        file = request.files['imagefile']
        filename = secure_filename(file.filename)

        if file is None or file.filename == "":
            out_message = "No file"
        elif not allowed_file(file.filename):
            out_message = "Format not currently supported"
        else:
            # save image in database
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\","/")
            file.save(image_path)

            # load & preprocess image
            image = load_img(image_path, target_size=(224, 224))
            image = img_to_array(image)
            image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
            image = preprocess_input(image)
            try:
                # predict
                y_pred = model.predict(image)
                label = decode_predictions(y_pred)
                label = label[0][0]
                out_message = "Your image is a %s (%.2f%%)" %(label[1], label[2]*100)
            except:
                out_message = "An error occured during prediction"

    return render_template('index.html', out_message=out_message)

if __name__ == '__main__':
    app.run(port=3000, debug=True)