import pyowm
import datetime
import vk
import time
import random

key = '53f7a0f7ea16615e1ddd55599261fe9c52f38044b5b6f781856d97cbbad6ac1b08fc36001d88dbf314374'

session = vk.Session (key)
api = vk.API(session)

owm = pyowm.OWM('1a21ea6f9ad17ed177341a1e5ee806e9')
observation = owm.weather_at_place('Rostov-on-Don,ru')

weather = observation.get_weather()
location = observation.get_location()

print(owm)
print(observation)
print(weather)
print(location)

translate = {'Rostov-na-Donu':'Ростов-на-Дону', 'RU':'Россия'}

def typeOfWind():
    if 0 <= weather.get_wind()['deg']<=45:
        return 'северный'
    if 45<=weather.get_wind()['deg']<=90:
        return 'северо-восточный'
    if 90<=weather.get_wind()['deg']<=135:
        return 'восточный'
    if 135<=weather.get_wind()['deg']<=180:
        return 'юго-восточный'
    if 180<=weather.get_wind()['deg']<=225:
        return 'южный'
    if 225<=weather.get_wind()['deg']<=270:
        return 'юго-западный'
    if 270<=weather.get_wind()['deg']<=315:
        return 'западный'
    if 315<=weather.get_wind()['deg']<=330:
        return 'северо-западный'
    if 330<=weather.get_wind()['deg']<=360:
        return 'северный'

def whatIsCloudness():

    if 0 <= weather.get_clouds() <= 10:
        return 'ясная'

    if 10 <= weather.get_clouds() <= 30:
        return 'немного облачная'

    if 30 <= weather.get_clouds() <= 70:
        return 'пасмурная'

    if 70 <= weather.get_clouds() <= 100:
        return 'мрачная'

w = ('Погода в городе ' + translate[location.get_name()] + ' (' + translate[location.get_country()] + ')' +
      ' на сегодня в ' + str(datetime.datetime.now().strftime('%H:%M'))+ ' ' + whatIsCloudness() + ', облачность составляет ' +
      str(weather.get_clouds()) + '%, давление ' + str(weather.get_pressure()['press']) + ' мм. рт. ст., температура '
      + str(int(weather.get_temperature('celsius')['temp'])) + ' градусов Цельсия, ночью ' +
      str(int(weather.get_temperature('celsius')['temp_min'])) + ', днем ' + str(int(weather.get_temperature('celsius')['temp_max'])) +
      '. Ветер ' + typeOfWind() + ' ' + str(weather.get_wind()['speed']) + ' м.\с.')

while (True):
    messages = api.messages.get()
    commands = ['--Привет', '--Пока', '--Как дела?', '--Какая погода?']
    messages = [(m['uid'], m['mid'], m['body'])
                for m in messages[1:] if m['body'] in commands and m['read_state'] == 0]

    for m in messages:
        user_id = m[0]
        messages_id = m[1]
        comand = m[2]

        if comand == '--Привет':
            api.messages.send(user_id=user_id,
                              message= 'Привет брат!')
        if comand == '--Пока':
            api.messages.send(user_id=user_id,
                              message= 'Пока, братишка)')
        if comand == '--Как дела?':
            api.messages.send(user_id=user_id,
                              message= 'Отлично, как твои?')

        if comand == '--Какая погода?':


            api.messages.send(user_id=user_id,
                              message= w)

    ids = ', '.join([str(m[1]) for m in messages])

    if ids:
        api.messages.markAsRead(message_ids=ids)

    time.sleep(3)


