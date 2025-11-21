from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
from datetime import datetime

class OpeningInventoryForm(FlaskForm):
    item_code = StringField('Item Code', validators=[DataRequired(), Length(min=1, max=50)])
    item_name = StringField('Item Name', validators=[DataRequired(), Length(min=1, max=100)])
    spec = StringField('Spec', validators=[Length(max=100)])
    unit = StringField('Unit', validators=[DataRequired(), Length(min=1, max=20)])
    quantity = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=0.0001)])
    unit_cost = FloatField('Unit Cost', validators=[DataRequired(), NumberRange(min=0.01)])
    opening_date = DateField('Opening Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=255)])
    submit = SubmitField('Submit')