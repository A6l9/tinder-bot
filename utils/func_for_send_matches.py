import asyncio
from asyncio import Task
import json

from loguru import logger

from sqlalchemy import and_, or_

from database.models import Users, Matches, BotReplicas
from keyboards.inline.inline_kbs import create_buttons_for_viewing_match
from loader import db, bot

class SendMatches:
    db = db
    bot = bot
    lock = asyncio.Semaphore(5)
    def __init__(self):
        self.users_for_send = []
        self.user_matches_id = {}
        self.send_storage = {}
        self.matches = []
        self.task_storage: dict[int: Task] = {}
        self.replica = None

    async def start(self):
        """
        Подгружает пользователей из бд и
        создает таски для отправки сообщений пользователям
        :return:
        """
        await db.initial()
        logger.info('Start SendMatches')
        while True:
            self.users_for_send = await self.db.get_row(
                Users,
                to_many=True,
            )
            self.replica = await db.get_row(BotReplicas, unique_name='you_have_match')
            if self.users_for_send:
                await self.set_storage(self.users_for_send)
            for user in self.users_for_send:
                if self.task_storage.get(user.tg_user_id):
                    cur_task = self.task_storage[user.tg_user_id]
                    cur_task.cancel()
                    logger.info('Send_task canceled')
                self.task_storage[user.tg_user_id] = asyncio.create_task(self.send_for_user(user))
                logger.info(f'Create task{self.task_storage}')
            await asyncio.sleep(120)


    async def send_for_user(self, user):
        """
        Проверяет, есть ли match для пользователя и
        делает 5 попыток отправки сообщения пользователю
        :param user:
        :return:
        """
        matches_list = self.send_storage.get(user.tg_user_id)
        amount_matches = len(matches_list)
        if amount_matches != 0:
            try:
                for i_match in matches_list:
                    for _ in range(5):
                        async with self.lock:
                            cancel = False
                            msg = None
                            try:
                                if i_match.user_id_two == user.tg_user_id:
                                    another_user = await db.get_row(Users, tg_user_id=i_match.user_id_one)
                                    flag = 'one'
                                elif i_match.user_id_one == user.tg_user_id:
                                    another_user = await db.get_row(Users, tg_user_id=i_match.user_id_two)
                                    flag = 'two'
                                content = json.loads(another_user.media).get('media')
                                if content[0][0] == 'photo':
                                    if another_user.about_yourself:
                                        description = another_user.about_yourself
                                    else:
                                        description = 'Нет описания'
                                    msg = await bot.send_photo(chat_id=int(user.tg_user_id),
                                                         photo=content[0][1],
                                                         caption=self.replica.replica.format(
                                                            name=another_user.username, age=another_user.age,
                                                            city=another_user.city, desc=description)
                                                         )
                                elif content[0][0] == 'video':
                                    if another_user.about_yourself:
                                        description = another_user.about_yourself
                                    else:
                                        description = 'Нет описания'
                                    msg = await bot.send_video(chat_id=int(user.tg_user_id),
                                                         photo=content[0][1],
                                                         caption=self.replica.replica.format(
                                                             name=another_user.username, age=another_user.age,
                                                             city=another_user.city, desc=description),
                                                         )
                                logger.info(f' Message sent successfully for user {user.username} '
                                            f'{user.tg_user_id}')
                                await asyncio.sleep(10)
                                break
                            except asyncio.CancelledError:
                                cancel = True
                                raise
                            finally:
                                if msg:
                                    if flag == 'one':
                                        await self.db.update_matches_row(Matches, tg_user_id=user.tg_user_id,
                                         tg_user_id_another_user=another_user.tg_user_id, user_id_two=1, is_send=True)
                                    elif flag == 'two':
                                        await self.db.update_matches_row(Matches, tg_user_id=user.tg_user_id,
                                         tg_user_id_another_user=another_user.tg_user_id, user_id_one=1, is_send=True)
            except Exception as exc:
                logger.exception(f'Error send message for user {user.username} with id: '
                                 f'{user.tg_user_id}. Error: {exc}')


    async def set_storage(self, users):
        await asyncio.gather(
            *[self.get_matches_for_user(user.tg_user_id)
              for user in users],
        )

    async def get_matches_for_user(self, user_id):
        """
        Получает свежие match с бд и записывает их в массив
        :param user_id:
        :return:
        """
        logger.info("Get matches for user")
        self.send_storage[user_id] = []
        sql_filter ={"filter": or_(and_(Matches.user_id_one == str(user_id), Matches.user_reaction_one.is_(True),
                                    Matches.user_reaction_two.is_(True), Matches.is_send.is_(False)), and_(
                                    Matches.user_id_two == str(user_id), Matches.user_reaction_one == True,
                                    Matches.user_reaction_two == True, Matches.is_send == False))}
        self.matches = await db.get_row(Matches, to_many=True, filter=sql_filter)
        print(f'id: {user_id} {self.matches}')
        self.send_storage[user_id] = [
            i for i in self.matches
        ]


async def main_send_matches():
    x = SendMatches()
    await x.start()


if __name__ == '__main__':
    asyncio.run(main_send_matches())

# reply_markup=await create_buttons_for_viewing_match(
#                                                              user_id=user.tg_user_id,
#                                                              another_user_id=another_user.tg_user_id)

# ,
#                                                          reply_markup=await create_buttons_for_viewing_match(
#                                                             user_id=user.tg_user_id,
#                                                             another_user_id=another_user.tg_user_id)