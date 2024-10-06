from pymongo import MongoClient
import hashlib

# MongoDB connection
client = MongoClient('mongodb+srv://datrujillo2099:TGwUy3xi6XyXfztY@cluster0.dgiwn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')  # Replace with your MongoDB URI if needed
db = client['App']  # database name
users_collection = db['user info']  # Collection name for storing user data

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to hash passwords for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function to register a new user
def register_user(username, password, sex, height, weight):
    # Check if the username already exists
    if users_collection.find_one({"username": username}):
        print("Username already exists.")
    else:
        hashed_password = hash_password(password)
        user_data = {
            "username": username,
            "password": hashed_password,
            "sex": sex,
            "height": height,
            "weight": weight,
            "heart_rate": [],
            "blood_pressure": []
        }
        users_collection.insert_one(user_data)
        print(f"User {username} registered successfully.")

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
def calculate_Daily_Calorie_intake(BMR_value, Activity):
    activity_levels = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extremely Active": 1.9
    }

    if Activity in activity_levels:
        return int(BMR_value * activity_levels[Activity])
    else:
        raise ValueError("Error: Invalid activity level")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions to log heart rate and find its average
def Heart_Rate_Log(username, heart_rate_input):
    user = users_collection.find_one({"username": username})
    if user:
        users_collection.update_one({"username": username}, {"$push": {"heart_rate": heart_rate_input}})
        print(f"Heart rate logged for {username}.")
    else:
        print("User not found. Please register first.")

def Average_Heart_Rate(username):
    user = users_collection.find_one({"username": username})
    if user and user["heart_rate"]:
        heart_rates = user["heart_rate"]
        average_heart_rate = sum(heart_rates) / len(heart_rates)
        return int(average_heart_rate)
    else:
        return "No heart rate data available."

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions to log blood pressure and find their average
def Blood_Pressure_Log(username, systolic, diastolic):
    user = users_collection.find_one({"username": username})
    if user:
        users_collection.update_one({"username": username}, {"$push": {"blood_pressure": (systolic, diastolic)}})
        print(f"Blood pressure logged for {username}.")
    else:
        print("User not found. Please register first.")

def Average_Blood_Pressure(username):
    user = users_collection.find_one({"username": username})
    if user and user["blood_pressure"]:
        blood_pressures = user["blood_pressure"]
        total_systolic = sum(bp[0] for bp in blood_pressures)
        total_diastolic = sum(bp[1] for bp in blood_pressures)
        average_systolic = total_systolic / len(blood_pressures)
        average_diastolic = total_diastolic / len(blood_pressures)
        return int(average_systolic), int(average_diastolic)
    else:
        return "No blood pressure data available."

register_user("johnDoe", "password123", "Male", 5.9, 180)
