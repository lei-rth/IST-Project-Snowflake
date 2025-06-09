import pandas as pd
from opensky_api import OpenSkyApi
from datetime import datetime, timedelta

def get_flights_from_zurich():
    api = OpenSkyApi()
    airport = 'LSZH'  # Zurich Airport ICAO code

    now = datetime.now()

    yesterday = now - timedelta(days=1)
    begin_of_yesterday = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
    end_of_yesterday = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)

    begin_unix = int(begin_of_yesterday.timestamp())
    end_unix = int(end_of_yesterday.timestamp())

    flights = api.get_departures_by_airport(airport, begin_unix, end_unix)

    data = []
    for flight in flights:
        flight_dict = {
            'icao24': flight.icao24,
            'firstSeen': flight.firstSeen,
            'estDepartureAirport': flight.estDepartureAirport,
            'lastSeen': flight.lastSeen,
            'estArrivalAirport': flight.estArrivalAirport,
            'callsign': flight.callsign,
            'estDepartureAirportHorizDistance': flight.estDepartureAirportHorizDistance,
            'estDepartureAirportVertDistance': flight.estDepartureAirportVertDistance,
            'estArrivalAirportHorizDistance': flight.estArrivalAirportHorizDistance,
            'estArrivalAirportVertDistance': flight.estArrivalAirportVertDistance,
            'departureAirportCandidatesCount': flight.departureAirportCandidatesCount,
            'arrivalAirportCandidatesCount': flight.arrivalAirportCandidatesCount,
        }
        data.append(flight_dict)

    # Create a pandas DataFrame
    df = pd.DataFrame(data)
    df.to_csv('data/flights_from_zurich.csv', index=False)
    return df

def get_all_data():
    api = OpenSkyApi()
    s = api.get_states()
    data = []

    for sv in s.states:
        data.append({
            'icao24': sv.icao24,
            'callsign': sv.callsign,
            'origin_country': sv.origin_country,
            'time_position': sv.time_position,
            'latitude': sv.latitude,
            'longitude': sv.longitude,
            'latitude': sv.latitude,
            'baro_altitude': sv.baro_altitude,
            'on_ground': sv.on_ground,
            'velocity': sv.velocity,
            'true_track': sv.true_track,
            'vertical_rate': sv.vertical_rate,
            'sensors': sv.sensors,
            'squawk': sv.squawk,
            'geo_altitude': sv.geo_altitude,
            'last_contact': sv.last_contact,
            'category' : sv.category
        })

    df = pd.DataFrame(data)
    df.to_csv('data/flight_data.csv', index=False)
    return df

if __name__ == "__main__":
    df = get_all_data()
    df = get_flights_from_zurich()