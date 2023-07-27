import requests


def measureDistance(lat1, lon1, lat2, lon2, apiKey):
    url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={apiKey}&start={lon1},{lat1}&end={lon2},{lat2}"
    response = requests.get(url)

    try:
        if response.status_code == 200:
            data = response.json()
            features = data['features']
            if features:
                distance = features[0]['properties']['summary']['distance']
                return distance
            else:
                print("No distance found.")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")
