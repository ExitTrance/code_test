import requests
import statistics

class Weather:
    # Used for checking validity of input
    valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] 
    valid_times = list(range(0, 24)) # Made the assumption that each entry represents hours starting with 00:00 to 01:00... 23:00 

    def __init__(self, candidate_id, api_link=""):
        self.candidate_id = candidate_id
        self.api_link = api_link

    def get_cities_list(self):
        link = self.api_link + "/api/cities/" 
        response = requests.get(link)
        response = response.json()['cities']
        return response


    def get_city_weather_json(self, city_name):
        city = city_name.lower()
        cities = self.get_cities_list()
        if city in cities:
            link = self.api_link + "/api/weather/{}/{}/".format(self.candidate_id, city)
            response = requests.get(link)
            return response.json()
        else:
            raise Exception("City name {}, does not exist.".format(city))

    def get_day(self, city_data, day):
        day_formatted = day.lower()
        if day_formatted in self.valid_days:
            return city_data[day_formatted]
        else:
            raise Exception("Not a valid day.")

    def get_hour(self, day_data, time):
        if time in self.valid_times:
            return day_data[time]
        else:
            raise Exception("Not a valid time.")
    
    def get_attribute(self, hour_data, attribute_name):
        # Some checks on the attribute names are required here.
        # Not sure if those attribute names will be changed later, so I will
        # just leave this unchecked for now.
        return hour_data[attribute_name]
    
    def get_attribute_hour(self, city_data, day, hour, attribute_name):
        day_data = self.get_day(city_data, day)
        hour_data = self.get_hour(day_data, hour)
        attribute_data = self.get_attribute(hour_data, attribute_name)
        return attribute_data 

    def get_attribute_week(self, city_data, attribute_name):
        # Usage of 'sum' here flattens the list.
        city_weather_list = sum(list(city_data.values()), [])
        attribute_concat = map(lambda day: self.get_attribute(day, attribute_name), city_weather_list)
        return list(attribute_concat)
   

    # EXTENSION: Extend this or previous 'attribute' functions to handle multiple attribute arguments
    def get_attribute_across_cities(self, attribute_name):
        cities = self.get_cities_list()
        cities_weather = map(lambda city: (city, self.get_city_weather_json(city)), cities)
        attribute = map(lambda data: (data[0], self.get_attribute_week(data[1], attribute_name)) , cities_weather)
        return list(attribute)


    def get_median_attribute_city(self, city_data, attribute_name):
        temps_list = self.get_attribute_week(city_data, attribute_name)
        return statistics.median_low(list(temps_list))

    def get_city_with_max_attribute(self, attribute_name):
        cities_attribute = self.get_attribute_across_cities(attribute_name)
        max_attribute = max(cities_attribute, key=lambda data: data[1])[1]
        max_attributes = filter(lambda x: x[1] == max_attribute, cities_attribute)
        max_attributes = list(max_attributes)
        max_attributes.sort(key=lambda data: data[0])
        return max_attributes[0][0]

    def check_if_snow(self):
        precip_req = 0
        temp_req = 2

        # Needs to be refactored alongside the 'attribute' functions.
        precips = self.get_attribute_across_cities("precipitation")
        temps = self.get_attribute_across_cities("temperature")
        
        # Iterate over both attributes and combine them into the form (City_Name, [(Attr1, Attr2), ...])
        zipped = [(p[0], list(zip(p[1], t[1]))) for p, t in zip(precips, temps)]

        # Iterate over data structure and check the tuples individually against snow condition
        filtered_zipped = filter(lambda data: any(t[0] > precip_req and t[1] < temp_req for t in data[1]), zipped)
        filtered_city_names = map(lambda data: data[0], filtered_zipped)
        
        return len(list(filtered_city_names)) > 0
    
        
