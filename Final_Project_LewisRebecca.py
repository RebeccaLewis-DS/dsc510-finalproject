#File: OLD_Final_Project_LewisRebecca.py
#Name: Rebecca Lewis
#Date: May 26, 2019
#Course: DSC 510
#Usage: Create an application that interacts with a webservice for OpenWeatherMap to obtain data requested by a user

class Forecast():
    '''Objet to hold the data for the forecast'''

    # Constructor
    def __init__(self):
        self.city = ''
        self.mintemp = 0
        self.maxtemp = 0
        self.temp = 0
        self.pressure = 0
        self.humidity = 0

    #set the forecast data for the city
    def setForecast(self, data):
        self.city = data['name']
        self.mintemp = data['main']['temp_min']
        self.maxtemp = data['main']['temp_max']
        self.temp = data['main']['temp']
        self.pressure = data['main']['pressure']
        self.humidity = data['main']['humidity']

    # return the current temperature based on the desired unit
    def getTemp(self, unit):
        if unit == "C":
            return pytemperature.k2c(self.temp)
        elif unit == "F":
            return pytemperature.k2f(self.temp)

    # return the min temperature based on the desired unit
    def getMinTemp(self, unit):
        if unit == "C":
            return pytemperature.k2c(self.mintemp)
        elif unit == "F":
            return pytemperature.k2f(self.mintemp)

    # return the max temperature based on the desired unit
    def getMaxTemp(self, unit):
        if unit == "C":
            return pytemperature.k2c(self.maxtemp)
        elif unit == "F":
            return pytemperature.k2f(self.maxtemp)

    # return the pressure
    def getPressure(self):
        return self.pressure

    # return the humidity
    def getHumidity(self):
        return self.humidity

    # return the name of the city
    def getName(self):
        return self.city

def cityValidate(userCity):
    '''This function validates the user input as a city as much as possible before calling the API with that data.  '''

    #If the user enters numbers within the city name, alert the user and return None
    if any(char.isdigit() for char in userCity):
        print("\nYou have entered digits in your city name.  If you would like to view the weather by zip, select option 2.\n")
        return None

    #It is quite possible that the user could enter a comma followed by a state.
    #This loop iterates through the user response and rebuilds a string until it hits a character.
    #Strip is also used to remove any leading or training spaces
    funcity = ''
    for char in userCity.strip():
        if char not in string.punctuation:
            funcity = funcity + char
        else:
            break

    #many states have spaces in the name.  Replace spaces in the name with %20
    funcity = funcity.replace(" ", "%20")

    return funcity #return the final reasult


def zipValidate(userZip):
    '''This function validates the user input as a zip code as much as possible before calling the API with that data.'''

    # the user may enter a long form zip including a hyphen.  the API will only accept a 5 digit zip code
    # This loop iterates through the user response and rebuilds a string until it hits a character.
    # Strip is also used to remove any leading or training spaces
    funzip = ''
    for dig in userZip.strip():
        if dig not in string.punctuation:
            funzip = funzip + dig
        else:
            break
    # if the resulting string contains alphabetical characters, alert the user and return None
    if not funzip.isdigit():
        print("\nYou have entered alphabetical characters in your zip code.  If you would like to view the weather by city, select option 1.\n")
        return None
    elif len(funzip)!= 5:               # if the resulting string is not 5 digits, alert the user and return none.
        print("\nYour zip code is an invalid length.  Please try again")
        return None
    else:
        return funzip                   # if we get through these checks, return the resulting string for use in our API call

def getUnits():
    '''Prompt the user for their preferred temperature unit and error check'''

    UnitValid = False
    while not UnitValid:
        userUnit = input("\nEnter C for Celsius or F for Fahreneheit:\n")
        if userUnit.upper() != 'C' and userUnit.upper() != 'F':
            print("Invalid response.")
        else:
            UnitValid = True

    return userUnit.upper()


def getWeather(urlstring):
    '''This function calls the OpenWeatherMap using the API string built in the main function.  It includes a try/except block to catch errors connecting'''

    r = requests.get(urlstring)
    weather_json = json.loads(r.text)       # read the response text into a json string

    # if an error is returned when checking the status, display a message to the user.  The API returns a json file whether the call is successful or not
    # so the raise_for_status method is used.
    try:
        r.raise_for_status()
        return weather_json
    except requests.exceptions.HTTPError:
         print("An error has been encountered while accessing the weather app.  {}.\n".format(str(weather_json['message']).capitalize()))

def prettyPrint(curentForecast, unit):
    '''This function prints the weather returned by the OpenWeatherMap'''

    #the temperature is returned in kelvin so the pytemperature module is used to convert it to fahrenheit
    print("\nCurrent Weather for {}".format(currentForecast.getName()))
    print("Current Temperature: {:.2f}\xb0{}".format(currentForecast.getTemp(unit), unit))
    print("Min Temperature: {:.2f}\xb0{}".format(currentForecast.getMinTemp(unit), unit))
    print("Max Temperature: {:.2f}\xb0{}".format(currentForecast.getMaxTemp(unit), unit))
    print("Humidity: {}%".format(currentForecast.getHumidity()))
    print("Pressure: {} hPa".format(currentForecast.getPressure()))

# MAIN #
import pytemperature
import requests
import json
import string

# welcome message
print("Welcome to the Lewis Weather App!")

# initialize variables
userResponse = ''
url = "https://api.openweathermap.org/data/2.5/weather"
appid = "7c82a4eac294c7e4197b6ec01048306b"

# main control loop; runs until the user enters exit
while userResponse.lower() != 'exit':
    userResponse = input("\nWould you like to view current weather information by US City or US Zip?\nEnter 1 for US City, 2 for US Zip or exit to quit the program:\n")

    # user input error checking and building the url string to fetch the data.
    if userResponse == "1":                     # if the user selects city, call the city validation function
        userCity = input("\nPlease enter a US city:\n")
        city = cityValidate(userCity)
        if city == None:                        # if the validation function returns None, the input was not valid continue is used to prompt the user again
            continue
        else:
            urlstring = "{}?q={}&APPID={}".format(url, city, appid)     # format the url string for city requests
    elif userResponse == "2":                   # if the user selects zip, call the zip validation function
        userZip = input("\nPlease enter a US zip code:\n")
        zipcode = zipValidate(userZip)
        if zipcode == None:                     # if the validation function returns None, the input was not valid continue is used to prompt the user again
            continue
        else:
            urlstring = "{}?zip={}&APPID={}".format(url, zipcode, appid)     # format the url string for zip requests
    elif userResponse.lower() == 'exit':        # if the user types exit, regardless of case, display and exit message and quit the program.
        print("\nThanks for using the Lewis Weather App.  Have a great day!")
        exit()
    else:                                       # if the user enters anything else, display a message and prompt again
        print("\nInvalid Response.  Please enter a 1 for US City or 2 for US Zip\n")
        continue


    # once the city/zip is validated, prompt the user for the desired units
    unit = getUnits()

    # call the get weather function get info using the API.
    weather_json = getWeather(urlstring)

    # create an instance of the current forecast and set the values based on the API response
    currentForecast = Forecast()
    currentForecast.setForecast(weather_json)

    #print the results to the screen
    prettyPrint(currentForecast, unit)



