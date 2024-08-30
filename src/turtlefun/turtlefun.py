"""src/turtlefun/turtlefun.py"""

from decimal import Decimal, getcontext
import decimal
import itertools
import math
import statistics
import os
from sympy import nextprime
from time import perf_counter
from typing import Union, List, Type

import click
import colorcet as cc
from loguru import logger
from prettytable import PrettyTable
from PIL.Image import Resampling
from PIL import Image, ImageDraw, ImageFont, ImageOps

from . import __version__
from .turtle import Turtle
from .turtle_explorer import explore_euler_spiral
from .turtle_animate_line import AnimateTurtle
from .turtle_slideshow import TurtleSlideshow
from .turtle_codewindow import TurtleCodeWindow
from .qualityldraw import QualityDraw
from . import samplevalues
from . import turtlefun_lines_manual
from . import turtle_originreturnsamples
from . import turtlefun_quotientlist
from .turtlent import TurtleNT
from .turtlent_noreturn_exploration import explore_euler_spiral_no_return
from .turtlefun_quotientlist_generation import create_quotient_list


def _run_speedtest(theta:Union[int, float], iterate:List[int]) -> Type[PrettyTable]:
    """Run speedtest on euler spiral generation
    
    Args:
        theta (int, float): Angle to use for speedtest
        iterate ([int]): Number of iterations to use
        
    Returns:
        Prettytable with results
    """
    result = PrettyTable(['Turtle', 'Theta', 'iterate', 'steps', 'draw', 'time', 'delta time'])
    last = 0
    for iteration in iterate:
        for draw in [False, True]:
            logger.debug("Running with {} iterations and drawing = {}", iteration, draw)
            t = Turtle(draw=draw)
            timer_start = perf_counter()
            t.euler_spiral(theta, iteration)
            timer_end = perf_counter()
            result.add_row([
                "Turtle",
                theta,
                iteration,
                t.step_num,
                draw,
                (timer_end - timer_start),
                (timer_end - timer_start) - last,
            ])
            last = (timer_end - timer_start)
            
    last = 0
    for iteration in iterate:
        for draw in [False, True]:
            logger.debug("Running with {} iterations and drawing = {}", iteration, draw)
            t = TurtleNT(theta)
            timer_start = perf_counter()
            t.euler_spiral(iteration)
            if draw:
                t.get_image()
            timer_end = perf_counter()
            result.add_row([
                "TurtleNT",
                theta,
                iteration,
                t.get_steps(),
                draw,
                (timer_end - timer_start),
                (timer_end - timer_start) - last,
            ])
            last = (timer_end - timer_start)
    return result

def _get_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dy = y2 - y1
    dx = x2 - x1
    return math.degrees(math.atan2(-dy, dx))

def is_line(theta:float, limit:int=1000000) -> Union[bool, None]:
    """Check if theta forms a line"""
    circle = 1
    while not round(360 * circle / theta, 10).is_integer():
        circle += 1
        if circle > limit:
            return None
    
    if round(circle / theta, 12) % 2 == 0:
        logger.success("theta={} is not a line, it takes {} circles for the angle to return to 0.", theta, circle)
        return False
    else:
        logger.success("theta={} is a line, it takes {} circles for the angle to return to 0.", theta, circle)
        return True

def get_primes(number:Union[int, float, str, Decimal]) -> List[Decimal]:
    """Generate primes for a given number"""
    primes = []
    prime = 1
    number = Decimal(str(number))
    if round(number, 0) != number:
        logger.critical("Primes can only be calculated for whole numbers.")
        raise ValueError("Whole number requires.")
    while True:
        prime = nextprime(prime)
        while round(number / Decimal(str(prime)), 0) == number / Decimal(str(prime)):
            number /= Decimal(str(prime))
            primes.append(Decimal(str(prime)))
        
        if number == 1:
            break
        if prime > number:
            logger.critical("Failed to calculate prime factors!")
            raise ValueError("Failed to calculate primes.")
    return primes

@click.group()
@click.version_option(version=__version__)
def turtlefun() -> None:
    """Let's have fun with turtle graphics"""
    
    
@turtlefun.command()
@click.argument("item", nargs=1, type=int)
@click.argument("theta", default=None, nargs=1, type=float, required=False)
def default(item:int, theta:float) -> None:
    """Create a predefined item
    
    \b
     num   theta   description
       1   0.576   animated line video, 120s
       2   0.064   animated line video, 120s
       3   0.128   animated line video, 120s
       4   0.256   animated line video, 120s
       5   multi.  generate speed corrected slim line animations
       6   multi.  generate picture frame animations
       7   1       base element animation with white and colored lines
       8   1       zoom on one of the circles
       9   multi   read input from origin_return textfile for animations
      10   multi   create origin return images
      11   1       create special angle hold point videos with colored geometric forms
      12   multi.  slideshow with calculated theta of base elements
      14   multi.  selected animations with circular color palette applied
      16   multi.  Determine line angle automatically
      17   multi.  line analysis for bug fixing animations; script could not handle less than 1 line per frame at time of writing.
      18   multi.  origin return animations
      19   multi.  Animate colored curves with antialiasing and manual option for iterations
      20   single  create high resolution T-Shirt print quality color graphics
      21   single  Frame animation with frame size tweaking parameters
      26   1,359   mirror animation
      27   120,240 flip animation
      28   multi.  create line images
      32   multi.  Calculate upper and lower bound for number of steps to complete image and compare with known examples
    """
    width = 2560
    height = 1440
    framerate = 50
    path = "/backup/turtlefunanimations"
    line_angles = {
        
    }
    
    if item == 1:
        theta = 0.576
        animationtype = "linewalk"
        name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + animationtype
        t = AnimateTurtle(
            angle = -45,
            duration = 120,
            iterations = 80000,
            stepsize = 20,
            linewidth = 5,
            
            xoffset = int(round(width * 0.8, 0)),
            yoffset = int(round(height / 2, 0)),
            
            autoscale = False,
            detect_origin_return = False,
            
            name = name,
            theta = theta,
            framerate = framerate,
            width = width,
            height = height,
            path = path,
        )
        t.animate()
    elif item == 2:
        theta = 0.064
        animationtype = "linewalk"
        name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + animationtype
        t = AnimateTurtle(
            angle = -45,
            duration = 120,
            iterations = 80000,
            stepsize = 15,
            linewidth = 5,
            
            xoffset = int(round(width * 0.7, 0)),
            yoffset = int(round(height / 2, 0)),
            
            autoscale = False,
            detect_origin_return = False,
            
            name = name,
            theta = theta,
            framerate = framerate,
            width = width,
            height = height,
            path = path,
        )
        t.animate()
    elif item == 3:
        theta = 0.128
        animationtype = "linewalk"
        name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + animationtype
        t = AnimateTurtle(
            angle = -90,
            duration = 120,
            iterations = 100000,
            stepsize = 15,
            linewidth = 5,
            
            xoffset = int(round(width * 0.8, 0)),
            yoffset = int(round(height / 2, 0)),
            
            autoscale = False,
            detect_origin_return = False,
            
            name = name,
            theta = theta,
            framerate = framerate,
            width = width,
            height = height,
            path = path,
        )
        t.animate()
    elif item == 4:
        theta = 0.256
        animationtype = "linewalk"
        name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + animationtype
        t = AnimateTurtle(
            angle = 180,
            duration = 120,
            iterations = 100000,
            stepsize = 15,
            linewidth = 5,
            
            image_speed = (0.254477163483436, 0),
            xoffset = int(round(width * 0.85, 0)),
            yoffset = int(round(height / 2, 0)),
            
            autoscale = False,
            detect_origin_return = False,
            
            name = name,
            theta = theta,
            framerate = framerate,
            width = width,
            height = height,
            path = path,
        )
        t.animate()
    elif item == 5:
        """Create line animations with autodetection of animation parameters (angle, speed, xoffset)"""
        height = 200
        linewidth = 6
        duration = 60
        xmax_border = 0.05

        for theta in reversed([
            0.064,
            0.128,
            0.192,
            0.256,
            0.32,
            0.384,
            0.512,
            0.576,
            0.064,
            0.704,
            0.768,
            0.832,
            0.896,
            1.024,
            1.6,
            4.8,
            8.0,
            14.4,
            24.0,
            40.0,
            72.0,
            120.0,
            ]):

            logger.debug("Creating slim line animation for theta={}", theta)

            animationtype = "slimline"
            name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + animationtype
            
            angle = 0
            iterations = 200000
            image_height = 0
            stepsize = 10 * theta
            n = 0
            while (image_height < height - 2 * linewidth or image_height > height) and n < 5:
                
                # determine the start angle
                t = Turtle(draw=False, angle=angle)
                t.euler_spiral(theta, iterations, stepsize)
                
                angles = []
                for i in range(int(round(360 / theta * 2, 0))):
                    t.rotmov(theta * t.step_num, stepsize)
                    pos = t.get_pos()
                    a = _get_angle((0, 0), pos)
                    logger.trace("Position {}, angle is {}", pos, a)
                    angles.append(a)
                    
                angle += statistics.fmean(angles)
                logger.success("For theta={} the average angle is {}", theta, angle)
                
                t = Turtle(angle=angle)
                t.euler_spiral(theta, iterations, stepsize)
                
                image_height = (t.ymax - t.ymin)
                stepsize = round(stepsize * (height - linewidth) / image_height, 10)
                logger.debug("Testheight was {}, new stepsize is {}", image_height, stepsize)
            
                t = Turtle(angle=angle)
                t.euler_spiral(theta, iterations, stepsize)
                
                time_to_fill_screen = 5
                image_speed_pixel_per_frame = int(round(width / (time_to_fill_screen * framerate), 0))
                image_speed_pixel_per_iteration = t.xmax / iterations
                iterations_per_frame = image_speed_pixel_per_frame / image_speed_pixel_per_iteration
                
                iterations = int(round((duration * framerate) * iterations_per_frame, 0))
                logger.debug("Testiterations is now {}", iterations)
                n += 1
            
            t = Turtle(angle=angle)
            t.euler_spiral(theta, iterations, stepsize)
            logger.success("Final height: {} with ymin={} and ymax={}, target height is {}", (t.ymax-t.ymin), t.ymin, t.ymax, height)
            logger.success("Final length: {}", t.xmax - t.xmin)
            logger.success("Final iterations: {}", iterations)
            
            yoffset = int(round(height / 2, 0))
            logger.debug("Yoffset for center of animation: {}", yoffset)
            yoffset_correction = t.ymax - (t.ymax - t.ymin) / 2
            yoffset -= yoffset_correction
            yoffset = int(round(yoffset, 0))
            logger.success("Yoffset of {} after correction of {}", yoffset, yoffset_correction)
            
            logger.debug("Determining x offset")
            xoffset = int(round(width / 2, 0))
            t = AnimateTurtle(
                draw = False,
                angle = angle,
                duration = duration,
                iterations = iterations,
                stepsize = stepsize,
                linewidth = linewidth,
                
                image_speed = (image_speed_pixel_per_iteration, 0),
                xoffset = xoffset,
                yoffset = yoffset,
                text = "θ" + " = " + str(theta),
                
                autoscale = False,
                detect_origin_return = False,
                
                name = name,
                theta = theta,
                framerate = framerate,
                width = width,
                height = height,
                path = path,
            )
            t.animate()
            
            x_target = width * (1 - xmax_border)
            delta_target = t.es_turtle.image_xmax - x_target
            xoffset = int(round(xoffset - delta_target,0 ))
            
            logger.success("New xoffset found: {}", xoffset)
            
            t = AnimateTurtle(
                angle = angle,
                duration = duration,
                iterations = iterations,
                stepsize = stepsize,
                linewidth = linewidth,
                
                image_speed = (image_speed_pixel_per_iteration, 0),
                xoffset = xoffset,
                yoffset = yoffset,
                text = "θ" + " = " + str(theta),
                
                autoscale = False,
                detect_origin_return = False,
                
                name = name,
                theta = theta,
                framerate = framerate,
                width = width,
                height = height,
                path = path,
            )
            t.animate()
    elif item == 6:
        linewidth = 5
        duration = 5
        es_line_width = 120
        frame_corners = [
            (2320, 1320),
            (240, 1320),
            (120, 1200),
            (120, 240),
            (240, 120),
            (2320, 120),
            (2440, 240),
            (2440, 1200),
            (2320, 1320),
        ]
        distance = 0
        angle_list = []
        distance_list = []
        for i in range(len(frame_corners) - 1):
            d= math.dist(frame_corners[i], frame_corners[i+1])
            distance += d
            distance_list.append(d)
            angle_list.append(_get_angle(frame_corners[i], frame_corners[i+1]))
            
        logger.debug("Total distance for line is {}", distance)
        logger.debug("Distances between points: {}", distance_list)
        logger.debug("Angles between points: {}", angle_list)

        for theta, angle, extra_iterations in [(0.064, -45, 0), (0.128, -90, -4), (0.256, 180, -5), (0.512, 0, -5), (0.704, -135, 6), (0.768, -90, -4), (0.832, 135, 0), (0.896, 90, -1), (1.024, 0, 0)]:
            
            logger.debug("Creating frame animation for theta={}, angle={}", theta, angle)
            try:
                iterations = 200000
                line_height = 0
                stepsize = 10
                n = 0
                while n < 10:
                    t = Turtle(angle=angle)
                    t.euler_spiral(theta, iterations, stepsize)
                    
                    line_height = (t.ymax - t.ymin)
                    stepsize = round(stepsize * es_line_width / line_height, 10)
                    logger.debug("Testheight was {}, new stepsize is {}", line_height, stepsize)
                
                    t = Turtle(angle=angle)
                    t.euler_spiral(theta, iterations, stepsize)
                    
                    image_speed_pixel_per_iteration = (t.xmax - t.xmin) / iterations
                    
                    iterations = int(round(distance / image_speed_pixel_per_iteration, 0))
                    logger.debug("Testiterations is now {}", iterations)
                    n += 1
                
                iterations_per_frame = iterations / (duration * framerate)
                iterations += int(round(iterations_per_frame * extra_iterations,0))
                
                t = Turtle(angle=angle)
                t.euler_spiral(theta, iterations, stepsize)
                logger.success("Final height: {} with ymin={} and ymax={}", (t.ymax-t.ymin), t.ymin, t.ymax)
                logger.success("Final length: {} with {} iterations", t.xmax - t.xmin, iterations)
                logger.success("Target distance: {}", distance)
                logger.success("Number of frames: {}", duration * framerate)
                
                pixel_per_iteration = (t.xmax - t.xmin) / iterations
                iterations_per_frame = iterations / (duration * framerate)
                pixel_per_frame = pixel_per_iteration * iterations_per_frame
                logger.success("Pixel per frame: {}", pixel_per_frame)
                
                extra_turns = {}
                turtangle = 0
                next_turn_frame = 0
                for i in range(len(frame_corners) - 1):
                    turn = (360 - ((angle_list[i] % 360) - turtangle)) % 360
                    turtangle = (turtangle - turn) % 360
                    extra_turns[next_turn_frame] = turn
                    logger.debug("Turn {} degree in frame {}, turtleangle at {}", turn, next_turn_frame, turtangle)
                    next_turn_frame += int(round(distance_list[i] / pixel_per_frame, 0))
                
                animationtype = "es-picture-frame"
                name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + animationtype
                t = AnimateTurtle(
                    angle = angle,
                    duration = duration,
                    iterations = iterations,
                    stepsize = stepsize,
                    linewidth = linewidth,
                    extra_turns = extra_turns,
                    
                    image_speed = (0, 0),
                    xoffset = int(round(frame_corners[0][0], 0)),
                    yoffset = int(round(frame_corners[0][1], 0)),
                    
                    autoscale = False,
                    detect_origin_return = False,
                    
                    name = name,
                    theta = theta,
                    framerate = framerate,
                    width = width,
                    height = height,
                    path = path,
                )
                t.animate()
            except Exception:
                logger.exception("Failed to create picture frame")
    elif item == 7:
        for line_color in [True, False]:
            for show_turtle in [True, False]:
                theta = 1
                animationtype = "baseelement"
                name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + str("color" if line_color else "white") + "_" + str("turtle" if show_turtle else "no-turtle") + "_" + animationtype
                t = AnimateTurtle(
                    angle = 0,
                    duration = 14.4,
                    iterations = 720,
                    stepsize = 10,
                    linewidth = 5,
                    show_turtle = show_turtle,
                    border = 0.1,
                    hold_after = 2,
                    
                    palette_lines = line_color,
                    
                    xoffset = int(round(width / 2, 0)),
                    yoffset = int(round(height / 2, 0)),
                    
                    autoscale = True,
                    detect_origin_return = False,
                    image_speed = (0,0),
                    
                    name = name,
                    theta = theta,
                    framerate = framerate,
                    width = width,
                    height = height,
                    path = path,
                )
                t.animate()
    elif item == 8:
        for line_color in [True, False]:
            theta = 1
            animationtype = "baseelement"
            name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + str(line_color) + "_" + animationtype
            t = AnimateTurtle(
                angle = 0,
                duration = 14.4,
                iterations = 720,
                stepsize = 300,
                linewidth = 5,
                show_turtle = True,
                border = 0.1,
                
                palette_lines = line_color,
                
                xoffset = int(round(-width/3, 0)),
                yoffset = int(round(-height, 0)),
                
                autoscale = False,
                detect_origin_return = False,
                image_speed = (0,0),
                
                name = name,
                theta = theta,
                framerate = framerate,
                width = width,
                height = height,
                path = path,
            )
            t.animate()
    elif item == 9:
        # ls | grep _origin-return.ini | grep -v _1.0000_ | cut -d "_" -f 2 | sort -n | uniq | sed 's/^00//' | sed 's/0*$//' | sed 's/\.$/.0/'
        # find | grep _origin-return.ini | grep -v _1.0000_ | cut -d "_" -f 2 | sort -n | uniq | sed 's/^00*/0/' | sed 's/0*$//' | sed 's/\.$/.0/' | sed 's/$/, /' > ../or.list
        origin_returns = []
        numlen = 0
        with open("./origin_returns.txt", "r") as fp:
            for line in fp:
                try:
                    numlen = max(numlen, len(line.strip().split(".")[1]))
                    origin_returns.append(float(line.strip()))
                except:
                    pass
        logger.debug("Successfully imported {} float values.", len(origin_returns))
        
        for theta in origin_returns:
            try:
                logger.debug("Running with theta={}", theta)
                animationtype = "origin-return"
                name = "tfa_" + "{:03d}".format(item) + "_" + ("{:0." + str(numlen) + "f}").format(theta).replace(".", "-") + "_" + animationtype
                t = AnimateTurtle(
                    angle = 0,
                    duration = 6,
                    iterations = 1000000,
                    stepsize = 10,
                    linewidth = 3,
                    show_turtle = False,
                    border = 0.02,
                    hold_after = 1,
                    
                    palette_lines = False,
                    
                    xoffset = int(round(width / 2, 0)),
                    yoffset = int(round(height / 2, 0)),
                    
                    autoscale = True,
                    detect_origin_return = True,
                    image_speed = (0,0),
                    
                    name = name,
                    theta = theta,
                    framerate = framerate,
                    width = width,
                    height = height,
                    path = path,
                )
                t.animate()
            except:
                logger.exception("Failed while creating theta={}", theta)
    elif item == 10:
        # lets create bigger images to downscale for anti aliasing reasons.
        width = width * 2
        height = height * 2
        
        path = os.path.join(path, "stillimages/raw")
        os.makedirs(path, exist_ok=True)
        
        origin_returns = []
        numlen = 0
        with open("./origin_returns.txt", "r") as fp:
            for line in fp:
                try:
                    numlen = max(numlen, len(line.strip().split(".")[1]))
                    origin_returns.append(float(line.strip()))
                except:
                    pass
        logger.debug("Successfully imported {} float values.", len(origin_returns))
        
        for theta in origin_returns:
            t = Turtle(draw=False, width=width, height=height)
            t.euler_spiral(theta, 1000000, 20)
            scale = t.autoscale(0.05)
            
            t = Turtle(draw=True, width=width, height=height, scale=scale)
            t.linewidth = 8
            t.euler_spiral(theta, 1000000, 20)
            t.save(None, path)        
    elif item == 11:
        for special_angles in [([179], 'magenta'), ([42,43,44,45,46,47,48,49], 'orange'), ([58, 59, 60, 61, 62, 63], 'blue'), ([89, 90, 91, 92], 'red'), ([119, 120, 121], 'yellow'), ([180], 'green')]:
            theta = 1
            animationtype = "special-angles"
            name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + str("-".join(str(x) for x in special_angles[0])) + "_" + animationtype
            t = AnimateTurtle(
                angle = 0,
                duration = (max(special_angles[0]) + 1) / framerate,
                iterations = max(special_angles[0]) + 1,
                stepsize = 300,
                linewidth = 5,
                show_turtle = True,
                border = 0.1,
                
                palette_lines = False,
                special_angles = special_angles[0],
                special_angle_color = special_angles[1],
                special_angle_linewidth = 20,
                
                xoffset = int(round(-width/3, 0)),
                yoffset = int(round(-height, 0)),
                
                autoscale = False,
                detect_origin_return = False,
                image_speed = (0,0),
                
                name = name,
                theta = theta,
                framerate = framerate,
                width = width,
                height = height,
                path = path,
            )
            t.animate()
    elif item == 12:
        origin_returns = []
        numlen = 0
        # with open("./origin_returns_base_elements.txt", "r") as fp:
        with open("./base_elements_generated.txt", "r") as fp:
            for line in fp:
                try:
                    numlen = max(numlen, len(line.strip().split(".")[1]))
                    origin_returns.append(float(line.strip()))
                except:
                    pass
        logger.debug("Successfully imported {} float values.", len(origin_returns))
        
        images_per_second = 3.1
        frames_per_image = int(round(framerate / images_per_second, 0))
        extension = "png"
        xshift = 500
        
        name = "slideshow"
        path = os.path.join(path, name)
        os.makedirs(path, exist_ok=True)
        
        slideshow = TurtleSlideshow(width, height)
        
        frame = 0
        for theta in origin_returns:
            logger.success("Starting generation of theta={}", theta)
            iterations = int(round(360 / theta * 2, 0) + 1)
            t = Turtle(draw=False, width=(width - xshift) * 4, height=height * 4)
            t.euler_spiral(theta, iterations, 20)
            scale = t.autoscale(0.05)
            
            t = Turtle(draw=True, width=(width - xshift) * 4, height=height * 4, scale=scale)
            t.linewidth = 6
            t.euler_spiral(theta, iterations, 20)
            
            slideshow.replace_background(t.image.resize((width - xshift, height), Resampling.LANCZOS), (xshift, 0))
            slideshow.add_text("θ" + " = " + str(theta))
            
            for _f in range(frames_per_image):
                slideshow.next().save(os.path.join(path, "{:012d}".format(frame)) + "." + extension)
                frame += 1
                
        logger.debug("Creating shell file to run ffmpeg")
        with open(os.path.join(path, "animate.sh"), "w") as file:
            file.write('#! /usr/bin/bash' + "\n" + \
                    'mv $(ls *.png | tail -n 1) ../' + name + '.png' + "\n" + \
                    '/usr/bin/ffmpeg -n -pattern_type glob -loglevel error -framerate ' + str(int(framerate)) + ' -i "*.' + extension + '" -c:v libx264 -pix_fmt yuv420p ' + name + '.mp4 && rm *.png && rm *.sh && mv * ..')
    elif item == 13:
        click.echo("find multiples of 360")
        inc = 0.0001
        for i in range(int(360 / inc - 1)):
            a = 360 / ((i + 1) * inc)
            if round(a, 0) == round(a, 15):
                click.echo(str(round((i + 1) * inc, 6)))
    elif item == 14:
        # [1.2258, 0.4914, 0.5796, 1.131, 1.2016, 1.3266, 1.5282, 1.6308]:
        # [28.3, -43.6, 66.9, 74.2, 178.032, 178.06, 179.15]:
        # [0.0567, 0.651, 1.7833]:
        for theta in [1.7883]:
            try:
                logger.debug("Running with theta={}", theta)
                animationtype = "thebeautiful_8_5s"
                name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.5f}".format(theta).replace(".", "-") + "_" + animationtype
                
                t = Turtle(draw=False, width=width, height=height)
                t.precision_angle = 1
                t.precision_pos = 0.4
                stepsize = 10
                t.euler_spiral(theta, 10000000, stepsize)
                
                if not t.last_origin:
                    logger.critical("No origin return detected!")
                    continue
                
                iterations = t.step_num
                stepsize = stepsize * t.autoscale()
                
                duration = 7
                hold_after = 1.5
                
                palette = cc.b_cyclic_mygbm_30_95_c78
                
                #
                t = AnimateTurtle(
                    angle = 0,
                    duration = duration,
                    iterations = iterations,
                    stepsize = 10,
                    linewidth = 3,
                    show_turtle = False,
                    border = 0.02,
                    hold_after = hold_after,
                    
                    color_palette = palette,
                    palette_lines = True,
                    steps_per_color = int(iterations/(len(palette)*2)),
                    
                    turtle_code_window = TurtleCodeWindow(width, height, 1890, 50, duration + hold_after - 3, framerate, iterations, theta, int(round(stepsize, 0)), True),
                    
                    xoffset = int(round(width / 2, 0)),
                    yoffset = int(round(height / 2, 0)),
                    
                    autoscale = True,
                    detect_origin_return = False,
                    image_speed = (0,0),
                    
                    name = name,
                    theta = theta,
                    framerate = framerate,
                    width = width,
                    height = height,
                    path = path,
                )
                t.animate()
            except:
                logger.exception("Failed while creating theta={}", theta)
    elif item == 15:
        
        name = "codewindowtest"
        path = os.path.join(path, name)
        os.makedirs(path, exist_ok=True)
        
        cw = TurtleCodeWindow(width, height, 1890, 50, 10, 50, 999999, 0.9999, 1234)
        for i in range(500):
            image = Image.new("RGB", (width, height), color=(0,0,0))
            
            image.paste(cw.next(),(0,0),cw.image)
            image.save(os.path.join(path, "{:012d}".format(i) + ".png"))
            
        logger.debug("Creating shell file to run ffmpeg")
        with open(os.path.join(path, "animate.sh"), "w") as file:
            file.write('#! /usr/bin/bash' + "\n" + \
                    'mv $(ls *.png | tail -n 1) ../' + name + '.png' + "\n" + \
                    '/usr/bin/ffmpeg -n -pattern_type glob -loglevel error -framerate ' + str(int(framerate)) + ' -i "*.png' + '" -c:v libx264 -pix_fmt yuv420p ' + name + '.mp4 && rm *.png && rm *.sh && mv * ..')   
    elif item == 16:
        
        logger.debug("Determining the angles of lines")
        # For theta=14.4 the average angle is -43.20189037101483 @ 5000000

        for theta in [14.4]:
            
            iterations = 10000000
            stepsize = 10
            t = Turtle(draw=False)
            t.euler_spiral(theta, iterations, stepsize)
            
            angles = []
            for i in range(10000):
                t.rotmov(theta * t.step_num, stepsize)
                pos = t.get_pos()
                a = _get_angle((0, 0), pos)
                logger.trace("Position {}, angle is {}", pos, a)
                angles.append(a)
                
            logger.success("For theta={} the average angle is {}", theta, statistics.fmean(angles))
    elif item == 17:
        height = 480
        width = 10 * width
        # (8.0, 0.7),
        # (14.4, 0.7),
        # (24.0, 0.7),
        # (40.0, 0.7),
        # (72.0, 0.5),
        # (120.0, 0.5)
        for theta in [8.0, 14.4, 24.0, 40.0, 72.0, 120.0]:
            
            animationtype = "mystery-lines"
            name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + animationtype
            t = Turtle(angle=-45, draw=True, width=width, height=height)
            t.linewidth = 5
            t.euler_spiral(theta, 200000, 10 * theta)
            t.save(name + ".png", path)
    elif item == 18:
        # for iter in $(ls | grep .png | grep origin-return | grep -v _1.0000_ | cut -d "_" -f 4 | sort -n | uniq); do ls *_"$iter"_*.png; done | grep -v _1.0000_ | tail -n 50 | cut -d "_" -f 2 | sed 's/^0*//' | sed 's/0*$//' | sed 's/\.$/.0/' | sed 's/^\./0./' > ~/git/turtlefun/most_iterations_top_50.txt
        
        origin_returns = []
        numlen = 0
        with open("./most_iterations_top_50.txt", "r") as fp:
            for line in fp:
                try:
                    numlen = max(numlen, len(line.strip().split(".")[1]))
                    origin_returns.append(float(line.strip()))
                except:
                    pass
        logger.debug("Successfully imported {} float values.", len(origin_returns))
        
        for theta in origin_returns:
            try:
                logger.debug("Running with theta={}", theta)
                
                t = Turtle(draw=False, width=width, height=height)
                stepsize = 10
                t.euler_spiral(theta, 10000000, stepsize)
                iterations = t.step_num
                stepsize = stepsize * t.autoscale()
                
                duration = 12
                hold_after = 3
                
                animationtype = "most-iterations"
                name = "tfa_" + "{:03d}".format(item) + "_" + "{:06d}".format(iterations) + "_" + "{:0.5f}".format(theta).replace(".", "-") + "_" + animationtype
                
                palette = cc.b_cyclic_mygbm_30_95_c78
                
                t = AnimateTurtle(
                    angle = 0,
                    duration = duration,
                    iterations = iterations,
                    stepsize = 10,
                    linewidth = 3,
                    show_turtle = False,
                    border = 0.02,
                    hold_after = hold_after,
                    
                    color_palette = palette,
                    palette_lines = True,
                    steps_per_color = int(iterations/(len(palette)*2)),
                    
                    turtle_code_window = TurtleCodeWindow(width, height, 1890, 50, duration + hold_after - 2, framerate, iterations, theta, int(round(stepsize, 0))),
                    
                    xoffset = int(round(width / 2, 0)),
                    yoffset = int(round(height / 2, 0)),
                    
                    autoscale = True,
                    detect_origin_return = False,
                    image_speed = (0,0),
                    
                    name = name,
                    theta = theta,
                    framerate = framerate,
                    width = width,
                    height = height,
                    path = path,
                )
                t.animate()
            except:
                logger.exception("Failed while creating theta={}", theta)
    elif item == 19:
        """Animate beautiful curves with static code window to make short animation times possible"""
        """Added antialiasing using quality_factor that upscales the image for drawing."""
        # [0.0567, 0.651, 1.7883]:
        # [0.5796]:
        palette = cc.b_cyclic_mygbm_30_95_c78
        
        palette = []
        for color in cc.b_cyclic_mygbm_30_95_c78:
            palette.append(color)
        palette.reverse()
        
        for theta, total_iterations in [(179.6063, 7199845)]:
            try:
                initial_iterations = 10000000
                logger.debug("Running with theta={}", theta)
                if total_iterations is not None:
                    logger.debug("Using fixed number of iterations! {}", total_iterations)
                    initial_iterations = total_iterations
                
                
                animationtype = "the-base-base-base"
                name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.5f}".format(theta).replace(".", "-") + "_" + animationtype
                
                t = Turtle(draw=False, width=width, height=height)
                stepsize = 10
                t.euler_spiral(theta, initial_iterations, stepsize)
                
                if t.last_origin:
                    iterations = t.step_num
                elif total_iterations is not None:
                    iterations = total_iterations
                else:
                    logger.critical("No origin return and no iteration number provided for theta={}!", theta)
                    continue
                    
                stepsize = stepsize * t.autoscale()
                
                hold_before = 0
                duration = 8
                hold_after = 2
                
                
                
                t = AnimateTurtle(
                    angle = 0,
                    duration = duration,
                    iterations = iterations,
                    stepsize = 10,
                    linewidth = 3,
                    show_turtle = False,
                    border = 0.02,
                    hold_before = hold_before,
                    hold_after = hold_after,
                    quality_factor = 4,
                    
                    color_palette = palette,
                    palette_lines = True,
                    steps_per_color = int(iterations/(len(palette)*2)),
                    reverse = False,
                    
                    xoffset = int(round(width / 2, 0)),
                    yoffset = int(round(height / 2, 0)),
                    
                    autoscale = True,
                    detect_origin_return = False,
                    image_speed = (0,0),
                    
                    name = name,
                    theta = theta,
                    framerate = framerate,
                    width = width,
                    height = height,
                    path = path,
                )
                t.animate()
                
            except:
                logger.exception("Failed while creating theta={}", theta)
    elif item == 20:
        """Create High Quality single image render of return to origin theta value with colormap"""
        animationtype = "HQ-still-images"
        # theta, angle, total_iterations = (179.168, -20.0, None)
        # theta, angle, total_iterations = (89.5033, 22.5, 7199980)
        # theta, angle, total_iterations = (89.507, 22.5, 710058)
        # theta, angle, total_iterations = (89.5095, -70, 159995)
        # theta, angle, total_iterations = (89.61, 45, 35991)
        # theta, angle, total_iterations = (89.616, -22.5, 14991)
        theta, angle, total_iterations = (119.9, 0, None)
        
        width = 4000
        height = 4000
        linewidth = 10       
        quality_factor = 4
        width *= quality_factor
        height *= quality_factor
        linewidth *= quality_factor
        
        path = os.path.join(path, animationtype)
        path = os.path.join(path, str(theta))
        
        for _p in ["transparent", "white", "black"]:
            os.makedirs(os.path.join(path, _p), exist_ok=True)
            
        logger.success("Running with theta={}", theta)
        
        stepsize = 10
        if total_iterations is None:
            t = Turtle(draw=False, width=width, height=height, angle=angle)
            t.euler_spiral(theta, 10000000, stepsize)
            if t.last_origin:
                iterations = t.step_num
            else:
                logger.critical("No origin return detected!")
                exit(1)
        else:
            iterations = total_iterations
        
        duration = 5 # As we do not draw, this does not matter at all, we only draw the final image
        for base_pallette, palette_name in [
            (["#000000", "#000000", "#000000", "#000000"], "black"),
            (["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"], "white"),
            (cc.b_cyclic_bgrmb_35_70_c75, "cyclic_bgrmb_35_70_c75"),
            (cc.b_cyclic_bgrmb_35_70_c75_s25, "cyclic_bgrmb_35_70_c75_s25"),
            (cc.b_cyclic_grey_15_85_c0, "cyclic_grey_15_85_c0"),
            (cc.b_cyclic_grey_15_85_c0_s25, "cyclic_grey_15_85_c0_s25"),
            (cc.b_cyclic_mrybm_35_75_c68, "cyclic_mrybm_35_75_c68"),
            (cc.b_cyclic_mrybm_35_75_c68_s25, "cyclic_mrybm_35_75_c68_s25"),
            (cc.b_cyclic_mybm_20_100_c48, "cyclic_mybm_20_100_c48"),
            (cc.b_cyclic_mybm_20_100_c48_s25, "cyclic_mybm_20_100_c48_s25"),
            (cc.b_cyclic_mygbm_30_95_c78, "cyclic_mygbm_30_95_c78"),
            (cc.b_cyclic_mygbm_30_95_c78_s25, "cyclic_mygbm_30_95_c78_s25"),
            (cc.b_cyclic_mygbm_50_90_c46, "cyclic_mygbm_50_90_c46"),
            (cc.b_cyclic_mygbm_50_90_c46_s25, "cyclic_mygbm_50_90_c46_s25"),
            (cc.b_cyclic_protanopic_deuteranopic_bwyk_16_96_c31, "cyclic_protanopic_deuteranopic_bwyk_16_96_c31"),
            (cc.b_cyclic_protanopic_deuteranopic_wywb_55_96_c33, "cyclic_protanopic_deuteranopic_wywb_55_96_c33"),
            (cc.b_cyclic_rygcbmr_50_90_c64, "cyclic_rygcbmr_50_90_c64"),
            (cc.b_cyclic_rygcbmr_50_90_c64_s25, "cyclic_rygcbmr_50_90_c64_s25"),
            (cc.b_cyclic_tritanopic_cwrk_40_100_c20, "cyclic_tritanopic_cwrk_40_100_c20"),
            (cc.b_cyclic_tritanopic_wrwc_70_100_c20, "cyclic_tritanopic_wrwc_70_100_c20"),
            (cc.b_cyclic_wrkbw_10_90_c43, "cyclic_wrkbw_10_90_c43"),
            (cc.b_cyclic_wrkbw_10_90_c43_s25, "cyclic_wrkbw_10_90_c43_s25"),
            (cc.b_cyclic_wrwbw_40_90_c42, "cyclic_wrwbw_40_90_c42"),
            (cc.b_cyclic_wrwbw_40_90_c42_s25, "cyclic_wrwbw_40_90_c42_s25"),
            (cc.b_cyclic_ymcgy_60_90_c67, "cyclic_ymcgy_60_90_c67"),
            (cc.b_cyclic_ymcgy_60_90_c67_s25, "cyclic_ymcgy_60_90_c67_s25"),
        ]:
        
            forward = []
            for _i in range(len(base_pallette)):
                forward.append(base_pallette[_i])
            
            reverse = []
            for color in reversed(forward):
                reverse.append(color)
            
            for palette, direction in [(forward, "forward"), (reverse, "reverse")]:
                
                if palette_name in ["black", "white"] and direction == "reverse":
                    continue
                
                name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.5f}".format(theta).replace(".", "-") + "_" + "{:0.2f}".format(angle).replace(".", "_") + "_" + palette_name + "_" + direction + "_" + animationtype
                
                t = AnimateTurtle(
                    angle = angle,
                    duration = duration,
                    iterations = iterations,
                    stepsize = stepsize,
                    linewidth = linewidth,
                    show_turtle = False,
                    border = 0.02,
                    draw = False,
                    
                    color_palette = palette,
                    palette_lines = True,
                    steps_per_color = int(iterations/(len(palette)*2)),
                    background_image = Image.new("RGBA", (width, height)),
                    
                    xoffset = int(round(width / 2, 0)),
                    yoffset = int(round(height / 2, 0)),
                    
                    quality_draw = True,
                    
                    autoscale = True,
                    detect_origin_return = False,
                    image_speed = (0,0),
                    
                    name = name,
                    theta = theta,
                    framerate = framerate,
                    width = width,
                    height = height,
                    path = path,
                )
                t.animate()
                image = t.es_turtle.image.resize((int(round(width / quality_factor,0)), int(round(height / quality_factor,0))), Resampling.LANCZOS)
                image.save(os.path.join(path, "transparent/" + name + ".png"))
                for bg in ["white", "black"]:
                    if bg == palette_name:
                        continue
                    bgimage = Image.new("RGB", (int(round(width / quality_factor,0)), int(round(height / quality_factor,0))), bg)
                    bgimage.paste(image, (0, 0), image)
                    bgimage.save(os.path.join(path, bg + "/" + name + "_" + bg + ".png"))
                logger.info("Finalized storing images for {}", name)            
    elif item == 21:
        linewidth = 5
        duration = 10
        es_line_width = 120
        
        theta = 0.512
        angle = 0
        extra_iterations = 0
        
        yt = -40
        yb = 0
        
        xl = 20
        xr = 20
        
        frame_corners = [
            (2320, 1320),
            (240, 1320),
            (120, 1200),
            (120, 240),
            (240, 120),
            (2320, 120),
            (2440, 240),
            (2440, 1200),
            (2320, 1320),
        ]
        
        new_corners = []
        for (x, y) in frame_corners:
            new_x, new_y = (x, y)
            if x < width / 2:
                new_x += xl
            else:
                new_x += xr
                
            if y < height / 2:
                new_y += yt
            else:
                new_y += yb
                
            new_corners.append((new_x, new_y))
            
        frame_corners = new_corners
                
        distance = 0
        angle_list = []
        distance_list = []
        for i in range(len(frame_corners) - 1):
            d= math.dist(frame_corners[i], frame_corners[i+1])
            distance += d
            distance_list.append(d)
            angle_list.append(_get_angle(frame_corners[i], frame_corners[i+1]))
            
        logger.debug("Total distance for line is {}", distance)
        logger.debug("Distances between points: {}", distance_list)
        logger.debug("Angles between points: {}", angle_list)

         
        logger.debug("Creating frame animation for theta={}, angle={}", theta, angle)

        iterations = 200000
        line_height = 0
        stepsize = 10
        n = 0
        while n < 10:
            t = Turtle(angle=angle)
            t.euler_spiral(theta, iterations, stepsize)
            
            line_height = (t.ymax - t.ymin)
            stepsize = round(stepsize * es_line_width / line_height, 10)
            logger.debug("Testheight was {}, new stepsize is {}", line_height, stepsize)
        
            t = Turtle(angle=angle)
            t.euler_spiral(theta, iterations, stepsize)
            
            image_speed_pixel_per_iteration = (t.xmax - t.xmin) / iterations
            
            iterations = int(round(distance / image_speed_pixel_per_iteration, 0))
            logger.debug("Testiterations is now {}", iterations)
            n += 1
        
        iterations_per_frame = iterations / (duration * framerate)
        iterations += int(round(iterations_per_frame * extra_iterations,0))
        
        t = Turtle(angle=angle)
        t.euler_spiral(theta, iterations, stepsize)
        logger.success("Final height: {} with ymin={} and ymax={}", (t.ymax-t.ymin), t.ymin, t.ymax)
        logger.success("Final length: {} with {} iterations", t.xmax - t.xmin, iterations)
        logger.success("Target distance: {}", distance)
        logger.success("Number of frames: {}", duration * framerate)
        
        pixel_per_iteration = (t.xmax - t.xmin) / iterations
        iterations_per_frame = iterations / (duration * framerate)
        pixel_per_frame = pixel_per_iteration * iterations_per_frame
        logger.success("Pixel per frame: {}", pixel_per_frame)
        
        extra_turns = {}
        turtangle = 0
        next_turn_frame = 0
        for i in range(len(frame_corners) - 1):
            turn = (360 - ((angle_list[i] % 360) - turtangle)) % 360
            turtangle = (turtangle - turn) % 360
            extra_turns[next_turn_frame] = turn
            logger.debug("Turn {} degree in frame {}, turtleangle at {}", turn, next_turn_frame, turtangle)
            next_turn_frame += int(round(distance_list[i] / pixel_per_frame, 0))
        
        animationtype = "es-picture-frame"
        name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.3f}".format(theta).replace(".", "-") + "_" + animationtype
        t = AnimateTurtle(
            angle = angle,
            duration = duration,
            iterations = iterations,
            stepsize = stepsize,
            linewidth = linewidth,
            extra_turns = extra_turns,
            hold_after = 5,
            
            image_speed = (0, 0),
            xoffset = int(round(frame_corners[0][0], 0)),
            yoffset = int(round(frame_corners[0][1], 0)),
            
            autoscale = False,
            detect_origin_return = False,
            
            name = name,
            theta = theta,
            framerate = framerate,
            width = width,
            height = height,
            path = path,
        )
        t.animate()
    elif item == 22:
        """Symmetrieslideshow, side by side"""
        animationtype = "syymetry-slideshow"
        name = name = "tfa_" + "{:03d}".format(item) + "_" + animationtype
        extension = "png"
        
        path = os.path.join(path, animationtype)
        os.makedirs(path, exist_ok=True)

        width = int(round(width / 2, 0))
        bborder = 100
        height -= bborder
        es_linewidth = 150
        linewidth = 10
        quality_factor = 4
        images_per_second = 6
        origin_radius = 20
        
        font = ImageFont.truetype("./freefont/FreeMonoBold.ttf", size=100)
       
        width *= quality_factor
        height *= quality_factor
        linewidth *= quality_factor
        es_linewidth *= quality_factor
        origin_radius *= quality_factor
       
        frame = 0
        for alpha in range(178):
           
            images = []
            for theta in [alpha + 1, 359 - alpha]:
                iterations = 100000
                stepsize = 100
                # line detection by origin return works for whole angle theta values
                t = Turtle(draw=False, width=width, height=height)
                t.euler_spiral(theta, iterations, stepsize)
                if t.last_origin:
                    logger.success("Origin return detected for theta={}", theta)
                    iterations = t.step_num
                    scale = t.autoscale(0.05)
                else:
                    logger.success("Line detected for theta={}", theta)
                    angles = []
                    for i in range(10000):
                        t.rotmov(theta * t.step_num, stepsize)
                        a = _get_angle((0, 0), t.get_pos())
                        angles.append(a)
                    angle = statistics.fmean(angles)
                    
                    t = Turtle(draw=False, width=width, height=height, angle=angle)
                    t.euler_spiral(theta, iterations, stepsize)
                    scale = es_linewidth / (t.ymax - t.ymin)
                    
                    logger.debug("Spiral line height was {} with target {} -> scale factor {}", (t.ymax - t.ymin), es_linewidth, scale)
                    
                t = Turtle(draw=True, width=width, height=height, scale=scale)
                t.linewidth = linewidth
                t.quality_draw = True
                t.euler_spiral(theta, iterations, stepsize)
                
                draw = ImageDraw.Draw(t.image)
                draw.ellipse((t.xoffset-origin_radius, t.yoffset-origin_radius, t.xoffset+origin_radius, t.yoffset+origin_radius), fill="red")
                
                images.append(t.image.resize((int(round(width / quality_factor,0)), int(round(height / quality_factor,0))), Resampling.LANCZOS))
            
            if len(images) != 2:
                continue
            
            center = int(round(width / quality_factor, 0))
            output_height =  int(round(height / quality_factor + bborder,0))
            
            image = Image.new("RGB", (int(center * 2), output_height), "black")
            image.paste(images[0], (0, 0))
            image.paste(images[1], (center, 0))
            
            draw = QualityDraw(image)
            draw.line(((center, 10), (center, output_height - 10)), fill="white", width=20)
            
            draw = ImageDraw.Draw(image)
            text = "θ = " + "{: 3d}".format(alpha + 1) + "   " + "θ = " + "{: 3d}".format(359 - alpha)
            _, _, w, h = draw.textbbox((0,0), text, font=font)
            draw.text((center - w / 2, output_height - 20 - h), text, font=font, fill=(255,255,255))
            
            for _f in range(int(round(framerate / images_per_second, 0))):
                filename = "{:012d}".format(frame)
                image.save(os.path.join(path,filename + "." + extension))
                frame += 1
                
        logger.debug("Creating shell file to run ffmpeg")
        with open(os.path.join(path, "animate.sh"), "w") as file:
            file.write('#! /usr/bin/bash' + "\n" + \
                    'mv $(ls *.png | tail -n 1) ../' + name + '.png' + "\n" + \
                    '/usr/bin/ffmpeg -n -pattern_type glob -loglevel error -framerate ' + str(int(framerate)) + ' -i "*.' + extension + '" -c:v libx264 -pix_fmt yuv420p ' + name + '.mp4 && rm *.png && rm *.sh && mv * ..')
    elif item == 23:
        """Let's Identify some lines!"""
        
        lines = []
        no_lines = []
        unknown = []
        
        try:
            inc = 0.0001
            for index in range(int(180 / inc)):
                theta = round((index + 1) * inc, 7)
                result = is_line(theta)
                if result is None:
                    unknown.append(theta)
                elif not result:
                    no_lines.append(theta)
                else:
                    lines.append(theta)
        except KeyboardInterrupt:
            pass
        
        logger.info("Found {} lines, {} no-lines and {} unknown", len(lines), len(no_lines), len(unknown))
        
        with open("./analysis_results.py", "w") as file:
            file.write('"""Result of Analysis"""' + "\n\n")
            file.write("THETA_LINES = " + str(lines) + "\n\n")
            file.write("THETA_NO_LINES = " + str(no_lines) + "\n\n")
            file.write("THETA_UNKNOWN = " + str(unknown) + "\n\n")     
    elif item == 24:
        """lets check our manual line list aginst the odd/even predictor"""   
        for theta in turtlefun_lines_manual.THETA_LINES:
            if not is_line(theta):
                logger.critical("NOT A LINE! theta = {}", theta)
    elif item == 25:
        """How can we even calculate the number of steps required to return home for an arbitrary angle?"""
        
        inc = 0.01
        for index in range(int(180 / inc)):
            theta = round((index + 1) * inc, 7)
            n = 1
            while round(n*(n+1)/2 * theta, 10) % 360 != 0:
                n += 1
            logger.debug("theta = {} --> n = {}; 360 / theta = {} rest {}", theta, n, 360 // theta, 360 % theta)
    elif item == 26:
        """Create fold over animation, vertical"""
        animationtype = "tfa_" + "{:03d}".format(item) + "_" + "syymetry-mirror"
        name = animationtype
        extension = "png"
        
        path = os.path.join(path, animationtype)
        os.makedirs(path, exist_ok=True)

        duration = 4
        width = int(round(width / 2, 0))
        bborder = 100
        height -= bborder
        es_linewidth = 150
        linewidth = 10
        quality_factor = 4
        images_per_second = 2.5
        origin_radius = 20
        
        font = ImageFont.truetype("./freefont/FreeMonoBold.ttf", size=100)
       
        width *= quality_factor
        height *= quality_factor
        linewidth *= quality_factor
        es_linewidth *= quality_factor
        origin_radius *= quality_factor
       
        frame = 0
        alpha = 0
           
        images = []
        for theta, linecolor in [(alpha + 1, "red"), (359 - alpha, "green")]:
            iterations = 100000
            stepsize = 100
            # line detection by origin return works for whole angle theta values
            t = Turtle(draw=False, width=width, height=height)
            t.euler_spiral(theta, iterations, stepsize)
            if t.last_origin:
                logger.success("Origin return detected for theta={}", theta)
                iterations = t.step_num
                scale = t.autoscale(0.05)
            else:
                logger.success("Line detected for theta={}", theta)
                angles = []
                for i in range(10000):
                    t.rotmov(theta * t.step_num, stepsize)
                    a = _get_angle((0, 0), t.get_pos())
                    angles.append(a)
                angle = statistics.fmean(angles)
                
                t = Turtle(draw=False, width=width, height=height, angle=angle)
                t.euler_spiral(theta, iterations, stepsize)
                scale = es_linewidth / (t.ymax - t.ymin)
                
                logger.debug("Spiral line height was {} with target {} -> scale factor {}", (t.ymax - t.ymin), es_linewidth, scale)
                
            t = Turtle(draw=True, width=width, height=height, scale=scale)
            t.linewidth = linewidth
            t.linecolor = linecolor
            t.quality_draw = True
            t.image = Image.new("RGBA", (width, height))
            t.euler_spiral(theta, iterations, stepsize)
            
            draw = ImageDraw.Draw(t.image)
            draw.ellipse((t.xoffset-origin_radius, t.yoffset-origin_radius, t.xoffset+origin_radius, t.yoffset+origin_radius), fill="red")
            
            images.append(t.image.resize((int(round(width / quality_factor,0)), int(round(height / quality_factor,0))), Resampling.LANCZOS))
        
        center = int(round(width / quality_factor, 0))
        change_per_frame = center / (framerate * duration - framerate / 2) * 2    
        for _f in range(int(round(framerate * duration, 0) + 2 * framerate)):    
            
            output_height =  int(round(height / quality_factor + bborder,0))
            
            image = Image.new("RGB", (int(center * 2), output_height), "black")
            draw = QualityDraw(image)
            draw.line(((center, 10), (center, output_height - 10)), fill="white", width=20)
            image.paste(images[0], (0, 0), images[0])
            
            if frame < framerate / 2:
                image.paste(images[1], (center, 0), images[1])
            elif frame < framerate / 2 + (framerate * duration - framerate / 2) / 2:
                reduce = int(round((frame - framerate / 2) * change_per_frame, 2))
                if center - reduce <= 0:
                    pass
                else:
                    resimage = images[1].resize((center - reduce, int(round(height / quality_factor, 0))), Resampling.LANCZOS)
                    image.paste(resimage, (center, 0), resimage)
            else:
                increase = int(round((frame - framerate / 2 - (framerate * duration - framerate / 2) / 2) * change_per_frame, 2))
                if increase > center:
                    resimage = ImageOps.mirror(images[1])
                    image.paste(resimage, (0, 0), resimage)
                else:
                    resimage = ImageOps.mirror(images[1].resize((increase,  int(round(height / quality_factor, 0))), Resampling.LANCZOS))
                    image.paste(resimage, (center - increase, 0), resimage)
            
            
            
            draw = ImageDraw.Draw(image)
            text = "θ = " + "{: 3d}".format(alpha + 1) + "   " + "θ = " + "{: 3d}".format(359 - alpha)
            _, _, w, h = draw.textbbox((0,0), text, font=font)
            draw.text((center - w / 2, output_height - 20 - h), text, font=font, fill=(255,255,255))
        
            filename = "{:012d}".format(frame)
            image.save(os.path.join(path,filename + "." + extension))
            frame += 1
                
        logger.debug("Creating shell file to run ffmpeg")
        with open(os.path.join(path, "animate.sh"), "w") as file:
            file.write('#! /usr/bin/bash' + "\n" + \
                    'mv $(ls *.png | tail -n 1) ../' + name + '.png' + "\n" + \
                    '/usr/bin/ffmpeg -n -pattern_type glob -loglevel error -framerate ' + str(int(framerate)) + ' -i "*.' + extension + '" -c:v libx264 -pix_fmt yuv420p ' + name + '.mp4 && rm *.png && rm *.sh && mv * ..')        
    elif item == 27:
        """Create fold over animation, horizontal"""
        animationtype = "tfa_" + "{:03d}".format(item) + "_" + "syymetry-flip"
        name = animationtype
        extension = "png"
        
        path = os.path.join(path, animationtype)
        os.makedirs(path, exist_ok=True)

        duration = 4
        width = width
        height = int(round(height / 2, 0))
        es_linewidth = 150
        linewidth = 10
        quality_factor = 4
        images_per_second = 2.5
        origin_radius = 20
        
        font = ImageFont.truetype("./freefont/FreeMonoBold.ttf", size=100)
       
        width *= quality_factor
        height *= quality_factor
        linewidth *= quality_factor
        es_linewidth *= quality_factor
        origin_radius *= quality_factor
       
        frame = 0
        alpha = 119
           
        images = []
        for theta, linecolor in [(alpha + 1, "red"), (359 - alpha, "green")]:
            iterations = 100000
            stepsize = 100
            # line detection by origin return works for whole angle theta values
            t = Turtle(draw=False, width=width, height=height)
            t.euler_spiral(theta, iterations, stepsize)
            if t.last_origin:
                logger.success("Origin return detected for theta={}", theta)
                iterations = t.step_num
                scale = t.autoscale(0.05)
            else:
                logger.success("Line detected for theta={}", theta)
                angles = []
                for i in range(10000):
                    t.rotmov(theta * t.step_num, stepsize)
                    a = _get_angle((0, 0), t.get_pos())
                    angles.append(a)
                angle = statistics.fmean(angles)
                
                t = Turtle(draw=False, width=width, height=height, angle=angle)
                t.euler_spiral(theta, iterations, stepsize)
                scale = es_linewidth / (t.ymax - t.ymin)
                
                logger.debug("Spiral line height was {} with target {} -> scale factor {}", (t.ymax - t.ymin), es_linewidth, scale)
                
            t = Turtle(draw=True, width=width, height=height, scale=scale)
            t.linewidth = linewidth
            t.linecolor = linecolor
            t.quality_draw = True
            t.xoffset = int(width / 3)
            if linecolor == "red":
                t.yoffset = 20 * quality_factor
            else:
                t.yoffset = t.height - 20 * quality_factor
                
            t.image = Image.new("RGBA", (width, height))
            t.euler_spiral(theta, iterations, stepsize)
            
            draw = ImageDraw.Draw(t.image)
            draw.ellipse((t.xoffset-origin_radius, t.yoffset-origin_radius, t.xoffset+origin_radius, t.yoffset+origin_radius), fill="red")
            
            images.append(t.image.resize((int(round(width / quality_factor,0)), int(round(height / quality_factor,0))), Resampling.LANCZOS))
        
        center = int(round(height / quality_factor, 0))
        change_per_frame = center / (framerate * duration - framerate / 2) * 2    
        for _f in range(int(round(framerate * duration, 0) + 2 * framerate)):    
            
            output_width =  int(round(width / quality_factor,0))
            
            image = Image.new("RGB", (output_width, int(center * 2)), "black")
            draw = QualityDraw(image)
            draw.line(((10, center), (output_width - 10, center)), fill="white", width=20)
            image.paste(images[0], (0, 0), images[0])
            
            if frame < framerate / 2:
                image.paste(images[1], (0, center), images[1])
            elif frame < framerate / 2 + (framerate * duration - framerate / 2) / 2:
                reduce = int(round((frame - framerate / 2) * change_per_frame, 2))
                if center - reduce <= 0:
                    pass
                else:
                    resimage = images[1].resize((int(round(width / quality_factor, 0)), center - reduce), Resampling.LANCZOS)
                    image.paste(resimage, (0, center), resimage)
            else:
                increase = int(round((frame - framerate / 2 - (framerate * duration - framerate / 2) / 2) * change_per_frame, 2))
                if increase > center:
                    resimage = ImageOps.flip(images[1])
                    image.paste(resimage, (0, 0), resimage)
                else:
                    resimage = ImageOps.flip(images[1].resize((int(round(width / quality_factor, 0)), increase), Resampling.LANCZOS))
                    image.paste(resimage, (0, center - increase), resimage)
            
            draw = ImageDraw.Draw(image)

            text = "θ = " + "{: 3d}".format(359 - alpha)
            _, _, w, h = draw.textbbox((0,0), text, font=font)
            draw.text((30, center * 3 / 2 - h / 2), text, font=font, fill=(255,255,255))
        
            text = "θ = " + "{: 3d}".format(alpha + 1) 
            _, _, w, h = draw.textbbox((0,0), text, font=font)
            draw.text((30, center / 2 - h / 2), text, font=font, fill=(255,255,255))
            
            filename = "{:012d}".format(frame)
            image.save(os.path.join(path,filename + "." + extension))
            frame += 1
                
        logger.debug("Creating shell file to run ffmpeg")
        with open(os.path.join(path, "animate.sh"), "w") as file:
            file.write('#! /usr/bin/bash' + "\n" + \
                    'mv $(ls *.png | tail -n 1) ../' + name + '.png' + "\n" + \
                    '/usr/bin/ffmpeg -n -pattern_type glob -loglevel error -framerate ' + str(int(framerate)) + ' -i "*.' + extension + '" -c:v libx264 -pix_fmt yuv420p ' + name + '.mp4 && rm *.png && rm *.sh && mv * ..')        
    elif item == 28:
        """Create sample images for lines"""
        height = 600
        width *= 2
        linewidth = 6
 
        animationtype = "linesample"       
        path = os.path.join(path, animationtype)
        os.makedirs(path, exist_ok=True)

        for theta in turtlefun_lines_manual.THETA_LINES:

            logger.debug("Creating slim line sample image for theta={}", theta)

            name = "tfa_" + "{:03d}".format(item) + "_" + "{:012.8f}".format(theta).replace(".", "-") + "_" + animationtype
            
            angle = 0
            iterations = 200000
            image_height = 0
            stepsize = 10 * theta
            n = 0
            while (image_height < height - 2 * linewidth or image_height > height) and n < 5:
                
                # determine the start angle
                t = Turtle(draw=False, angle=angle)
                t.euler_spiral(theta, iterations, stepsize)
                
                angles = []
                for i in range(int(round(360 / theta * 2, 0))):
                    t.rotmov(theta * t.step_num, stepsize)
                    pos = t.get_pos()
                    a = _get_angle((0, 0), pos)
                    logger.trace("Position {}, angle is {}", pos, a)
                    angles.append(a)
                    
                angle += statistics.fmean(angles)
                logger.success("For theta={} the average angle is {}", theta, angle)
                
                t = Turtle(angle=angle, draw=False)
                t.euler_spiral(theta, iterations, stepsize)
                
                image_height = (t.ymax - t.ymin)
                stepsize = round(stepsize * (height - linewidth) / image_height, 10)
                logger.debug("Testheight was {}, new stepsize is {}", image_height, stepsize)
            
                t = Turtle(angle=angle, draw=False)
                t.euler_spiral(theta, iterations, stepsize)

                image_speed_pixel_per_iteration = t.xmax / iterations
                iterations = int(round(width * 2 / image_speed_pixel_per_iteration))
                logger.debug("Testiterations is now {}", iterations)
                n += 1
            
            t = Turtle(angle=angle, draw=False)
            t.euler_spiral(theta, iterations, stepsize)
            logger.success("Final height: {} with ymin={} and ymax={}, target height is {}", (t.ymax-t.ymin), t.ymin, t.ymax, height)
            logger.success("Final length: {}", t.xmax - t.xmin)
            logger.success("Final iterations: {}", iterations)
            
            yoffset = int(round(height / 2, 0))
            logger.debug("Yoffset for center of animation: {}", yoffset)
            yoffset_correction = t.ymax - (t.ymax - t.ymin) / 2
            yoffset -= yoffset_correction
            yoffset = int(round(yoffset, 0))
            logger.success("Yoffset of {} after correction of {}", yoffset, yoffset_correction)
            
            xoffset = int(round(-1 * width / 2, 0))
            
            t = Turtle(width=width, height=height, angle=angle, draw=True)
            t.quality_draw = True
            t.linewidth = linewidth
            t.xoffset = xoffset
            t.yoffset = yoffset
            
            t.euler_spiral(theta, iterations, stepsize)
            
            t.save(name + ".png", path)
    elif item == 29:
        """Create High Quality single image render of return to origin theta value with colormap"""
        animationtype = "Feynman-exploration"
        
        linewidth = 5
        quality_factor = 4
        zoom_factor = 1
        width *= quality_factor * zoom_factor
        height *= quality_factor * zoom_factor
        linewidth *= quality_factor
        
        path = os.path.join(path, animationtype)
        path = os.path.join(path, "onemore")
        
        for _p in ["transparent", "white", "black"]:
            os.makedirs(os.path.join(path, _p), exist_ok=True)
            
        logger.success("Running with theta={}", theta)
        
        duration = 5 # As we do not draw, this does not matter at all, we only draw the final image
            # (1, 0, 720)
            # (1.1, 0, 7200),
            # (1.01, 0, 72000),
            # (1.001, 0, 720000),
            # (1.0001, 0, 7200000),
            # (1.00001, 0, 72000000),
            # (1.000001, 0, 720000000),
        for  theta, angle, total_iterations in [
            (1, 0, 720),
            (1.1, 0, 7200),
            (1.01, 0, 72000),
            (1.001, 0, 720000),
            (1.0001, 0, 7200000),
            (1.00001, 0, 72000000),
            (1.000001, 0, 720000000),
        ]:
            
            base_pallette, palette_name = (cc.b_cyclic_mygbm_30_95_c78, "b_cyclic_mygbm_30_95_c78")
            
            if total_iterations == 720:
                # coloring the base element required some special treatment of the colormap,
                # reducing the colors to 180 to make even color steps possible
                plaette = []
                n = 1
                for i in range(len(base_pallette)):
                    if n * (len(base_pallette) / (len(base_pallette) - 180)) < i:
                        n += 1
                    else:
                        plaette.append(base_pallette[i])
                        
                base_pallette = plaette
            
                
            name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.5f}".format(theta).replace(".", "-") + "_" + "{:0.2f}".format(angle).replace(".", "_") + "_" + palette_name + "_" + animationtype
            
            t = AnimateTurtle(
                angle = angle,
                duration = duration,
                iterations = total_iterations,
                stepsize = 10,
                linewidth = linewidth,
                show_turtle = False,
                border = 0.02,
                draw = False,
                
                color_palette = base_pallette,
                palette_lines = True,
                steps_per_color = int(total_iterations/(len(base_pallette)*2)),
                background_image = Image.new("RGBA", (width, height)),
                
                xoffset = int(round(width / 2, 0)),
                yoffset = int(round(height / 2, 0)),
                
                quality_draw = True,
                
                autoscale = True,
                detect_origin_return = False,
                image_speed = (0,0),
                
                name = name,
                theta = theta,
                framerate = framerate,
                width = width,
                height = height,
                path = path,
            )
            t.animate()
            image = t.es_turtle.image.resize((int(round(width / quality_factor,0)), int(round(height / quality_factor,0))), Resampling.LANCZOS)
            image.save(os.path.join(path, "transparent/" + name + ".png"))
            for bg in ["white", "black"]:
                if bg == palette_name:
                    continue
                bgimage = Image.new("RGB", (int(round(width / quality_factor,0)), int(round(height / quality_factor,0))), bg)
                bgimage.paste(image, (0, 0), image)
                bgimage.save(os.path.join(path, bg + "/" + name + "_" + bg + ".png"))
            logger.info("Finalized storing images for {}", name)  
    elif item == 30:
        """Ok, why can't we estimate the number of steps until return?
        Lets have another try."""
        # yipiieee this really seems to go in the right direction, finally!
        
        analyze = theta
        
        angle_list = []
        table = PrettyTable(["angle", "quotient", "turtle view"])
        factor = 10**4
        for angle in reversed(range(int(360 * factor))):
            theta = round((angle + 1) / factor, 15)
            n = round(360 / theta, 12)
            if n.is_integer():
                table.add_row([theta, n, round((n * (n + 1) / 2 * theta) % 360, 5)])
                angle_list.append(theta)
        click.echo(str(table))
        
        table = PrettyTable(["theta", "step num", "summands", "quotients", "least common multiple", "Angle after first cycle"])
        
        for theta, experimental_steps in turtle_originreturnsamples.TURTLE_ORIGIN_RETURN_SAMPLES:
            logger.debug("Analyzing theta={}", theta)
            analyze = theta
            sums = []
            quotients = []
            
            for angle in angle_list:
                while analyze >= angle:
                    sums.append(angle)
                    quotients.append(int(round(360 / angle, 0)))
                    analyze -= angle
                    analyze = round(analyze, 12)
                    
                if analyze <= 0:
                    break
            
            lcm = math.lcm(*quotients)
            cycle_angle =  round(lcm * (lcm + 1) / 2 * theta % 360, 5)
            
            table.add_row([theta, experimental_steps, str(sums), str(quotients), lcm, cycle_angle])
        
        click.echo(str(table))
    elif item == 31:
        """Pre-Calculate 360 degree table for the evaluation of the steps per cycle"""
        angle_list = []
        table = PrettyTable(["theta", "quotient", "alpha"])
        
        decimal_places = Decimal(9)
        factor = Decimal(10**decimal_places)
        full_circle = Decimal(360) * factor
        n = 0
        for angle in reversed(range(int(full_circle / Decimal('23')))):
            n += 1
            theta = Decimal(angle + 1)
            if n % 1000000 == 0:
                logger.debug("Calculating theta={}.", theta)
            quotient = full_circle / theta
            if round(quotient, 0) == quotient:
                list_theta = theta * Decimal(360) / full_circle 
                list_alpha = ((quotient * (quotient + Decimal(1)) / Decimal(2) * theta) % full_circle) / factor
                angle_list.append((list_theta, quotient, list_alpha))
                table.add_row([list_theta, quotient, list_alpha])
                logger.success("Found theta = {} to be a dominant angle", list_theta)
        
        click.echo(table)
        with open("turtlefun_quotientlist.py", "w") as file:
            file.write('"""Quotient list for calculating euler spiral steps with a precision of ' + str(int(decimal_places)) + '"""' + "\n\n")
            file.write("from decimal import Decimal\n\n")          
            file.write("TURTLEFUN_QUOTIENT_LIST = [\n")
            for entry in angle_list:
                file.write("    " + str(entry) + ",\n")
            file.write("    ]\n")
    elif item == 32:
        """Try to calculate origin return values and compare with available experimental data."""
        decimal.getcontext().prec = 100
        
        count_correct = 0
        table_entries = 0
        upper_correct = 0
        lower_correct = 0
        none_correct = 0
        
        table = PrettyTable(["#", "theta", "exp steps", "low limit", "ll fac.", "up limit", "ul fac.", "angle summands", "quotients", "lcm", "1st cycl. Angle"])
        for theta, experimental_steps in turtle_originreturnsamples.TURTLE_ORIGIN_RETURN_SAMPLES:
            logger.debug("Analyzing theta={}", theta)
            analyze = Decimal(str(theta))
            sums = []
            quotients = []
            int_quotients = []
            
            theta_decimals = 0
            if "." in str(theta):
                theta_decimals = len(str(theta).strip("0").split(".")[1])
            
            # Identify the dominant angles
            for angle, quotient, alpha in turtlefun_quotientlist.TURTLEFUN_QUOTIENT_LIST:
                
                angle_decimal = 0
                if "." in str(angle):
                    angle_decimal = len(str(angle).strip("0").split(".")[1])
                    
                if angle_decimal > theta_decimals:
                    continue
                
                while analyze >= angle:
                    sums.append(angle)
                    quotients.append(quotient)
                    int_quotients.append(int(quotient))
                    analyze -= angle
                    
                if analyze <= 0:
                    break
            
            lcm = math.lcm(*int_quotients) # least common multiple

            cycle_angle_rot_sum = (Decimal(lcm) * (Decimal(lcm) + Decimal('1')) / Decimal('2'))
            cycle_angle = Decimal(cycle_angle_rot_sum) * Decimal(str(theta)) % Decimal('360')

            logger.debug("Least common multiple = {} resulting in {} total rotations and an end of cycle angle of {}", lcm, cycle_angle_rot_sum, cycle_angle)
            
            required_cycles = Decimal('1')
            while (required_cycles * cycle_angle) % Decimal('360') != 0:
                required_cycles += Decimal('1')
            calculated_steps = lcm * required_cycles
            
            # somehow the calculated steps are an upper limit for the experimental steps.
            # let's get the prime factors of the calculated steps to reduce the steps to
            # the heoretical minimum to get a lower bound.
            
            primes = []
            prime = 1
            steps = calculated_steps
            while True:
                prime = nextprime(prime)
                while round(steps / Decimal(str(prime)), 0) == steps / Decimal(str(prime)):
                    steps /= Decimal(str(prime))
                    primes.append(Decimal(str(prime)))
                
                if steps == 1:
                    break
                if prime > steps:
                    logger.critical("Failed to calculate prime factors!")
            
            reduced_steps = calculated_steps
            combination = [] # empty list 
            for r in range(1, len(primes) + 1):
                combination += itertools.combinations(primes, r)
            
            for primelist in combination:
                prime = math.prod(primelist)
                steps = calculated_steps / Decimal(str(prime))
                if (steps * (steps + Decimal('1')) / Decimal('2') * Decimal(str(theta))) % Decimal('360') == 0:
                    reduced_steps = min(reduced_steps, steps)
            
            
            if calculated_steps != reduced_steps:
                if calculated_steps == experimental_steps:
                    upper_correct += 1
                elif reduced_steps == experimental_steps:
                    lower_correct += 1
                else:
                    none_correct += 1
                    table_entries += 1 
                    table.add_row([
                        table_entries,
                        theta,
                        experimental_steps,
                        reduced_steps,
                        round(reduced_steps / experimental_steps, 2),
                        calculated_steps,
                        round(calculated_steps / experimental_steps, 0),
                        ", ".join(map(str, sums)),
                        ", ".join(map(str, quotients)),
                        lcm,
                        str(round(cycle_angle,0)),
                        ])
            
            else:
                count_correct += 1
            
            if experimental_steps < reduced_steps or experimental_steps > calculated_steps:
                logger.critical("Experimental steps {} outside of {} <= steps >= {}", experimental_steps, reduced_steps, calculated_steps)
                exit()
                
        click.echo(table.get_string(sortby="theta"))
        click.echo("\n  " + str(count_correct) + " correct with upper-limit == lower-limit")
        click.echo("  " + str(upper_correct) + " with upper limit correct, but wrong lower limit")
        click.echo("  " + str(lower_correct) + " with lower limit correct, but wrong upperlimit")
        click.echo("  " + str(none_correct) + " with neither upper nor lower limit correct.")
        click.echo("  " + str(len(turtle_originreturnsamples.TURTLE_ORIGIN_RETURN_SAMPLES)) + " total theta values tested.\n")
    elif item == 33:
        """Animate beautiful curves in a very short time
        Added antialiasing using quality_factor that upscales the image for drawing.
        Added flip and mirror to reverse, so removing goes in the same direction."""
        # [0.165, 1.135, 9.89, 14.455, 177.68, 179.792, 30.03, 44.96, 59.92, 89.9, 119.34, 122.42, 122.9, 48.56, 54.1, 54.28, 54.46, 71.06]

        palette = cc.b_cyclic_mygbm_30_95_c78
        palette = cc.b_cyclic_mrybm_35_75_c68_s25
        
        # palette = []
        # for color in cc.b_cyclic_mygbm_30_95_c78:
        #     palette.append(color)
        # palette.reverse()
        
        animationtype = "quickin-quickout"
        
        for theta in [119.9]:
            try:
                total_iterations = None
                for t, i in turtle_originreturnsamples.TURTLE_ORIGIN_RETURN_SAMPLES:
                    if t == theta:
                        total_iterations = i
                        break
                
                if total_iterations is None:
                    logger.critical("Could not find iterations for theta={}", theta)
                    continue
                    
                name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.5f}".format(theta).replace(".", "-") + "_" + animationtype
                
                hold_before = 0.25
                duration = 5
                hold_after = 0.5

                t = AnimateTurtle(
                    angle = 0,
                    duration = duration,
                    iterations = total_iterations,
                    stepsize = 10,
                    linewidth = 3,
                    show_turtle = False,
                    border = 0.02,
                    hold_before = hold_before,
                    hold_after = hold_after,
                    
                    quality_factor = 4,
                    quality_draw = True,
                    
                    color_palette = palette,
                    palette_lines = True,
                    steps_per_color = int(total_iterations/(len(palette)*2)),
                    reverse = True,
                    reverse_flip_mirror = False,
                    
                    xoffset = int(round(width / 2, 0)),
                    yoffset = int(round(height / 2, 0)),
                    
                    autoscale = True,
                    detect_origin_return = False,
                    image_speed = (0,0),
                    
                    name = name,
                    theta = theta,
                    framerate = framerate,
                    width = width,
                    height = height,
                    path = path,
                )
                t.animate()
                
            except:
                logger.exception("Failed while creating theta={}", theta)
    elif item == 34:
        explore_euler_spiral_no_return()
    elif item == 35:
        angle_list = []
        my_range = 1000000000000
        
        timer_start = perf_counter()
        
        numerator = Decimal('360')
        pre_num_primes = get_primes(numerator)
        
        for number in range(my_range):
            if number % 10000 == 0 and number > 0:
                logger.debug("Reached number {} of {}, time remaining is {}s", number, my_range, (perf_counter() - timer_start) / number * (my_range - number))
            
            denominator = Decimal(str(number + 1))
            num_primes = pre_num_primes.copy()
            den_primes = get_primes(denominator)
            for prime in num_primes.copy():
                if prime in den_primes:
                    num_primes.remove(prime)
                    den_primes.remove(prime)
            # logger.trace("{} / {} was reduced to ({}) / ({})", numerator, denominator, " * ".join(str(n) for n in num_primes), " * ".join(str(n) for n in den_primes))
            for prime in den_primes.copy():
                if prime in [2, 5]:
                    den_primes.remove(prime)
                else:
                    break
            if len(den_primes) == 0:
                fraction = numerator / denominator
                alpha = ((denominator * (denominator + Decimal('1')) / Decimal('2') * fraction) % Decimal('360'))
                logger.success("{} as denominator of 360 gives a finite fraction of {}, final turtle angle is {}°", str(denominator), str(fraction), str(alpha))
                angle_list.append((fraction, denominator, alpha))
                
        with open("turtlefun_denominatorlist.py", "w") as file:
            file.write('"""Quotient list for calculating euler spiral quotients from 1 to ' + str(int(my_range)) + '"""' + "\n\n")
            file.write("from decimal import Decimal\n\n")          
            file.write("TURTLEFUN_QUOTIENT_LIST = [\n")
            for entry in angle_list:
                file.write("    " + str(entry) + ",\n")
            file.write("    ]\n")
    elif item == 36:
        create_quotient_list(1000000000000, 140624, True)
    elif item == 37:
        """Yet another approach to the quotient list"""
        getcontext().prec = 200
        
        numberlist = []
        depth = 200
        for five in range(depth):
            logger.debug("five = {}", five)
            for two in range(depth):
                for three in range(3):
                    num = Decimal('5')**Decimal(five) * Decimal('2')**Decimal(two) * Decimal('3')**Decimal(three)
                    if num not in numberlist:
                        numberlist.append(num)
        numberlist.sort()
        logger.debug("Created numberlist with {} entries", len(numberlist))
        
        quotientlist = []
        with open("turtlefun_quotients_from_exponents.py", "w") as file:
            file.write('"""Quotient list for calculating euler spiral quotients from exponents of 2 and five up to ' + str(int(depth)) + '"""' + "\n\n")
            file.write("from decimal import Decimal\n\n")          
            file.write("TURTLEFUN_QUOTIENT_LIST = [\n")
            for num in numberlist:
                if num <= Decimal('360000000000000'):
                    fraction = Decimal('360') / num
                    alpha = ((num * (num + Decimal('1')) * fraction / Decimal('2')) % Decimal('360'))
                    entry = (fraction, num, alpha)
                    quotientlist.append(entry)
                    file.write("    " + str(entry) + ",\n")
            file.write("    ]\n")
        
        for entry in turtlefun_quotientlist.TURTLEFUN_QUOTIENT_LIST:
            if entry not in quotientlist:
                logger.warning("Entry {} not found in new list!", entry)
            else:
                logger.debug("Entry {} successfully identified in new list.", entry)   
    elif item == 38:
        """Lets find a good demonstration angle for the home return prediction
        THIS APPROACH WAS TOTALLY NOT SUCCESSFULL!
        WELL, IN THE END IT WAS --> fixed an error in the turtlent library, where we started with the biggest step number
        instead of trying the small ones first - so we never found the smaller return angles.
        """
        
        dominant_angle_list = []
        for dominant, quotient, alpha in turtlefun_quotientlist.TURTLEFUN_QUOTIENT_LIST:
            if quotient < 800 and quotient >= 200:
                dominant_angle_list.append(dominant)
        logger.debug("Selected {} dominant angles out of {}", len(dominant_angle_list), len(turtlefun_quotientlist.TURTLEFUN_QUOTIENT_LIST))
        
        combination = itertools.combinations(dominant_angle_list, 5) # 4 dominant angles
        
        theta_list = []
        for c in combination:
            t = Decimal('0')
            for n in c:
                t += n
            theta_list.append(t)
        theta_list = list(set(theta_list))
        theta_list.sort(reverse=True)
        logger.debug("Created {} theta values out of the list.", len(theta_list))
        
        candidates = []
        for theta in theta_list:
            if theta < 1:
                break
            t = TurtleNT(theta=theta)
            if len(t.origin_return_estimation()) >= 4 and \
                len(t.origin_return_estimation()) <= 5 and \
                t.origin_return_estimation()[0] < 100000 and \
                len(t.dominant_angles()) >= 3:
                candidates.append(theta)
                logger.debug("Candidate theta={}, {}", theta, t.origin_return_estimation())
        
        logger.debug("Identified {} candidates.", len(candidates))
        
        for theta in candidates:
            t = TurtleNT(theta=theta)
            t.euler_spiral()
            if t.is_home() and t.get_steps() < t.origin_return_estimation()[0] and t.get_steps() > t.origin_return_estimation()[-1]:
                t.save_image()
                logger.success("Finalist identified theta={}, steps={} out of {}", theta, t.get_steps(), t.origin_return_estimation())
    elif item == 39:
        """Draw Images for dominant angle explanation"""
        
        for theta, steps in turtle_originreturnsamples.TURTLE_ORIGIN_RETURN_SAMPLES:
            if steps < 1000000:
                t = TurtleNT(theta)
                t.euler_spiral()
                if t.is_home() and t.get_steps() < t.origin_return_estimation()[0]:
                    logger.success("Candidate theta={} after {} steps, {}", theta, t.get_steps(), t.origin_return_estimation())
                    t.save_image()
    elif item == 40:
        """ℕ, ∈ δ Animation of dominant angles."""
        n = 0
        i = 0
        
        radius = int(round(0.75 * height * 4 / 2, 0))
        lineradius = int(round(0.9 * height * 4 / 2, 0))
        center = int(round(height * 4 / 2, 0))
        textcenter = int(round(width * 4 * 7 / 10, 0))
        linewidth = 20 * 4
        
        font = ImageFont.truetype("./freefont/FreeMonoBold.ttf", size=600)
        image = Image.new("RGB", (width * 4, height * 4), "black")
        draw = ImageDraw.Draw(image)
        _, _, _, textheight = draw.textbbox((0,0), "0123456789pieces", font=font)
        
        for delta, denominator, alpha in turtlefun_quotientlist.TURTLEFUN_QUOTIENT_LIST:
            n += 1
            
            image = Image.new("RGB", (width * 4, height * 4), "black")
            draw = ImageDraw.Draw(image)
            qdraw = QualityDraw(image)
            
            
            draw.ellipse((center - radius, center - radius, center + radius, center + radius), fill="white")
            draw.ellipse((center - radius + linewidth, center - radius + linewidth, center + radius - linewidth, center + radius - linewidth), fill="black")
            
            for r in range(int(denominator)):
                angle = r * delta
                logger.debug("Drawing line for angle {}", angle)
                radians = math.radians(angle)
                qdraw.line(((center, center), (center + math.sin(radians) * lineradius, center + math.cos(radians) * lineradius)),
                           fill="white",
                           width=int(linewidth / 5))
            
            text = str(denominator) + " "
            _, _, w, h = draw.textbbox((0,0), text, font=font)
            draw.text((textcenter - w, center - 2*textheight), text, "white", font)
            draw.text((textcenter, center - 2*textheight), "pieces", "white", font)
            
            text = str("δ = ")
            _, _, w, h = draw.textbbox((0,0), text, font=font)
            draw.text((textcenter - w, center), text, "white", font)
            draw.text((textcenter, center), str(delta) + "°", "white", font)
              
            image = image.resize((width, height), Resampling.LANCZOS)
            
            # 28 seconds
            # first image 2 second
            # 25 seconds for 38 images --> 33 frames per image
            # last image 1 second
            count = 33
            if n == 1:
                count = 100
            elif n == 40:
                count = 50
            
            for _ in range(count):
                i += 1
                image.save("tfa_0040_" + "{:05d}".format(i) + ".png")
            
            if n >= 40:
                break
    elif item == 41:
        theta = 6.609375
        logger.debug("Running with theta={}", theta)
        animationtype = "example-home-return"
        name = "tfa_" + "{:03d}".format(item) + "_" + "{:0.5f}".format(theta).replace(".", "-") + "_" + animationtype
        
        iterations = 5120
        stepsize = 10
        t = Turtle(draw=False, width=width, height=height)
        t.euler_spiral(theta, iterations, stepsize)
        stepsize = stepsize * t.autoscale()
        
        duration = 24
        hold_after = 0
        
        palette = cc.b_cyclic_mygbm_30_95_c78

        t = AnimateTurtle(
            angle = 0,
            duration = duration,
            iterations = iterations,
            stepsize = 10,
            linewidth = 3,
            show_turtle = False,
            border = 0.02,
            hold_after = hold_after,
            
            color_palette = palette,
            palette_lines = True,
            steps_per_color = int(iterations/(len(palette)*2)),
            
            turtle_code_window = TurtleCodeWindow(width, height, 1890, 50, duration + hold_after - 3, framerate, iterations, theta, int(round(stepsize, 0)), False),
            step_counter = True,
            
            xoffset = int(round(width / 2, 0)),
            yoffset = int(round(height / 2, 0)),
            
            autoscale = True,
            detect_origin_return = False,
            image_speed = (0,0),
            
            name = name,
            theta = theta,
            framerate = framerate,
            width = width,
            height = height,
            path = path,
        )
        t.animate()        
              
@turtlefun.command()
@click.option("--theta", "-t", default=1, type=float, help="Theta angle of spiral")
@click.option("--iterations", "-i", default=100000, type=int, show_default=True, help="Interations to run through")
@click.option("--stepsize", "-s", default=10, type=float, help="Nominal step length")
@click.option("--home", "-h", default=10, type=float, help="Size of home")
def homereturn(theta, iterations, stepsize, home):
    """For large number of iterations or structures that are very busy around the origin point,
    automatic detection of the home base fails regulary. Here is a tool to manually determine this point."""
    t =Turtle(draw=False, home=home)
    t.euler_spiral(theta, iterations, stepsize)
    scale = t.autoscale()
    
    t=Turtle(draw=True, home=home, scale=scale)
    t.home_color_change = True
    t.euler_spiral(theta, iterations, stepsize)
    
    image = t.image
    draw = ImageDraw.Draw(image)
    length = 50
    draw.ellipse(((t.xoffset - length, t.yoffset - length), (t.xoffset + length, t.yoffset + length)), fill=(255, 0, 0), outline=(255, 255, 0))
    t.save("homereturnsearch.png", "./")
    
    click.echo(str(t.step_num) + " steps used for testing.")
    click.echo("The turtle is looking at " + str(t.angle))
    click.echo(t.home_analysis.print())
    click.echo("Final position: " + str(round(t.xpos, 0)) + " x " + str(round(t.ypos,0 )))
    
    t=TurtleNT(theta)
    click.echo("The dominant angles of theta=" + str(theta) + " are: " + ", ".join(str(e) for e in t.dominant_angles()))
    click.echo("Possible final return iterations: " + ", ".join(str(e) for e in t.origin_return_estimation()))
    
             
@turtlefun.command()
@click.option("--theta", "-t", default=1, type=float, help="Theta angle of spiral")
@click.option("--iterations", "-i", default=100000, type=int, show_default=True, help="Interations to run through")
@click.option("--stepsize", "-s", default=10, type=float, help="Nominal step length")
@click.option("--startangle", "-a", default=0, type=float, help="Initial rotaion before starting the spiral")
@click.option("--path", "-p", default=None, type=str, help="Path for images")
@click.option("--linewidth", "-l", default=5, type=int, help="linewidth")
@click.option("--duration", "-d", default=5, type=float, help="duration in seconds")
def animate(theta:float, iterations:List[int], stepsize:float, startangle:float, path:str, linewidth:int, duration:float) -> None:
    """Create animation images for euler spiral lines"""
    t = AnimateTurtle(
        theta=theta,
        angle=startangle,
        stepsize=stepsize,
        iterations=iterations,
        path=path,
        linewidth=linewidth,
        duration=duration
        )
    t.animate()
    
@turtlefun.command()
@click.option("--threads", "-t", default=4, type=int, help="Number of threads to use for exploration")
@click.option("--path", "-p", default=None, type=str, help="Path for exploration results")
@click.option("--start", "-s", default=0.9, type=float, help="Starting point for theta exploration")
@click.option("--stop", "-e", default=1.1, type=float, help="End point for theta exploration.")
@click.option("--increment", "-a", default=1.1, type=float, help="Increment between theta points.")
@click.option("--iterations", "-i", default=100000, type=int, help="Number of iterations per euler spiral.")
def explore(threads:int, path:str, start:float, stop:float, increment:int, iterations:int) -> None:
    """Explore the Euler Spiral space"""
    explore_euler_spiral(start, stop, increment, iterations, threads, path)

@turtlefun.command()
@click.option("--theta", "-t", default=1, type=float, help="Theta angle of spiral")
@click.option("--iterations", "-i", default=1000000, type=int, help="Maximum number of iterations")
@click.option("--stepsize", "-s", default=10, type=float, help="Nominal step length")
@click.option("--width", "-w", default=3840, type=int, help="Width of image")
@click.option("--height", "-h", default=2160, type=int, help="Height of image")
@click.option("--path", "-p", default=None, type=str, help="Path for images")
@click.option("--do-scale/--no-scale", "-d/-n", default=True, type=bool, help="Run twice to get scaled image or only raw")
def spiral(theta:float, iterations:int, stepsize:float, width:int, height:int, path:str, do_scale:bool) -> None:
    """Generate a Euler spiral with the given parameters"""
    t = Turtle(draw=True, width=width, height=height)
    t.euler_spiral(theta, iterations, stepsize)
    t.save(None, path)
    
    if do_scale:
        scale = t.autoscale(0.01)
        t = Turtle(draw=True, width=width, height=height, scale=scale)
        t.linewidth = max(min(int(scale), 10), 1)
        t.euler_spiral(theta, iterations, stepsize)
        t.save(None, path)
    
@turtlefun.command()
@click.option("--theta", "-t", default=0.9876, type=float, help="Theta angle to run tests.")
@click.option("--iterations", "-i", default=[100, 10000, 1000000], type=int, multiple=True, show_default=True, help="Interations to run through")
def speedtest(theta:Union[int, float], iterations:List[int]) -> None:
    """Test the speed of Euler spiral generation"""
    logger.debug("Running speedtest with theta of {}", theta)
    logger.debug("Running speedtest for {} iterations", iterations)
    click.echo(_run_speedtest(theta, iterations))
    