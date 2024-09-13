"""srce/turtle.py"""

#import colorcet as cc
from configparser import ConfigParser
import math
import os
#from PIL import Image
#from PIL.ImageDraw import Draw
#from prettytable import PrettyTable
import sys
from time import perf_counter

#from loguru import logger
from typing import Union, Tuple
import logging
logger = logging.getLogger(__name__)
def logger_trace(*x):
    pass
logger.trace = logger_trace

from .qualityldraw import QualityDraw

class TurtleHome:
    """Support data to determine origin return on complex theta values"""
    
    def __init__(self, home_size:float = 3) -> None:
        
        self.home_size = home_size
        
        self.step_num = 0
        
        self.is_home = True
        self.home_id_count = {}
        
        self.color_palette = ["#000000"] # cc.b_glasbey_category10
        self.current_color = 0
        self.color = None
        self._set_color()
        self.used_colors = 1
        
        self.home_id = 0
        self.home_id_steplimit = 100
        self.home_id_count[self.home_id] = {"steps": 0, "total": self.step_num, "color": self.color}
        
    def _set_color(self):
        self.color = tuple(int(self.color_palette[self.current_color].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
    def check(self, xpos, ypos, iteration):
        home_now = abs(math.dist((0, 0), (xpos, ypos))) < self.home_size
        
        if home_now is not self.is_home:
            self.is_home = home_now
            
            self.home_id_count[self.home_id]["total_end"] = self.step_num
            
            self.home_id += 1
            self.current_color += 1
            self.current_color = self.current_color % len(self.color_palette)
            self._set_color()
            logger.trace("New line color is {}", self.color)
            
        if self.home_id not in self.home_id_count:
            self.home_id_count[self.home_id] = {"steps": 0, "total": self.step_num, "color": self.color}
        
        self.home_id_count[self.home_id]["steps"] += 1
        self.step_num += 1
        
        return self.color
    
    def estimate_homereturn(self):
        self.home_id_count[self.home_id]["total_end"] = self.step_num
        pass
            
    def print(self) -> str:
        
        self.estimate_homereturn()
                
        prstr = ""
        
        prstr += "Entries and exits out of the home base.\n"
        prstr += "Home size is " + "{:0.2f}".format(self.home_size) + "\n\n"
        
        prstr += "Home id step limit is " + str(self.home_id_steplimit) + "\n"
        
        table = PrettyTable()
        table.field_names = ["home id", "steps", "total at start", "total at end", "color"]
        
        for key in self.home_id_count:
            steps = self.home_id_count[key]["steps"]
            total = self.home_id_count[key]["total"]
            total_end = self.home_id_count[key]["total_end"]
            color = self.home_id_count[key]["color"]
            if steps > self.home_id_steplimit:
                table.add_row([key, steps, total, total_end, color])
        prstr += table.get_string()
        return prstr
            
        
class Turtle:
    """Very basic turtle class that creates a pixel graphic
    and tracks so position of the turtle"""

    def __init__(self, **kwargs) -> None:
        """Initialize turtle
        
        Args:
            width (int): Width of the generated pixel image
            height (int): height of the generated pixel image
            angle (float, int): starting angle of turtle
            draw (bool): draw image of turtle if True
            scale (float, int): scale drawing by scale
        """
        self._init_image_parameters()
        self._init_turtle_parameters()       
        self._init_kwargs(kwargs)
        
        self._angle_cleanup()
        self._check_configuration()
        self._init_image()
        
    def _init_turtle_parameters(self) -> None:
        """Initialize the parameters for the turtle run."""
        self.angle = 0.0
        self.xpos = 0.0
        self.ypos = 0.0
        
        self.xmax = 0.0
        self.ymax = 0.0
        self.xmin = 0.0
        self.ymin = 0.0
        self.image_xmax = 0.0
        self.image_ymax = 0.0
        self.image_xmin = 0.0
        self.image_ymin = 0.0
        self.step_num = 0
        
        self.precision_pos = 1e-5
        self.precision_angle = 1e-2
        
        self.last_theta = None
        self.last_config = None
        self.last_origin = None
        
    def _init_image_parameters(self) -> None:
        """Initialize the image generation parameters."""
        self.draw = False
        self.image = None
        self.image_extension = "png"
        self.image_default_path = "./"
        self.width = 3840  # for testing: multiple of 10
        self.height = 2160 # for testing: multiple of 10
        self.scale = 1
        self.background = (0, 0, 0)
        self.linecolor = (255, 255, 255)
        self.linewidth = 1
        self.home_color_change = False
        self.quality_draw = False
        
    def _create_config(self) -> None:
        """Create a config file with information on the euler spiral run."""
        self.last_config = ConfigParser()
        es = "es_config"
        self.last_config.add_section(es)
        for key, value in [
            ("angle", self.angle),
            ("xpos", self.xpos),
            ("ypos", self.ypos),
            ("precision_pos", self.precision_pos),
            ("precision_angle", self.precision_angle),
            ("last_theta", self.last_theta),
            ("step_num", self.step_num),
            ("draw", self.draw),
            ("image_extension", self.image_extension),
            ("image_default_path", self.image_default_path),
            ("width", self.width),
            ("height", self.height),
            ("scale", self.scale),
            ("background", self.background),
            ("linecolor", self.linecolor),
            ("linewidth", self.linewidth),
        ]:
            self.last_config.set(es, key, str(value))
        
    def _init_image(self) -> None:
        """Initialize image, if drawing is requested."""
        if self.draw:
            self.image = Image.new('RGB', (self.width, self.height), color=self.background)

    def _init_kwargs(self, kwargs:dict) -> None:
        """Initialize Turtle using kwargs variables"""

        if "width" in kwargs:
            self.width = int(kwargs["width"])

        if "height" in kwargs:
            self.height = int(kwargs["height"])

        if "angle" in kwargs:
            self.angle = float(kwargs["angle"])
            
        if "draw" in kwargs:
            self.draw = bool(kwargs["draw"])
            
        if "scale" in kwargs:
            self.scale = float(kwargs["scale"])
            
        self.home_size = 20
        if "home" in kwargs:
            self.home_size = float(kwargs["home"])
        self.home_analysis = TurtleHome(self.home_size)   
            
        self.xoffset = int(self.width / 2)
        self.yoffset = int(self.height / 2)

    def _check_configuration(self) -> None:
        """Check configuration and warn on problems
        try to keep running no matter what"""

        if self.width < 100 or self.height < 100:
            logger.warning("Image is only {}x{} and probably way to small!", self.width, self.height)
            
        if self.scale < 0:
            logger.warning("Scaling for drawing is negative!")  
        elif self.scale == 0:
            logger.warning("Scaling for drawing is zero, noting will be drawn")

    def _angle_cleanup(self) -> None:
        """Clean up angle"""
        self.angle = self.angle % 360
        
    def _image_pos(self) -> None:
        """Return current Turtle position in image"""
        return (int(self.xpos * self.scale + self.xoffset), int(self.ypos * self.scale + self.yoffset))
    
    def get_pos(self) -> Tuple[Union[int,float], Union[int, float]]:
        """Return current turtle position"""
        return (self.xpos, self.ypos)

    def forward(self, step:Union[int, float]) -> None:
        """Move turtle in direction of angle

        Args:
            step (int, float): Distance to move forward
        """
        if self.draw:
            frompos = self._image_pos()

        rad = math.radians(self.angle)
        self.xpos += math.cos(rad) * step
        self.ypos += math.sin(rad) * step
        
        self.step_num += 1
        
        self.xmax = max(self.xmax, self.xpos)
        self.ymax = max(self.ymax, self.ypos)
        self.xmin = min(self.xmin, self.xpos)
        self.ymin = min(self.ymin, self.ypos)
        
        col = self.home_analysis.check(self.xpos, self.ypos, self.step_num)
        
        if self.draw:
                    
            if self.home_color_change:
                self.linecolor = col
            
            if self.quality_draw:
                QualityDraw(self.image).line((frompos, self._image_pos()), fill=self.linecolor, width=self.linewidth)
            else:
                Draw(self.image).line([frompos, self._image_pos()], fill=self.linecolor, width=self.linewidth)
            
            x, y = self._image_pos()
            self.image_xmax = max(self.image_xmax, x)
            self.image_xmin = min(self.image_xmin, x)
            self.image_ymax = max(self.image_ymax, y)
            self.image_ymin = min(self.image_ymin, y)

    def rotate(self, angle:Union[int, float]) -> None:
        """Rotate turtle

        Args:
            angle (int,float): Rotate by angle in degree
        """
        self.angle += angle
        self._angle_cleanup()

    def rotmov(self, angle:Union[int, float], step:Union[int, float]) -> None:
        """Rotate turtle and step forward

        Args:
            angle (int,float): Rotate by angle in degree
            step (int, float): Distance to move forward
        """
        self.rotate(angle)
        self.forward(step)

    def euler_spiral(self, theta:Union[int, float], iterate:int, step:Union[int, float] = 10) -> None:
        """Create an Euler spiral
        
        see: https://www.youtube.com/watch?v=kMBj2fp52tA for explanation and inspiration
        
        Create an Eurler spiral. Detect return to original start point with given precision
        
        Args:
            theta (int, float): Angle to rotate by
            iterate (int): Maximum number of iterations
            step (int, float): Steps to move forward, default = 10
        """
        timer_start = perf_counter()
        self.last_theta = theta
        self._create_config()
        origin = False
        
        (fromxpos, fromypos) = self.get_pos()
        fromangle = self.angle
        
        for iteration in range(iterate):
            self.rotmov(iteration * theta, step)
            
            theta_change = iteration * theta % 360
            print(f"After {iteration}, ({self.xpos}, {self.ypos}) with {self.angle} after change of {theta_change}")
            if theta_change == 0:
                print("Z" * 30)
            if self.angle == 0:
                print("Y" * 30)
            if self.angle == 180:
                print("X" * 30)
            if abs(fromangle - self.angle) < self.precision_angle:
                if abs(fromxpos - self.xpos) < self.precision_pos and \
                    abs(fromypos - self.ypos) < self.precision_pos:
                        logger.info("Euler spiral has returned to origin.")
                        print("Origin!")
                        origin = True
                        break
        timer_stop = perf_counter()
        
        if origin:
            self.last_origin = origin
        
        es = "es_results"
        self.last_config.add_section(es)
        for key, value in [
            ("step_num", self.step_num),
            ("timer_start", timer_start),
            ("timer_stop", timer_stop),
            ("timer_time", (timer_stop - timer_start)),
            ("iterate", iterate),
            ("theta", theta),
            ("step", step),
            ("origin_return", origin),
            ("xpos", self.xpos),
            ("ypos", self.ypos),
            ("xmin", self.xmin),
            ("xmax", self.xmax),
            ("ymin", self.ymin),
            ("ymax", self.ymax),
            ("angle", self.angle),
        ]:
            self.last_config.set(es, key, str(value))

    def autoscale(self, border:float = 0.0) -> float:
        """Calculate autoscaling parameter to user drawing area more effective.
        Requirese reruning routine with new scaling parameter
        
        Args:
            border (float): keep border while scaling (given in factor of width/heigt,
                            0: no-border, 1: only border)
        """
        
        s = self.scale
        y_used = 2 * max(abs(s * self.ymin), abs(s * self.ymax))
        x_used = 2 * max(abs(s * self.xmin), abs(s * self.xmax))
        
        logger.debug("Autoscaling with x_used {} and y_used {}", x_used, y_used)
        
        scale = None
        
        if y_used < 3 and x_used < 3:
            scale = 1
        elif y_used < 3 and x_used >= 3:
            scale = self.width * (1-border) / x_used
        elif x_used < 3 and y_used >= 3:
            scale = self.height * (1-border) / y_used
        else:
            scale = min(self.width * (1-border) / x_used, self.height * (1-border) / y_used)
        
        logger.debug("Auto scaling factor determined: {}", scale)
        
        return scale
    
    def create_filename(self, path:Union[None, str]=None, extension:Union[None, str]=None) -> str:
        """Generate parameter based filename"""
        if path is None:
            path = self.image_default_path
        
        basename = "tf_"
        if self.last_theta is not None:
            basename += "{:012.8f}".format(float(self.last_theta)) + "_"
            
        basename += "{:.4f}".format(self.scale) + "_"
            
        basename += str(self.step_num)
        
        if self.last_origin is True:
            basename += "_origin-return"
        
        basename += "."
        if extension is None:
            basename += self.image_extension
        else:
            basename += extension
            
        return os.path.join(path, basename)

    def save(self, filename:Union[str, None] = None, path:Union[str, None] = None) -> bool:
        """Store drawn image to file
        
        Args:
            filename (str): Filename of created file
            path (str): Path to use for filename creation
        
        Returns:
            False if no image was available, True otherwise
        """
        if self.image is None:
            logger.info("No image data created. Image cannot be saved.")
            return False
        
        if path is None:
            path = self.image_default_path
        
        if filename is None:
            filename = self.create_filename(path, self.image_extension)
            config_filename = self.create_filename(path, "ini")
        else:
            filename = os.path.join(path, filename)
            config_filename = os.path.join(path, filename + ".ini")
        
        logger.info("Storing image in {}", filename)
        self.image.save(filename)
        if self.last_config is not None:
            logger.info("Storing config information in {}", config_filename)
            self.last_config.write(open(config_filename, "w"))
        
        return True


if __name__ == "__main__":
    t =Turtle(draw=False, home=10)
    for theta in [15, 16]:
        print(f"theta={theta}")
        t.euler_spiral(theta, 50, 1)
        print()
