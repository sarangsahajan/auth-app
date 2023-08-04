import os
from django.core.management.utils import get_random_secret_key


file_path = 'secret_key.txt'

if os.path.exists(file_path):
    print("Error: Secret key file already exists. Please don't overwrite it.")
else:
    secret_key = get_random_secret_key()
    with open(file_path, 'w') as f:
        f.write(secret_key)
    print("Secret key saved to secret_key.txt successfully.")
