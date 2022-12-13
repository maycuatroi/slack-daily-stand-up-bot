import os

TOKEN = os.environ.get("TOKEN")  # YOUR_TOKEN

__is_loaded = False


def load_config():
    global __is_loaded, TOKEN
    try:
        from daily_stand_up_bot.private_config import TOKEN as private_token

        TOKEN = private_token
    finally:
        print("Config loaded")
    __is_loaded = True


if not __is_loaded:
    load_config()
