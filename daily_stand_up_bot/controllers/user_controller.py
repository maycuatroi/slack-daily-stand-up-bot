from daily_stand_up_bot.controllers.db_controller import DatabaseController


class UserController:
    def __init__(self):
        self.db_controller = DatabaseController()

    def save_user(self, user_id, authed_response: dict):
        """
        Save user to database
        document path: users/{user_id}/authed_response
        """

        self.db_controller.db.collection("users").document(user_id).set(
            {"authed_response": authed_response}
        )

    def get_user(self, user_id):
        """
        Get user from database
        """
        return self.db_controller.db.collection("users").document(user_id).get()