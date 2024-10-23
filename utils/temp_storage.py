
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
