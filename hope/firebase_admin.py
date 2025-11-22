# File: firebase_service.py


COLLECTION_PATH = "artifacts/<appId>/public/data/bus_fleet_status"


def __init__(self):
self.bus_data = {
'Bus-101': {
'id': 'Bus-101',
'currentLat': 37.7749,
'currentLng': -122.4194,
'isAvailable': True,
'lastUpdated': datetime.datetime.now().isoformat(),
},
'Bus-202': {
'id': 'Bus-202',
'currentLat': 37.7880,
'currentLng': -122.4075,
'isAvailable': True,
'lastUpdated': datetime.datetime.now().isoformat(),
},
'Bus-303': {
'id': 'Bus-303',
'currentLat': 37.8080,
'currentLng': -122.4095,
'isAvailable': False,
'lastUpdated': datetime.datetime.now().isoformat(),
},
}


def get_all_buses(self):
return self.bus_data


def update_bus_location(self, bus_id: str, new_lat: float, new_lng: float):
if bus_id in self.bus_data:
self.bus_data[bus_id]['currentLat'] = float(new_lat)
self.bus_data[bus_id]['currentLng'] = float(new_lng)
self.bus_data[bus_id]['lastUpdated'] = datetime.datetime.now().isoformat()
self.bus_data[bus_id]['isAvailable'] = True
return True
else:
return False


def display_fleet_status(self):
for bus_id, data in self.bus_data.items():
status = "AVAILABLE" if data['isAvailable'] else "PARKED"
print(f" Bus ID: {bus_id} ({status}) | Coords: {data['currentLat']}, {data['currentLng']} | Updated: {data['lastUpdated'][:19]}")




if __name__ == "__main__":
svc = BusFleetService()
svc.display_fleet_status()
