import os
from typing import Optional, Dict

from dotenv import load_dotenv
from redis import Redis
from redis_om import HashModel

load_dotenv()
redis_client = Redis(
    host=os.getenv("REDIS_HOST"),
    port=6379,
    db=1,
    decode_responses=True,
)


class Log(HashModel):
    level: str
    data_time: str
    folder_name: str
    filename: str
    message: str
    metadata: Optional[Dict] = None

    class Meta:
        database = redis_client
