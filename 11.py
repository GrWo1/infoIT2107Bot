import requests

params = {
    'lat': '55.75396',
    'lon': '37.620393',
    'appid': '87da88c8017d9374989a48ebba1e3e52',
    'units': 'metric',
}

address = f'https://api.openweathermap.org/data/2.5/weather?'
response2 = requests.get(url=address, params=params).json()
# response2 = response2.get('main')
# temp = round(response2['temp'])
print(response2)
# print(f'{temp} гр.')
