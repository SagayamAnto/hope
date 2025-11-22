"""
Streamlit app for Bus Fleet Manager.
This version uses a lightweight mock service by default (firebase_service.BusFleetService).
Set environment variable USE_FIREBASE=1 and provide a valid Firebase service account
configuration in __firebase_config (as JSON string) to use Firestore instead.


This file is defensive: it will not import the firebase_admin package unless
USE_FIREBASE is enabled, avoiding the old naming/import conflicts.
"""


import os
import json
from datetime import datetime
import streamlit as st
import pandas as pd


# Try importing local mock service (provided) — this is safe and expected
from firebase_service import BusFleetService


# --- Configuration ---
USE_FIREBASE = os.getenv("USE_FIREBASE", "0") in ("1", "true", "True")
FIREBASE_CONFIG = os.getenv("__firebase_config", "")
APP_ID = os.getenv("__app_id", "demo-app")


st.set_page_config(page_title="Bus Fleet Manager", page_icon="🚌", layout="wide")


# --- Service wrapper: either Firestore-backed (optional) or mock ---
class FleetBackend:
def __init__(self):
self.use_firebase = False
self.mock = BusFleetService()
self.fb_db = None


if USE_FIREBASE and FIREBASE_CONFIG:
try:
import firebase_admin
from firebase_admin import credentials, firestore


cfg = json.loads(FIREBASE_CONFIG)
cred = credentials.Certificate(cfg)
if not firebase_admin._apps:
firebase_admin.initialize_app(cred)
self.fb_db = firestore.client()
self.use_firebase = True
except Exception as e:
st.warning(f"Firebase init failed, using mock backend. Reason: {e}")
self.use_firebase = False


def collection_path(self):(self):
return f"artifacts/{APP_ID}/public/data/bus_fleet_status"


def get_all(self):
if self.use_firebase and self.fb_db:
coll = self.fb_db.collection(self.collection_path())
docs = coll.stream()
st.caption("Tip: To use Firestore, set environment variables USE_FIREBASE=1 and __firebase_config to a JSON service account.")
