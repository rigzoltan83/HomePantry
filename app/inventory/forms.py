from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional,
)


class StorageLocationForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=160,
            ),
        ],
    )

    location_type = SelectField(
        "Type",
        choices=[
            ("room", "Room"),
            ("cabinet", "Cabinet"),
            ("shelf", "Shelf"),
            ("fridge", "Fridge"),
            ("freezer", "Freezer"),
            ("drawer", "Drawer"),
            ("box", "Box"),
            ("storage", "Other storage"),
        ],
        validators=[
            DataRequired(),
        ],
    )

    parent_id = SelectField(
        "Parent location",
        coerce=int,
        validators=[
            Optional(),
        ],
    )

    sort_order = IntegerField(
        "Sort order",
        default=100,
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                max=99999,
            ),
        ],
    )

    submit = SubmitField(
        "Save"
    )
