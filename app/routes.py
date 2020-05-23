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
    image_red = image[:, :, 0]
    image_green = image[:, :, 1]
    image_blue = image[:, :, 2]

    U_r, d_r, V_r = np.linalg.svd(image_red, full_matrices=True)
    U_g, d_g, V_g = np.linalg.svd(image_green, full_matrices=True)
    U_b, d_b, V_b = np.linalg.svd(image_blue, full_matrices=True)

    U_r_k = U_r[:, 0:rank]
    V_r_k = V_r[0:rank, :]
    U_g_k = U_g[:, 0:rank]
    V_g_k = V_g[0:rank, :]
    U_b_k = U_b[:, 0:rank]
    V_b_k = V_b[0:rank, :]

    d_r_k = d_r[0:rank]
    d_g_k = d_g[0:rank]
    d_b_k = d_b[0:rank]

    image_red_approx = np.dot(U_r_k, np.dot(np.diag(d_r_k), V_r_k))
    image_green_approx = np.dot(U_g_k, np.dot(np.diag(d_g_k), V_g_k))
    image_blue_approx = np.dot(U_b_k, np.dot(np.diag(d_b_k), V_b_k))

    new_image = np.zeros((row, col, 3))

    new_image[:, :, 0] = image_red_approx
    new_image[:, :, 1] = image_green_approx
    new_image[:, :, 2] = image_blue_approx

    new_image[new_image < 0] = 0
    new_image[new_image > 1] = 1

    new_image = (new_image * 255).astype(np.uint8)
    im = Image.fromarray(new_image)
    im.save("app/static/compressed_{}_{}".format(rank, filename))
    return "static/compressed_{}_{}".format(rank, filename)
