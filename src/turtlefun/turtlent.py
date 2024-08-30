"""src/turtlefun/turtlent.py"""

from decimal import Decimal, getcontext
import itertools
from loguru import logger
import math
import os
from PIL import Image, ImageDraw
from sympy import nextprime
from time import perf_counter
from typing import Union, List, Tuple

from .turtlefun_quotientlist import TURTLEFUN_QUOTIENT_LIST

DEFAULT_IMAGE_WIDTH = 2560
DEFAULT_IMAGE_HEIGHT = 1440

def decimal_places(number:Union[float, str, Decimal, int]) -> int:
    """Determine the number of relevant decimal places in a number"""
    
    number = str(number).strip("0")
    
    exponent = None
    if "E" in number:
        number, exponent = number.split("E")
    elif "e" in number:
        number, exponent = number.split("e")
    
    decimal = None
    if "." in number:
        number, decimal = number.split(".")
        
    number_of_decimals = 0
    
    if exponent is not None:
        number_of_decimals -= float(exponent)
        
    if decimal is not None:
        number_of_decimals += len(decimal)
        
    if number_of_decimals < 0:
        number_of_decimals = 0
        
    return int(number_of_decimals)

class TurtleNT:
    """New Technology Turtle with some of the thoughts out of the Euler Spiral development"""
    
    def __init__(
        self,
        theta:Union[str, int, float, Decimal],
        image_background:Union[str, Tuple[int], None] | None = "black",
        image_fileformat:str | None = "png",
        image_height:int | None = DEFAULT_IMAGE_HEIGHT,
        image_linecolor:Union[str, Tuple[int]] | None = "white",
        image_linewidth:int | None = 3,
        image_width:int | None = DEFAULT_IMAGE_WIDTH,
        image_x_offset:int | None = None,
        image_y_offset:int | None = None,
        path:str | None = "./turtlefun_images",
        steplimit:int | None = 100000000,
        stepsize:Union[int, float] | None = 100,
    ) -> None:
        """Create a turtle that is specialized in Euler Spirals
        
        Args:
            image_background (str, Tuple(int), None): Color of background, if None, RGBA is used for Mode instead of RGB
            image_fileformat (str): file format for saving of image file
            image_height (int): height of the images to be created
            image_linecolor (str, Tuple(int)): Color of the foreground drawing
            image_linewidth (int): width of the turtle lines
            image_width (int): with of the images to be created
            image_x_offset (int): x-offset in image for center of the turtle
            image_y_offset (int): y_offset in image for center of the turtle
            path (str): path to store images in
            stepsize (float, int): stepsize to take when moving the turtle
            theta (str, int, float, Decimal): Euler Spiral base angle theta
        """
        
        self._theta = None
        self.set_theta(theta)
        
        self.path = os.path.join(path, "")
        
        self.image_width = image_width
        self.image_height = image_height
        self.image_x_offset = image_x_offset if image_x_offset is not None else int(round(self.image_width / 2, 0))
        self.image_y_offset = image_y_offset if image_y_offset is not None else int(round(self.image_height / 2, 0))
        self._image = None
        self._image_draw = None
        
        self.image_background = image_background
        self.image_linecolor = image_linecolor
        self.image_linewidth = image_linewidth
        self.image_fileformat = image_fileformat

        self._origin_return_estimation = None
        self._origin_return_estimation_theta = None
        self._origin_return_dominant_angles = None

        self.stepsize = stepsize
        self.steplimit = steplimit
        self._xpos_list = [Decimal('0')]
        self._ypos_list = [Decimal('0')]
        self._xmax = None
        self._xmin = None
        self._ymax = None
        self._ymin = None
        self._minmax_step_num = None
        
        self._scale = None
        
        self._angle = None
        self.set_angle('0')
        self._step_num = Decimal('0')
    
    def _angle_cleanup(self) -> None:
        """Clean up _angle to be within 360°"""
        self._angle = self._angle % Decimal('360')
        
    def _autoscale(self) -> Decimal:
        """Calculate autoscale factor to position drawing within canvas
        boundaries, while keeping the origin at the center position."""
        self._calculate_min_max_positions()
        
        xmax = getcontext().abs(getcontext().max_mag(self._xmax, self._xmin))
        xscale = ((self.image_width / Decimal('2')) / xmax) if xmax != 0 else Decimal('1')
        
        ymax = getcontext().abs(getcontext().max_mag(self._ymax, self._ymin))
        yscale = ((self.image_height / Decimal('2')) / ymax) if ymax != 0 else Decimal('1')
        
        scale = getcontext().min(xscale, yscale)
        logger.debug("Scaling factor determined for plotting is {}", scale)
        return scale
        
    def _calculate_min_max_positions(self) -> None:
        """Calculate xmax, xmin, ymax, ymin"""
        if self._minmax_step_num == self._step_num and \
            self._xmax is not None and \
                self._xmin is not None and \
                    self._ymax is not None and \
                        self._ymin is not None:
            return
        
        self._xmax = self._xpos_list[0]
        self._xmin = self._xpos_list[0]
        for x in self._xpos_list:
            self._xmax = Decimal.max(self._xmax, x)
            self._xmin = Decimal.min(self._xmin, x)
            
        self._ymax = self._ypos_list[0]
        self._ymin = self._ypos_list[0]
        for y in self._ypos_list:
            self._ymax = Decimal.max(self._ymax, y)
            self._ymin = Decimal.min(self._ymin, y)
            
        self._minmax_step_num = self._step_num
        
        logger.debug("Boundary corners at {} steps are ({}, {}), ({}, {})", self._minmax_step_num, self._xmin, self._ymin, self._xmax, self._ymax)
        
    def _clear_image(self) -> None:
        """Create a clean new image canvas."""
        if self.image_background is None:
            self._image = Image.new("RGBA", (self.image_width, self.image_height))
        else:
            self._image = Image.new("RGB", (self.image_width, self.image_height), self.image_background)
        self._image_draw = ImageDraw.Draw(self._image)
    
    def _draw_line(self, x1:Union[int, float], y1:Union[int, float], x2:Union[int, float], y2:Union[int, float]) -> None:
        """Draw a line"""
        self._image_draw.line((x1 + self.image_x_offset, y1 + self.image_y_offset, x2 + self.image_x_offset, y2 + self.image_y_offset), fill=self.image_linecolor, width=self.image_linewidth)
        self._draw_point(x2, y2)
       
    def _draw_point(
        self,
        x:Union[int, float],
        y:Union[int, float],
        width:int | None = None,
        color:Union[str, Tuple[int]] | None = None,
        ) -> None:
        """Draw a point of linewidth diameter at the given position"""
        if width is None:
            width = self.image_linewidth - 2
        if color is None:
            color = self.image_linecolor
            
        radius = int(round((width) / 2, 0))
        x1 = x - radius + self.image_x_offset
        x2 = x1 + width
        y1 = y - radius + self.image_y_offset
        y2 = y1 + width
        
        self._image_draw.ellipse((x1, y1, x2, y2), fill=color)
           
    def rotate(self) -> None:
        """Rotate turtle by theta"""
        self._angle += self._theta * self._step_num
        self._angle_cleanup()
    
    def forward(self) -> None:
        """Move Turtle forward by stepsize
        
        The functions utilizes the math.sin and math.cos function,
        as the extra precision is way to costly in terms of computing power.
        """
        
        rad = math.radians(float(self._angle))
        self._xpos_list.append(self._xpos_list[-1] + Decimal(str(math.cos(rad))) * self.stepsize)
        self._ypos_list.append(self._ypos_list[-1] + Decimal(str(math.sin(rad))) * self.stepsize)
        
        self._step_num += 1
    
    def is_home(self) -> bool:
        """Returns true, if the current final positions is close to the home position"""
        x = self._xpos_list[-1]
        y = self._ypos_list[-1]
        dist = self.stepsize
        
        logger.debug("Evaluating home for ({}, {}) and distance {} at angle {}", x, y, dist, self._angle)
        
        if not (self._angle < Decimal('0.5') and self._angle >= Decimal('0') or \
            self._angle <= Decimal('360') and self._angle > Decimal('359.5')):
            logger.debug("Angle {} not in applicable range 359.5° - 0.5°", self._angle)
            return False
        
        if x < -dist:
            logger.debug("X is to small")
            return False
        if x > dist:
            logger.debug("X is to big")
            return False
        if y < -dist:
            logger.debug("Y is to small")
            return False
        if y > dist:
            logger.debug("Y is to big")
            return False
        
        return True
    
    def _euler_spiral(self, total_steps:Union[int, str, Decimal]) -> None:
        """Go forward in euler spiral until total number of steps reaches total_steps
        
        Return:
            duration of euler spiral run
        """
        
        timer_start = perf_counter()
        step_start = self._step_num
        
        if type(total_steps) is not Decimal:
            total_steps = Decimal(str(total_steps))
            
        if total_steps >= self.steplimit:
            return False
        
        logger.debug("Current step number: {}", self._step_num)
        while self._step_num < total_steps and self._step_num <= self.steplimit:
            self.rotate()
            self.forward()
            
            if self._step_num % 100000 == 0:
                steps_per_second = float(self._step_num - step_start) / (perf_counter() - timer_start)
                logger.debug("Advanced to step {} out of {}, remaining time estimate {}s", self._step_num, total_steps, float(total_steps - self._step_num) / steps_per_second)
    
        timer_stop = perf_counter()
        logger.debug("Total duration of Euler Sprial run was {}s", timer_stop - timer_start)
        
        if self._step_num >= self.steplimit:
            logger.warning("Eulerspiral stopped during execution! Steplimit {} reached!", self.steplimit)
            return False
        return True
    
    def euler_spiral(
        self,
        total_steps:Union[int, str, Decimal, None] | None = None
        ) -> None:
        """Go forward in euler spiral until total number of steps reaches total_steps
        
        Return:
            duration of euler spiral run
        """
        return_value = None
        if total_steps is not None:
            self._euler_spiral(total_steps)
        else:
            for total_steps in sorted(self.origin_return_estimation()):
                if total_steps <= 1:
                    continue
                return_value = self._euler_spiral(total_steps)
                if self.is_home():
                    break
                if not return_value:
                    break
                    
        if self.is_home():
            logger.success("Turtle did return home after {} steps", self._step_num)
        else:
            logger.success("Turtle did not return home after {} steps", self._step_num)
        return return_value
    
    def file_exists(self) -> bool:
        """Estimate if the image file already exists."""
        path = self.get_path()
        
        file = None
        for file in os.listdir(path):
            if file.endswith("." + self.image_fileformat) and \
                file.startswith("tfnt" + "_" + "{:012.8f}".format(self._theta)):
                logger.debug("Image file found the represents theta={}: {}", self._theta, file)
                return True
        return False
                
    def get_angle(self) -> Decimal:
        """Return the current angle of the turtle"""
        return self._angle
    
    def set_angle(self, angle:Union[int, float, str, Decimal]) -> None:
        """Set the angle of the turtle"""
        self._angle = Decimal(str(angle))
    
    def get_path(self) -> str:
        """Create path and return path string."""
        theta_str = "{:0.8}".format(float(self._theta)).split(".")
        path = os.path.join(self.path, theta_str[0] + "-" + theta_str[1][:1])
        
        os.makedirs(path, exist_ok=True)
        
        return path
      
    def get_filename(self) -> str:
        """Autogenerate a filename"""
        
        filename = "tfnt"
        filename += "_" + "{:012.8f}".format(self._theta)
        filename += "_" + "{:.4f}".format(float(self._scale))
        filename +=    "_" + str(self._step_num)
        filename += "_origin-return" if self.is_home() else ""
        filename += "." + self.image_fileformat
        
        return os.path.join(self.get_path(), filename)
        
    def get_image(
        self,
        autoscale:bool | None = True,
        force_redraw:bool | None = False,
        mark_origin:bool | None = False,
    ) -> Image:
        """Create image from current position list.
        Returns last image, if image exists, except farce_redraw == True
        
        Args:
            autoscale (bool): Scale the turtle positions to fit into image size
            force_redraw (bool): Redraw image, even an image exists allready.
            mark_origin (bool): draw a red dot at the origin position of the turtle.
        """
        if type(self._image) is Image and not force_redraw:
            return self._image
        
        logger.debug("Drawing new {}x{} image.", self.image_width, self.image_height)
        if len(self._xpos_list) != len(self._ypos_list):
            logger.critical("x and y lists are not of equal length!")
            exit(1)
        
        timer_start = perf_counter()
        self._clear_image()
        scale = Decimal('1.0')
        if autoscale:
            scale = self._autoscale()
        self._scale = scale
            
        self._draw_point(self._xpos_list[0], self._ypos_list[0])
        for index in range(len(self._xpos_list) - 1):
            self._draw_line(
                self._xpos_list[index] * scale,
                self._ypos_list[index] * scale,
                self._xpos_list[index + 1] * scale,
                self._ypos_list[index + 1] * scale
                )
            if index % 100000 == 0 and index > 0:
                steps_per_second = index / (perf_counter() - timer_start)
                logger.debug("Drawing step {} out of {}, remaining time estimate {}s", index, len(self._xpos_list), float(len(self._xpos_list) - index) / steps_per_second)
        
        if mark_origin:
            self._draw_point(0, 0, 4 * self.image_linewidth, "red")
        
        return self._image
      
    def get_pos(self) -> Tuple[Decimal]:
        """Return the current position of the turtle"""
        return (self._xpos_list[-1], self._ypos_list[-1])
    
    def get_steps(self) -> Decimal:
        """Return current step count"""
        return self._step_num
    
    def get_theta(self) -> Decimal:
        """Return the current theta value"""
        return self._theta
    
    def set_theta(self, theta:Union[int, float, str, Decimal]) -> None:
        """Set a new theta value"""
        self._theta = Decimal(str(theta))
        
    def get_xmax(self) -> Decimal:
        """Maximum xposition reached"""
        self._calculate_min_max_positions()
        return self._xmax
    
    def get_xmin(self) -> Decimal:
        """Minimum xposition reached"""
        self._calculate_min_max_positions()
        return self._xmin
    
    def get_ymax(self) -> Decimal:
        """Maximum yposition reached"""
        self._calculate_min_max_positions()
        return self._ymax
    
    def get_ymin(self) -> Decimal:
        """Minimum yposition reached"""
        self._calculate_min_max_positions()
        return self._ymin
    
    def save_image(
        self,
        filename:str | None = None,
        ) -> None:
        """Store the image to file"""
        
        image = self.get_image()
        
        if filename is None:
            filename = self.get_filename()
            
        logger.info("Storing image file at {}", filename)
        image.save(filename)
    
    def dominant_angles(self) -> List[Decimal]:
        """Return the dominant angles of theta"""
        
        if self._origin_return_estimation is None or \
            self._origin_return_dominant_angles is None or \
            self._origin_return_estimation_theta != self._theta:
                self.origin_return_estimation()
                
        return self._origin_return_dominant_angles
        
    def origin_return_estimation(self) -> List[Decimal]:
        """Estimate the origin return steps of the projects theta value"""
        
        if self._origin_return_estimation is not None and \
            self._origin_return_estimation_theta == self._theta:
                return self._origin_return_estimation
        
        self._origin_return_estimation_theta = self._theta
        self._origin_return_estimation = []
        
        analyze = self._theta
        theta_decimals = decimal_places(analyze)
        
        self._origin_return_dominant_angles = []
        quotients = []
        int_quotients = []
        
        # Identify the dominant angles
        for angle, quotient, _a in TURTLEFUN_QUOTIENT_LIST:
            
            angle_decimal = decimal_places(angle) 
            if angle_decimal > theta_decimals:
                continue
            
            while analyze >= angle:
                self._origin_return_dominant_angles.append(angle)
                quotients.append(quotient)
                int_quotients.append(int(quotient))
                analyze -= angle
                
            if analyze <= 0:
                break
        
        lcm = math.lcm(*int_quotients) # least common multiple

        cycle_angle_rot_sum = (Decimal(lcm) * (Decimal(lcm) + Decimal('1')) / Decimal('2'))
        cycle_angle = Decimal(cycle_angle_rot_sum) * Decimal(str(self._theta)) % Decimal('360')
        
        required_cycles = Decimal('1')
        while (required_cycles * cycle_angle) % Decimal('360') != 0:
            required_cycles += Decimal('1')
        steps_upper_limit = lcm * required_cycles
        
        # somehow the calculated steps are an upper limit for the experimental steps.
        # let's get the prime factors of the calculated steps and create a list of the
        # possible origin return steps.
        
        primes = []
        prime = 1
        steps = steps_upper_limit
        while True:
            prime = nextprime(prime)
            while round(steps / Decimal(str(prime)), 0) == steps / Decimal(str(prime)):
                steps /= Decimal(str(prime))
                primes.append(Decimal(str(prime)))
            
            if steps == 1:
                break
            if prime > steps:
                logger.critical("Failed to calculate prime factors!")
                exit(1)
        
        combination = []
        for r in range(1, len(primes) + 1):
            combination += itertools.combinations(primes, r)
        
        logger.trace("Identified prime combinations for {} are {}", steps_upper_limit, combination)
        
        self._origin_return_estimation = [steps_upper_limit]
        for primelist in combination:
            prime = math.prod(primelist)
            steps = steps_upper_limit / Decimal(str(prime))
            if steps not in self._origin_return_estimation and \
                (steps * (steps + Decimal('1')) / Decimal('2') * Decimal(str(self._theta))) % Decimal('360') == 0:
                    self._origin_return_estimation.append(steps)

        return self._origin_return_estimation
