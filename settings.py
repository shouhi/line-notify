import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ID = os.environ.get("LOGIN_ID_KEY")
PWD = os.environ.get("LOGIN_PASS_KEY")
LINE_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")
LINE_API = os.environ.get("LINE_NOTIFY_API")