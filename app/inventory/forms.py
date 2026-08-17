from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    DecimalField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional,
)


class StorageLocationForm(FlaskForm):
    name = StringField(
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=160,
            ),
        ],
    )

    location_type = SelectField(
        choices=[],
        validators=[
            DataRequired(),
        ],
    )

    parent_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            Optional(),
        ],
    )

    sort_order = IntegerField(
        default=100,
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                max=99999,
            ),
        ],
    )

    submit = SubmitField()


class InventoryBatchForm(FlaskForm):
    ingredient_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    product_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            Optional(),
        ],
    )

    storage_location_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    quantity = DecimalField(
        places=6,
        validators=[
            DataRequired(),
            NumberRange(
                min=0.000001
            ),
        ],
    )

    unit_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    purchase_date = DateField(
        validators=[
            Optional(),
        ],
    )

    expiration_date = DateField(
        validators=[
            Optional(),
        ],
    )

    note = TextAreaField(
        validators=[
            Optional(),
            Length(max=2000),
        ],
    )

    submit = SubmitField()


