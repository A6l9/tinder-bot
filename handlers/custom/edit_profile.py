import json
import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from storage.states import States
from loader import db, bot, user_manager
from database.models import BotReplicas, Users, Cities
from keyboards.inline.inline_kbs import create_buttons_cities_edit, \
    create_location_edit_buttons, create_cancel_button, create_delete_or_no_buttons
from keyboards.reply.reply_kbs import create_share_location_button
from loguru import logger
from utils.haversine import haversine
from utils.function_for_sending_a_profile import func_for_send_prof


edit_profile_router = Router()


@edit_profile_router.callback_query(F.data == 'change_questionnaire')
async def change_questionnaire_again(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.age_question)
    replica = await db.get_row(BotReplicas, unique_name='age_question')
    await call.message.answer(replica.replica)

@edit_profile_router.callback_query(F.data.startswith('edit_'))
async def change_distributor(call: CallbackQuery, state: FSMContext):
    point = call.data.split('_')[1]
    if point == 'name':
        replica = await db.get_row(BotReplicas, unique_name='new_name')
        await call.message.answer(replica.replica, reply_markup=create_cancel_button())
        await state.set_state(States.name_question_edit)
    elif point == 'city':
        replica = await db.get_row(BotReplicas, unique_name='city_question')
        await call.message.answer(replica.replica, reply_markup=create_location_edit_buttons())
    elif point == 'description':
        replica = await db.get_row(BotReplicas, unique_name='write_new_description')
        await call.message.answer(replica.replica, reply_markup=create_cancel_button())
        await state.set_state(States.description_question_edit)





@edit_profile_router.callback_query(F.data.startswith('editname_'))
async def name_question_edit_take_answer_from_button(call: CallbackQuery, state: FSMContext):
    try:
        await db.update_user_row(model=Users, tg_user_id=call.from_user.id, username=call.from_user.username)
        await func_for_send_prof(user_id=call.from_user.id)
        await state.clear()
    except Exception as exc:
        logger.error(f'Error updating username: {exc}')

@edit_profile_router.message(States.name_question_edit)
async def name_question_edit_take_answer_from_message(message: Message, state: FSMContext):
    get_username = await db.get_row(Users, username=str(message.text))
    if not get_username:
        try:
            await db.update_user_row(model=Users, tg_user_id=message.from_user.id, username=str(message.text))
            await func_for_send_prof(user_id=message.from_user.id)
            await state.clear()
        except Exception as exc:
            logger.error(f'Error updating username: {exc}')
    elif get_username and get_username.tg_user_id == str(message.from_user.id):
        replica = await db.get_row(BotReplicas, unique_name='write_name_another')
        await message.answer(replica.replica, reply_markup=create_cancel_button())
    else:
        replica = await db.get_row(BotReplicas, unique_name='name_is_busy')
        await message.answer(replica.replica, reply_markup=create_cancel_button())

@edit_profile_router.callback_query(F.data.startswith('editlocation_'))
async def location_question_take_answer(call: CallbackQuery, state: FSMContext):
    type_record_location = call.data.split('_')[1]
    if type_record_location == 'share':
        try:
            replica = await db.get_row(BotReplicas, unique_name='share_location')
            await call.message.answer(replica.replica, reply_markup=create_share_location_button())
            await state.set_state(States.location_edit_share)
        except Exception as exc:
            logger.error(f'Error take user location: {exc}')
    elif type_record_location == 'write':
        try:
            replica = await db.get_row(BotReplicas, unique_name='write_location')
            await call.message.answer(replica.replica)
            await state.set_state(States.location_edit_write)
        except Exception as exc:
            logger.error(f'Error take user location: {exc}')


@edit_profile_router.message(States.location_edit_write)
async def location_write_search_city(message: Message, state: FSMContext):
    cities_matches = await db.search_cities(str(message.text))
    if cities_matches:
        replica = await db.get_row(BotReplicas, unique_name='city_choose')
        await message.answer(replica.replica, reply_markup=create_buttons_cities_edit(cities_matches))
        await state.clear()
    else:
        replica = await db.get_row(BotReplicas, unique_name='city_not_found')
        await message.answer(replica.replica)


@edit_profile_router.callback_query(F.data.startswith('editcity_'))
async def edit_location_write_take_answer(call: CallbackQuery, state: FSMContext):
    city_code = call.data.split('_')[1]
    city = await db.get_row(Cities, postal_code=int(city_code))
    if city:
        try:
            await db.update_user_row(model=Users, tg_user_id=call.from_user.id, address=city.address,
                                 postal_code=city.postal_code, country=city.country,
                                 federal_district=city.federal_district, region_type=city.region_type,
                                 region=city.region, area_type=city.area_type, area=city.area,
                                 city_type=city.city_type, city=city.city)
            await func_for_send_prof(user_id=call.from_user.id)
            await state.clear()
        except Exception as exc:
            logger.error(f'Error updating user location: {exc}')

@edit_profile_router.message(States.location_edit_share, F.location)
async def edit_location_share_take_answer(message: Message, state: FSMContext):
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
                await func_for_send_prof(message.from_user.id)
                await state.clear()
            except Exception as exc:
                logger.error(f'Error updating user location: {exc}')
            break

@edit_profile_router.message(States.description_question_edit)
async def edit_about_yourself_get_answer(message: Message, state: FSMContext):
    description = message.text
    if description:
        try:
            await db.update_user_row(model=Users, tg_user_id=message.from_user.id, about_yourself=description)
            await func_for_send_prof(user_id=message.from_user.id)
            await state.clear()
        except Exception as exc:
            logger.error(f'Error updating user description: {exc}')
    else:
        replica = await db.get_row(BotReplicas, unique_name='null_description')
        await message.answer(replica.replica)

@edit_profile_router.callback_query(F.data == 'add_media')
async def add_new_media(call: CallbackQuery, state: FSMContext):
    replica = await db.get_row(BotReplicas, unique_name='send_new_photo_or_video')
    await call.message.answer(replica.replica, reply_markup=create_cancel_button())
    await state.set_state(States.send_new_photo_or_video)

@edit_profile_router.message(States.send_new_photo_or_video, F.content_type.in_({'photo', 'video'}))
async def take_new_photo_or_video(message: Message, state: FSMContext):
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
                await func_for_send_prof(user_id=message.from_user.id)
                await state.clear()
            else:
                file_id = message.photo[-1].file_id
                list_photos.insert(0, file_id)
                await db.update_user_row(model=Users, tg_user_id=message.from_user.id,
                                         photos=json.dumps({'photos': list_photos}),
                                         video='')
                await func_for_send_prof(user_id=message.from_user.id)
                await state.clear()
    elif message.video:
        if message.video.duration <=15:
            await func_for_send_prof(user_id=message.from_user.id)
            await state.clear()
        else:
            replica = await db.get_row(BotReplicas, unique_name='wrong_duration')
            await message.answer(replica.replica)
    else:
        replica = await db.get_row(BotReplicas, unique_name='wrong_type')
        await message.answer(replica.replica)


@edit_profile_router.callback_query(F.data == 'cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    await func_for_send_prof(user_id=call.from_user.id)
    await state.clear()


@edit_profile_router.callback_query(F.data == 'delete')
async def delete_media_question(call: CallbackQuery, state: FSMContext):
    user = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    if len(json.loads(user.photos).get('photos')) > 1:
        replica = await db.get_row(BotReplicas, unique_name='delete_question')
        await call.message.answer(replica.replica, reply_markup=create_delete_or_no_buttons())
        await state.set_state(States.delete_media)
    elif len(json.loads(user.photos).get('photos')) == 1:
        replica = await db.get_row(BotReplicas, unique_name='cant_delete')
        await call.message.answer(replica.replica, reply_markup=create_cancel_button())
        await state.set_state(States.send_media_before_delete)


@edit_profile_router.callback_query(States.delete_media, F.data == 'yes')
async def delete_media(call: CallbackQuery, state: FSMContext):
    temp_storage = user_manager.get_user(call.from_user.id)
    user = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    user_media = json.loads(user.photos)['photos']
    user_media.pop(temp_storage.num_elem)
    try:
        await db.update_user_row(Users, tg_user_id=str(call.from_user.id), photos=json.dumps({'photos': user_media}))
        replica = await db.get_row(BotReplicas, unique_name='delete_complete')
        await call.message.answer(replica.replica)
        await func_for_send_prof(user_id=call.from_user.id)
        await state.clear()
    except Exception as exc:
        logger.error(f'Update user media failed {exc}')

@edit_profile_router.message(States.send_media_before_delete, F.content_type.in_({'photo', 'video'}))
async def send_media_before_delete(message: Message, state: FSMContext):
    x = user_manager
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
                await func_for_send_prof(user_id=message.from_user.id)
                await state.clear()
            else:
                temp_storage = user_manager.get_user(message.from_user.id)
                media = temp_storage.photo_storage[message.from_user.id]
                media.pop(temp_storage.num_elem)
                file_id = message.photo[-1].file_id
                list_photos.insert(0, file_id)
                await db.update_user_row(model=Users, tg_user_id=message.from_user.id,
                                         photos=json.dumps({'photos': list_photos}),
                                         video='')
                await func_for_send_prof(user_id=message.from_user.id)
                await state.clear()
    elif message.video:
        if message.video.duration <= 15:
            await func_for_send_prof(user_id=message.from_user.id)
            await state.clear()
        else:
            replica = await db.get_row(BotReplicas, unique_name='wrong_duration')
            await message.answer(replica.replica)
    else:
        replica = await db.get_row(BotReplicas, unique_name='wrong_type')
        await message.answer(replica.replica)