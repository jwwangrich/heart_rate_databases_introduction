.. y documentation master file, created by
   sphinx-quickstart on Fri Mar 23 01:00:34 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to y's documentation!
=============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
:param:
   """
        validate the user email, age, heart rate have correct type and no
        value missed
        :param r: requested json file
        :return: information to understand whether the values are correct
   """
   """
    store heart rate measurement for the user with user email
    :param email: str email of the user
    :param heart_rate: number heart_rate measurement of the user
    :param time: the datetime of the heart_rate measurement
    :return: json file format
   """
   """
        For the user can GET all the heart rate measurements
        :param user_email: user specific email information
        :return: json file format of the user information and all the
                 measurements.
   """
"""
        This function is to test whether the given user with their ages,
        average interval heart rate is tachycardic or not. If they are
        under this type of disease, the return value is true, vice versa
        :param user_age: user given age when they measure their HR
        :param int_ave: given time of heart_rate measurement
        :return: True or False
        """
	"""
        For the user can GET the average heart rate for the user since the time
        they given
        :return: json file format of the user email, the specific user average
        heart rate and the interval average of the heart rate, respectively
    """
    
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
