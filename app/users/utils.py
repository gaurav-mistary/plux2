import random
import string

def generate_verification_code(size=8):
    verification_code = ''.join(
        [
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            ) for n in range(size)
        ]
    )
    
    return verification_code

