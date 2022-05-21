"""This module implements the configuration structure for MusicWebsite."""

import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    """Data structure that contains the configuration for MusicWebsite."""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "i-guess-youll-never-know"

    SQLALCHEMY_DATABASE_URI = os.environ.get("SECRET_KEY") or "sqlite:///" + str(
        BASE_DIR.joinpath("app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
