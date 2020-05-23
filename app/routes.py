# -*- coding: utf-8 -*-
from flask import render_template
from app import app
from app.forms import ImageForm
import numpy as np
from PIL import Image


@app.route('/', methods=["GET", "POST"])
def index():
    image_form = ImageForm()
    if image_form.validate_on_submit():
        image = image_form.image.data
        rank = image_form.rank.data
        image.save(image.filename)
        return render_template('result.html', filename=svd_compress(image.filename, rank))
    return render_template('index.html', image_form=image_form)


def svd_compress(filename, rank):
    image = np.array(Image.open(filename))
    image = image / 255
    row, col, _ = image.shape
    new_image = np.zeros((row, col, 3))

    for i in range(3):
        layer = image[:, :, i]

        U, d, V = np.linalg.svd(layer, full_matrices=True)

        U_new = U[:, 0:rank]
        V_new = V[0:rank, :]
        d_new = d[0:rank]

        layer = np.dot(U_new, np.dot(np.diag(d_new), V_new))
        new_image[:, :, i] = layer

    new_image = np.clip(new_image, 0, 1)

    new_image = (new_image * 255).astype(np.uint8)
    im = Image.fromarray(new_image)
    im.save("app/static/compressed_{}_{}".format(rank, filename))
    return "static/compressed_{}_{}".format(rank, filename)
