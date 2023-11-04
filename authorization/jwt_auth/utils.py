from datetime import datetime, timedelta
from bson.objectid import ObjectId
import jwt
import uuid

from core import settings



def gen_jti():
    """Generate hexed unique jti for user"""
    return str(uuid.uuid4().hex)

jti = gen_jti()




