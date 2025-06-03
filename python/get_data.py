from opensky_api import OpenSkyApi

def get_data():
    api = OpenSkyApi()
    s = api.get_states()
    return s

if __name__ == "__main__":
    data = get_data()