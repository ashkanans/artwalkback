class AWUsers:
    def __init__(self, user_id, username, email, mobile_phone, hash_password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.mobile_phone = mobile_phone
        self.hash_password = hash_password

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "mobile_phone": self.mobile_phone,
            "hash_password": self.hash_password
        }

    @staticmethod
    def list_to_dict(users_list):
        return [user.to_dict() for user in users_list]
