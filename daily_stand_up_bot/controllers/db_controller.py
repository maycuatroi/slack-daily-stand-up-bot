"""
Database controller using firebase Firestore
"""
from datetime import datetime, timedelta, timezone

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from daily_stand_up_bot import config

cred = credentials.Certificate(config.FIREBASE_SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred)


class DatabaseController:
    db = None

    def __init__(self):
        if DatabaseController.db is None:
            DatabaseController.db = firestore.client()

    def get_all_users(self):
        return self.db.collection("users").get()

    def get_access_token_by_team_id(self, team_id: str):
        """
        Get access token by team id
        Document path: /teams/{team_id}/access_token
        """
        doc_ref = self.db.collection("teams").document(team_id)
        doc = doc_ref.get()
        return doc.to_dict()["access_token"]

    def add_access_token(self, team_id: str, access_token: str):
        """
        Add access token to database
        Document path: /teams/{team_id}/access_token
        """
        doc_ref = self.db.collection("teams").document(team_id)
        doc_ref.set({"access_token": access_token})

    def is_user_answered_question(self, user_id, key, date):
        """
        Check if user has already answered question
        Document path: /answers/{user_id}/{date}/{key}
        """
        doc_ref = self.db.collection("answers").document(user_id).collection(date)
        doc = doc_ref.document(key).get()
        return doc.exists
    def is_user_answered_all_question(self, total_question, user_id, date):
        """
        Check if user has answered all question
        Document path: /answers/{user_id}/{date}
        """
        doc_ref = self.db.collection("answers").document(user_id).collection(date)
        docs = doc_ref.stream()
        return len(list(docs)) == total_question

    def get_user_answers(self, user_id, date):
        """
        Get user answers
        Document path: /answers/{user_id}/{date}
        """
        doc_ref = self.db.collection("answers").document(user_id).collection(date)
        docs = doc_ref.stream()
        return docs

    def save_answer(self, user_id, key, answer, today):
        """
        Save user answer
        Document path: /answers/{user_id}/{date}/{key}
        """
        doc_ref = self.db.collection("answers").document(user_id).collection(today)
        doc_ref.document(key).set({"answer": answer})