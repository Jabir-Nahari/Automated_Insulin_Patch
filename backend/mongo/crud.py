from pymongo import MongoClient
from datetime import datetime, timedelta
import os
import time
import uuid

# Load environment variables
mongo_uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.0"
# try:
# Connect to MongoDB


class connect_db:
    def __init__(self):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.aip
        self.insulin_collection = self.db.insulin_schedule
        self.temp_collection = self.db.temperature_readings

    # --- CREATE: Insert Insulin Dose Schedule ---
    def add_insulin_dose(self, scheduled_time, status, amount, notes=""):
        """Add a single insulin dose schedule."""
        try:
            unique_id = str(uuid.uuid4())
            result = self.insulin_collection.insert_one(
                {
                    "dose_id": unique_id,
                    "scheduled_time": scheduled_time,
                    "status": status,
                    "amount": amount,
                    "notes": notes,
                }
            )
            print(f"Inserted insulin dose")
        except Exception as e:
            print(f"Error inserting insulin dose: {e}")

    # --- CREATE: Batch Insert Temperature Readings ---
    def single_insert_temperatures(self, temprature, timestamp):
        """Batch insert temperature readings to optimize memory usage."""
        try:
            result = self.temp_collection.insert_one(
                {"temprature": temprature, "timestamp": timestamp}
            )
            print(f"Inserted {len(result.inserted_ids)} temperature readings")
        except Exception as e:
            print(f"Error inserting temperature readings: {e}")

    # -- Create: Batch insert temprature readings --
    # def batch_insert_temperatures(readings):
    #     """Batch insert temperature readings to optimize memory usage."""
    #     try:
    #         result = temp_collection.insert_many(readings)
    #         print(f"Inserted {len(result.inserted_ids)} temperature readings")
    #     except Exception as e:
    #         print(f"Error inserting temperature readings: {e}")

    # --- READ: Get Pending Insulin Doses ---
    def get_dose(self, dose_id):
        try:
            dose = self.insulin_collection.find_one({"dose_id": dose_id})
            return dose
        except Exception as e:
            print(f"cannot retrieve dose {dose_id}")

    def get_doses(self):
        """Retrieve pending insulin doses within a time window."""
        try:
            # end_time = datetime.now() + timedelta(hours=time_window_hours)
            doses = self.insulin_collection.find({})
            # doses = self.insulin_collection.find()
            all_doses = list(doses)
            return all_doses
        except Exception as e:
            print(f"Error retrieving doses: {e}")
            return []

    def update_dose(self, dose_id, scheduled_time, status, amount, notes):
        try:
            self.insulin_collection.update_one(
                {"dose_id": dose_id},
                {
                    "$set": {
                        "scheduled_time": scheduled_time,
                        "status": status,
                        "amount": amount,
                        "notes": notes,
                    }
                },
            )
        except Exception as e:
            print(f"Cannot update schedule of dose {dose_id}")

    # --- READ: Get Recent Temperature Readings ---
    def get_recent_temperatures(limit=10):
        """Retrieve the most recent temperature readings."""
        try:
            readings = temp_collection.find().sort("timestamp", -1).limit(limit)
            return list(readings)
        except Exception as e:
            print(f"Error retrieving temperatures: {e}")
            return []

    # --- UPDATE: Mark Dose as Taken ---
    def mark_dose_taken(self, dose_id):
        try:
            result = self.insulin_collection.update_one(
                {"dose_id": dose_id},
                {"$set": {"status": "taken", "notes": "Dose taken on time"}},
            )
            print(f"Updated {result.modified_count} dose(s)")
        except Exception as e:
            print(f"Error updating dose: {e}")
            
            
    def delete_dose(self, dose_id):
        try:
            result = self.insulin_collection.delete_one({
                "dose_id": dose_id
            })
            print(f"Deleted dose {result}")
        except Exception as e:
            print(f'Error removing dose {e}')

    # --- DELETE: Remove Old Temperature Readings ---
    def delete_old_temperatures(self, before_date):
        try:
            result = self.temp_collection.delete_many(
                {"timestamp": {"$lt": before_date}}
            )
            print(f"Deleted {result.deleted_count} old temperature readings")
        except Exception as e:
            print(f"Error deleting temperatures: {e}")

    def close_db(self):
        self.client.close()


#     # --- Example Usage ---
#     # Add an insulin dose
#     add_insulin_dose(
#         dose=10,
#         scheduled_time=datetime(2025, 4, 21, 8, 0),  # 8:00 AM
#         notes="Morning dose"
#     )

#     # Simulate continuous temperature sensor data (batch insert)
#     temperature_readings = [
#         {
#             "temperature": 36.6 + (i * 0.1),
#             "timestamp": datetime.utcnow() - timedelta(minutes=i),
#         } for i in range(5)
#     ]
#     batch_insert_temperatures(temperature_readings)

#     # Get pending doses for the next hour
#     pending_doses = get_pending_doses("user123")
#     print("Pending Doses:", [dose for dose in pending_doses])

#     # Get the 5 most recent temperature readings
#     recent_temps = get_recent_temperatures("user123", limit=5)
#     print("Recent Temperatures:", [temp for temp in recent_temps])

#     # Mark a dose as taken (replace with actual ObjectId from pending_doses)
#     # mark_dose_taken(pending_doses[0]["_id"])  # Uncomment with valid ID

#     # Delete temperature readings older than a day
#     delete_old_temperatures(datetime.utcnow() - timedelta(days=1))
# except Exception as e:
#     print(f"Error: {e}")
