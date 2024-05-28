import random
import string
def generate_profile_id():
    digits = ''.join(random.choices(string.digits, k=5))
    return digits


