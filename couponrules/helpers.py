import string
import random

from django.conf import settings


def get_random_code(length=12):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))