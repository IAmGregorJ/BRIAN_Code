'''imports'''
import json
from configparser import ConfigParser
import geocoder
import requests
from geopy.geocoders import Nominatim
import Communication.Output as out

#import Communication.Output as out

# pylint: disable=consider-using-f-string
class Weather():
    '''answer to the question how's the weather?'''
    def __init__(self):
        config = ConfigParser()
        config.read("App/secrets.ini")
        self.__app_id = config.get("weather", "api_key")
        self.ip = self.get_ip()
        self.lat = str(self.ip.lat)
        self.lng = str(self.ip.lng)
        self.city = self.get_city()
        self.url = "https://api.openweathermap.org/data/2.5/onecall?lat=" \
                    "%s&lon=%s&appid=%s&units=metric" % (self.lat, self.lng, self.__app_id)
        self.data = self.get_api_data()
        self.current_temp = round(self.data["current"]["temp"])
        self.current_feels_like = round(self.data["current"]["feels_like"])
        self.current_weather = self.data["current"]["weather"]
        self.current_description = self.current_weather[0]["description"]

    def give_weather(self):
        '''give an output of the current local weather'''
        out.Output.say(f"The current temperature here in {self.city} is {self.current_temp} " \
                        f"degrees with {self.current_description}.")
    def get_ip(self):
        '''get the current user's ip address'''
        return geocoder.ip('me')
    def get_city(self):
        '''Obtains the current city name'''
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(self.lat+","+self.lng)
        address = location.raw['address']
        return address.get('city', '')
    def get_api_data(self):
        '''Obtains the data from the weather api'''
        response = requests.get(self.url)
        return json.loads(response.text)
