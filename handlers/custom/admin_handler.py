import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from database.models import BotReplicas, Users, Matches
from loader import db, bot, user_manager
from keyboards.inline.inline_kbs import create_admin_panel_buttons, create_close_wrap_admin_panel_button
from handlers.custom.show_my_questionnaire import show_questionnaire
from utils.clear_back import clear_back
from storage.states import States
from aiogram.fsm.storage.base import StorageKey

from utils.extra_tools import CustomCall
from utils.func_for_mailing import Disturb

admin_panel_router = Router()


@admin_panel_router.callback_query(F.data == 'admin_panel')
async def admin_panel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    if not user_data.is_admin:
        replica = await db.get_row(BotReplicas, unique_name='is_not_admin')
        await call.message.answer(replica.replica, protect_content=True)
        await show_questionnaire(call.message)
    else:
        temp_storage = user_manager.get_user(call.from_user.id)
        try:
            await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
        except:
            ...
        replica = await db.get_row(BotReplicas, unique_name='admin_panel_message')
        await call.message.answer(replica.replica, protect_content=True, reply_markup=create_admin_panel_buttons())


@admin_panel_router.callback_query(F.data == 'statistics')
async def statistics(call: CallbackQuery):
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    if not user_data.is_admin:
        replica = await db.get_row(BotReplicas, unique_name='is_not_admin')
        await call.message.answer(replica.replica, protect_content=True)
        await show_questionnaire(call.message)
    else:
        replica = await db.get_row(BotReplicas, unique_name='statistic_message')
        users = await db.get_users_info(Users, to_many=True)
        matches = await db.get_matches_info(Matches, to_many=True)
        await call.message.answer(replica.replica.format(amount=users[2],
                                                         amount_nodone=users[3],
                                                         mans=users[0],
                                                         woman=users[1],
                                                         matches=matches[0],),
                                                         protect_content=True,
                                                         reply_markup=create_close_wrap_admin_panel_button())


@admin_panel_router.callback_query(F.data == 'delete_user_profile')
async def delete_user_profile(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    if not user_data.is_admin:
        replica = await db.get_row(BotReplicas, unique_name='is_not_admin')
        await call.message.answer(replica.replica, protect_content=True)
        await show_questionnaire(call.message)
    else:
        await state.storage.set_data(key=StorageKey(bot_id=call.message.from_user.id,
                                                    user_id=call.from_user.id,
                                                    chat_id=call.from_user.id),
                                     data={str(call.from_user.id): call})
        replica = await db.get_row(BotReplicas, unique_name='write_user_id_for_delete')
        await call.message.answer(replica.replica, protect_content=True,
                                  reply_markup=create_close_wrap_admin_panel_button())
        await state.set_state(States.delete_user_profile)


@admin_panel_router.message(States.delete_user_profile,
                            ~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}))
async def get_user_if_for_delete(message: Message, state: FSMContext):
    user_data = await db.get_row(Users, tg_user_id=str(message.from_user.id))
    if not user_data.is_admin:
        replica = await db.get_row(BotReplicas, unique_name='is_not_admin')
        await message.answer(replica.replica, protect_content=True)
        await show_questionnaire(message)
    else:
        temp_storage = user_manager.get_user(message.from_user.id)
        if message.text.isdigit():
            user_data = await db.get_row(Users, tg_user_id=message.text)
            if user_data and int(user_data.tg_user_id) != message.from_user.id:
                await db.delete_rows(Users, tg_user_id=str(message.text))
                replica = await db.get_row(BotReplicas, unique_name='delete_user_successfully')
                await message.answer(replica.replica)
                await asyncio.sleep(2)
                call = await state.get_data()
                await admin_panel(call[str(message.from_user.id)], state)
                try:
                    await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
                except:
                    ...
                await state.clear()
            else:
                replica = await db.get_row(BotReplicas, unique_name='no_user_with_this_id_delete')
                await message.answer(replica.replica, protect_content=True,
                                     reply_markup=create_close_wrap_admin_panel_button())
                try:
                    await asyncio.sleep(1)
                    await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
                except:
                    ...
        else:
            replica = await db.get_row(BotReplicas, unique_name='wrong_type_user_id_delete')
            await message.answer(replica.replica, protect_content=True,
                                 reply_markup=create_close_wrap_admin_panel_button())
            try:
                await asyncio.sleep(1)
                await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
            except:
                ...


@admin_panel_router.callback_query(F.data == 'ban_user')
async def ban_user_profile(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    if not user_data.is_admin:
        replica = await db.get_row(BotReplicas, unique_name='is_not_admin')
        await call.message.answer(replica.replica, protect_content=True)
        await show_questionnaire(call.message)
    else:
        await state.storage.set_data(key=StorageKey(bot_id=call.message.from_user.id,
                                                    user_id=call.from_user.id,
                                                    chat_id=call.from_user.id),
                                     data={str(call.from_user.id): call})
        replica = await db.get_row(BotReplicas, unique_name='write_user_id_for_ban')
        await call.message.answer(replica.replica, protect_content=True,
                                  reply_markup=create_close_wrap_admin_panel_button())
        await state.set_state(States.ban_user_profile)


@admin_panel_router.message(States.ban_user_profile,
                            ~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}))
async def get_user_if_for_ban(message: Message, state: FSMContext):
    user_data = await db.get_row(Users, tg_user_id=str(message.from_user.id))
    if not user_data.is_admin:
        replica = await db.get_row(BotReplicas, unique_name='is_not_admin')
        await message.answer(replica.replica, protect_content=True)
        await show_questionnaire(message)
    else:
        temp_storage = user_manager.get_user(message.from_user.id)
        if message.text.isdigit():
            user_data = await db.get_row(Users, tg_user_id=message.text)
            if user_data:
                await db.update_user_row(Users, tg_user_id=str(message.text), is_blocked=True)
                replica = await db.get_row(BotReplicas, unique_name='ban_user_successfully')
                await message.answer(replica.replica)
                await asyncio.sleep(2)
                call = await state.get_data()
                await admin_panel(call[str(message.from_user.id)], state)
                try:
                    await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
                except:
                    ...
                await state.clear()
            else:
                replica = await db.get_row(BotReplicas, unique_name='no_user_with_this_id_delete')
                await message.answer(replica.replica, protect_content=True,
                                     reply_markup=create_close_wrap_admin_panel_button())
                try:
                    await asyncio.sleep(1)
                    await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
                except:
                    ...
        else:
            replica = await db.get_row(BotReplicas, unique_name='wrong_type_user_id_delete')
            await message.answer(replica.replica, protect_content=True,
                                 reply_markup=create_close_wrap_admin_panel_button())
            try:
                await asyncio.sleep(1)
                await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
            except:
                ...


@admin_panel_router.message(States.mailing, ~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}),
                            F.content_type.in_({'photo', 'video', 'video_note', 'text'}))
async def new_post_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    msg_data = state_data.get('msg_data', {})
    try:
        text = message.html_text
        msg_data.update(text=text)
    except:
        text = None
    photos = None
    if message.content_type == 'photo':
        if not message.media_group_id:
            photos = [message.photo[-1].file_id]
        else:
            media_group = state_data.get('media_group', [])
            if text:
                msg_data.update(text=text)
            await asyncio.sleep(1)
            state_data = await state.get_data()
            new_media_group = state_data.get('media_group', [])
            if len(media_group) != len(new_media_group):
                notifs = state_data.get('notif', [])
                notifs.append(message)
                await state.update_data(notif=notifs, msg_data=msg_data)
                return

        msg_data.update(photo=photos, video=None, video_note=None)

    elif message.content_type == 'video':
        msg_data.update(video=message.video.file_id, photo=None, text=text, video_note=None)
    elif message.content_type == 'video_note':
        msg_data.update(video_note=message.video_note.file_id, photo=None, text=None, video=None)

    call = state_data.get('call', CustomCall(message))
    await state.update_data(notif=[], msg_data=msg_data)
    call.data = f'view_{state_data.get("current_key")}'
    return await admin_distrub(call, state)

@admin_panel_router.callback_query(F.data == 'mailing')
async def admin_distrub(call: CustomCall, state: FSMContext):
    state_data = await state.get_data()
    if Disturb.is_running:
        text = (
            'Идет рассылка\n\n'
            f'Запланировано: {Disturb.send_progress["users"]}\n'
            f'Доставлено: {Disturb.send_progress["success"]}\n'
            f'Не удалось: {Disturb.send_progress["failed"]}\n'
        )
    else:
        if state_data.get('msg_data'):
            user_rows = await db.get_row(Users, to_many=True, done_questionnaire=True, order_by='id')
            users = [user.tg_user_id for user in user_rows]
            admins = [user.tg_user_id for user in user_rows if user.is_admin]
            asyncio.create_task(Disturb.run_disturb(users, admins, state_data.get('msg_data')))
            await state.clear()
            text = 'Рассылка началась. По окончании рассылки вам придет уведомление'

        else:
            await state.set_state(States.mailing)
            text = 'Отправьте сообщение для рассылки'
    return await call.message.answer(
        text
    )


@admin_panel_router.callback_query(F.data == 'close_wrap_admin_panel')
async def close_wrap_admin_panel(call: CallbackQuery, state: FSMContext):
    await admin_panel(call, state)


@admin_panel_router.callback_query(F.data == 'close_admin_panel')
async def close_admin_panel(call: CallbackQuery):
        await show_questionnaire(call.message)
