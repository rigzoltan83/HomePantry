from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class RegisterForm(FlaskForm):
    display_name = StringField(
        "Display name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=120,
            ),
        ],
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=255),
        ],
    )

    household_name = StringField(
        "Household name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=160,
            ),
        ],
    )

    preferred_language = SelectField(
        "Language",
        choices=[
            ("hu", "Magyar"),
            ("en", "English"),
        ],
        default="hu",
        validators=[
            DataRequired(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8),
        ],
    )

    password_confirm = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match.",
            ),
        ],
    )

    submit = SubmitField(
        "Create account"
    )


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField(
        "Sign in"
    )
