import argparse
import json
from weather import Weather


def q1(weather):
    city = weather.get_city_weather_json("Bath")
    temp = weather.get_attribute_hour(city, "Friday", 10, "temperature")
    return temp

def q2(weather):
    pressure_req = 1000
    city = weather.get_city_weather_json("Edinburgh")
    pressure_list = weather.get_attribute_week(city, "pressure")
    return any(p < pressure_req for p in pressure_list)

def q3(weather):
    city = weather.get_city_weather_json("Cardiff")
    return weather.get_median_attribute_city(city, "temperature")

def q4(weather):
    return weather.get_city_with_max_attribute('wind_speed')

def q5(weather):
    return weather.check_if_snow()
    


if __name__  == "__main__":
    # I use argparse instead of sys.argv for an easier out-of-box solution for cmdl arguments
    argparse = argparse.ArgumentParser()

    argparse.add_argument("-i", "--id", required=True, help="Candidate ID for use with the API")
    argparse.add_argument("-a", "--link", required=True, help="API link in the form https://something.com")
    argparse.add_argument("-o", "--output", required=True, help="File location and name where JSON will be stored in .txt format")
    # vars returns a dict
    args = vars(argparse.parse_args())

    # Unpack args for easier use
    candidate_id = int(args['id'])
    api_link = args['link']
    output_location = args['output']
    
    weather = Weather(candidate_id, api_link)

    answer = [
        q1(weather),
        q2(weather),
        q3(weather),
        q4(weather),
        q5(weather)
    ]
   
    # Simply JSON dump the list constructed above at specified location + name i.e. 'output.txt'
    with open(output_location, "w") as f:
        f.write(json.dumps(answer))
