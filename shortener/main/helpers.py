import string
import random
import re

__chars = list(string.ascii_letters) + [str(i) for i in range(0,9)]
__length = 6
__seed = 1
random.seed(__seed)
# set seed w/ session?
    
def validate(short):
    if re.search('\W', short):
        raise ValueError('Short URL contains invalid characters!')
    else:
        return True

def encode(long_url):
    return "".join([random.choice(__chars) for i in range(__length)])