# from aiogram import Router, F
# from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo
# from loader import user_manager, db, bot
# from database.models import BotReplicas, Users
# from keyboards.inline.inline_kbs import create_buttons_for_viewing_match
# import json
#
#
# show_match_profile = Router()
#
#
# @show_match_profile.callback_query(F.data == 'swipe_right_match')
# async def swipe_right_photo_match(call: CallbackQuery):
#     temp_storage = user_manager.get_user(call.from_user.id)
#     if temp_storage.num_page_photo_for_another_user + 1 == len(temp_storage.another_photo_storage):
#         replica = await db.get_row(BotReplicas, unique_name='no_more_photos')
#         await call.answer(text=replica.replica)
#     else:
#         temp_storage.num_page_photo_for_another_user += 1
#         another_user_data = await db.get_row(Users, tg_user_id=str(
#             temp_storage.another_users_id[temp_storage.index_another_user]))
#         content = None
#         replica = await db.get_row(BotReplicas, unique_name='you_have_match')
#         if json.loads(another_user_data.media).get('media'):
#             content = json.loads(another_user_data.media).get('media')
#             if another_user_data.about_yourself:
#                 description = another_user_data.about_yourself
#             else:
#                 description = 'Нет описания'
#             another_user = await bot.get_chat(int(another_user_data.tg_user_id))
#             user_link = (f'<a href="tg://user?id={another_user.id}"'
#                          f'>@{another_user.username}</a>')
#             if content[temp_storage.num_page_photo_for_another_user][0] == 'photo':
#                 media_type = InputMediaPhoto(media=content[temp_storage.num_page_photo_for_another_user][1],
#                                              caption=replica.replica.replace('|n', '\n').format(
#                                                  name=another_user_data.username,
#                                                  age=another_user_data.age,
#                                                  link=user_link,
#                                                  city=another_user_data.city,
#                                                  desc=description))
#                 await bot.edit_message_media(chat_id=call.from_user.id,
#                                              media=media_type, message_id=call.message.message_id,
#                                              reply_markup=await create_buttons_for_viewing_match(call.from_user.id,
#                                                     temp_storage.another_users_id[temp_storage.index_another_user]))
#             elif content[temp_storage.num_page_photo_for_another_user][0] == 'video':
#                 if another_user_data.about_yourself:
#                     description = another_user_data.about_yourself
#                 else:
#                     description = 'Нет описания'
#                 media_type = InputMediaVideo(media=content[temp_storage.num_page_photo_for_another_user][1],
#                                              caption=replica.replica.replace('|n', '\n').format(
#                                                  name=another_user_data.username,
#                                                  age=another_user_data.age,
#                                                  link=user_link,
#                                                  city=another_user_data.city,
#                                                  desc=description))
#                 await bot.edit_message_media(chat_id=call.from_user.id,
#                                              media=media_type, message_id=call.message.message_id,
#                                              reply_markup=await create_buttons_for_viewing_match(call.from_user.id,
#                                                     temp_storage.another_users_id[temp_storage.index_another_user]))
#         else:
#             replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
#             await call.answer(replica.replica)
#
#
# @show_match_profile.callback_query(F.data == 'swipe_left')
# async def swipe_left_photo_match(call: CallbackQuery):
#     temp_storage = user_manager.get_user(call.from_user.id)
#     if temp_storage.num_page_photo_for_another_user == 0:
#         replica = await db.get_row(BotReplicas, unique_name='no_more_photos')
#         await call.answer(text=replica.replica)
#     else:
#         temp_storage.num_page_photo_for_another_user -= 1
#         another_user_data = await db.get_row(Users,
#                                      tg_user_id=str(temp_storage.another_users_id[temp_storage.index_another_user]))
#         another_user = await bot.get_chat(int(another_user_data.tg_user_id))
#         user_link = (f'<a href="tg://user?id={another_user.id}"'
#                      f'>@{another_user.username}</a>')
#         content = None
#         replica = await db.get_row(BotReplicas, unique_name='you_have_match')
#         if json.loads(another_user_data.media).get('media'):
#             content = json.loads(another_user_data.media).get('media')
#             if another_user_data.about_yourself:
#                 description = another_user_data.about_yourself
#             else:
#                 description = 'Нет описания'
#             if content[temp_storage.num_page_photo_for_another_user][0] == 'photo':
#                 media_type = InputMediaPhoto(media=content[temp_storage.num_page_photo_for_another_user][1],
#                                              caption=replica.replica.replace('|n', '\n').format(
#                                                  name=another_user_data.username,
#                                                  age=another_user_data.age,
#                                                  link=user_link,
#                                                  city=another_user_data.city,
#                                                  desc=description))
#                 await bot.edit_message_media(chat_id=call.from_user.id,
#                                              media=media_type, message_id=call.message.message_id,
#                                              reply_markup=await create_buttons_for_viewing_match(call.from_user.id,
#                                                     temp_storage.another_users_id[temp_storage.index_another_user]))
#             elif content[temp_storage.num_page_photo_for_another_user][0] == 'video':
#                 if another_user_data.about_yourself:
#                     description = another_user_data.about_yourself
#                 else:
#                     description = 'Нет описания'
#                 media_type = InputMediaVideo(media=content[temp_storage.num_page_photo_for_another_user][1],
#                                              caption=replica.replica.replace('|n', '\n').format(
#                                                  name=another_user_data.username,
#                                                  age=another_user_data.age,
#                                                  link=user_link,
#                                                  city=another_user_data.city,
#                                                  desc=description))
#                 await bot.edit_message_media(chat_id=call.from_user.id,
#                                              media=media_type, message_id=call.message.message_id,
#                                              reply_markup=await create_buttons_for_viewing_match(call.from_user.id,
#                                                     temp_storage.another_users_id[temp_storage.index_another_user]))
#         else:
#             replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
#             await call.answer(replica.replica)