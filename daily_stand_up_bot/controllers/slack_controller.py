import typing
import slack_sdk

from daily_stand_up_bot import config
from daily_stand_up_bot.controllers.db_controller import DatabaseController
from daily_stand_up_bot.entities.user import User


class SlackController:
    def __init__(self, team_id: str = None):
        self.team_id = team_id
        if team_id is not None:
            # get token from database
            dbc = DatabaseController()
            token = dbc.get_access_token_by_team_id(team_id)
        else:
            token = config.TOKEN

        self.client = slack_sdk.WebClient(token=token)

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

            # format mesage with user real name
            message = message_template.format(user=user)

            self.send_message(user.id, message)

    def forward_message_to_general_channel(self, user_id, message, chanel_id="general"):
        """
        Forward message to general channel
        """
        message_template = f"""
        <@{user_id}> have a great day!:
        "{message}"
        """
        self.client.chat_postMessage(channel=chanel_id, text=message_template)


if __name__ == "__main__":
    slack_controller = SlackController()
    slack_controller.forward_message_to_general_channel(
        "U04FEGY7JHE",
        "I am fine, thank you! To day I am going to do some work on my project",
    )
