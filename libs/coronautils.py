# Usefull functions
import string
import random

class CoronaUtils:

    def randomStringGenerator(self, size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))
