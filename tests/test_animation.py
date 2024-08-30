"""/src/tests/test_animation.py"""

from turtlefun.turtle_animate_line import AnimateTurtle as AT

def test_measure_line_speed_diag_1():
    t = AT(theta=0.576, angle=0, stepsize=10, iterations=1000)
    t._measure_line_speed()
    assert t.image_speed[0] > 0
    assert t.image_speed[1] > 0
    
def test_measure_line_speed_diag_2():
    t = AT(theta=0.576, angle=90, stepsize=10, iterations=1000)
    t._measure_line_speed()
    assert t.image_speed[0] < 0
    assert t.image_speed[1] > 0
    
def test_measure_line_speed_diag_3():
    t = AT(theta=0.576, angle=180, stepsize=10, iterations=1000)
    t._measure_line_speed()
    assert t.image_speed[0] < 0
    assert t.image_speed[1] < 0
    
def test_measure_line_speed_diag_4():
    t = AT(theta=0.576, angle=270, stepsize=10, iterations=1000)
    t._measure_line_speed()
    assert t.image_speed[0] > 0
    assert t.image_speed[1] < 0
    
def test_measure_line_speed_horizontal_1():
    t = AT(theta=0.576, angle=-45, stepsize=10, iterations=1000)
    t._measure_line_speed()
    assert t.image_speed[0] > 0
    assert t.image_speed[1] == 0

def test_measure_line_speed_horizontal_2():
    t = AT(theta=0.576, angle=180-45, stepsize=10, iterations=1000)
    t._measure_line_speed()
    assert t.image_speed[0] < 0
    assert t.image_speed[1] == 0
    
def test_measure_line_speed_vertical_1():
    t = AT(theta=0.576, angle=45, stepsize=10, iterations=1000)
    t._measure_line_speed()
    assert t.image_speed[0] == 0
    assert t.image_speed[1] > 0
    
def test_measure_line_speed_vertical_2():
    t = AT(theta=0.576, angle=45 + 180, stepsize=10, iterations=1000)
    t._measure_line_speed()
    assert t.image_speed[0] == 0
    assert t.image_speed[1] < 0
     
def test_measure_line_speed_no_line():
    t = AT(theta=1, angle=0, stepsize=10, iterations=1000)
    t._measure_line_speed()
    assert t.image_speed[0] == 0
    assert t.image_speed[1] == 0
    
def test_init_blank_at():
    t = AT()
    
def test_init_precsision():
    t = AT(precision=1)
    assert t.precision == 1
    
def test_init_theta():
    t = AT(theta=10)
    assert t.theta == 10
    
def test_init_angle():
    t = AT(angle=32)
    assert t.angle == 32
    
def test_init_stepsize():
    t = AT(stepsize=30)
    assert t.stepsize == 30
    
def test_init_framerate():
    t = AT(framerate=10)
    assert t.framerate == 10
    
def test_inti_duration():
    t = AT(duration=123)
    assert t.duration == 123
    
def test_init_detect_origin_return():
    t = AT(detect_origin_return=False)
    assert not t.detect_origin_return
    
def test_init_width():
    t = AT(width=5)
    assert t.width == 5
    
def test_inti_height():
    t = AT(height=5)
    assert t.height == 5
    
def test_init_iterations():
    t = AT(iterations=10)
    assert t.iterations == 10
    
def test_inti_scale():
    t = AT(scale=7)
    assert t.scale == 7
    
def test_init_autoscale():
    t = AT(autoscale=False)
    assert t.autoscale == False
    
def test_init_border():
    t = AT(border=0.5)
    assert t.border == 0.5
    
def test_init_xoffset():
    t = AT(xoffset=5)
    assert t.xoffset == 5
    
def test_init_yoffset():
    t = AT(yoffset = 5)
    assert t.yoffset == 5
    
def test_origin_return():
    t = AT(theta=1, detect_origin_return=True)
    t._detect_origin_return()
    assert t.iterations == 720
    
def test_no_origin_return():
    t = AT(theta=1, detect_origin_return=False)
    t._detect_origin_return()
    assert t.iterations == 1000000
    
def test_origin_return_no_origin():
    t = AT(theta=1, detect_origin_return=True, iterations=100)
    t._detect_origin_return()
    assert t.iterations == 100
    
def test_autoscale_no_image_speed():
    t = AT(theta=1, autoscale=True, iterations=1000)
    t._autoscale()
    assert t.image_speed == (0,0)
    assert t.scale > 10