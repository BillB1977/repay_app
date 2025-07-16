from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange, Optional, Email

class PaymentForm(FlaskForm):
    last_payment = DateField('Last Payment Date (YYYY-MM-DD)', validators=[DataRequired()])
    rent = DecimalField('Monthly Rent', validators=[DataRequired(), NumberRange(min=0)])
    protection = DecimalField('Protection Plan', validators=[DataRequired(), NumberRange(min=0)])
    gate = DecimalField('Gate Access', validators=[DataRequired(), NumberRange(min=0)])
    additional_costs = DecimalField('Additional Monthly Costs', validators=[DataRequired(), NumberRange(min=0)])
    late_fee_percent = DecimalField('Late Fee Percent (e.g., 20 for 20%)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Generate Repayment Plan')