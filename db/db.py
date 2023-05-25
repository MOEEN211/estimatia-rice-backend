import pyrebase

config = {
    "apiKey": "AIzaSyCBaNr9snAoZTC0T7EdHaBj3xvut2_rpWU",
    "authDomain": "rice-estimatia.firebaseapp.com",
    "databaseURL": "https://rice-estimatia-default-rtdb.firebaseio.com",
    "projectId": "rice-estimatia",
    "storageBucket": "rice-estimatia.appspot.com",
    "messagingSenderId": "285272956913",
    "appId": "1:285272956913:web:0dfb51b83ca0bbbeda2e50",
    "measurementId": "G-TH7M3RYG3B"
}


# This function returns firebase instance


def get_connection():
    firebase = pyrebase.initialize_app(config)
    return firebase.database()
