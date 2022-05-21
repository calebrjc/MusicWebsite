"""This module implements the routes for MusicWebsite."""

from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.wrappers import Response

from music_website import app, forms, models


@app.route("/")
def index() -> str:
    """Render the home page of MusicWebsite."""
    return render_template("index.html", posts=models.get_all_posts())


@app.route("/profile")
@login_required
def profile() -> str:
    """Handle the profile logic of MusicWebsite."""
    return render_template("profile.html")


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile() -> str | Response:
    """Handle the profile editing logic of MusicWebsite."""
    form = forms.EditProfileForm()
    if form.validate_on_submit():
        # Commit the new details to the database
        if form.username.data:
            current_user.username = form.username.data

        if form.email.data:
            current_user.email = form.email.data

        current_user.commit_to_database()

        if form.username.data or form.email.data:
            flash("Your changes have been saved.")
        return redirect(url_for("profile"))
    return render_template("edit_profile.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """Handle the login logic for MusicWebsite."""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        # Try to find a user with a matching username or email in the database
        user = models.User.from_username(form.identifier.data)
        if user is None:
            user = models.User.from_email(form.identifier.data)

        # Check the password if possible
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username/email or password")
            return redirect(url_for("login"))

        # Success! Log the user in
        login_user(user, remember=form.remember_me.data)
        flash(f"Welcome back, {user.username}!")

        # See if the user needs to go back to a certain page
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)
    return render_template("login.html", title="Log In", form=form)


@app.route("/logout")
def logout() -> Response:
    """Handle the logout logic for MusicWebsite."""
    logout_user()
    flash("You have been logged out successfully.")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    """Handle the registration logic for MusicWebsite."""
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        # Add the new user to the database
        user = models.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.commit_to_database()

        flash(f"Welcome to MusicWebsite, {user.username}!")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)
