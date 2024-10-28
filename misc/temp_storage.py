
class TempStorage:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(TempStorage, cls).__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]
    def __init__(self, user_id):
        if not hasattr(self, 'initialized'):
            self.user_id = user_id
            self.photo_storage = {self.user_id: []}
            self.another_users_id = []
            self.another_photo_storage = []
            self.index_another_user = 0
            self.num_page_photo_for_another_user = 0
            self.num_elem = 0
            self.id_message = 0
            self.start_message = 0

class UserManager:
    def __init__(self):
        self.users = {}

    def get_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = TempStorage(user_id)
        return self.users[user_id]