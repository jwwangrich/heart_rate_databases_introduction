from flask import Flask, jsonify, request
from pymodm import connect
from main import add_heart_rate, create_user, print_user
import numpy as np
import models
import datetime
import time


connect("mongodb://localhost:27017/heart_rate")
app = Flask(__name__)

def validate_heart_rate_request(r):
    """
        validate the user email, age, heart rate have correct type and no
        value missed
        :param r: requested json file
        :return: information to understand whether the values are correct
        """
    try:
        email = r["user_email"]
        assert(type(email)==str)
        age = r["user_age"]
        assert(type(age)==int)
        heart_rate = r["heart_rate"]
        assert(type(heart_rate)==float)
        return True
    except:
        return False

@app.route("/api/heart_rate", methods=["POST"])
def post():
    """
    store heart rate measurement for the user with user email
    :param email: str email of the user
    :param heart_rate: number heart_rate measurement of the user
    :param time: the datetime of the heart_rate measurement
    :return: json file format
    """
    r = request.get_json()
    email = r["user_email"]
    age = r["user_age"]
    heart_rate = r["heart_rate"]
    time = datetime.datetime.now()
    try:
        add_heart_rate(email, heart_rate, time)
        data = {"message": "Succeed"}
        return jsonify(data), 200
    except:
        print("new user was created")
        create_user(email, age, heart_rate, time)
        return jsonify(r["user_email"]), 400

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def get_user(user_email):
    """
        For the user can GET all the heart rate measurements
        :param user_email: user specific email information
        :return: json file format of the user information and all the
                 measurements.
        """
    try:
        user = models.User.objects.raw({"_id": user_email}).first()
        return jsonify(user.heart_rate), 200
    except:
        print("no user available")
        return 400

@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def get_ave(user_email):
    """
        For the user can GET the average of all the heart rate measurements
        :param user_email: user specific email information
        :param heart_rate: all the heart rate measurements
        :param ave_hr: the average of all heart rate measurements
        :return: json file format of the user email and the specific user average
         heart rate.
    """
    try:
        user = models.User.objects.raw({"_id": user_email}).first()
        heart_rate = user.heart_rate
        ave_hr = np.mean(heart_rate)
        data = {"usr_mail": user.email,
                "ave_HR": ave_hr}
        return jsonify(data), 200
    except:
        print("no user available")
        return 200

def tachycardic(user_age, int_ave):
    """
        This function is to test whether the given user with their ages,
        average interval heart rate is tachycardic or not. If they are
        under this type of disease, the return value is true, vice versa
        :param user_age: user given age when they measure their HR
        :param int_ave: given time of heart_rate measurement
        :return: True or False
        """
    if (user_age >= 1 and user_age <= 2):
        if (int_ave > 151):
            return True
        else:
            return False
    if (user_age >= 3 and user_age <= 4):
        if (int_ave > 137):
            return True
        else:
            return False
    if (user_age >= 5 and user_age <= 7):
        if (int_ave > 133):
            return True
        else:
            return False
    if (user_age >= 8 and user_age <= 11):
        if (int_ave >130):
            return True
        else:
            return False
    if (user_age >= 12 and user_age <= 15):
        if (int_ave > 119):
            return True
        else:
            return False
    if (user_age > 15):
        if (int_ave > 100):
            return True
        else:
            return False

@app.route("/api/heart_rate/interval_average", methods=["POST"])
def get_int_ave():
    """
        For the user can GET the average heart rate for the user since the time
        they given
        :return: json file format of the user email, the specific user average
        heart rate and the interval average of the heart rate, respectively
    """
    try:
        r = request.get_json()
        email = r["user_email"]
        my_time = r["heart_rate_average_since"]
        set_time = time.strptime(my_time, "%Y-%m-%d %H:%M:%S.%f")

        user = models.User.objects.raw({"_id": email}).first()
        hr_rate = user.heart_rate
        hr_times = user.heart_rate_times

        for t, p in enumerate(hr_times):
            p1 = p.strftime('%Y-%m-%d %H:%M:%S.%f')
            p2 = time.strptime(p1, "%Y-%m-%d %H:%M:%S.%f")
            if (p2 > set_time):
                hr_rate.append(hr_rate[t])
        int_ave = np.mean(hr_rate)
        data = {"user_email": email,
                "heart_rate_average_since": my_time,
                "interval_average": int_ave}
        return jsonify(data), 200
    except:
        print("need user")
        return 400

if __name__ == "__main__":
    app.run(host="127.0.0.1")