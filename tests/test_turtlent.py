"""tests/test_turtlent.py"""

from decimal import Decimal, getcontext
from random import randrange as random

from turtlefun.turtlent import decimal_places, TurtleNT, DEFAULT_IMAGE_HEIGHT, DEFAULT_IMAGE_WIDTH
from turtlefun.turtlefun_quotientlist import TURTLEFUN_QUOTIENT_LIST
from turtlefun.turtle_originreturnsamples import TURTLE_ORIGIN_RETURN_SAMPLES
from turtlefun.turtlefun_lines_manual import THETA_LINES


def test_decimal_places_int():
    assert decimal_places(int(5)) == 0
    assert decimal_places(5) == 0

def test_decimal_places_float():
    assert decimal_places(float(5)) == 0
    assert decimal_places(float(1.2)) == 1
    assert decimal_places(float(1.123)) == 3
    
def test_decimmal_places_exponent():
    assert decimal_places(float(1E-5)) == 5
    assert decimal_places(float(1.2E3)) == 0
    
def test_decimal_places_str():
    assert decimal_places("1.2345E3") == 1
    assert decimal_places("1.234E3") == 0
    assert decimal_places("1.24E3") == 0
    assert decimal_places("1.234E-7") == 10
    assert decimal_places("1") == 0
    assert decimal_places("1.0") == 0
    assert decimal_places("000001.123400000") == 4
    assert decimal_places("-1.234") == 3
    assert decimal_places(".1234") == 4

def test_init_theta():
    t = TurtleNT("0.1")
    assert t.get_theta() == Decimal("0.1")
    assert t.image_width == DEFAULT_IMAGE_WIDTH
    assert t.image_height == DEFAULT_IMAGE_HEIGHT
    assert t.stepsize == 100
    assert t.image_background == "black"
    
    t = TurtleNT(theta=5, image_width=10, image_height=20, stepsize=5, image_background="white")
    assert t.get_theta() == Decimal("5")
    assert t.image_width == 10
    assert t.image_height == 20
    assert t.stepsize == 5
    assert t.image_background == "white"
    
def test_origin_return_dominant_angles():
    for theta, quotient, alpha in TURTLEFUN_QUOTIENT_LIST[:20]:
        t = TurtleNT(theta)
        assert len(t.origin_return_estimation()) >= 1
        if alpha == 180:
            assert 2 * quotient in t.origin_return_estimation()
        else:
            assert quotient in t.origin_return_estimation()
            
def test_origin_return_origin_return_samples():
    for _r in range(50):
        # testing all takes nearly a minute...
        index = random(len(TURTLE_ORIGIN_RETURN_SAMPLES))
        theta, steps = TURTLE_ORIGIN_RETURN_SAMPLES[index]
        t = TurtleNT(str(theta))
        assert steps in t.origin_return_estimation()

def test_eurler_spiral_run_simple(tmp_path):
    
    t = TurtleNT('1', path=tmp_path)
    t.euler_spiral('720')
    t.save_image()
    
    x, y = t.get_pos()
    assert round(x, 10) == 0
    assert round(y, 10) == 0
    assert t.get_angle() == 0
    assert t.is_home() is True
    assert len(t._xpos_list) == 721
    assert len(t._ypos_list) == 721
    
def test_euler_sprial_straight_line():   
    t = TurtleNT('0')
    t.euler_spiral('100000')
    assert t.get_pos() == (100000 * t.stepsize, 0)
    assert t.get_angle() == 0
    
def test_eurler_spiral_run_simple_home_return_test(tmp_path):
    
    t = TurtleNT('1', path=tmp_path)
    t.euler_spiral()
    t.save_image()
    t._calculate_min_max_positions()
    
    x, y = t.get_pos()
    assert round(x, 10) == 0
    assert round(y, 10) == 0
    assert t.get_angle() == 0
    assert t.is_home() is True
    assert len(t._xpos_list) == 721
    assert len(t._ypos_list) == 721
    
def test_euler_sprial_transparent_image(tmp_path):   
    t = TurtleNT('1', image_background=None, path=tmp_path)
    t.euler_spiral()
    t.get_image(False, False, True)
    t.save_image()
    