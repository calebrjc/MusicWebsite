"""This module implements the models for MusicWebsite."""

from __future__ import annotations

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from music_website import db, login_manager


class User(UserMixin, db.Model):  # type: ignore
    """Represents a MusicWebsite user."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password: str) -> None:
        """Generate the user's password hash using the password specified."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Return true if the password checks positively against this user's password hash."""
        return check_password_hash(self.password_hash, password)

    def add_to_database(self) -> None:
        """Commit any changes to this user to the database."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def from_username(username: str) -> User | None:
        """Return the user that corresponds to the username.

        Returns None if no such user exists.
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def from_email(email: str) -> User | None:
        """Return the user that corresponds to the email.

        Returns None if no such user exists.
        """
        return User.query.filter_by(email=email).first()

    def __repr__(self) -> str:
        """Return a string representation of this user."""
        return f"User(id={self.id}, username={self.username}, email={self.email})"


@login_manager.user_loader
def load_user(user_id: int) -> User:
    """Return the user that corresponds to the id."""
    return User.query.get(int(user_id))


class Post(db.Model):  # type: ignore
    """Represents a news post on MusicWebsite."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(360))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def post_time(self) -> str:
        """Return a nicely formatted string representing this post's timestamp."""
        return self.timestamp.strftime("%A, %B %-d")

    def __repr__(self) -> str:
        """Return a string representation of this post."""
        return f"Post(id={self.id}, title={self.title}, timestamp={self.timestamp})"


def get_all_posts() -> list[Post]:
    """Return a list of all posts currently in the database.

    Posts are in descending order by timestamp.
    """
    all_posts: list[Post] = Post.query.order_by(Post.timestamp.desc()).all()
    return all_posts


"""
User:
    id: int
    username: str
    email: str
    password_hash: str
    music: list[Track]

Album:
    id: int
    name: str
    image: str
    tracks: list[Track]

Track:
    id: int
    name: str
    image: str
    album: Album
"""
