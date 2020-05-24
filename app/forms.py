from flask_wtf import FlaskForm
from wtforms import IntegerField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, NumberRange


class SvdForm(FlaskForm):
    image = FileField('Image', validators=[DataRequired("Please, select an image")])
    rank = IntegerField('Rank', validators=[DataRequired("Please, enter valid rank"),
                                            NumberRange(1, None, "Please, input postive value")])


class ResizeForm(FlaskForm):
    image = FileField('Image', validators=[DataRequired("Please, select an image")])
    coefficient = IntegerField('Coefficient', validators=[DataRequired("Please, enter valid coefficient"),
                                                          NumberRange(1, None, "Please, input postive value")])
