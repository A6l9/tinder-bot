from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    age_question = State()
    sex_question = State()
    location_share = State()
    location_write = State()
    choose_city = State()
    name_question = State()
    about_yourself = State()
    send_video_or_photo = State()
    name_question_edit = State()
    location_edit_share = State()
    location_edit_write = State()
    description_question_edit = State()
    send_new_photo_or_video = State()
    delete_media = State()
    send_media_before_delete = State()
