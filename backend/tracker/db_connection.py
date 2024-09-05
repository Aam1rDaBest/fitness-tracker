# backend/tracker/db_connection.py
from mongoengine import connect

# Connect to the MongoDB instance
connect(
    db='fitness-tracker',        # Database name
    host='mongodb://172.21.15.111:27018/'  # MongoDB connection URI
)
