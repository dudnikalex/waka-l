from flask_wtf import FlaskForm
from wtforms import IntegerField 
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

class ImageForm(FlaskForm):
    image = FileField('Image', validators=[DataRequired("Please, select an image")])
    rank = IntegerField('Rank', validators=[DataRequired("Please, enter valid rank")])
