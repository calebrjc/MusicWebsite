"""This module implements the forms needed by MusicWebsite."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError

from music_website import models


class LoginForm(FlaskForm):  # type: ignore
    """Implements input structure and validation for logging users into MusicWebsite."""
    identifier = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):  # type: ignore
    """Implements input structure and validation for registering users for MusicWebsite."""
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username_field: StringField) -> None:
        """Raise a ValidationError if the username is already taken."""
        user = models.User.from_username(username_field.data)
        if user is not None:
            raise ValidationError("Please choose another username.")

    def validate_email(self, email_field: StringField) -> None:
        """Raise a ValidationError if the email is already taken."""
        user = models.User.from_email(email_field.data)
        if user is not None:
            raise ValidationError("Please use a different email address.")


class EditProfileForm(FlaskForm):
    """Implements input structure and validation for editing profiles in MusicWebsite."""
    username = StringField("Username", validators=[Optional()])
    email = StringField("Email", validators=[Optional(), Email()])
    submit = SubmitField("Submit")

    def validate_username(self, username_field: StringField) -> None:
        """Raise a ValidationError if the username is already taken."""
        user = models.User.from_username(username_field.data)
        if user is not None:
            raise ValidationError("Please choose another username.")

    def validate_email(self, email_field: StringField) -> None:
        """Raise a ValidationError if the email is already taken."""
        user = models.User.from_email(email_field.data)
        if user is not None:
            raise ValidationError("Please use a different email address.")
