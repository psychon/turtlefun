"""src/turtlefun/turtle_slideshow.py"""

from loguru import logger
from PIL import Image, ImageFont, ImageDraw
import os
from typing import Tuple

class TurtleSlideshow:
    """Create a turtle slideshow with theta values dropping down."""
    
    def __init__(self, width:int, height:int) -> None:
        
        self.width = width 
        self.height = height
            
        self.current_frame = 0
        
        self.background_image = Image.new('RGBA', (self.width, self.height), color=(0, 0, 0))
        
        self.text_color = 'white'
        self.text_size = 100
        self.text_font = ImageFont.truetype("./freefont/FreeMonoBold.ttf", size=self.text_size)
        
        self.text_xpos_start = 50
        self.text_ypos_start = 5
        
        self.text_x_speed = 0
        self.text_y_speed = 5
        
        self.text = []
        
    def add_text(self, text:str) -> None:
        """Drop new element for the next frame"""
        self.text.append((self.current_frame, text))
    
    def replace_background(self, image:Image, offset:Tuple[int] = (0, 0)) -> None:
        """Place a new background image"""
        self.background_image = Image.new('RGBA', (self.width, self.height), color=(0, 0, 0))
        self.background_image.paste(image, offset)
    
    def next(self):
        """Get the next frame."""
        image = Image.new('RGBA', (self.width, self.height))
        image.paste(self.background_image)
        text = self._create_text_image()
        image.paste(text, (0,0), text)
        self.current_frame += 1
        return image
        
    def _create_text_image(self) -> Image:
        """Create the text image with the given text loactions."""
        image = Image.new('RGBA', (self.width, self.height))
        draw = ImageDraw.Draw(image)
        
        for frame, text in self.text:
            x = self.text_xpos_start + self.text_x_speed * (self.current_frame - frame)
            y = self.text_ypos_start + self.text_y_speed * (self.current_frame - frame)
            draw.text((x, y), text, font=self.text_font, fill=self.text_color)
            
        return image
        