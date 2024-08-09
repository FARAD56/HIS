import random
import string

def generate_profile_id():
    first_digit = random.choice(string.digits[1:])  # Select a digit from 1 to 9 for the first digit
    remaining_digits = ''.join(random.choices(string.digits, k=4))  # Generate the remaining 4 digits
    return first_digit + remaining_digits
