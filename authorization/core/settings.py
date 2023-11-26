from decouple import config


# Important settings for fastapi app. env is used as in settings.

JWT_SECRET = config("JWT_SECRET_KEY")
JWT_ALGORITHM = config("JWT_ALGORITHM")

TIME_DICT = {
    "A":"seconds",
    "B":"minutes",
    "C":"hours",
    "D":"days"
}

ACCESS_TOKEN_TIME_UNIT = TIME_DICT["B"]
REFRESH_TOKEN_TIME_UNIT = TIME_DICT["B"]

ACCESS_TOKEN_EXPIRE = 5
REFRESH_TOKEN_EXPIRE = 10


REDIS_HOST_ADDRESS = "redis://127.0.0.1:6379/0"
MONGODB_HOST_ADDRESS = "mongodb://localhost:27017/"

ACCOUNT_ADDRESS = "http://127.0.0.1:8000/account"
DATA_ADDRESS = "http://127.0.0.1:8000/data"