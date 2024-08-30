"""/src/turtlefun/turtle_codewindow.py"""

from loguru import logger
from PIL import Image, ImageDraw, ImageFont
        
class TurtleCodeWindow:
    """Animate a Code Window coming in and going out"""
    
    def __init__(self, width:int, height:int, xpos:int, ypos:int, duration:float, framerate:int, iterations:int, theta:float, stepsize:int, static:bool = False) -> None:
        """Initialize Turtle Code Window"""
        
        self.width = width
        self.height = height
        self.duration = duration
        self.framerate = framerate
        self.theta = theta
        self.iterations = iterations
        self.stepsize = stepsize
        self.static = static
        
        self.text = "REPEAT " + str(self.iterations) + " [\n RT # * " + str(self.theta) + "\n FD " + str(stepsize) + "\n]"
        self.text_cursor = "█"
        self.cursor_on = True
        self.cursor_mod = 30
        self.font = ImageFont.truetype("./freefont/FreeMonoBold.ttf", size=60)
        self.lineheight = 85
        logger.debug("Lineheight for text is {}", self.lineheight)
        
        self.code_xpos_target = xpos
        self.code_ypos_target = ypos
        
        self.step_total = self.duration * self.framerate
        
        self.step_num = 0
        
        self.mode_status = {}
        self.mode_current = 0
        
        self.image = None
        self._clear_image()
        
        self.code_head = Image.open("./images/Code-Window-head.png")
        self.code_center = Image.open("./images/Code-Window-center.png")
        self.code_foot = Image.open("./images/Code-Window-foot.png")
        
        self.code_width = self.code_center.size[0]
        self.code_height = self.code_head.size[1] + self.code_center.size[1] + self.code_foot.size[1]
        
        if self.code_xpos_target >= self.width / 2:
            self.code_xpos_start = self.width
        else:
            self.code_xpos_start = -self.code_center.size[0]
            
        self.code_xpos = self.code_xpos_start
        self.code_ypos = self.code_ypos_target
        
        if self.static:
            self.cursor_on = False
            self.code_xpos = self.code_xpos_target
            self.code_ypos = self.code_ypos_target
            
            text_image = self._type_text()
            self._clear_image()
            self.image.paste(self.code_head, (self.code_xpos, self.code_ypos), self.code_head)
            self.image.paste(self.code_center, (self.code_xpos, self.code_ypos + self.code_head.size[1]), self.code_center)
            self.image.paste(self.code_foot, (self.code_xpos, self.code_ypos + self.code_head.size[1] + self.code_center.size[1]), self.code_foot)
            self.image.paste(text_image, (self.code_xpos, self.code_ypos), text_image)
        
    def next(self):
        
        if self.static:
            return self.image
        
        if self.mode_current == 0:
            self._mode_wait_before()
        elif self.mode_current == 1:
            self._mode_fly_in()
        elif self.mode_current == 2:
            self._mode_open()
        elif self.mode_current == 3:
            self._mode_typing()
        elif self.mode_current == 4:
            self._mode_show()
        elif self.mode_current == 5:
            self._mode_close()
        elif self.mode_current == 6:
            self._mode_fly_out()
        elif self.mode_current == 7:
            self._mode_wait_after()
        
        self.step_num += 1
        
        if self.step_num % self.cursor_mod == 0:
            self.cursor_on = not self.cursor_on
        
        return self.image
    
    def _type_text(self, chars:int = None) -> Image:
        image = Image.new("RGBA", (self.code_width, self.code_height))
        draw = ImageDraw.Draw(image)
        
        y = int(round(self.code_head.size[1]))
        x = 25
        
        text = self.text
        if chars is not None and chars < len(self.text):
            text = self.text[:chars]
        if self.cursor_on:
            text += self.text_cursor
        
        for line in text.split("\n"):
            draw.text((x, y), line, font=self.font, fill=(255,255,255))
            y += self.lineheight
            
        return image
            
    def _clear_image(self):
        self.image = Image.new("RGBA", (self.width, self.height))
        
    def _mode_wait(self, modename, fraction):
        if not modename in self.mode_status:
            self.mode_status[modename] = {}
            self.mode_status[modename]["start"] = self.step_num
            self.mode_status[modename]["end"] = int(round(self.step_num + fraction * self.step_total, 0))
            
        if self.step_num >= self.mode_status[modename]["end"]:
            self.mode_current += 1     
    
    def _mode_fly(self, modename, fraction):
        if not modename in self.mode_status:
            self.mode_status[modename] = {}
            self.mode_status[modename]["start"] = self.step_num
            
            if abs(self.code_xpos_target - self.code_xpos) > abs(self.code_xpos_start - self.code_xpos):
                # we are probably at the start, go to target
                self.mode_status[modename]["xpos_goto"] = self.code_xpos_target
            else:
                # we are probably at the target, go to start
                self.mode_status[modename]["xpos_goto"] = self.code_xpos_start
                
            self.mode_status[modename]["speed"] = (self.mode_status[modename]["xpos_goto"] - self.code_xpos) / (fraction * self.step_total)
        
        if (self.code_xpos > self.mode_status[modename]["xpos_goto"] and self.code_xpos + self.mode_status[modename]["speed"] <= self.mode_status[modename]["xpos_goto"]) or \
              (self.code_xpos < self.mode_status[modename]["xpos_goto"] and self.code_xpos + self.mode_status[modename]["speed"] >= self.mode_status[modename]["xpos_goto"]):
                  # we have transitioned beyound the final point
                  self.code_xpos = self.mode_status[modename]["xpos_goto"]
                  self.mode_current += 1
        else:
            self.code_xpos += self.mode_status[modename]["speed"]
            self.code_xpos = int(round(self.code_xpos, 0))
            
        self._clear_image()
        self.image.paste(self.code_head, (self.code_xpos, self.code_ypos), self.code_head)
        self.image.paste(self.code_foot, (self.code_xpos, self.code_ypos + self.code_head.size[1]), self.code_foot)
        
    def _mode_open_close(self, modename, fraction):
        if not modename in self.mode_status:
            self.mode_status[modename] = {}
            self.mode_status[modename]["start"] = self.step_num
            self.mode_status[modename]["speed"] = self.code_center.size[1] / (fraction * self.step_total)
            
            if modename == "close":
                self.mode_status[modename]["speed"] *= -1
                self.mode_status[modename]["ytarget"] = 0
                self.mode_status[modename]["ystart"] = self.code_center.size[1]
            else:
                self.mode_status[modename]["ytarget"] = self.code_center.size[1]
                self.mode_status[modename]["ystart"] = 0
            return
            
        yopen = (self.step_num - self.mode_status[modename]["start"]) * self.mode_status[modename]["speed"] + self.mode_status[modename]["ystart"]
        logger.debug("yopen = {}", yopen)
        
        if yopen >= self.mode_status[modename]["ytarget"]  and modename == "open" or yopen <= self.mode_status[modename]["ytarget"] and modename=="close":
            yopen = self.mode_status[modename]["ytarget"] 
            self.mode_current += 1

        yopen = int(round(yopen, 0))

        if yopen > 0:
            self._clear_image()
            center = Image.open("./images/Code-Window-center.png")
            center = center.crop((0, 0, center.size[0], yopen))
            self.image.paste(self.code_head, (self.code_xpos, self.code_ypos), self.code_head)
            self.image.paste(center, (self.code_xpos, self.code_ypos + self.code_head.size[1]), center)
            self.image.paste(self.code_foot, (self.code_xpos, self.code_ypos + self.code_head.size[1] + yopen), self.code_foot)
            if modename == "close":
                text_image = self._type_text()
                text_image = text_image.crop((0, 0, center.size[0], yopen + self.code_head.size[1]))
                self.image.paste(text_image, (self.code_xpos, self.code_ypos), text_image)
        else:
            self._clear_image()
            self.image.paste(self.code_head, (self.code_xpos, self.code_ypos), self.code_head)
            self.image.paste(self.code_foot, (self.code_xpos, self.code_ypos + self.code_head.size[1]), self.code_foot)
            
    def _mode_wait_before(self):
        self._mode_wait("wait_before", 0.03)       
    
    def _mode_fly_in(self):
        self._mode_fly("fly_in", 0.02)
        
    def _mode_open(self):
        self._mode_open_close("open", 0.05)
    
    def _mode_typing(self):
        modename = "typing"
        fraction = 0.2
        if not modename in self.mode_status:
            self.mode_status[modename] = {}
            self.mode_status[modename]["start"] = self.step_num
            self.mode_status[modename]["speed"] = len(self.text) / (fraction * self.step_total)
        
        chars = int(round((self.step_num - self.mode_status[modename]["start"]) * self.mode_status[modename]["speed"], 0))
        if chars >= len(self.text):
            self.mode_current += 1
            
        logger.debug("Number of chars is {} out of {}", chars, len(self.text))
        
        text_image = self._type_text(chars)
        self._clear_image()
        self.image.paste(self.code_head, (self.code_xpos, self.code_ypos), self.code_head)
        self.image.paste(self.code_center, (self.code_xpos, self.code_ypos + self.code_head.size[1]), self.code_center)
        self.image.paste(self.code_foot, (self.code_xpos, self.code_ypos + self.code_head.size[1] + self.code_center.size[1]), self.code_foot)
        self.image.paste(text_image, (self.code_xpos, self.code_ypos), text_image)
    
    def _mode_show(self):
        self._mode_wait("show", 0.6)
        text_image = self._type_text()
        self._clear_image()
        self.image.paste(self.code_head, (self.code_xpos, self.code_ypos), self.code_head)
        self.image.paste(self.code_center, (self.code_xpos, self.code_ypos + self.code_head.size[1]), self.code_center)
        self.image.paste(self.code_foot, (self.code_xpos, self.code_ypos + self.code_head.size[1] + self.code_center.size[1]), self.code_foot)
        self.image.paste(text_image, (self.code_xpos, self.code_ypos), text_image)
    
    def _mode_close(self):
        self._mode_open_close("close", 0.05)
    
    def _mode_fly_out(self):
        self._mode_fly("fly_out", 0.02)
    
    def _mode_wait_after(self):
        self._mode_wait("wait_after", 0.03)