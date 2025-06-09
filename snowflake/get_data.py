import pandas as pd
from opensky_api import OpenSkyApi

def get_data():
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
    df = get_data()