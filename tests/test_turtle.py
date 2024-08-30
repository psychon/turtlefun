"""tests/test_turtle.py"""

import pytest
import os

import filetype

from turtlefun.turtle import Turtle

def test_kwargs():
    t = Turtle(width=1024, height=768)
    assert t.width == 1024
    assert t.height == 768

def test_kwargs_width():
    t = Turtle(width=-1)
    assert t.width == -1

def test_kwargs_width_fail():
    with pytest.raises(ValueError):
        t = Turtle(width="seven")

def test_kwargs_height():
    t = Turtle(height=-1)
    assert t.height == -1

def test_kwargs_height_fail():
    with pytest.raises(ValueError):
        t = Turtle(height="seven")

def test_kwargs_angle():
    t = Turtle(angle=180.4)
    assert t.angle == 180.4

def test_kwargs_angle_fail():
    with pytest.raises(ValueError):
        t = Turtle(angle="seven")

def test_kwargs_scale():
    t = Turtle(scale=-2.5)
    assert t.scale == -2.5

def test_kwargs_scale_zero():
    t = Turtle(scale=0)
    assert t.scale == 0

def test_kwargs_scale_fail():
    with pytest.raises(ValueError):
        t = Turtle(scale="Seven")
    
def test_kwargs_draw_default():
    t = Turtle()
    assert t.draw == False
    
def test_kwargs_draw():
    t = Turtle(draw=True)
    assert t.draw == True

def test_forward_simple():
    t = Turtle()
    t.forward(1)
    assert t.xpos == 1
    assert t.ypos == 0

def test_rotate_simple():
    t = Turtle()
    t.rotate(90)
    assert t.angle == 90

def test_angle_cleanup():
    nums = [
        (0, 0),
        (360, 0),
        (-90, 270),
        (720, 0),
        (90, 90),
        (132, 132),
        (1.23456, 1.23456),
        (-3.786, 356.214),
        (-720, 0),
    ]
    for input, output in nums:
        t = Turtle(angle=input)
        assert t.angle == output

def test_rotmov():
    nums = [
        (0, 1, 1, 0),
        (180, 1, -1, 0),
        (90, 1, 0, 1),
        (-90, 1, 0, -1),
    ]
    for angle, step, xpos, ypos in nums:
        t = Turtle()
        t.rotmov(angle, step)
        assert abs(t.xpos - xpos) < 1e-15
        assert abs(t.ypos - ypos) < 1e-15

def test_image_initialization():
    t = Turtle(draw=True)
    assert t.image.size == (t.width, t.height)
    assert t.image.getpixel((0,0)) == t.background
    
def test_draw_line_x():
    t = Turtle(draw=True)
    for x in range(10):
        assert t.image.getpixel((x + t.xoffset, t.yoffset)) == t.background
    t.forward(10)
    for x in range(10):
        assert t.image.getpixel((x + t.xoffset, t.yoffset)) == t.linecolor
        assert t.image.getpixel((x + t.xoffset, t.yoffset + 1)) == t.background
        assert t.image.getpixel((x + t.xoffset, t.yoffset - 1)) == t.background
        assert t.image.getpixel((x + 11 + t.xoffset, t.yoffset)) == t.background
        assert t.image.getpixel((-1 * x - 1 + t.xoffset, t.yoffset)) == t.background
             
def test_draw_line_y():
    t = Turtle(draw=True)
    for y in range(10):
        assert t.image.getpixel((t.xoffset, y + t.yoffset)) == t.background
    t.rotate(90)
    t.forward(10)
    for y in range(10):
        assert t.image.getpixel((t.xoffset, y + t.yoffset)) == t.linecolor
        assert t.image.getpixel((t.xoffset + 1, y + t.yoffset)) == t.background
        assert t.image.getpixel((t.xoffset - 1, y + t.yoffset)) == t.background
        assert t.image.getpixel((t.xoffset, y + 11 + t.yoffset)) == t.background
        assert t.image.getpixel((t.xoffset, -1 * y - 1 + t.yoffset)) == t.background

def test_draw_line_x_scale():
    t = Turtle(draw=True, scale=4)
    for x in range(40):
        assert t.image.getpixel((x + t.xoffset, t.yoffset)) == t.background
    t.forward(10)
    for x in range(40):
        assert t.image.getpixel((x + t.xoffset, t.yoffset)) == t.linecolor
        assert t.image.getpixel((x + t.xoffset, t.yoffset + 1)) == t.background
        assert t.image.getpixel((x + t.xoffset, t.yoffset - 1)) == t.background
        assert t.image.getpixel((x + 41 + t.xoffset, t.yoffset)) == t.background
        assert t.image.getpixel((-1 * x - 1 + t.xoffset, t.yoffset)) == t.background

def test_xmin():
    t = Turtle()
    t.rotate(180)
    t.forward(10)
    assert t.xmin == -10
    assert t.xmax == 0
    
def test_xmax():
    t = Turtle()
    t.forward(10)
    assert t.xmax == 10
    assert t.xmin == 0
    
def test_ymin():
    t = Turtle()
    t.rotate(-90)
    t.forward(10)
    assert t.ymin == -10
    assert t.ymax == 0
    
def test_ymax():
    t = Turtle()
    t.rotate(90)
    t.forward(10)
    assert t.ymax == 10
    assert t.ymin == 0
    
def test_save_no_image(tmp_path):
    t = Turtle()
    assert not t.save(tmp_path / "test_save_no_image.png")
    
def test_save_image_png(tmp_path):
    t = Turtle(draw=True)
    filename = tmp_path / "test_save_image.png"
    assert t.save(filename)
    assert os.path.isfile(filename)
    assert filetype.guess(filename).mime == "image/png"
    
def test_save_image_jpeg(tmp_path):
    t = Turtle(draw=True)
    filename = tmp_path / "test_save_image.jpeg"
    assert t.save(filename)
    assert os.path.isfile(filename)
    assert filetype.guess(filename).mime == "image/jpeg"
    
def test_save_image_autofilename(tmp_path):
    t = Turtle(draw=True)
    assert t.save(None, tmp_path)
    assert os.path.isfile(t.create_filename(tmp_path))
    assert filetype.guess(t.create_filename(tmp_path)).mime == "image/" + t.image_extension
    
def test_save_image_manualfilename(tmp_path):
    t = Turtle(draw=True)
    filename = t.create_filename(tmp_path, "jpeg")
    assert t.save(filename)
    assert os.path.isfile(filename)
    assert filetype.guess(filename).mime == "image/jpeg"
       
def test_save_image_autofilename_spiral(tmp_path):
    t = Turtle(draw=True)
    t.euler_spiral(1, 360, 100)
    assert t.save(None, tmp_path)
    assert os.path.isfile(t.create_filename(tmp_path))
    assert filetype.guess(t.create_filename(tmp_path)).mime == "image/" + t.image_extension
    
def test_save_image_autofilename_no_path(tmp_path):
    t = Turtle(draw=True)
    assert t.save()
    assert os.path.isfile(t.create_filename())
    assert filetype.guess(t.create_filename()).mime == "image/" + t.image_extension
    os.remove(t.create_filename())
    
def test_step_num():
    t = Turtle()
    t.forward(1)
    assert t.step_num == 1
    
def test_step_num_multiple():
    t = Turtle()
    for _x in range(1234):
        t.rotmov(1, _x)
    assert t.step_num == 1234

def test_euler_spiral():
    t = Turtle()
    t.euler_spiral(1, 10000)
    assert t.step_num == 720
    
def test_euler_spiral_premature():
    t = Turtle()
    t.euler_spiral(1, 360)
    assert t.step_num == 360
    
def test_autoscale_zero():
    t = Turtle()
    assert t.autoscale() == 1
    
def test_autoscale_x():
    t = Turtle()
    t.forward(t.width / 10)
    assert t.autoscale() == 5
    
def test_autoscale_y():
    t = Turtle()
    t.rotate(90)
    t.forward(t.height / 10)
    assert t.autoscale() == 5
     
def test_autoscale_xy():
    t = Turtle()
    t.forward(t.width / 20)
    t.rotate(90)
    t.forward(t.height / 10)
    assert t.autoscale() == 5
       
def test_autoscale_yx():
    t = Turtle()
    t.forward(t.width / 10)
    t.rotate(90)
    t.forward(t.height / 20)
    assert t.autoscale() == 5
    
def test_autoscale_x_over():
    t = Turtle()
    t.forward(t.width * 10)
    assert t.autoscale() == 0.05
    
def test_autoscale_y_over():
    t = Turtle()
    t.rotate(90)
    t.forward(t.height * 10)
    assert t.autoscale() == 0.05
    
def test_autoscale_border():
    t = Turtle()
    t.forward(t.width / 10)
    assert t.autoscale(0.2) == 4
