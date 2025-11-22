import streamlit as st 
import firebase_service
from firebase_service import BusFleetServic
import json
import os
from datetime import datetime

# Assuming global variables are set as environment variables or provided
firebase_config = json.loads(os.getenv('__firebase_config', '{}'))
app_id = os.getenv('__app_id', 'default-app-id')
initial_auth_token = os.getenv('__initial_auth_token', None)

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config) if firebase_config else None
    if cred:
        firebase_admin.initialize_app(cred)
    else:
        firebase_admin.initialize_app()

db = firestore.client()

collection_path = f'/artifacts/{app_id}/public/data/bus_fleet_status'

def initialize_buses():
    buses_ref = db.collection(collection_path)
    if not buses_ref.get():
        default_buses = [
            {'id': 'Bus-101', 'currentLat': 37.7749, 'currentLng': -122.4194, 'isAvailable': True},
            {'id': 'Bus-202', 'currentLat': 37.7749, 'currentLng': -122.4194, 'isAvailable': True},
            {'id': 'Bus-303', 'currentLat': 37.7749, 'currentLng': -122.4194, 'isAvailable': True},
        ]
        for bus in default_buses:
            buses_ref.document(bus['id']).set({
                **bus,
                'lastUpdated': firestore.SERVER_TIMESTAMP
            })

def get_buses():
    buses_ref = db.collection(collection_path)
    docs = buses_ref.stream()
    return {doc.id: doc.to_dict() for doc in docs}

def update_bus_location(bus_id, lat, lng):
    bus_ref = db.collection(collection_path).document(bus_id)
    bus_ref.update({
        'currentLat': lat,
        'currentLng': lng,
        'lastUpdated': firestore.SERVER_TIMESTAMP
    })

st.title("Bus Fleet Manager")

# Initialize buses if needed
initialize_buses()

# Get all buses
buses = get_buses()
bus_ids = list(buses.keys())

# Bus Selection
selected_bus_id = st.selectbox("Select Active Bus", bus_ids, key="bus_select")

# Location Update
st.subheader("Update Location")
lat = st.number_input("Latitude", value=buses[selected_bus_id]['currentLat'] if selected_bus_id in buses else 37.7749, key="lat")
lng = st.number_input("Longitude", value=buses[selected_bus_id]['currentLng'] if selected_bus_id in buses else -122.4194, key="lng")

if st.button("Update Bus Location"):
    update_bus_location(selected_bus_id, lat, lng)
    st.success("Location updated!")

# Real-Time Map Display
st.subheader("Real-Time Map")
if selected_bus_id in buses:
    bus_data = buses[selected_bus_id]
    map_lat = bus_data.get('currentLat', 37.7749)
    map_lng = bus_data.get('currentLng', -122.4194)
    last_updated = bus_data.get('lastUpdated')
    if last_updated:
        last_updated_str = last_updated.strftime("%Y-%m-%d %H:%M:%S") if isinstance(last_updated, datetime) else str(last_updated)
    else:
        last_updated_str = "N/A"
    
    map_url = f"https://maps.google.com/maps?q={map_lat},{map_lng}&z=15&output=embed"
    st.components.v1.iframe(map_url, width=600, height=400)
    
    st.write(f"**Latitude:** {map_lat}")
    st.write(f"**Longitude:** {map_lng}")
    st.write(f"**Last Updated:** {last_updated_str}")
else:
    st.write("No bus selected or data unavailable.")



