import asyncio
import json
import re

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.models import BotReplicas, Users, Matches, Cities
from loader import db, bot, user_manager
from keyboards.inline.inline_kbs import create_admin_panel_buttons, create_close_wrap_admin_panel_button, \
    create_buttons_cities_mailing, create_sex_buttons_mailing, create_buttons_for_ban_profile, \
    create_buttons_for_delete_profile
from handlers.custom.show_my_questionnaire import show_questionnaire
from utils.clear_back import clear_back
from storage.states import States
from loguru import logger
from utils.extra_tools import CustomCall
from utils.func_for_mailing import Disturb

admin_panel_router = Router()


@admin_panel_router.callback_query(F.data == 'admin_panel')
async def admin_panel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    try:
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
    except Exception as exc:
        logger.exception(f'Exception {exc}')


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
        if message.text.startswith('@'):
            username = message.text[1:]
            user_data = await db.get_row(Users, tg_username=username)
        else:
            username = message.text
            user_data = await db.get_row(Users, tg_username=username)
        if user_data and user_data.done_questionnaire:
            user_tg_id = {'user_tg_id': user_data.tg_user_id}
            await state.update_data(user_tg_id)
            replica = await db.get_row(BotReplicas, unique_name='show_profile')
            if json.loads(user_data.media).get('media'):
                content = json.loads(user_data.media).get('media')
                if user_data.about_yourself:
                    description = user_data.about_yourself
                else:
                    description = 'Нет описания'
                if content[temp_storage.num_elem][0] == 'photo':
                    sex = None
                    if user_data.sex == 'man':
                        sex = 'Мужской'
                    elif user_data.sex == 'woman':
                        sex = 'Женский'
                    await bot.send_photo(chat_id=message.chat.id,
                                         photo=content[temp_storage.num_elem][1],
                                         protect_content=True,
                                         caption=replica.replica.replace('|n', '\n').format(
                                             name=user_data.username,
                                             age=user_data.age,
                                             sex=sex,
                                             city=user_data.city,
                                             desc=description),
                                         reply_markup=create_buttons_for_delete_profile())
                elif content[temp_storage.num_elem][0] == 'video':
                    if user_data.about_yourself:
                        description = user_data.about_yourself
                    else:
                        description = 'Нет описания'
                    sex = None
                    if user_data.sex == 'man':
                        sex = 'Мужской'
                    elif user_data.sex == 'woman':
                        sex = 'Женский'
                    await bot.send_video(chat_id=message.chat.id,
                                         video=content[temp_storage.num_elem][1],
                                         protect_content=True,
                                         caption=replica.replica.replace('|n', '\n').format(
                                             name=user_data.username,
                                             age=user_data.age,
                                             sex=sex,
                                             city=user_data.city,
                                             desc=description),
                                         reply_markup=create_buttons_for_delete_profile())
        else:
            replica = await db.get_row(BotReplicas, unique_name='no_user_with_this_id_delete')
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
        if message.text.startswith('@'):
            username = message.text[1:]
            user_data = await db.get_row(Users, tg_username=username)
        else:
            username = message.text
            user_data = await db.get_row(Users, tg_username=username)
        if user_data and user_data.done_questionnaire:
            user_tg_id = {'user_tg_id': user_data.tg_user_id}
            await state.update_data(user_tg_id)
            replica = await db.get_row(BotReplicas, unique_name='show_profile')
            if json.loads(user_data.media).get('media'):
                content = json.loads(user_data.media).get('media')
                if user_data.about_yourself:
                    description = user_data.about_yourself
                else:
                    description = 'Нет описания'
                if content[temp_storage.num_elem][0] == 'photo':
                    sex = None
                    if user_data.sex == 'man':
                        sex = 'Мужской'
                    elif user_data.sex == 'woman':
                        sex = 'Женский'
                    await bot.send_photo(chat_id=message.chat.id,
                                         photo=content[temp_storage.num_elem][1],
                                         protect_content=True,
                                         caption=replica.replica.replace('|n', '\n').format(
                                             name=user_data.username,
                                             age=user_data.age,
                                             sex=sex,
                                             city=user_data.city,
                                             desc=description),
                                         reply_markup=create_buttons_for_ban_profile())
                elif content[temp_storage.num_elem][0] == 'video':
                    if user_data.about_yourself:
                        description = user_data.about_yourself
                    else:
                        description = 'Нет описания'
                    sex = None
                    if user_data.sex == 'man':
                        sex = 'Мужской'
                    elif user_data.sex == 'woman':
                        sex = 'Женский'
                    await bot.send_video(chat_id=message.chat.id,
                                         video=content[temp_storage.num_elem][1],
                                         protect_content=True,
                                         caption=replica.replica.replace('|n', '\n').format(
                                             name=user_data.username,
                                             age=user_data.age,
                                             sex=sex,
                                             city=user_data.city,
                                             desc=description),
                                         reply_markup=create_buttons_for_ban_profile())
        else:
            replica = await db.get_row(BotReplicas, unique_name='no_user_with_this_id_delete')
            await message.answer(replica.replica, protect_content=True,
                                 reply_markup=create_close_wrap_admin_panel_button())
            try:
                await asyncio.sleep(1)
                await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
            except:
                ...
        try:
            await asyncio.sleep(1)
            await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
        except:
            ...


@admin_panel_router.callback_query(F.data == 'ban_user_profile')
async def yes_ban_user_profile(call: CallbackQuery, state: FSMContext):
    temp_storage = user_manager.get_user(call.from_user.id)
    state_data = await state.get_data()
    user_tg_id = state_data.get('user_tg_id')
    await db.update_user_row(Users, tg_user_id=user_tg_id, is_blocked=True)
    replica = await db.get_row(BotReplicas, unique_name='ban_user_successfully')
    await call.message.answer(replica.replica)
    await asyncio.sleep(2)
    await admin_panel(call, state)
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...


@admin_panel_router.callback_query(F.data == 'yes_delete_user_profile')
async def yes_delete_user_profile(call: CallbackQuery, state: FSMContext):
    temp_storage = user_manager.get_user(call.from_user.id)
    state_data = await state.get_data()
    user_tg_id = state_data.get('user_tg_id')
    await db.delete_rows(Users, tg_user_id=user_tg_id)
    replica = await db.get_row(BotReplicas, unique_name='delete_user_successfully')
    await call.message.answer(replica.replica)
    await asyncio.sleep(2)
    await admin_panel(call, state)
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...
    await state.clear()


@admin_panel_router.callback_query(F.data == 'write_username_again_delete')
async def write_username_again_delete(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.delete_user_profile)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await delete_user_profile(call, state)


@admin_panel_router.callback_query(F.data == 'write_username_again_ban')
async def write_username_again_ban(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.ban_user_profile)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await ban_user_profile(call, state)



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
            user_rows = await db.get_users_for_mailing(parameters=state_data.get('parameters'))
            admins = await db.get_row(Users, is_admin=True, to_many=True, done_questionnaire=True)
            users = [user.tg_user_id for user in user_rows]
            admins = [user.tg_user_id for user in admins]
            asyncio.create_task(Disturb.run_disturb(users, admins, state_data.get('msg_data')))
            await state.clear()
            text = 'Рассылка началась. По окончании рассылки вам придет уведомление'
        else:
            replica = await db.get_row(BotReplicas, unique_name='write_city_mailing')
            await state.set_state(States.city_parameter_for_mailing)
            return await call.message.answer(replica.replica, protect_content=True,
                                             reply_markup=create_close_wrap_admin_panel_button())
    return await call.message.answer(
        text
    )


@admin_panel_router.message(States.city_parameter_for_mailing,
                            ~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}), F.text)
async def write_city_mailing(message: Message):
    city_matches = await db.search_cities(message.text)
    if city_matches:
        replica = await db.get_row(BotReplicas, unique_name='city_choose')
        await message.answer(replica.replica, protect_content=True,
                             reply_markup=create_buttons_cities_mailing(city_matches))
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        replica = await db.get_row(BotReplicas, unique_name='city_not_found')
        await message.answer(replica.replica, protect_content=True)


@admin_panel_router.callback_query(F.data.startswith('mailing_city_'))
async def location_for_mailing_take_answer(call: CallbackQuery, state: FSMContext):
    city_code = call.data.split('_')[2]
    city = await db.get_row(Cities, postal_code=int(city_code))
    state_data = await state.get_data()
    if city:
        if await db.get_users_with_city(postal_code=int(city_code)):
            parameters = state_data.get('parameters', {})
            parameters.update(city=city.address)
            await state.update_data(parameters=parameters)
            await state.set_state(States.age_parameter_for_mailing)
            replica = await db.get_row(BotReplicas, unique_name='write_age_range_mailing')
            await call.message.edit_text(replica.replica, protect_content=True)
        else:
            replica = await db.get_row(BotReplicas, unique_name='users_with_city_not_found')
            await call.message.answer(replica.replica, protect_content=True)


@admin_panel_router.message(States.age_parameter_for_mailing,
                            ~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}), F.text)
async def take_answer_age_mailing(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if message.text:
        pattern = r'^\d{2}-\d{2}$'
        match = re.search(pattern, str(message.text))
        if match:
            if (int(match.group().split('-')[0]) == int(match.group().split('-')[1]) and
                    16 <= int(match.group().split('-')[0]) < 46 and 16 <= int(match.group().split('-')[1]) < 46):
                if await db.get_users_with_age(match.group(), address=state_data.get('parameters')['city']):
                    parameters = state_data.get('parameters', {})
                    parameters.update(age_range=message.text)
                    await state.update_data(parameters=parameters)
                    replica = await db.get_row(BotReplicas, unique_name='choose_sex_mailing')
                    await message.answer(replica.replica, protect_content=True,
                                         reply_markup=create_sex_buttons_mailing())
                else:
                    replica = await db.get_row(BotReplicas, unique_name='users_with_age_not_found')
                    await message.answer(replica.replica, protect_content=True)
            elif (16 <= int(match.group().split('-')[0]) < 46 and 16 <= int(match.group().split('-')[1]) < 46
                  and int(match.group().split('-')[0]) < int(match.group().split('-')[1])):
                if await db.get_users_with_age(match.group(), address=state_data.get('parameters')['city']):
                    parameters = state_data.get('parameters', {})
                    parameters.update(age_range=message.text)
                    await state.update_data(parameters=parameters)
                    replica = await db.get_row(BotReplicas, unique_name='choose_sex_mailing')
                    await message.answer(replica.replica, protect_content=True,
                                         reply_markup=create_sex_buttons_mailing())
                else:
                    replica = await db.get_row(BotReplicas, unique_name='users_with_age_not_found')
                    await message.answer(replica.replica, protect_content=True)
            else:
                replica = await db.get_row(BotReplicas, unique_name='wrong_age_range')
                await message.answer(replica.replica, protect_content=True)
        else:
            replica = await db.get_row(BotReplicas, unique_name='wrong_type_age_range')
            await message.answer(replica.replica.replace('|n', '\n'), protect_content=True)


@admin_panel_router.callback_query(F.data.startswith('mailing_sex_'))
async def take_answer_sex_mailing(call: CallbackQuery, state: FSMContext):
    sex = call.data.split('_')[2]
    state_data = await state.get_data()
    if await db.get_row(Users, to_many=True, sex=sex, address=state_data['parameters']['city']) or sex == 'no':
        parameters = state_data.get('parameters', {})
        parameters.update(sex=sex)
        await state.update_data(parameters=parameters)
        await state.set_state(States.mailing)
        replica = await db.get_row(BotReplicas, unique_name='write_mailing_message')
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(replica.replica, protect_content=True)
    else:
        replica = await db.get_row(BotReplicas, unique_name='users_with_sex_not_found')
        await call.message.edit_text(replica.replica, protect_content=True, reply_markup=create_sex_buttons_mailing())


@admin_panel_router.callback_query(F.data == 'close_wrap_admin_panel')
async def close_wrap_admin_panel(call: CallbackQuery, state: FSMContext):
    await admin_panel(call, state)


@admin_panel_router.callback_query(F.data == 'close_admin_panel')
async def close_admin_panel(call: CallbackQuery):
        await show_questionnaire(call.message)
