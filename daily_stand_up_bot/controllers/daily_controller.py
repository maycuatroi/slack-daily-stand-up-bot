import os
from datetime import datetime, timedelta, timezone

from daily_stand_up_bot.controllers.db_controller import DatabaseController
from daily_stand_up_bot.controllers.slack_controller import SlackController


class DailyController:
    QUESTIONS = {
        "warm_up": """Hello {user.real_name}! :wave: It's time for Daily Standup in #general. 
Please share what you've been working on.
How do you feel today?""",
        "yesterday": "What did you do yesterday?",
        "today": "What are you going to do today?",
        "blockers": "What are your blockers?",
    }

    def __init__(self, team_id: str):
        self.dbc = DatabaseController()
        self.slack_controller = SlackController(team_id)

    def start(self, user_id):
        key, question = self.get_next_question(user_id)
        if key is None:
            self.slack_controller.send_message_to_user(
                user_id, "You have answered all questions today"
            )
        else:
            self.slack_controller.send_message_to_user(user_id, question)

    def get_next_question(self, user_id) -> (str, str):
        today = self.get_today().strftime("%Y-%m-%d")
        for key, question in self.QUESTIONS.items():
            # check if user has already answered questions
            is_user_answered_question = self.dbc.is_user_answered_question(
                user_id, key, today
            )
            if not is_user_answered_question:
                return key, question
        return (
            None,
            "Thank you for your answers, I have sent them to general channel :clap:",
        )

    def answer(self, user_id, answer):
        """
        Save user answer to database and send next question
        """
        today = self.get_today().strftime("%Y-%m-%d")
        current_question_key, current_question = self.get_next_question(
            user_id
        )  # get next question because answer is not stored yet

        self.dbc.save_answer(user_id, current_question_key, answer, today)

        is_answer_all_questions = self.dbc.is_user_answered_all_question(
            total_question=len(self.QUESTIONS), user_id=user_id, date=today
        )

        if is_answer_all_questions:
            self.slack_controller.send_message_to_user(
                user_id,
                "Thank you for your answers, I have sent them to general channel :clap:",
            )
            self.send_all_answer_to_general_channel(user_id, today)
        else:
            key, question = self.get_next_question(user_id)
            self.slack_controller.send_message_to_user(user_id, question)

    def send_all_answer_to_general_channel(self, user_id, today):
        message_template = f"""
                           <@{user_id}> have a great day!:
                           """
        for key, question in self.QUESTIONS.items():
            answers = self.dbc.get_user_answers(user_id, today)
            answer = answers[key]
            message_template += f"""
                                {question}
                                {answer}
                                """

        self.slack_controller.post_message(
            channel_id="general", message=message_template
        )

    def get_today(self):
        time_zone = os.getenv("TIME_ZONE", "+7")
        time_zone = timedelta(hours=int(time_zone))
        # get to day at UTC
        today = datetime.now(timezone.utc)
        # convert to user time zone
        today = today.astimezone(timezone(time_zone))
        return today


if __name__ == "__main__":
    today = DailyController("U01BQJZLZ7B", "C01BQJZLZ7B").get_today()
    print(today)
