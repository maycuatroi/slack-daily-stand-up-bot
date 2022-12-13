import typing

from slack.web import client
from slack_sdk import WebClient

from daily_stand_up_bot import config
from daily_stand_up_bot.entities.user import User


class SlackController:
    def __init__(self):
        self.client = WebClient(token=config.TOKEN)

    def get_all_users(self) -> typing.List[User]:
        """
        Use slack sdk to get all user in the workspace
        """
        result = self.client.users_list()
        users = [User(user) for user in result["members"]]
        users = [user for user in users if not user.is_bot]
        return users

    def send_message(self, user_id: str, message: str):
        self.client.chat_postMessage(channel=user_id, text=message)

    def send_message_to_all_users(self, message_template: str):
        """
        Send message to all users in the workspace

        Args:
            message_template: Message template, use {user} to replace with user name
                Examples: "Hello {user.real_name}, how are you today?"
        """
        users = self.get_all_users()
        for user in users:

            #format mesage with user real name
            message = message_template.format(user=user)

            self.send_message(user.id, message)


if __name__ == "__main__":
    slack_controller = SlackController()
    slack_controller.send_message_to_all_users("Hello {user.real_name}, how are you today?")
