import pytest
import math
from minimon import validate_heart_rate_request, tachycardic


def test_validate_heart_rate_request():

    i1 = {
            "user_email": "richwang@email.com",
            "user_age": 28,
            "heart_rate": 98.2
    }
    r1 = validate_heart_rate_request(i1)
    assert r1 is True

    i2 = {
            "user_email": 5,
            "user_age": -6,
            "heart_rate": "200"
    }
    with pytest.raises(TypeError):
        r2 = validate_heart_rate_request(i2)
        assert r2 is False

def test_tachycardic():

    r1 = tachycardic(2, 200)
    assert r1 == True

    r2 = tachycardic(15, 120)
    assert r2 == True

    r3 = tachycardic(15, 110)
    assert r3 == False
