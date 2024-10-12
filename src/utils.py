import os
from typing import *

def load_env(env_file:str='.env'):
    '''
    Load all variables defined in the .env file as environment variables

    Parameters:
        env_file: the path to file with the setup
    '''
    try:
        with open(env_file) as file:
            for line in file:
                # Strip whitespace and ignore empty lines or comments
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        print(f"Error: {env_file} file not found.")
    except Exception as e:
        print(f"Error while loading environment variables: {e}")