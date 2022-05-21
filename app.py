"""This script serves as an entry point to MusicWebsite."""

from typing import Any

from music_website import app, db
from music_website.models import User, Post


@app.shell_context_processor  # type: ignore
def create_shell_context() -> dict[str, Any]:
    """Return a dictionary that defines pieces of context for the "flask shell" command."""
    return {"db": db, "User": User, "Post": Post}
