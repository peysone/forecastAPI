"""
Napisz program, który sprawdzi, czy danego dnia będzie padać. Użyj do tego poniższego API. Aplikacja ma działać następująco:

Program pyta dla jakiej daty należy sprawdzić pogodę.
Data musi byc w formacie YYYY-mm-dd, np. 2022-11-03.
W przypadku nie podania daty, aplikacja przyjmie za poszukiwaną datę następny dzień.
Aplikacja wykona zapytanie do API w celu poszukiwania stanu pogody.
Istnieją trzy możliwe informacje dla opadów deszczu:
Będzie padać (dla wyniku większego niż 0.0)
Nie będzie padać (dla wyniku równego 0.0)
Nie wiem (gdy wyniku z jakiegoś powodu nie ma lub wartość jest ujemna)
Będzie padać
Nie będzie padać
Nie wiem
Wyniki zapytań powinny być zapisywane do pliku.
Jeżeli szukana data znajduje sie juz w pliku, nie wykonuj zapytania do API, tylko zwróć wynik z pliku.

URL do API:
https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}

W URL należy uzupełnić parametry: latitude, longitude oraz searched_date
"""



import requests
import json
from datetime import datetime, timedelta


def check_rain_forecast(date, latitude, longitude):
    # Sprawdzenie, czy data została podana, jeśli nie, przyjmij następny dzień
    if date is None:
        search_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        search_date = date

    # Sprawdzenie, czy plik z danymi istnieje i zawiera odpowiedź dla danej daty
    filename = "forecast_data.json"
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            if search_date in data:
                return data[search_date]
    except FileNotFoundError:
        pass

    # Wykonanie zapytania do API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain_1h&daily=rain_sum&timezone=Europe%2FLondon&start_date={search_date}&end_date={search_date}"
    response = requests.get(url)
    response_json = response.json()

    print(json.dumps(response_json))


    # Zapisanie wyniku do pliku
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[search_date] = "Nieznana prognoza"

    with open(filename, "w") as file:
        json.dump(data, file)

    return "Nieznana prognoza"


date_to_check = input("Podaj datę w formacie RRRR - mm - dd (np. 2023-06-29): ")
latitude_input = input("Podaj szerokość geograficzną (latitude): ")
longitude_input = input("Podaj długość geograficzną (longitude): ")

forecast_result = check_rain_forecast(date_to_check, latitude_input, longitude_input)
print(f"Prognoza dla {date_to_check}: {forecast_result}")



# Latitude: 54.372158
# Longitude: 18.638306