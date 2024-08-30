"""src/turtlefun/qualityline.py"""

from PIL import Image, ImageDraw
from typing import Tuple, Union, Sequence

class QualityDraw:
    
    def __init__(self, image:Image):
        self.image = image
        self.draw = ImageDraw.Draw(self.image)
        
    def line(
        self,
        xy: Sequence[Sequence[float]],
        fill: Union[float, Tuple[int, ...], str] | None = None,
        width: int = 0,
        joint: str | None = None,) -> None:
        """Draw a PIL line with circles at the ends to prevent triangle spaces
        for thick lines"""
        
        self.draw.line(xy, fill=fill, width=width, joint=joint)
        
        if width < 6:
            return
        
        for px, py in list(xy):
            reduce = 2
            radius = int(round((width - reduce) / 2, 0))
            x1 = px - radius
            x2 = x1 + width - reduce
            y1 = py - radius
            y2 = y1 + width - reduce
            
            self.draw.ellipse((x1, y1, x2, y2), fill=fill)
    