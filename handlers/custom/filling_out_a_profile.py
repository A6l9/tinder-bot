import asyncio
import json

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from loguru import logger

from utils.clear_back import clear_back
from utils.function_for_sending_a_profile import func_for_send_prof
from utils.haversine import haversine
from loader import db, user_manager
from database.models import BotReplicas, Users, Cities
from aiogram.fsm.context import FSMContext
from keyboards.inline.inline_kbs import (create_sex_buttons, create_preference_buttons, create_location_buttons,
                                         create_name_question, create_buttons_cities, create_skip_button, \
                                         create_add_or_no_buttons, create_goto_profile_if_limit_photo_button,
                                         create_go_to_somewhere_buttons)
from keyboards.reply.reply_kbs import create_share_location_button
from storage.states import States
from utils.user_lock import get_user_lock
from utils.get_picture import get_picture
from loader import bot

profile_router = Router()

@profile_router.callback_query(F.data == 'start_completion')
async def start_completion(call: CallbackQuery, state: FSMContext):
    await db.initial()
    user_lock = await get_user_lock(call.from_user.id)
    user = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    if user.is_blocked:
        replica = await db.get_row(BotReplicas, unique_name='is_blocked')
        await call.message.answer(replica.replica, protect_content=False)
    else:
        await db.update_user_row(Users, tg_user_id=str(call.from_user.id), media=json.dumps({"media": []}),
                                 about_yourself=None)
        async with user_lock:
            if not user:
                try:
                    temp_storage = user_manager.get_user(call.from_user.id)
                    temp_storage.start_message = call.message
                    await db.add_row(Users, tg_user_id=str(call.from_user.id))
                except Exception as exc:
                    logger.error(exc)
                    await call.message.answer('Произошла ошибка, попробуйте еще раз!', protect_content=False)
        await state.set_state(States.age_question)
        replica = await db.get_row(BotReplicas, unique_name='age_question')
        await call.message.edit_text(replica.replica)

@profile_router.message(~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}), States.age_question,
                        F.text)
async def age_question_take_answer(message: Message, state: FSMContext):
    temp_storage = user_manager.get_user(message.from_user.id)
    if message.text:
        if message.text.isdigit() and 16 <= int(message.text) < 46:
            try:
                await db.update_user_row(model=Users, tg_user_id=message.from_user.id, age=str(message.text))
                replica = await db.get_row(BotReplicas, unique_name='sex_question')
                await message.answer(replica.replica, protect_content=False, reply_markup=create_sex_buttons())
                await state.clear()
            except Exception as exc:
                logger.error(f'Error updating user age: {exc}')
        else:
            replica = await db.get_row(BotReplicas, unique_name='wrong_age')
            await message.answer(replica.replica, protect_content=False)
    try:
        await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
    except:
        ...

@profile_router.callback_query(F.data.startswith('sex_'))
async def sex_question_take_answer(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    sex = call.data.split('_')[1]
    try:
        await db.update_user_row(model=Users, tg_user_id=call.from_user.id, sex=sex)
        replica = await db.get_row(BotReplicas, unique_name='preference_question')
        await call.message.answer(replica.replica, protect_content=False, reply_markup=create_preference_buttons())
    except Exception as exc:
        logger.error(f'Error updating user sex: {exc}')
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...

@profile_router.callback_query(F.data.startswith('preference_'))
async def preference_question_take_answer(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    preference = call.data.split('_')[1]
    try:
        await db.update_user_row(model=Users, tg_user_id=call.from_user.id, preference=preference)
        replica = await db.get_row(BotReplicas, unique_name='city_question')
        await call.message.answer(replica.replica, protect_content=False, reply_markup=create_location_buttons())
    except Exception as exc:
        logger.error(f'Error updating user preference: {exc}')
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...

@profile_router.callback_query(F.data.startswith('location_'))
async def location_question_take_answer(call: CallbackQuery, state: FSMContext):
    type_record_location = call.data.split('_')[1]
    if type_record_location == 'share':
        try:
            replica = await db.get_row(BotReplicas, unique_name='share_location')
            await call.message.answer(replica.replica, protect_content=False,
                                      reply_markup=create_share_location_button())
            await state.set_state(States.location_share)
        except Exception as exc:
            logger.error(f'Error take user location: {exc}')
    elif type_record_location == 'write':
        try:
            replica = await db.get_row(BotReplicas, unique_name='write_location')
            await call.message.answer(replica.replica, protect_content=False)
            await state.set_state(States.location_write)
        except Exception as exc:
            logger.error(f'Error take user location: {exc}')


@profile_router.message(States.location_write, ~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}),
                        F.text)
async def location_write_search_city(message: Message, state: FSMContext):
    temp_storage = user_manager.get_user(message.from_user.id)
    cities_matches = await db.search_cities(str(message.text))
    if cities_matches:
        replica = await db.get_row(BotReplicas, unique_name='city_choose')
        await message.answer(replica.replica, protect_content=False, reply_markup=create_buttons_cities(cities_matches))
        await state.clear()
        try:
            await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
        except:
            ...
    else:
        replica = await db.get_row(BotReplicas, unique_name='city_not_found')
        await message.answer(replica.replica, protect_content=False)


@profile_router.callback_query(F.data.startswith('city_'))
async def location_write_take_answer(call: CallbackQuery, state: FSMContext):
    temp_storage = user_manager.get_user(call.from_user.id)
    city_code = call.data.split('_')[1]
    city = await db.get_row(Cities, postal_code=int(city_code))
    if city:
        try:
            await db.update_user_row(model=Users, tg_user_id=call.from_user.id, address=city.address,
                                 postal_code=city.postal_code, country=city.country,
                                 federal_district=city.federal_district, region_type=city.region_type,
                                 region=city.region, area_type=city.area_type, area=city.area,
                                 city_type=city.city_type, city=city.city)
            replica = await db.get_row(BotReplicas, unique_name='name_question')
            if call.from_user.first_name:
                await call.message.answer(replica.replica, protect_content=False,
                                          reply_markup=create_name_question(call.from_user.first_name,
                                                                            flag='first_name'))
            elif call.from_user.username:
                await call.message.answer(replica.replica, protect_content=False,
                                          reply_markup=create_name_question(call.from_user.username,
                                                                                 flag='username'))
            await state.set_state(States.name_question)
        except Exception as exc:
            logger.error(f'Error updating user location: {exc}')
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...


@profile_router.message(States.location_share, F.location)
async def location_share_take_answer(message: Message, state: FSMContext):
    temp_storage = user_manager.get_user(message.from_user.id)
    cities = await db.get_row(Cities, to_many=True)
    latitude = message.location.latitude
    longitude = message.location.longitude
    location = False
    for city in cities:
        distance = haversine(float(city.geo_lat), float(city.geo_lon), float(latitude), float(longitude))
        if distance < 20:
            location = True
            try:
                await bot.send_message(message.from_user.id, 'Обработка...', reply_markup=ReplyKeyboardRemove())
                await asyncio.sleep(1)
                await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
                await db.update_user_row(model=Users, tg_user_id=message.from_user.id, address=city.address,
                                         postal_code=city.postal_code, country=city.country,
                                         federal_district=city.federal_district, region_type=city.region_type,
                                         region=city.region, area_type=city.area_type, area=city.area,
                                         city_type=city.city_type, city=city.city)
                replica = await db.get_row(BotReplicas, unique_name='name_question')
                if message.from_user.first_name:
                    await message.answer(replica.replica, protect_content=False,
                                              reply_markup=create_name_question(message.from_user.first_name,
                                                                                flag='first_name'))
                elif message.from_user.username:
                    await message.answer(replica.replica, protect_content=False,
                                              reply_markup=create_name_question(message.from_user.username,
                                                                                flag='username'))
                await state.set_state(States.name_question)
            except Exception as exc:
                logger.error(f'Error updating user location: {exc}')
            break
    if location:
        ...
    else:
        replica = await db.get_row(BotReplicas, unique_name='location_false')
        await message.answer(replica.replica, protect_content=False, reply_markup=create_location_buttons())
        try:
            await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
        except:
            ...


@profile_router.callback_query(F.data.startswith('name_'))
async def name_question_take_answer_from_button(call: CallbackQuery, state: FSMContext):
    temp_storage = user_manager.get_user(call.from_user.id)
    type_name = call.data.split('_')[1]
    try:
        if type_name == 'username':
            await db.update_user_row(model=Users, tg_user_id=call.from_user.id, username=call.from_user.username)
        elif type_name == 'firstname':
            await db.update_user_row(model=Users, tg_user_id=call.from_user.id, username=call.from_user.first_name)
        replica = await db.get_row(BotReplicas, unique_name='about_yourself')
        await call.message.answer(replica.replica, protect_content=False, reply_markup=create_skip_button())
        await state.set_state(States.about_yourself)
    except Exception as exc:
        logger.error(f'Error updating username: {exc}')
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...

@profile_router.message(States.name_question, ~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}),
                        F.text)
async def name_question_take_answer_from_message(message: Message, state: FSMContext):
    temp_storage = user_manager.get_user(message.from_user.id)
    try:
        await db.update_user_row(model=Users, tg_user_id=message.from_user.id, username=str(message.text))
        replica = await db.get_row(BotReplicas, unique_name='about_yourself')
        await message.answer(replica.replica, protect_content=False, reply_markup=create_skip_button())
        await state.set_state(States.about_yourself)
    except Exception as exc:
        logger.error(f'Error updating username: {exc}')
    try:
        await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
    except:
        ...


@profile_router.callback_query(F.data == 'skip')
async def about_yourself_skip(call: CallbackQuery, state: FSMContext):
    temp_storage = user_manager.get_user(call.from_user.id)
    replica = await db.get_row(BotReplicas, unique_name='send_video_or_photo')
    await call.message.answer(replica.replica.replace('|n', '\n'), protect_content=False,)
    await state.set_state(States.send_video_or_photo)
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...


@profile_router.message(States.about_yourself, F.text,
                        ~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}))
async def about_yourself_get_answer(message: Message, state: FSMContext):
    temp_storage = user_manager.get_user(message.from_user.id)
    description = message.text
    if description:
        try:
            await db.update_user_row(model=Users, tg_user_id=message.from_user.id, about_yourself=description)
            replica = await db.get_row(BotReplicas, unique_name='send_video_or_photo')
            await message.answer(replica.replica.replace('|n', '\n'), protect_content=False)
            await state.set_state(States.send_video_or_photo)
        except Exception as exc:
            logger.error(f'Error updating user description: {exc}')
    else:
        replica = await db.get_row(BotReplicas, unique_name='null_description')
        await message.answer(replica.replica, protect_content=False,)
    try:
        await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
    except:
        ...


@profile_router.message(States.send_video_or_photo, F.content_type.in_({'photo', 'video', 'video_note'}))
async def take_photo_or_video(message: Message, state: FSMContext):
    temp_storage = user_manager.get_user(message.from_user.id)
    storage = await state.get_data()
    if message.photo:
        content_type = 'photo'
        if message.media_group_id:
            if storage.get(message.media_group_id):
                ...
            else:
                await state.update_data({message.media_group_id: True})
                replica = await db.get_row(BotReplicas, unique_name='only_one_photo_or_video')
                await message.answer(replica.replica, protect_content=False,)
        else:
            user_data = await db.get_row(Users, tg_user_id=str(message.from_user.id))
            list_media = json.loads(user_data.media).get('media')
            list_media_url_format = json.loads(user_data.media_url_format).get('media')
            if len(list_media) == 5:
                replica = await db.get_row(BotReplicas, unique_name='media_limit_exceeded')
                await message.answer(replica.replica.replace('|n', '\n'), protect_content=False,
                                     reply_markup=create_goto_profile_if_limit_photo_button())
                await state.clear()
            else:
                file_id = message.photo[-1].file_id
                list_media.insert(0, [content_type, file_id])
                list_media_url_format.insert(0, [content_type, await get_picture(file_id)])
                await db.update_user_row(model=Users, tg_user_id=message.from_user.id,
                                         media=json.dumps({'media': list_media}),
                                         media_url_format=json.dumps({'media': list_media_url_format}))
                if len(list_media) == 5:
                    replica = await db.get_row(BotReplicas, unique_name='media_limit_exceeded')
                    await message.answer(replica.replica.replace('|n', '\n'), protect_content=False,
                                         reply_markup=create_goto_profile_if_limit_photo_button())
                    await state.clear()
                else:
                    replica = await db.get_row(BotReplicas, unique_name='add_more_media')
                    await message.answer(replica.replica, protect_content=False,
                                         reply_markup=create_add_or_no_buttons())
                    await state.set_state(States.add_or_no_media)
    elif message.video:
        content_type = 'video'
        if message.video.duration <=15:
            user_data = await db.get_row(Users, tg_user_id=str(message.from_user.id))
            list_media = json.loads(user_data.media).get('media')
            list_media_url_format = json.loads(user_data.media_url_format).get('media')
            if len(list_media) == 5:
                replica = await db.get_row(BotReplicas, unique_name='media_limit_exceeded')
                await message.answer(replica.replica.replace('|n', '\n'), protect_content=False,
                                     reply_markup=create_goto_profile_if_limit_photo_button())
                await state.clear()
            else:
                file_id = message.video.file_id
                list_media.insert(0, [content_type, file_id])
                list_media_url_format.insert(0, [content_type, await get_picture(file_id)])
                await db.update_user_row(model=Users, tg_user_id=message.from_user.id,
                                         media=json.dumps({'media': list_media}),
                                         media_url_format=json.dumps({'media': list_media_url_format}))
                replica = await db.get_row(BotReplicas, unique_name='add_more_media')
                await message.answer(replica.replica, protect_content=False, reply_markup=create_add_or_no_buttons())
                await state.set_state(States.add_or_no_media)
        else:
            replica = await db.get_row(BotReplicas, unique_name='wrong_duration')
            await message.answer(replica.replica, protect_content=False,)
    elif message.video_note:
        replica = await db.get_row(BotReplicas, unique_name='videonote_warning')
        await message.answer(replica.replica, protect_content=False)
    else:
        replica = await db.get_row(BotReplicas, unique_name='wrong_type')
        await message.answer(replica.replica, protect_content=False)
    try:
        await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
    except:
        ...


@profile_router.message(States.send_video_or_photo, F.content_type.in_({'document', 'voice', 'sticker', 'text'}))
async def if_another_type_media(message: Message, state: FSMContext):
    await state.clear()
    replica = await db.get_row(BotReplicas, unique_name='wrong_type')
    await message.answer(replica.replica)
    await state.set_state(States.send_video_or_photo)

@profile_router.callback_query(States.add_or_no_media, F.data == 'yes_more_media')
async def yes_add_more_media(call: CallbackQuery, state: FSMContext):
    temp_storage = user_manager.get_user(call.from_user.id)
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    list_media = json.loads(user_data.media).get('media')
    if len(list_media) == 5:
        replica = await db.get_row(BotReplicas, unique_name='media_limit_exceeded')
        await call.message.answer(replica.replica.replace('|n', '\n'), protect_content=False,
                             reply_markup=create_goto_profile_if_limit_photo_button())
        await state.clear()
    else:
        replica = await db.get_row(BotReplicas, unique_name='send_video_or_photo')
        await call.message.answer(replica.replica.replace('|n', '\n'), protect_content=False)
        await state.set_state(States.send_video_or_photo)
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...


@profile_router.callback_query(States.add_or_no_media, F.data == 'no_more_media')
async def no_more_media(call: CallbackQuery, state: FSMContext):
    temp_storage = user_manager.get_user(call.from_user.id)
    await db.update_user_row(Users, tg_user_id=str(call.from_user.id), done_questionnaire=True)
    replica = await db.get_row(BotReplicas, unique_name='done_questionnaire')
    await call.message.answer(replica.replica, protect_content=False, reply_markup=create_go_to_somewhere_buttons())
    await state.clear()
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...


@profile_router.callback_query(F.data == 'ok_goto_profile')
async def goto_profile(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    await db.update_user_row(Users, tg_user_id=str(call.from_user.id), done_questionnaire=True)
    replica = await db.get_row(BotReplicas, unique_name='done_questionnaire')
    await call.message.answer(replica.replica, protect_content=False,)
    await func_for_send_prof(call.from_user.id, call.message)
    try:
        await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
    except:
        ...
