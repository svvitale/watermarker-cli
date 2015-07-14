from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
import copy


class Watermark(object):

    ALIGNMENTS = ['center', 'left', 'right']
    VALIGNMENTS = ['middle', 'top', 'bottom']

    DEFAULTS = {
        'font': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Qwigley-Regular.ttf'),
        'align': ALIGNMENTS[0],
        'valign': VALIGNMENTS[0],
        'scale': 0.2,
        'tile': False,
        'opacity': 0.2,
        'color': None,
        'margin': (0, 0)
    }

    def __init__(self, filename):

        if not os.path.isfile(filename):
            raise ValueError("Invalid file specified")

        self.__image = Image.open(filename)

        if self.__image.mode != "RGBA":
            self.__image = self.__image.convert("RGBA")

        self.__options = copy.deepcopy(Watermark.DEFAULTS)

    def __getattr__(self, name):
        if hasattr(self.__image, name):
            return getattr(self.__image, name)
        else:
            # Default behaviour
            raise AttributeError("Invalid attribute requested: " + name)

    def apply_text(self, text, **kwargs):

        # Pull in keyword arguments as options
        self.__options.update(**kwargs)

        # Create font instance of the proper size
        width, height = self.size
        font_size = int(self.__options.get('scale') * height)
        font = ImageFont.truetype(self.__options.get('font'), font_size)

        # Create text layer with the same size as the original image
        text_layer = Image.new("RGBA", self.size, (0, 0, 0, 0))

        # Calculate the size of the drawn text
        text_draw = ImageDraw.Draw(text_layer)
        text_width, text_height = text_draw.textsize(text, font=font)
        text_x_margin, text_y_margin = self.__options.get('margin')

        # Calculate the position of the drawn text
        if self.__options.get('tile'):
            # Tiling, we're going to draw the text multiple times
            text_x = (width / 2.0) - (text_width / 2.0)
            text_y = text_y_margin

            while (text_y + text_height + text_y_margin) < height:
                text_draw.text((text_x, text_y), text, font=font, fill=self.__options.get('color'))
                text_y += text_height + text_y_margin
        else:
            # Not tiling, must be a fixed position
            if self.__options.get('align') == 'center':
                text_x = (width / 2.0) - (text_width / 2.0)
            elif self.__options.get('align') == 'left':
                text_x = text_x_margin
            elif self.__options.get('align') == 'right':
                text_x = width - text_width - text_x_margin
            else:
                raise ValueError('Invalid horizontal alignment specified')

            if self.__options.get('valign') == 'middle':
                text_y = (height / 2.0) - (text_height / 2.0)
            elif self.__options.get('valign') == 'top':
                text_y = text_y_margin
            elif self.__options.get('valign') == 'bottom':
                text_y = height - text_height - text_y_margin
            else:
                raise ValueError('Invalid vertical alignment specified')

            # Draw the text once
            text_draw.text((text_x, text_y), text, font=font, fill=self.__options.get('color'))

        # Adjust opacity
        if self.__options.get('opacity') != 1:
            alpha = text_layer.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(self.__options.get('opacity'))
            text_layer.putalpha(alpha)

        # Update our internal image
        self.__image = Image.composite(text_layer, self.__image, text_layer)
