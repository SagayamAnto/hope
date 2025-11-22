import datetime
import json
import time 

class BusFleetService:
    """
    A service class to simulate the backend logic for managing a fleet of buses.

    In a real-world application, this data would be stored in a persistent,
    real-time database like Firestore. Here, we use an in-memory dictionary
    for simulation purposes.
    """

    # Mock collection path for reference, as requested by the prompt
    COLLECTION_PATH = "artifacts/<appId>/public/data/bus_fleet_status"

    def __init__(self):
        """Initializes the service with mock bus data."""
        print(f"--- Initializing Bus Fleet Service ---")
        self.bus_data = {
            'Bus-101': {
                'id': 'Bus-101',
                'currentLat': 37.7749,
                'currentLng': -122.4194,
                'isAvailable': True,
                # Use ISO format string to simulate a database timestamp
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
        """
        Retrieves the status and location for all buses in the fleet.
        This simulates the data feed for the real-time map display.
        """
        return self.bus_data

    def update_bus_location(self, bus_id: str, new_lat: float, new_lng: float):
        """
        Updates the location (Lat/Lng) for a specific bus ID.

        This simulates an operator selecting a bus and sending a new location.

        :param bus_id: The ID of the bus to update (e.g., 'Bus-101').
        :param new_lat: The new latitude coordinate.
        :param new_lng: The new longitude coordinate.
        :return: A message indicating success or failure.
        """
        if bus_id in self.bus_data:
            self.bus_data[bus_id]['currentLat'] = new_lat
            self.bus_data[bus_id]['currentLng'] = new_lng
            self.bus_data[bus_id]['lastUpdated'] = datetime.datetime.now().isoformat()
            # If a bus is updated, we assume it's active/available.
            self.bus_data[bus_id]['isAvailable'] = True
            return f"SUCCESS: Location for {bus_id} updated to ({new_lat}, {new_lng})."
        else:
            return f"ERROR: Bus ID '{bus_id}' not found in the fleet."

    def display_fleet_status(self):
        """Helper method to print the current state of the fleet."""
        print("\n--- CURRENT FLEET STATUS ---")
        for bus_id, data in self.bus_data.items():
            status = "AVAILABLE" if data['isAvailable'] else "PARKED"
            print(f" Bus ID: {bus_id} ({status})")
            print(f"   Coords: {data['currentLat']}, {data['currentLng']}")
            # Truncate the timestamp for cleaner display
            print(f"   Updated: {data['lastUpdated'][:19]}")
        print("----------------------------\n")


# --- Demonstration Block ---
if __name__ == "__main__":
    # 1. Initialize the service
    fleet_manager = BusFleetService()

    # 2. Show the initial state (how the map sees the buses when the app starts)
    fleet_manager.display_fleet_status()

    print("\n[OPERATOR ACTION]: Bus-101 is selected for a new location update.")

    # 3. Simulate an operator updating the location of Bus-101
    new_lat_101 = 37.7950
    new_lng_121 = -122.3930 # Moving the bus closer to the bay
    result = fleet_manager.update_bus_location('Bus-101', new_lat_101, new_lng_121)
    print(f"\nUpdate Result: {result}")
    
    # 4. Simulate a short time delay
    time.sleep(0.5)

    print("\n[OPERATOR ACTION]: Bus-303 is being brought back into service.")
    # 5. Simulate updating Bus-303 (which was initially unavailable)
    new_lat_303 = 37.8000
    new_lng_303 = -122.4000
    result_303 = fleet_manager.update_bus_location('Bus-303', new_lat_303, new_lng_303)
    print(f"\nUpdate Result: {result_303}")

    # 6. Show the final state (the real-time map updates instantly)
    fleet_manager.display_fleet_status()
    
    print("--- Simulation Complete ---")
