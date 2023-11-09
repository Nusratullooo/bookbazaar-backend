from .base import *  # noqa

# TODO: as soon as the project goes to production fix allowed hosts
SERVER_IP = os.environ["SERVER_IP"]
ALLOWED_HOSTS = [SERVER_IP, "bookbazaar-api.uz"]
DEBUG = os.environ["DEBUG"]
