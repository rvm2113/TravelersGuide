import json
import requests
import StringIO
from elasticsearch import Elasticsearch
from elasticsearch import helpers



'''
WeatherGuide objects
store the city, country, and 
weather statistics for a 
given location.
'''

class WeatherGuide(object):
	def __init__(self, city_location = ' '):
		self.name = city_location
		self.resp = {}
		api_key = '135ca7e8eb4df5675b8aae75dfc205fc'
		query = {}
		query['q'] = city_location
		query['units'] = 'imperial'
		query['appid'] = api_key
		url = 'http://api.openweathermap.org/data/2.5/forecast'
		self.overall_cloud_percentage = 0
		self.overall_humidity_percentage = 0 
		self.overall_temperature = 0 
		self.overall_wind_speed = 0
		'''
		A request is made to 
		OpenWeatherMap's 5-day, 3-hour API
		to obtain weather data for the current location/city.
		'''
		try:
			self.resp = requests.get(url, query)
		except requests.exceptions.RequestException as error: 
			print error
			sys.exit(1)
	def compute_aggregate_weather_information(self):
		#if the dictionary resp is not empty
		if(bool(self.resp)):
			for entry in range(len(self.resp.json()['list'])):
				self.overall_cloud_percentage += self.resp.json()['list'][entry]['clouds']['all']
				self.overall_wind_speed += self.resp.json()['list'][entry]['wind']['speed']
				self.overall_temperature += self.resp.json()['list'][entry]['main']['temp']
				self.overall_humidity_percentage += self.resp.json()['list'][entry]['main']['humidity']

			self.overall_humidity_percentage/=len(self.resp.json()['list'])
			self.overall_temperature/=len(self.resp.json()['list'])
			self.overall_wind_speed/=len(self.resp.json()['list'])
			self.overall_cloud_percentage/=len(self.resp.json()['list'])
		
