from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
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


class RecipeForm(FlaskForm):
    title = StringField(
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=255,
            ),
        ],
    )

    difficulty = SelectField(
        choices=[
            ("", ""),
            ("easy", "easy"),
            ("medium", "medium"),
            ("hard", "hard"),
        ],
        validators=[
            Optional(),
        ],
    )

    servings = IntegerField(
        validators=[
            Optional(),
            NumberRange(
                min=1,
                max=1000,
            ),
        ],
    )

    prep_time_minutes = IntegerField(
        validators=[
            Optional(),
            NumberRange(
                min=0,
                max=100000,
            ),
        ],
    )

    cook_time_minutes = IntegerField(
        validators=[
            Optional(),
            NumberRange(
                min=0,
                max=100000,
            ),
        ],
    )

    instructions_text = TextAreaField(
        validators=[
            Optional(),
        ],
    )

    submit = SubmitField()

class RecipeTagForm(FlaskForm):
    name = StringField(
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=120,
            ),
        ],
    )

    key = StringField(
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=80,
            ),
        ],
    )

    group_name = SelectField(
        choices=[],
        validators=[
            DataRequired(),
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

    is_active = BooleanField(
        default=True,
    )

    submit = SubmitField()
