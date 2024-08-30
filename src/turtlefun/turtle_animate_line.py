"""src/turtlefun/turtle_animate_line.py"""

import colorcet as cc
from loguru import logger
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from prettytable import PrettyTable
from typing import Union, List

from .turtle import Turtle

class AnimateTurtle:
    """Create animations from turtle graphics."""
    
    def __init__(self, **kwargs) -> None:
        """Initialize animation.
        Args:
            theta (float, int): Theta angle for line
            angle (float, int): Rotation of turtle before start of animation
            stepsize (float, int): Stepsize of pixels.
            precision (int): rounding of float number for comparison reasons
            width (int): Width of the animation frame
            height (int): height of the animation frame
            framerate (float): number of frames per second for final animation
            duration (float): number of seconds of final animation
            iterations (int): number of steps to be drawn
            detect_origin_return (bool): reduce number of iterations if origin return is detected
            scale (float): scale factor for image drawing
            autoscale (bool): dry run to set scale factor
            boder (float): border as fraction of image to keep free when autoscaling
            xoffset (int): image offset in x-direction
            yoffset (int): image offset in y-direction
            path (str): path for animation images
        """
        self._init_kwargs(kwargs)
        
        self.turtle = Turtle(angle=self.angle)
        self.turtle.euler_spiral(self.theta, self.iterations, self.stepsize)
        
    def _init_kwargs(self, kwargs) -> None:
        """Initialize variables from kwargs"""
        
        self.image_speed = None
        if "image_speed" in kwargs:
            self.image_speed = kwargs["image_speed"]
        
        self.theta = 1
        if "theta" in kwargs:
            self.theta = float(kwargs["theta"])
        
        self.angle = 0
        if "angle" in kwargs:
            self.angle = float(kwargs["angle"])
        
        self.stepsize = 10
        if "stepsize" in kwargs:
            self.stepsize = float(kwargs["stepsize"])
            
        self.precision = 15
        if "precision" in kwargs:
            self.precision = int(kwargs["precision"])
            
        self.width = 3840
        if "width" in kwargs:
            self.width = int(kwargs["width"])
        self.width_output = self.width
            
        self.height = 2160
        if "height" in kwargs:
            self.height = int(kwargs["height"])
        self.height_output = self.height
            
        self.framerate = 50
        if "framerate" in kwargs:
            self.framerate = float(kwargs["framerate"])
        
        self.duration = 5
        if "duration" in kwargs:
            self.duration = float(kwargs["duration"])
            
        self.iterations = 1000000
        if "iterations" in kwargs:
            self.iterations = int(kwargs["iterations"])
            
        self.detect_origin_return = True
        if "detect_origin_return" in kwargs:
            self.detect_origin_return = bool(kwargs["detect_origin_return"])
            
        self.scale = 1.0
        if "scale" in kwargs:
            self.scale = float(kwargs["scale"])
            
        self.autoscale = True
        if "autoscale" in kwargs:
            self.autoscale = bool(kwargs["autoscale"])
            
        self.border = 0.02
        if "border" in kwargs:
            self.border = float(kwargs["border"])
            
        self.xoffset = int(self.width * 0.8)
        if "xoffset" in kwargs:
            self.xoffset = int(kwargs["xoffset"])
            
        self.yoffset = int(self.height / 2)
        if "yoffset" in kwargs:
            self.yoffset = int(kwargs["yoffset"])
            
        self.name = "turtlefunanimation"
        if "name" in kwargs:
            self.name = str(kwargs["name"])
                
        self.draw = True,
        if "draw" in kwargs:
            self.draw = bool(kwargs["draw"])
            
        self.path = "./animation"
        if "path" in kwargs and kwargs["path"] is not None:
            self.path = str(kwargs["path"])
        if self.draw:
            self.path = os.path.join(self.path, self.name)
            if os.path.isdir(self.path):
                logger.warning("Path for animation images allready exists: {}", self.path)
            else:
                os.makedirs(self.path)
            
        self.linewidth = 5
        if "linewidth" in kwargs:
            self.linewidth = int(kwargs["linewidth"])
            
        self.extension = "png"
        if "extension" in kwargs:
            self.extension = str(kwargs["extension"])
            
        self.extra_turns = {}
        if "extra_turns" in kwargs:
            self.extra_turns = kwargs["extra_turns"]
            
        self.turtle_size = 0.1 # relative to image
        if "turtle_size" in kwargs:
            self.turtle_size = float(kwargs["turtle_size"])
            
        self.show_turtle = False
        if "show_turtle" in kwargs:
            self.show_turtle = bool(kwargs["show_turtle"])
            
        self.color_palette = cc.b_glasbey_category10
        if "color_palette" in kwargs:
            self.color_palette = kwargs["color_palette"]
        self.current_color = 0
        
        self.palette_lines = False
        if "palette_lines" in kwargs:
            self.palette_lines = bool(kwargs["palette_lines"])
            
        self.steps_per_color = 1
        if "steps_per_color" in kwargs:
            self.steps_per_color = int(kwargs["steps_per_color"])
        self.current_color_step = 0

        self.hold_after = 0
        if "hold_after" in kwargs:
            self.hold_after = float(kwargs["hold_after"])
 
        self.hold_before = 0
        if "hold_before" in kwargs:
            self.hold_before = float(kwargs["hold_before"])
                       
        self.special_angles = []
        if "special_angles" in kwargs:
            self.special_angles = kwargs["special_angles"]
            
        self.special_angle_color = "red"
        if "special_angle_color" in kwargs:
            self.special_angle_color = kwargs["special_angle_color"]
        
        self.special_angle_linewidth = self.linewidth
        if "special_angle_linewidth" in kwargs:
            self.special_angle_linewidth = kwargs["special_angle_linewidth"]
            
        self.turtle_code_window = None
        if "turtle_code_window" in kwargs:
            self.turtle_code_window = kwargs["turtle_code_window"]
        
        self.text = ""
        if "text" in kwargs:
            self.text = kwargs["text"]
        self.font = ImageFont.truetype("./freefont/FreeMonoBold.ttf", size=140)
        
        self.quality_draw = False
        if "quality_draw" in kwargs:
            self.quality_draw = bool(kwargs["quality_draw"])
        
        self.quality_factor = 1
        if "quality_factor" in kwargs:
            self.quality_factor = int(kwargs["quality_factor"])

        if self.quality_factor > 1:
            self.width *= self.quality_factor
            self.height *= self.quality_factor
            self.linewidth *= self.quality_factor
            self.xoffset *= self.quality_factor
            self.yoffset *= self.quality_factor
            self.stepsize *= self.quality_factor / 2
            
        self.reverse = False
        if "reverse" in kwargs:
            self.reverse = bool(kwargs["reverse"])
            
        self.reverse_flip_mirror = False
        if "reverse_flip_mirror" in kwargs:
            self.reverse_flip_mirror = bool(kwargs["reverse_flip_mirror"])
            
        self.background_image = None
        if "background_image" in kwargs:
            self.background_image = kwargs["background_image"]
            
        self.step_counter = False
        if "step_counter" in kwargs:
            self.step_counter = bool(kwargs["step_counter"])
            
    def animate(self):
        """Run the animation"""
        
        self._measure_line_speed()
        self._detect_origin_return()
        self._autoscale()
        
        # even when draw is False, it needs to be true for the turtle to determine how much we draw over the image borders with shifting offsets
        self.es_turtle = Turtle(width=self.width, height=self.height, angle=self.angle, draw=True, scale=self.scale)
        self.es_turtle.linewidth = self.linewidth
        self.es_turtle.xoffset = self.xoffset
        self.es_turtle.yoffset = self.yoffset
        self.es_turtle.quality_draw = self.quality_draw
        if self.background_image is not None:
            self.es_turtle.image = self.background_image
        
        self.es_iteration = 0
        
        self.frames = int(round((self.framerate * self.duration), 0)) + 1
        logger.debug("Creating {} frames for the animation.", self.frames)
        
        self.es_iterations_per_frame = self.iterations / self.frames
        logger.debug("Running {} iterations per frame resulting in {} iteraions", self.es_iterations_per_frame, self.es_iterations_per_frame * self.frames)
        
        self.es_shift_x_per_frame = self.image_speed[0] * self.es_iterations_per_frame
        self.es_shift_y_per_frame = self.image_speed[1] * self.es_iterations_per_frame
        
        logger.debug("Shifting per frame: {}, {}", self.es_shift_x_per_frame, self.es_shift_y_per_frame)
        
        self.es_x_shift = 0
        self.es_y_shift = 0
        
        self.frame = 0
        self._hold_before()
        self.dummy_frames = self.frame

        for _i in range(self.frames):
            self.frame += 1
            self._save_file()
            self._shift_image()
            self._extra_turns()
            """
            for _i in range(self.es_iterations_per_frame):
                self._palette_lines()
                self._move()
                self.es_iteration += 1
            """
            while self.es_iteration < (self.frame - self.dummy_frames) * self.es_iterations_per_frame:
                self._palette_lines()
                self._move()
                self.es_iteration += 1
        
        self._hold_after()
        
        if self.draw:
            logger.debug("Creating shell file to run ffmpeg")
            with open(os.path.join(self.path, "animate.sh"), "w") as file:
                file.write('#! /usr/bin/bash' + "\n" + \
                        'mv $(ls *.png | tail -n 1) ../' + self.name + '.png' + "\n" + \
                        '/usr/bin/ffmpeg -n -pattern_type glob -loglevel error -framerate ' + str(int(self.framerate)) + ' -i "*.' + self.extension + '" -c:v libx264 -pix_fmt yuv420p ' + self.name + '.mp4 && rm *.png && rm *.sh && mv * ..')
   
    def _move(self):
        """Move the turtle"""
        is_special = False
        for angle in self.special_angles:
            if round((self.es_iteration % 360) - (angle % 360), self.precision) == 0:
                is_special = True
                logger.debug("Special angle detected: {}", angle)
                break
        
        if is_special:
            linecolor = self.es_turtle.linecolor
            linewidth = self.es_turtle.linewidth
            self.es_turtle.linecolor = self.special_angle_color
            self.es_turtle.linewidth = self.special_angle_linewidth
        
        self.es_turtle.rotmov(self.theta * self.es_iteration, self.stepsize)
        
        if is_special:
            self.es_turtle.linecolor = linecolor
            self.es_turtle.linewidth = linewidth
        
    def _hold_before(self):
        """Hold first image for additional time, if requested."""
        if self.hold_before > 0:
            for _i in range(int(self.hold_before * self.framerate)):
                self.frame += 1
                self._save_file()
                       
    def _hold_after(self):
        """Hold last images for additional time, if requested."""
        if self.hold_after > 0:
            for _i in range(int(self.hold_after * self.framerate)):
                self.frame += 1
                self._save_file()
        
    def _palette_lines(self):
        """Change line color inbetween steps to make process visible"""
        if not self.palette_lines:
            return
        
        self.current_color = self.current_color % len(self.color_palette)
        
        next_color = self.color_palette[self.current_color].lstrip('#')
        color = tuple(int(next_color[i:i+2], 16) for i in (0, 2, 4))
        self.es_turtle.linecolor = color
        logger.trace("New line color selected {} / #{}", color, next_color)
        
        self.current_color_step += 1
        if self.current_color_step % self.steps_per_color == 0:
            self.current_color += 1      
    
    def _save_file(self):
        """Modify and save image."""
        
        if not self.draw:
            return
        
        image = Image.new('RGBA', (self.width_output, self.height_output), color=self.es_turtle.background)
        image.paste(self.es_turtle.image.resize((self.width_output, self.height_output), Image.Resampling.LANCZOS))
        
        if self.show_turtle:
            turtle = Image.open("./images/turtle.png")
            size = turtle.size
            scale = min(
                self.width_output * self.turtle_size / size[0],
                self.height_output * self.turtle_size / size[1],
            )
            turtle_width = int(round(size[0] * scale, 0))
            turtle_height = int(round(size[1] * scale, 0))
            logger.trace("Rescaling turtle from {}x{} to {}x{}", size[0], size[1], turtle_width, turtle_height)
            turtle = turtle.resize((turtle_width, turtle_height), Image.Resampling.LANCZOS)
            turtle = turtle.rotate((-self.es_turtle.angle - 90) % 360, expand=True)
            size = turtle.size
            image.paste(turtle, (int(self.es_turtle._image_pos()[0] - size[0] / 2), int(self.es_turtle._image_pos()[1] - size[1] / 2)), turtle)
        
        if self.turtle_code_window is not None:
            code = self.turtle_code_window.next()
            image.paste(code, (0,0), code)
            
        if len(self.text) > 0:
            draw = ImageDraw.Draw(image)
            draw.text((20, 10), self.text, font=self.font, fill=(255,255,255))
        
        if self.step_counter:
            show_step = self.es_iteration
            if show_step == 5116:
                show_step = 5120
            elif show_step == 2558:
                show_step = 2560
            draw = ImageDraw.Draw(image)
            draw.text((20, self.height_output - 140 - 10), "# = " + str(show_step), font=self.font, fill=(255,255,255))
            
        filename = os.path.join(self.path, "{:020d}".format(self.frame) + "." + self.extension)
        image.save(filename)
        logger.info("Saving file to {}", filename)
        
        if self.reverse:
            if self.reverse_flip_mirror:
                image = ImageOps.mirror(image)
                image = ImageOps.flip(image)
            filename = os.path.join(self.path, "{:020d}".format(100000000000000000000 - self.frame) + "." + self.extension)
            image.save(filename)
            logger.info("Saving reverse file to {}", filename)
              
    def _extra_turns(self):
        """Rotate on given frame if required to draw images."""
        if self.frame in self.extra_turns:
            self.es_turtle.rotate(self.extra_turns[self.frame])
            logger.debug("Adding extra rotation by {} degree in frame {}.", self.extra_turns[self.frame], self.frame)
        
    def _shift_image(self):
        """Shift the image and the offset"""
        if self.image_speed != (0, 0):
            x_target = int(round(self.frame * self.es_shift_x_per_frame, 0))
            y_target = int(round(self.frame * self.es_shift_y_per_frame, 0))
            
            x_go = int(x_target - self.es_x_shift)
            y_go = int(y_target - self.es_y_shift)
            
            if self.draw:
                image = Image.new('RGB', (self.es_turtle.width, self.es_turtle.height), color=self.es_turtle.background)
                image.paste(self.es_turtle.image, (-1 * x_go, -1 * y_go))
                self.es_turtle.image.paste(image)
            
            self.es_turtle.xoffset -= x_go
            self.es_turtle.yoffset -= y_go
            
            self.es_x_shift += x_go
            self.es_y_shift += y_go
        
    def _autoscale(self):
        """Autoscale if requested, only for non moving images"""
        if not self.autoscale:
            return
        
        if self.image_speed is None:
            self._measure_line_speed()
            
        if self.image_speed == (0,0):
            used_height = self.turtle.ymax - self.turtle.ymin
            used_width = self.turtle.xmax - self.turtle.xmin
            self.scale = min(self.width * (1 - self.border) / used_width, self.height * (1 - self.border) / used_height)
        else:
            logger.warning("Autoscaling not implemented due to moving image.")
        
    def _detect_origin_return(self):
        """Dry run to correct number of iterations for origin return"""
        if not self.detect_origin_return:
            return
        
        if self.turtle.last_origin:
            self.iterations = self.turtle.step_num
            logger.debug("Origin return detected. iterations reduced to {}", self.iterations)

    def _measure_line_speed(self) -> None:
        """Measure the speed that an euler spiral line progresses with."""
        if self.image_speed is not None:
            return
        
        final = [
            self.iterations,
            round(self.turtle.xmin / self.iterations, self.precision),
            round(self.turtle.xmax / self.iterations, self.precision),
            round(self.turtle.ymin / self.iterations, self.precision),
            round(self.turtle.ymax / self.iterations, self.precision),
            ]
        
        xspeed = 0
        if final[1] == 0 and final[2] != 0:
            logger.debug("xmin speed == 0")
            xspeed = final[2]
        if final[2] == 0 and final[1] != 0:
            logger.debug("xmax speed == 0")
            xspeed = final[1]
            
        yspeed = 0
        if final[3] == 0 and final[4] != 0:
            logger.debug("ymin speed == 0")
            yspeed = final[4]
        if final[4] == 0 and final[3] != 0:
            logger.debug("ymax speed == 0")
            yspeed = final[3]
        
        logger.debug("Individual speeds: +x={}, -x={}, +y={}, -y={}", final[2], final[1], final[4], final[3])
        logger.debug("Detected image speeds: x-speed={}, y-speed={}", xspeed, yspeed)
        self.image_speed = (xspeed, yspeed)
        