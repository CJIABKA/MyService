from app import crontab
import json
from app.models import Stations, Services, Photos, Goods
from app import db
#import requests

@crontab.job(day=2)
def scheduled_job_1():
    put_data_in_db_1()


@crontab.job(hour=12)
def scheduled_job_2():
    put_data_in_db_2()


def take_data_from_source_1():
    #data = requests.get("https://service_1.com/somedata")
    #some code to remake given data to properly formed json
    #taking data from synt json file
    with open("../synt_sources/source_1.json", encoding='cp1251') as read_file:
        data = json.load(read_file)
    return data


def take_data_from_source_2():
    #data = requests.get("https://service_2.com/somedata")
    #some code to remake given data to properly formed json
    #taking data from synt json file
    with open("../synt_sources/source_2.json", encoding='cp1251') as read_file:
        data = json.load(read_file)
    return data


def put_data_in_db_1():
    data = take_data_from_source_1()
    for station_id in data.keys():
        coordinates = data[station_id]['coordinates']
        number = data[station_id]['number']
        address = data[station_id]['address']
        photos = data[station_id]['photos']
        services = data[station_id]['services']
        station = Stations.query.filter_by(id=station_id).first()
        if station is not None:
            station.coordinates = coordinates
            station.address = address
            station.number = number
        else:
            station = Stations(id=station_id, coordinates=coordinates, address=address, number=number)
            db.session.add(station)
        for url in photos:
            photo = Photos.query.filter_by(url=url, station_id=station_id).first()
            if photo is None:
                photo = Photos(url=url)
                db.session.add(photo)
                station.photos.append(photo)
        for srv in services:
            service = Services.query.filter_by(title=srv).first()
            if service is not None and service not in station.services:
                station.services.append(service)
            if service is None:
                service = Services(title=srv)
                db.session.add(service)
                station.services.append(service)
        db.session.commit()


def put_data_in_db_2():
    data = take_data_from_source_2()
    for station_id in data.keys():
        station = Stations.query.filter_by(id=station_id).first()
        if station is None:
            station = Stations(id=station_id)
            db.session.add(station)
        for title in data[station_id].keys():
            amount = data[station_id][title][0]
            currency = data[station_id][title][1]
            goods = Goods.query.filter_by(title=title, station_id=station_id).first()
            if goods is None:
                goods = Goods(title=title, amount=float(amount), currency=currency)
                db.session.add(goods)
                station.goods.append(goods)
            else:
                goods.amount = amount
                goods.currency = currency
        db.session.commit()


if __name__ == "__main__":
    #put_data_in_db_1()
    put_data_in_db_2()
