from typing import Iterable, List

from loguru import logger
from sqlalchemy import Select, update, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Query
from sqlalchemy.sql.ddl import DropTable
from typing_extensions import Any
from database.models import Users, Cities, Matches
from database.database import Base

class BaseInterface:
    def __init__(self, db_url: str):
        """
        Класс-интерфейс для работы с БД. Держит сессию и предоставляет методы для работы с БД.

        :param db_url: Путь к БД формата: "database+driver://name:password@host/db_name"
        self.base базовый класс моделей с которыми будете работать.
        """
        self.engine = create_async_engine(db_url, pool_timeout=60, pool_size=900, max_overflow=100)
        self.async_ses = async_sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        self.base = Base

    async def initial(self):
        """
        Метод иницилизирует соединение с БД.
        :return:
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.create_all)

    async def _drop_all(self):
        """
        Метод для удаления всех таблиц текущей БД.
        :return:
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)

    async def del_has_rows(self, rows_object):
        async with self.async_ses() as session:
            for rec in rows_object:
                await session.delete(rec)
            await session.commit()

    async def delete_rows(self, model: Any, **filter_by):
        async with self.async_ses() as session:
            records = await session.execute(Query(model).filter_by(**filter_by))
            res = records.scalars()
            if res:
                try:
                    for rec in res:
                        await session.delete(rec)
                    await session.commit()
                    return True
                except Exception:
                    pass

    async def get_all_set(self, table_model, field) -> set:
        """
        Метод принимает класс модели и название поля,
        и возвращает множество всех полученных значений.
        :param table_model: Класс модели
        :param field: Название поля
        :return: set
        """
        async with self.async_ses() as session:
            rows = await session.execute(Select(table_model.__table__.c[field]))
            return {row for row in rows.scalars()}

    async def drop_tables(self, table_models: Iterable):
        """
        Метод принимает коллекцию классов моделей и удаляет данные таблицы из БД.
        :param table_models:
        :return:
        """
        async with self.async_ses() as session:
            for table in table_models:
                await session.execute(DropTable(table.__table__))
                logger.info(f'{table.__tablename__} is dropped')
            await session.commit()

    async def add_row(self, model: Any, **kwargs):
        """
        Метод принимает класс модели и поля со значениями,
        и создает в таблице данной модели запись с переданными аргументами.
        :param model: Класс модели
        :param kwargs: Поля и их значения
        :return:
        """

        async with self.async_ses() as session:
            row = model(**kwargs)
            session.add(row)
            try:
                await session.commit()
                return row
            except Exception as ex:
                logger.exception(ex)
                logger.warning(f'FAILED ADD ROW, {model.__name__}, {kwargs=}')
                return


    async def get_row(self, model: Any, to_many=False, order_by='id', filter=None, **kwargs):
        """
        Метод принимает класс модели и имена полей со значениями,
        и если такая строка есть в БД - возвращает ее.
        :param to_many: Флаг для возврата одного или нескольких значений
        :param model: Класс модели
        :param kwargs: Поля и их значения
        :return:
        """
        async with self.async_ses() as session:
            if filter:
                row = await session.execute(
                    Query(model).filter_by(**kwargs).filter(filter['filter']).order_by(order_by))
            else:
                row = await session.execute(Query(model).filter_by(**kwargs).order_by(order_by))
            if to_many:
                res = [*row.scalars()]
            else:
                res = row.scalar()
            return res

    async def get_or_create_row(self, model: Any, filter_by=None, **kwargs):
        """
        Метод находит в БД запись, и возвращает ее. Если записи нет - создает и возвращает.
        :param model: Класс модели
        :param filter_by: Параметры для поиска записи. По умолчанию поиск идет по **kwargs
        :param kwargs: Поля и их значения
        :return:
        """
        if not filter_by:
            filter_by = kwargs

        async with self.async_ses() as session:
            row = await session.execute(Query(model).filter_by(**filter_by))
            res = row.scalar()
            if res is None:
                res = model(**kwargs)
                session.add(res)
                try:
                    await session.commit()
                except Exception as ex:
                    logger.warning(f'COMMIT FAILED: {model.__name__}, {kwargs=}')
            return res

    async def update_user_row(self, model, tg_user_id, **kwargs):

        async with self.async_ses() as session:
            row = await session.execute(update(model).where(Users.tg_user_id == str(tg_user_id )).values(**kwargs))

            try:
                await session.commit()
            except Exception as ex:
                print(ex)
                print(f'failed update {model.__tablename__}')

    async def update_matches_row(self, model, tg_user_id, tg_user_id_another_user,
                                 user_id_one=None, user_id_two=None, **kwargs):

        async with self.async_ses() as session:
            if user_id_one:
                row = await session.execute(update(Matches).where(Matches.user_id_one == str(
                    tg_user_id), Matches.user_id_two == str(tg_user_id_another_user)).values(**kwargs))
            elif user_id_two:
                row = await session.execute(update(Matches).where(
                    Matches.user_id_one == str(tg_user_id_another_user), Matches.user_id_two == str(
                    tg_user_id)).values(**kwargs))
            try:
                await session.commit()
            except Exception as ex:
                print(ex)
                print(f'failed update {model.__tablename__}')

    async def get_user_tags(self, model: Any=Users, to_many=False, order_by='id', filter=None, **kwargs):
        """
        Метод принимает класс модели и имена полей со значениями,
        и если такая строка есть в БД - возвращает ее.
        :param to_many: Флаг для возврата одного или нескольких значений
        :param model: Класс модели
        :param kwargs: Поля и их значения
        :return:
        """
        async with self.async_ses() as session:
            if filter:
                row = await session.execute(
                    Query(model).filter_by(**kwargs).filter(filter['filter']).order_by(order_by))
            else:
                row = await session.execute(Query(model).filter_by(**kwargs).order_by(order_by))
            if to_many:
                res = [*row.scalars()]
            else:
                res = row.scalar()
            return res

    async def update_data_user(self, model, usr_id):
        """
        Метод для изменения полей в таблице Users
        :return:
        """
        async with self.async_ses() as session:
            try:
                await session.commit()
                logger.debug(f'Successfully update data user {usr_id}')
            except Exception as ex:
                print(ex)
                print(f'failed update {model.__tablename__}')

    async def add_rows(self, lst: List):
        """
        Метод принимает класс модели и поля со значениями,
        и создает в таблице данной модели запись с переданными аргументами.
        :param lst: Список
        :return:
        """
        async with self.async_ses() as session:
            async with session.begin():
                session.add_all(lst)
            try:
                await session.commit()
                logger.info('Add new row')
            except Exception as exc:
                logger.exception(exc)

    async def search_cities(self, fragment: str):
        async with self.async_ses() as session:
            query = select(Cities).where(Cities.city.ilike(f'{fragment}%'))
            result = await session.execute(query)
            cities = result.scalars().all()
            res = [*cities]
            return res

    async def get_users_info(self, model: Any=Users, to_many: bool=True):
        async with self.async_ses() as session:
            row_mans = await session.execute(Query(model).filter_by(sex='man'))
            row_girls = await session.execute(Query(model).filter_by(sex='woman'))
            row_users = await session.execute(Query(model).filter_by())
            row_users_nodone_profile = await session.execute(Query(model).filter_by(done_questionnaire=False))
            if to_many:
                res = [len([*row_mans.scalars()]), len([*row_girls.scalars()]),
                       len([*row_users]), len([*row_users_nodone_profile])]
            return res

    async def get_matches_info(self, model: Any=Matches, to_many: bool=True):
        async with self.async_ses() as session:
            row_matches = await session.execute(Query(model).filter_by(user_reaction_one=True, user_reaction_two=True))
            if to_many:
                res = [len([*row_matches.scalars()])]
            return res

    async def get_users_with_city(self, postal_code: int):
        async with self.async_ses() as session:
            query = select(Users).where(Users.done_questionnaire == True, Users.postal_code == postal_code)
            result = await session.execute(query)
            cities = result.scalars().all()
            res = [*cities]
            return res

    async def get_users_with_age(self, age_range: str, address: str):
        start_age = int(age_range.split('-')[0])
        end_age = int(age_range.split('-')[1])
        async with self.async_ses() as session:
            query = select(Users).where(Users.done_questionnaire == True,
                                        Users.age.between(start_age, end_age), Users.address == address)
            result = await session.execute(query)
            users = result.scalars().all()
            res = [*users]
            return res

    async def get_users_for_mailing(self, parameters):
        async with self.async_ses() as session:
            if not parameters:
                parameters = {}
            if 'age_range' in parameters:
                start_age = parameters['age_range'].split('-')[0]
                end_age = parameters['age_range'].split('-')[1]
            else:
                start_age = '16'
                end_age = '45'
            sex_list = ['man', 'woman']
            if  not 'sex' in parameters and not 'city' in parameters:
                query = select(Users).where(Users.done_questionnaire == True,
                                            Users.age.between(int(start_age), int(end_age)))
            elif not 'sex' in parameters:
                query = select(Users).where(Users.done_questionnaire == True,
                                            Users.address == parameters['city'],
                                            Users.age.between(int(start_age), int(end_age)))
            elif not 'city' in parameters:
                if parameters['sex'] in sex_list:
                    query = select(Users).where(Users.done_questionnaire == True,
                                            Users.age.between(int(start_age), int(end_age)),
                                                              Users.sex == parameters['sex'])
                else:
                    query = select(Users).where(Users.done_questionnaire == True,
                                                Users.age.between(int(start_age), int(end_age)))
            elif parameters['sex'] in sex_list:
                query = select(Users).where(Users.done_questionnaire == True,
                                Users.address == parameters['city'], Users.age.between(int(start_age), int(end_age)),
                                Users.sex == parameters['sex'])
            else:
                query = select(Users).where(Users.done_questionnaire == True,
                                Users.address == parameters['city'], Users.age.between(int(start_age), int(end_age)),
                                Users.sex.in_(sex_list))
            result = await session.execute(query)
            users = result.scalars().all()
            res = [*users]
            return res
