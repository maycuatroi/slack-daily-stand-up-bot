"""
Create one time trigger, auto trigger when https request is received.
"""

from typing import Union

from fastapi import FastAPI

from daily_stand_up_bot.controllers.user_controllers import UserController

app = FastAPI()


@app.post("/daily")
async def daily():
    user_controller = UserController()
    users = user_controller.get_all_users()


    return {"message": "Daily"}