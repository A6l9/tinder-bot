import asyncio
import json

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from loguru import logger

from utils.haversine import haversine

from loader import db
from database.models import BotReplicas, Users, Cities
from aiogram.fsm.context import FSMContext
from keyboards.inline.inline_kbs import (create_sex_buttons, create_preference_buttons, create_location_buttons,
                                         create_name_question, create_buttons_cities, create_skip_button,
                                         )
from keyboards.reply.reply_kbs import create_share_location_button
from storage.states import States
from loader import bot

profile_router = Router()

@profile_router.callback_query(F.data == 'start_completion')
async def start_completion(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.age_question)
    replica = await db.get_row(BotReplicas, unique_name='age_question')
    await call.message.edit_text(replica.replica)

@profile_router.message(States.age_question)
async def age_question_take_answer(message: Message, state: FSMContext):
    if message.text.isdigit() and 10 <= int(message.text) < 100:
        try:
            await db.update_user_row(model=Users, tg_user_id=message.from_user.id, age=str(message.text))
            replica = await db.get_row(BotReplicas, unique_name='sex_question')
            await message.answer(replica.replica, reply_markup=create_sex_buttons())
            await state.clear()
        except Exception as exc:
            logger.error(f'Error updating user age: {exc}')
    else:
        replica = await db.get_row(BotReplicas, unique_name='wrong_age')
        await message.answer(replica.replica)

@profile_router.callback_query(F.data.startswith('sex_'))
async def sex_question_take_answer(call: CallbackQuery):
    sex = call.data.split('_')[1]
    try:
        await db.update_user_row(model=Users, tg_user_id=call.from_user.id, sex=sex)
        replica = await db.get_row(BotReplicas, unique_name='preference_question')
        await call.message.answer(replica.replica, reply_markup=create_preference_buttons())
    except Exception as exc:
        logger.error(f'Error updating user sex: {exc}')

@profile_router.callback_query(F.data.startswith('preference_'))
async def preference_question_take_answer(call: CallbackQuery):
    preference = call.data.split('_')[1]
    try:
        await db.update_user_row(model=Users, tg_user_id=call.from_user.id, preference=preference)
        replica = await db.get_row(BotReplicas, unique_name='city_question')
        await call.message.answer(replica.replica, reply_markup=create_location_buttons())
    except Exception as exc:
        logger.error(f'Error updating user preference: {exc}')

@profile_router.callback_query(F.data.startswith('location_'))
async def location_question_take_answer(call: CallbackQuery, state: FSMContext):
    type_record_location = call.data.split('_')[1]
    if type_record_location == 'share':
        try:
            replica = await db.get_row(BotReplicas, unique_name='share_location')
            await call.message.answer(replica.replica, reply_markup=create_share_location_button())
            await state.set_state(States.location_share)
        except Exception as exc:
            logger.error(f'Error take user location: {exc}')
    elif type_record_location == 'write':
        try:
            replica = await db.get_row(BotReplicas, unique_name='write_location')
            await call.message.answer(replica.replica)
            await state.set_state(States.location_write)
        except Exception as exc:
            logger.error(f'Error take user location: {exc}')


@profile_router.message(States.location_write)
async def location_write_search_city(message: Message, state: FSMContext):
    cities_matches = await db.search_cities(str(message.text))
    if cities_matches:
        replica = await db.get_row(BotReplicas, unique_name='city_choose')
        await message.answer(replica.replica, reply_markup=create_buttons_cities(cities_matches))
        await state.clear()
    else:
        replica = await db.get_row(BotReplicas, unique_name='city_not_found')
        await message.answer(replica.replica)


@profile_router.callback_query(F.data.startswith('city_'))
async def location_write_take_answer(call: CallbackQuery, state: FSMContext):
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
            await call.message.answer(replica.replica, reply_markup=create_name_question(call.from_user.username))
            await state.set_state(States.name_question)
        except Exception as exc:
            logger.error(f'Error updating user location: {exc}')

@profile_router.message(States.location_share, F.location)
async def location_share_take_answer(message: Message, state: FSMContext):
    cities = await db.get_row(Cities, to_many=True)
    latitude = message.location.latitude
    longitude = message.location.longitude
    for city in cities:
        distance = haversine(float(city.geo_lat), float(city.geo_lon), float(latitude), float(longitude))
        if distance < 20:
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
                await message.answer(replica.replica, reply_markup=create_name_question(message.from_user.username))
                await state.set_state(States.name_question)
            except Exception as exc:
                logger.error(f'Error updating user location: {exc}')
            break

@profile_router.callback_query(F.data.startswith('name_'))
async def name_question_take_answer_from_button(call: CallbackQuery, state: FSMContext):
    try:
        await db.update_user_row(model=Users, tg_user_id=call.from_user.id, username=call.from_user.username)
        replica = await db.get_row(BotReplicas, unique_name='about_yourself')
        await call.message.answer(replica.replica, reply_markup=create_skip_button())
        await state.set_state(States.about_yourself)
    except Exception as exc:
        logger.error(f'Error updating username: {exc}')

@profile_router.message(States.name_question)
async def name_question_take_answer_from_message(message: Message, state: FSMContext):
    get_username = await db.get_row(Users, username=str(message.text))
    if not get_username:
        try:
            await db.update_user_row(model=Users, tg_user_id=message.from_user.id, username=str(message.text))
            replica = await db.get_row(BotReplicas, unique_name='about_yourself')
            await message.answer(replica.replica, reply_markup=create_skip_button())
            await state.set_state(States.about_yourself)
        except Exception as exc:
            logger.error(f'Error updating username: {exc}')
    elif get_username and get_username.tg_user_id == str(message.from_user.id):
        replica = await db.get_row(BotReplicas, unique_name='write_name_another')
        await message.answer(replica.replica)
    else:
        replica = await db.get_row(BotReplicas, unique_name='name_is_busy')
        await message.answer(replica.replica)

@profile_router.callback_query(F.data == 'skip')
async def about_yourself_skip(call: CallbackQuery, state: FSMContext):
    replica = await db.get_row(BotReplicas, unique_name='send_video_or_photo')
    await call.message.answer(replica.replica.replace('|n', '\n'))
    await state.set_state(States.send_video_or_photo)

@profile_router.message(States.about_yourself)
async def about_yourself_get_answer(message: Message, state: FSMContext):
    description = message.text
    if description:
        try:
            await db.update_user_row(model=Users, tg_user_id=message.from_user.id, about_yourself=description)
            replica = await db.get_row(BotReplicas, unique_name='send_video_or_photo')
            await message.answer(replica.replica.replace('|n', '\n'))
            await state.set_state(States.send_video_or_photo)
        except Exception as exc:
            logger.error(f'Error updating user description: {exc}')
    else:
        replica = await db.get_row(BotReplicas, unique_name='null_description')
        await message.answer(replica.replica)

@profile_router.message(States.send_video_or_photo, F.content_type.in_({'photo', 'video'}))
async def take_photo_or_video(message: Message, state: FSMContext):
    storage = await state.get_data()
    if message.photo:
        if message.media_group_id:
            if storage.get(message.media_group_id):
                ...
            else:
                await state.update_data({message.media_group_id: True})
                replica = await db.get_row(BotReplicas, unique_name='only_one_photo')
                await message.answer(replica.replica)
        else:
            user_data = await db.get_row(Users, tg_user_id=str(message.from_user.id))
            list_photos = json.loads(user_data.photos).get('photos')
            if len(list_photos) == 5:
                replica = await db.get_row(BotReplicas, unique_name='photo_limit_exceeded')
                await message.answer(replica.replica.replace('|n', '\n'))
                await state.clear()
            else:
                file_id = message.photo[-1].file_id
                list_photos.append(file_id)
                await db.update_user_row(model=Users, tg_user_id=message.from_user.id,
                                         photos=json.dumps({'photos': list_photos}),
                                         video='')
                replica = await db.get_row(BotReplicas, unique_name='done_questionnaire')
                await message.answer(replica.replica)
                await db.update_user_row(Users, tg_user_id=str(message.from_user.id), done_questionnaire=True)
                await state.clear()
    elif message.video:
        if message.video.duration <=15:
            file_id = message.video.file_id
            await db.update_user_row(model=Users, tg_user_id=message.from_user.id, video=str(file_id), photo='')
            replica = await db.get_row(BotReplicas, unique_name='done_questionnaire')
            await message.answer(replica.replica)
            await state.clear()
        else:
            replica = await db.get_row(BotReplicas, unique_name='wrong_duration')
            await message.answer(replica.replica)
    else:
        replica = await db.get_row(BotReplicas, unique_name='wrong_type')
        await message.answer(replica.replica)
