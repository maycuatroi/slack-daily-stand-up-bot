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
        return self.db.collection(u'users').get()