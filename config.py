import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    W_SECRET = os.environ.get('W_SECRET') or 'you-will-never-guess'