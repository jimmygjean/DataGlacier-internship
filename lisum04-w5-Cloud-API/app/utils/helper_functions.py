

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
def allowed_file(filename):
    # xx.png
    out = ("." in filename) and (filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS)
    return out