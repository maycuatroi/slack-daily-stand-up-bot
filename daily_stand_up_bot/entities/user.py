from daily_stand_up_bot.entities.abtract_entity import AbstractEntity


class User(AbstractEntity):
    def __init__(self, data=None):
        self.id = None
        self.team_id = None
        self.name = None
        self.deleted = None
        self.color = None
        self.real_name = None
        self.tz = None
        self.tz_label = None
        self.tz_offset = None
        self.profile = None
        self.is_admin = None
        self.is_owner = None
        self.is_primary_owner = None
        self.is_restricted = None
        self.is_ultra_restricted = None
        self.is_bot = None
        self.is_app_user = None
        self.updated = None
        self.is_email_confirmed = None
        self.who_can_share_contact_card = None

        super().__init__(data)

    def __repr__(self):
        return f"{self.name} - {self.real_name}"
