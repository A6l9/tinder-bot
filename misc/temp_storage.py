
class TempStorage:
    def __init__(self, user_id):
        self.user_id = user_id
        self.photo_storage = {self.user_id: []}
        self.another_users_id = []
        self.another_photo_storage = []
        self.index_another_user = 0
        self.num_page_photo_for_another_user = 0
        self.num_elem = 0
        self.id_message = 0
        self.start_message = 0
        self.exceptions_messages = []


class UserManager:
    def __init__(self):
        self.users = {}

    def get_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = TempStorage(user_id)
        return self.users[user_id]
