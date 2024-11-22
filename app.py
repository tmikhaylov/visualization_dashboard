from flask import Flask, jsonify, send_from_directory
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Initialize Flask app
app = Flask(__name__, static_folder="static")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client["community_data"]

# Default route to serve the frontend
@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

# API endpoints
@app.route("/data/housing", methods=["GET"])
def get_housing_data():
    housing_data = list(db.housing_projects.find({}, {"_id": 0}))
    return jsonify(housing_data)

@app.route("/data/volunteers", methods=["GET"])
def get_volunteer_data():
    volunteer_data = list(db.volunteer_engagement.find({}, {"_id": 0}))
    return jsonify(volunteer_data)

@app.route("/data/community", methods=["GET"])
def get_community_data():
    # Retrieve data from MongoDB
    community_data = list(db.community_impact.find({}, {"_id": 0}))
    housing_data = list(db.housing_projects.find({}, {"_id": 0}))

    # Create a dictionary to map House ID to Location
    house_id_to_location = {house["House ID"]: house["Location"] for house in housing_data}

    # Add Location to community_data based on Project ID matching House ID
    for item in community_data:
        house_id = item.get("Project ID")
        item["Location"] = house_id_to_location.get(house_id, "Unknown")  # Fallback to "Unknown" if no match

    return jsonify(community_data)

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
