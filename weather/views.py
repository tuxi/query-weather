from django.shortcuts import render

# Create your views here.

import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from django.db.models import Q
from datetime import datetime, timezone, timedelta
from conf import openweathermap_api_key
from xpinyin import Pinyin

class Weather(Exception):
    pass

def query_weather(cities, is_search_key):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f59ed52c59be226eefd9174e337d7c5c'
    weather_data = []
    for city in cities:
        if len(city.name) == 0:
            raise Weather("City name must be not null")

        # 当查询城市的时间已过10分钟时在查询
        # astimezone()将转换时区为北京时间:
        nowtime = datetime.utcnow().replace(tzinfo=timezone.utc)
        bj_nowtime = nowtime.astimezone(timezone(timedelta(hours=8)))
        if city.query_time == None:
            city.query_time = bj_nowtime

        # TypeError: can't subtract offset-naive and offset-aware datetimes
        diff_seconds = (nowtime - city.query_time).seconds

        if diff_seconds > 600 or city.query_time == bj_nowtime or is_search_key:
            # 将中文city转换为拼音
            p = Pinyin()
            city_pinyin = p.get_pinyin(city.name, '')
            dict = requests.get(url.format(city_pinyin)).json()

            city.temperature = dict['main']['temp']
            city.weather_description = dict['weather'][0]['description']
            city.icon = dict['weather'][0]['icon']
            city.latitude = dict['coord']['lat']
            city.longitude = dict['coord']['lon']
            city.max_temperature = int(dict["main"]['temp_max'])
            city.min_temperature = int(dict["main"]['temp_min'])
            city.wind_speed = float(dict["wind"]["speed"])
            city.weather = dict['weather'][0]['main']
            city.country = dict['sys']['country']
            city_weather = city.to_dict()

            # 查询数据库中是否有
            cites = City.objects.filter(name=city.name, country=city_weather['country'])
            if len(cites) == 0:
                city.save()
            else:
                # 更新数据库中dedel
                cites.update(
                    weather=city_weather['weather'],
                    weather_description=city_weather['description'],
                    icon=city_weather['icon'],
                    latitude=city_weather['latitude'],
                    longitude=city_weather['longitude'],
                    temperature=city_weather['temperature'],
                    max_temperature=city_weather['max_temperature'],
                    min_temperature=city_weather['min_temperature'],
                    wind_speed=city_weather['wind_speed'],
                    country=city_weather['country'],
                    query_time=nowtime
                )


        else:
            # 使用数据库的缓存 存在时间的city 数据库肯定有记录
            city_weather = city.to_dict()
            # city.save()
        weather_data.append(city_weather)
    return weather_data



def index(request):

    weather_data = []

    currentName = ""

    # 查询当前输入的城市
    if request.method == 'POST':
        form = CityForm(request.POST)
        currentName = form.data["name"]
        # form.save()
        print(form.data["name"])

        # currentCityQuerySet = City.objects.filter(name=currentName)
        # if len(currentCityQuerySet):
        #     currentCity = currentCityQuerySet[0]
        # else:
        #     currentCity = City(name=currentName)
        currentCity = City(name=currentName)
        currentCityWeather = query_weather([currentCity], True)

        weather_data += currentCityWeather

    # 查询数据库中已有的城市，需要过滤掉当前查询的城市，防止与要查询的想重合
    #  ~Q(name=currentName) 表示非
    cities = City.objects.filter(~Q(name=currentName)).order_by('-query_time')
    weather_data += query_weather(cities, False)

    context = {'weather_data' : weather_data, 'form' : CityForm()}
    return render(request, 'weather/weather.html', context)
