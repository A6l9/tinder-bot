import asyncio
from abc import ABC

from loguru import logger
from loader import bot


class Disturb(ABC):
    is_running = False
    send_progress = {}

    @classmethod
    async def run_disturb(cls, users, admins, msg_data):
        cls.is_running = True
        cls.send_progress = {'success': 0, 'failed': 0, 'users': len(users)}
        for user_tg_id in users:
            try:
                if msg_data.get('photo'):
                    print(msg_data.get('photo'))
                    if msg_data.get('text'):
                        await bot.send_photo(user_tg_id, caption=msg_data.get('text'),
                                             photo=msg_data.get('photo')[0])
                    else:
                        await bot.send_photo(user_tg_id, photo=msg_data.get('photo')[0])
                elif msg_data.get('video'):
                    if msg_data.get('text'):
                        await bot.send_video(user_tg_id, caption=msg_data.get('text'),
                                             video=msg_data.get('video'))
                    else:
                        await bot.send_video(user_tg_id, video=msg_data.get('video'))
                elif msg_data.get('video_note'):
                        await bot.send_video_note(user_tg_id,
                                                  video_note=msg_data.get('video_note'))
                elif msg_data.get('text'):
                    await bot.send_message(user_tg_id,
                                              text=msg_data.get('text'))
                cls.send_progress['success'] += 1
            except Exception as e:
                logger.warning(f'Failed send disturb: {e}')
                cls.send_progress['failed'] += 1
            await asyncio.sleep(1)

        for admin in admins:
            text = (
                'Рассылка завершена\n\n'
                f'Запланировано: {Disturb.send_progress["users"]}\n'
                f'Доставлено: {Disturb.send_progress["success"]}\n'
                f'Не удалось: {Disturb.send_progress["failed"]}\n'
            )
            try:
                await bot.send_message(admin,
                                       text=text)
            except Exception as e:
                logger.warning(f'Failed send disturb report: {e}')
            await asyncio.sleep(1)
        cls.is_running = False
