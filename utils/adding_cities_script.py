from loader import db
import asyncio
import csv
from database.models import Cities



async def add_cities():
    await db.initial()
    list_to_add = []
    list_cities = [i.postal_code for i in await db.get_row(Cities, to_many=True)]
    with open('../misc/city.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for i_elem in reader:
            if i_elem[1] == '':
                postal_code = 366281
            else:
                postal_code = int(i_elem[1])
            if postal_code not in list_cities:
                list_to_add.append(Cities(address=i_elem[0], postal_code=postal_code, country=i_elem[2],
                                          federal_district=i_elem[3], region_type=i_elem[4], region=i_elem[5],
                                          area_type=i_elem[6], area=i_elem[7], city_type=i_elem[8], city=i_elem[9],
                                          geo_lat=i_elem[20], geo_lon=i_elem[21]))
        if len(list_to_add) != 0:
            await db.add_rows(list_to_add)


if __name__ == '__main__':
    asyncio.run(add_cities())
