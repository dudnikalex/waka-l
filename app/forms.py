from flask_wtf import FlaskForm
from wtforms import IntegerField 
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

class ImageForm(FlaskForm):
    image = FileField('Image', validators=[DataRequired()])
    rank = IntegerField('Rank', validators=[DataRequired()])
