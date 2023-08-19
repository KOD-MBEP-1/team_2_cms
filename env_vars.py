"""
Module to import variables from .env file
"""

import os

from dotenv import load_dotenv


load_dotenv()


DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
