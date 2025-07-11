# shared/auth.py

import os

# Just hardcode the secret directly
SERVER_SECRET = "secret123"

def validate_token(received_token):
    return received_token == SERVER_SECRET
