"""
Database controller using firebase Firestore
"""

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
