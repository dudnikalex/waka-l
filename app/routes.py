# -*- coding: utf-8 -*-
from flask import render_template
from app import app
from app.forms import SvdForm, ResizeForm
import numpy as np
from PIL import Image


@app.route('/', methods=["GET", "POST"])
def index():
    image_form = SvdForm()
    if image_form.validate_on_submit():
        image = image_form.image.data
        rank = image_form.rank.data
        image.save(image.filename)
        return render_template('result.html', filename=svd_compress(image.filename, rank))
    return render_template('index.html', image_form=image_form)


@app.route('/resize', methods=["GET", "POST"])
def resize():
    image_form = ResizeForm()
    if image_form.validate_on_submit():
        image = image_form.image.data
        coefficient = image_form.coefficient.data
        image.save(image.filename)
        return render_template('result.html', filename=resize_compress(image.filename, coefficient))
    return render_template('resize.html', image_form=image_form)


def svd_compress(filename, rank):
    image = np.array(Image.open(filename))
    image = image / 255
    compressed_image = np.zeros_like(image)

    for depth in range(image.shape[-1]):
        layer = image[:, :, depth]

        U, d, V = np.linalg.svd(layer, full_matrices=True)

        U_new = U[:, 0:rank]
        V_new = V[0:rank, :]
        d_new = d[0:rank]

        layer = np.dot(U_new, np.dot(np.diag(d_new), V_new))
        compressed_image[:, :, depth] = layer

    compressed_image = np.clip(compressed_image, 0, 1)

    compressed_image = (compressed_image * 255).astype(np.uint8)
    compressed_image = Image.fromarray(compressed_image)

    compressed_image_path = "static/compressed_{}_{}".format(rank, filename)
    compressed_image.save("app/" + compressed_image_path)
    return compressed_image_path


def resize_compress(filename, coefficient):
    image = Image.open(filename)
    image = image.resize(size=(image.size[0] // coefficient, image.size[1] // coefficient))

    compressed_image_path = "static/resized_{}_{}".format(coefficient, filename)
    image.save("app/" + compressed_image_path)
    return compressed_image_path
