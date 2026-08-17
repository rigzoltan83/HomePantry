from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
)


LANGUAGE_CHOICES = [
    ("hu", "Magyar"),
    ("en", "English"),
]


MEASUREMENT_CHOICES = [
    ("metric", "Metric"),
    ("imperial", "Imperial (UK)"),
    ("us_customary", "US customary"),
]


ROLE_CHOICES = [
    ("owner", "Owner"),
    ("admin", "Admin"),
    ("member", "Member"),
]


class ProfileForm(FlaskForm):
    display_name = StringField(
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=120,
            ),
        ],
    )

    username = StringField(
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=80,
            ),
        ],
    )

    email = EmailField(
        validators=[
            DataRequired(),
            Email(),
            Length(max=255),
        ],
    )

    preferred_language = SelectField(
        choices=LANGUAGE_CHOICES,
        validators=[
            DataRequired(),
        ],
    )

    measurement_system = SelectField(
        choices=MEASUREMENT_CHOICES,
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField()


class HouseholdMemberForm(ProfileForm):
    role = SelectField(
        choices=ROLE_CHOICES,
        validators=[
            DataRequired(),
        ],
    )

    is_active = BooleanField()

    submit = SubmitField()

class NewHouseholdUserForm(FlaskForm):
    display_name = StringField(
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=120,
            ),
        ],
    )

    username = StringField(
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=80,
            ),
        ],
    )

    email = EmailField(
        validators=[
            DataRequired(),
            Email(),
            Length(max=255),
        ],
    )

    password = PasswordField(
        validators=[
            DataRequired(),
            Length(
                min=8,
                max=128,
            ),
        ],
    )

    preferred_language = SelectField(
        choices=LANGUAGE_CHOICES,
        validators=[
            DataRequired(),
        ],
    )

    measurement_system = SelectField(
        choices=MEASUREMENT_CHOICES,
        validators=[
            DataRequired(),
        ],
    )

    role = SelectField(
        choices=[
            ("admin", "Admin"),
            ("member", "Member"),
        ],
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField()
