from time import time
from datetime import datetime
from urllib.parse import urlparse

buckets = {
    "user": "user-t3-bucket",
    "spend": "spend-t3-bucket"
}


def get_epoch_timestamp():
    return int(time())


def get_current_datetime():
    now = datetime.now()
    dateFormat = now.strftime("%m/%d/%Y, %H:%M:%S")
    return dateFormat


def get_bucket_name(file_type):
    return buckets[file_type]


def is_valid_url(url):
    """
    Check if a URL is valid
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
