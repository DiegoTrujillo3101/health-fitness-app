#  This is where the backend code for the app will go
from pymongo import MongoClient
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for MongoDB URI)
load_dotenv()

# MongoDB connection using environment variable for security
client = MongoClient(os.getenv('MONGO_URI'))  # Ensure that MONGO_URI is in our .env file
db = client['App']  # Database name
users_collection = db['user_info']  # Collection name for storing user data

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Generate a random salt
def generate_salt():
    return os.urandom(16).hex()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to hash passwords with salt
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to register a new user with salt and hashed password
def register_user(username, password, sex, height, weight):
    # Check if the username already exists
    if users_collection.find_one({"username": username}):
        print("Username already exists.")
    else:
        try:
            salt = generate_salt()  # Generate a salt for this user
            hashed_password = hash_password(password, salt)
            user_data = {
                "username": username,
                "password": hashed_password,
                "salt": salt,  # Store the salt in the database
                "sex": sex,
                "height": height,
                "weight": weight,
                "heart_rate": [],
                "blood_pressure": [],
                "water_consumed": 0  # Initialize water consumed to 0 cups
            }
            users_collection.insert_one(user_data)
            print(f"User {username} registered successfully.")
        except Exception as e:
            print(f"An error occurred during registration: {e}")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to convert height from feet to inches for calculation purposes
def feet_to_inches(feet):
    whole_feet = int(feet)
    fractional_feet = feet - whole_feet
    inches = (whole_feet * 12) + (fractional_feet * 12)
    return inches

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to calculate Basal Metabolic Rate (BMR)
def calculate_bmr(sex, weight, age, height_in_feet):
    height_in_inches = feet_to_inches(height_in_feet)
    if sex == "Male":
        bmr = 66 + (6.23 * weight) + (12.7 * height_in_inches) - (6.8 * age)
    elif sex == "Female":
        bmr = 655 + (4.35 * weight) + (4.7 * height_in_inches) - (4.7 * age)
    else:
        raise ValueError("Error: Sex must be 'Male' or 'Female'")
    return bmr

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to calculate Daily calories based on activity level of the person
def calculate_daily_calorie_intake(bmr_value, activity):
    activity_levels = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extremely Active": 1.9
    }

    if activity in activity_levels:
        return int(bmr_value * activity_levels[activity])
    else:
        raise ValueError("Error: Invalid activity level")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions to log heart rate and find its average
def heart_rate_log(username, heart_rate_input):
    user = users_collection.find_one({"username": username})
    if user:
        users_collection.update_one({"username": username}, {"$push": {"heart_rate": heart_rate_input}})
        print(f"Heart rate logged for {username}.")
    else:
        print("User not found. Please register first.")

def average_heart_rate(username):
    user = users_collection.find_one({"username": username})
    if user and user["heart_rate"]:
        heart_rates = user["heart_rate"]
        average_heart_rate = sum(heart_rates) / len(heart_rates)
        return int(average_heart_rate)
    else:
        return "No heart rate data available."

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions to log blood pressure and find their average
def blood_pressure_log(username, systolic, diastolic):
    user = users_collection.find_one({"username": username})
    if user:
        users_collection.update_one({"username": username}, {"$push": {"blood_pressure": {"systolic": systolic, "diastolic": diastolic}}})
        print(f"Blood pressure logged for {username}.")
    else:
        print("User not found. Please register first.")

def average_blood_pressure(username):
    user = users_collection.find_one({"username": username})
    if user and user["blood_pressure"]:
        blood_pressures = user["blood_pressure"]
        total_systolic = sum(bp["systolic"] for bp in blood_pressures)
        total_diastolic = sum(bp["diastolic"] for bp in blood_pressures)
        average_systolic = total_systolic / len(blood_pressures)
        average_diastolic = total_diastolic / len(blood_pressures)
        return int(average_systolic), int(average_diastolic)
    else:
        return "No blood pressure data available."

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to update user's password with salt
def change_password(username, old_password, new_password):
    user = users_collection.find_one({"username": username})
    if user:
        old_salt = user["salt"]
        if user["password"] == hash_password(old_password, old_salt):
            new_salt = generate_salt()
            users_collection.update_one({"username": username}, {"$set": {
                "password": hash_password(new_password, new_salt),
                "salt": new_salt
            }})
            print("Password changed successfully.")
        else:
            print("Old password is incorrect.")
    else:
        print("User not found.")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to update user's username
def change_username(old_username, new_username):
    user = users_collection.find_one({"username": old_username})
    if user:
        if not users_collection.find_one({"username": new_username}):  # Ensure new username doesn't exist
            users_collection.update_one({"username": old_username}, {"$set": {"username": new_username}})
            print(f"Username changed to {new_username}.")
        else:
            print("New username already taken.")
    else:
        print("Old username not found.")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to update user's weight
def change_weight(username, new_weight):
    user = users_collection.find_one({"username": username})
    if user:
        users_collection.update_one({"username": username}, {"$set": {"weight": new_weight}})
        print(f"Weight updated to {new_weight} lbs.")
    else:
        print("User not found.")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to increase water consumption by 1 cup
def increase_water_consumption(username):
    user = users_collection.find_one({"username": username})
    if user:
        users_collection.update_one({"username": username}, {"$inc": {"water_consumed": 1}})
        print(f"Water consumption increased by 1 cup for {username}.")
    else:
        print("User not found.")

# Function to decrease water consumption by 1 cup (cannot go below 0)
def decrease_water_consumption(username):
    user = users_collection.find_one({"username": username})
    if user:
        if user["water_consumed"] > 0:
            users_collection.update_one({"username": username}, {"$inc": {"water_consumed": -1}})
            print(f"Water consumption decreased by 1 cup for {username}.")
        else:
            print("Cannot decrease further, water consumption is already at 0.")
    else:
        print("User not found.")

# Function to get the current water consumption for a user
def get_water_consumption(username):
    user = users_collection.find_one({"username": username})
    if user:
        return user["water_consumed"]
    else:
        return "User not found."
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


