from flask import Flask, jsonify, request
from pymodm import connect
from main import add_heart_rate, create_user, print_user
import numpy as np
import models
import datetime
import time


connect("mongodb://localhost:27017/heart_rate")
app = Flask(__name__)

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
        return jsonify(data)
    except:
        print("new user was created")
        create_user(email, age, heart_rate, time)
        return jsonify(r["user_email"])

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def get_user(user_email):
    """
        For the user can GET all the heart rate measurements
        :param user_email: user specific email information
        :return: json file format of the user information and all the
                 measurements.
        """

    user = models.User.objects.raw({"_id": user_email}).first()
    return jsonify(user.heart_rate)

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

    user = models.User.objects.raw({"_id": user_email}).first()
    heart_rate = user.heart_rate
    ave_hr = np.mean(heart_rate)
    data = {"usr_mail": user.email,
            "ave_HR": ave_hr}
    return jsonify(data)

@app.route("/api/heart_rate/interval_average", methods=["POST"])
def get_int_ave():
    """
        For the user can GET the average heart rate for the user since the time
        they given
        :return: json file format of the user email, the specific user average
        heart rate and the interval average of the heart rate, respectively
    """
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
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1")
