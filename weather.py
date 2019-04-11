from conf import *
import json
import requests


def query(city_name="", city_id=0, zip_code="", lat=0.0, lon=0.0):
    if len(city_name):
        return queryByCityName(city_name)
    elif city_id > 0:
        return queryByCityID(city_id)
    elif len(zip_code):
        return queryByZip(zip_code)
    else:
        return queryByGeo(lat=lat, lon=lon)


def queryByCityName(city_name):
    '''
    根据城市名称查询
    :param city_name:
    :return:
    '''
    return request_api(openweathermap_url, {"q": city_name, "APPID": openweathermap_api_key})

def queryByCityID(city_id):
    '''
    根据城市id查询
    :param city_id:
    :return:
    '''
    return request_api(openweathermap_url, {"id": city_id, "APPID": openweathermap_api_key})


def queryByZip(zip):
    '''
    根据邮政编码
    :param zip:
    :return:
    '''
    return request_api(openweathermap_url, {"zip": zip, "APPID": openweathermap_api_key})


def queryByGeo(lat, lon):
    '''
    根据经纬度查询天气
    :param lat:
    :param lng:
    :return:
    '''
    return request_api(openweathermap_url, {"lat": lat, "lon": lon, "APPID": openweathermap_api_key})


def request_api( url, params):
    text = requests.get(url, params=params).text
    response = json.loads(text)
    return Weather(response)

class Weather(object):
    def __init__(self, dict):
        self.country = dict['sys']['country']
        self.latitude = dict['coord']['lat']
        self.longitude = dict['coord']['lon']
        # 天气，比如多云
        self.main = dict['weather'][0]['main']
        # 天气的描述
        self.description = dict['weather'][0]['description']
        # 当前温度 开尔文
        self.temperature = int(dict["main"]['temp']) - 273
        # 最高温
        self.max_temperature = int(dict['main']['temp_max']) - 273
        # 最低温
        self.min_temperature = int(dict['main']['temp_min']) - 273
        # 风速
        self.wind_speed = float(dict["wind"]["speed"])
        # 风向
        self.wind_direction = float(dict["wind"]["deg"])
        # 天气的图标id
        self.icon = dict['weather'][0]['icon']
        # 城市名称
        self.city_name = dict["name"]

    def getWeatherInfo(self):
        return {
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "main": self.main,
            "description": self.description,
            "temperature": self.temperature,
            "max_temperature": self.max_temperature,
            "min_temperature": self.min_temperature,
            "wind_speed": self.wind_speed,
            "wind_direction": self.wind_direction,
            "icon": self.icon,
            "city_name": self.city_name
        }

    def debugDescription(self):
        result = """
                ======================================
                ||  Country         : {country}
                ||  City            : {city}
                ||  Latitude        : {lat}
                ||  Longitude       : {long}
                ||  Whether         : {weather}
                ||  Description     : {description}
                ||  Min Temp        : {min_temp}
                ||  Max Temp        : {max_temp}
                ||  Current Temp    : {temp}
                ======================================""".format(country=self.country,
                                                                 city=self.city_name,
                                                                 lat=self.latitude,
                                                                 long=self.longitude,
                                                                 weather=self.main,
                                                                 description=self.description,
                                                                 min_temp=self.min_temperature,
                                                                 max_temp=self.max_temperature,
                                                                 temp=self.temperature)

        return result

if __name__ == "__main__":
    # 根据经纬度查询天气
    # weather = query(lat=39.91, lon=116.4)

    # 根据城市名称查询天气
    # weather = query(city_name="Beijing")

    # 根据城市id查询天气
    weather = query(city_id=2038349)
    print(weather.debugDescription())