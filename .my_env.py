#!/usr/bin/python3

import os

def set_environment_variables(variables):
    for key, value in variables.items():
        os.environ[key] = value

if __name__ == "__main__":
    # Define the environment variables as a dictionary
    env_variables = {
        "HBNB_ENV": "dev",
        "HBNB_MYSQL_USER": "hbnb_dev",
        "HBNB_MYSQL_PWD": "hbnb_dev_pwd",
        "HBNB_MYSQL_HOST": "localhost",
        "HBNB_MYSQL_DB": "hbnb_dev_db",
        "HBNB_TYPE_STORAGE": "db"
    }

    # Set the environment variables
    set_environment_variables(env_variables)

    # Verify env variables are set
    print("Environment variables set:")
    for key, value in env_variables.items():
        print(f"{key}: {value}")
