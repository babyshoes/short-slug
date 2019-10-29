import string
import random
import re

__chars = list(string.ascii_letters) + [str(i) for i in range(0,9)]
__length = 6
__seed = 1
random.seed(__seed)

# check if valid long first??
def scrub(long):
    return long.replace("http://", "")

def recreate(long):
    return "http://" + long
    
def validate(short):
    if re.search('\W', short):
        raise ValueError('Short URL contains invalid characters!')
    else:
        return True

def check_if_exists(long_url):
    # and has random short already
    pass

def encode(long_url):
    return "".join([random.choice(__chars) for i in range(__length)])

def decode(short_url):
    pass