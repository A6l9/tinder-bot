import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove
from loguru import logger
from utils.haversine import haversine

from loader import db
from database.models import BotReplicas, Users, Cities
from aiogram.fsm.context import FSMContext
from keyboards.inline.inline_kbs import (create_sex_buttons, create_preference_buttons, create_location_buttons,
                                         create_name_question
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
        logger.error(f'Error updating user age: {exc}')

@profile_router.callback_query(F.data.startswith('preference_'))
async def preference_question_take_answer(call: CallbackQuery):
    preference = call.data.split('_')[1]
    try:
        await db.update_user_row(model=Users, tg_user_id=call.from_user.id, preference=preference)
        replica = await db.get_row(BotReplicas, unique_name='city_question')
        await call.message.answer(replica.replica, reply_markup=create_location_buttons())
    except Exception as exc:
        logger.error(f'Error updating user age: {exc}')

@profile_router.callback_query(F.data.startswith('location_'))
async def location_question_take_answer(call: CallbackQuery, state: FSMContext):
    type_record_location = call.data.split('_')[1]
    if type_record_location == 'share':
        try:
            replica = await db.get_row(BotReplicas, unique_name='share_location')
            await call.message.answer(replica.replica, reply_markup=create_share_location_button())
            await state.set_state(States.location_share)
        except Exception as exc:
            logger.error(f'Error updating user age: {exc}')
    elif type_record_location == 'write':
        try:
            replica = await db.get_row(BotReplicas, unique_name='write_location')
            await call.message.answer(replica.replica)
            await state.set_state(States.location_write)



@profile_router.message(F.location)
async def location_share_take_answer(message: Message):
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
            except Exception as exc:
                logger.error(f'Error updating user age: {exc}')
            break

@profile_router.callback_query(F.data.startswith('name_'))
async def name_question_take_answer_from_button(call: CallbackQuery, state: FSMContext):
    try:
        await db.update_user_row(model=Users, tg_user_id=call.from_user.id, username=call.from_user.username)
        await call.message.answer('Имя добавлено(заглушка)')
        # replica = await db.get_row(BotReplicas, unique_name='share_location')
        # await call.message.answer(replica.replica, reply_markup=create_share_location_button())
        # await state.set_state(States.location_share)
    except Exception as exc:
        logger.error(f'Error updating user age: {exc}')