"""
copy and rewrite code of wuspy/portal_calendar/resource/build_font.py
fixed width and height of fonts
there is not for 4 grey level
"""
import io
from os import path
import argparse

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from compiler import compile_image


def encode_get_utf8_size(utf):
    if utf < 0x80:
        return 1
    if utf >= 0x80 and utf < 0xC0:
        return -1
    if utf >= 0xC0 and utf < 0xE0:
        return 2
    if utf >= 0xE0 and utf < 0xF0:
        return 3
    if utf >= 0xF0 and utf < 0xF8:
        return 4
    if utf >= 0xF8 and utf < 0xFC:
        return 5
    if utf >= 0xFC:
        return 6


def encode_utf8_to_unicode(utf8):
    utfbytes = encode_get_utf8_size(utf8[0])
    if utfbytes == 1:
        unic = utf8[0]
    if utfbytes == 2:
        b1 = utf8[0]
        b2 = utf8[1]
        if ((b2 & 0xE0) != 0x80):
            return -1
        unic = ((((b1 << 6) + (b2 & 0x3F)) & 0xFF) << 8) | (((b1 >> 2) & 0x07) & 0xFF)
    if utfbytes == 3:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80)):
            return -1
        unic = ((((b1 << 4) + ((b2 >> 2) & 0x0F)) & 0xFF) << 8) | (((b2 << 6) + (b3 & 0x3F)) & 0xFF)

    if utfbytes == 4:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        b4 = utf8[3]
        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80) or ((b4 & 0xC0) != 0x80)):
            return -1
        unic = ((((b3 << 6) + (b4 & 0x3F)) & 0xFF) << 16) | ((((b2 << 4) + ((b3 >> 2)
                                                                  & 0x0F)) & 0xFF) << 8) | ((((b1 << 2) & 0x1C) + ((b2 >> 4) & 0x03)) & 0xFF)
    if utfbytes == 5:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        b4 = utf8[3]
        b5 = utf8[4]
        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80) or ((b4 & 0xC0) != 0x80) or ((b5 & 0xC0) != 0x80)):
            return -1
        unic = ((((b4 << 6) + (b5 & 0x3F)) & 0xFF) << 24) | (((b3 << 4) + ((b4 >> 2) & 0x0F) & 0xFF) << 16) | ((((b2 << 2) + ((b3 >> 4) & 0x03)) & 0xFF) << 8) | (((b1 << 6)) & 0xFF)
    if utfbytes == 6:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        b4 = utf8[3]
        b5 = utf8[4]
        b6 = utf8[5]

        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80) or ((b4 & 0xC0) != 0x80) or ((b5 & 0xC0) != 0x80) or ((b6 & 0xC0) != 0x80)):
            return -1

        unic = ((((b5 << 6) + (b6 & 0x3F)) << 24) & 0xFF) | (((b5 << 4) + ((b6 >> 2) & 0x0F) << 16) & 0xFF) | ((((b3 << 2) + ((b4 >> 4) & 0x03)) << 8) & 0xFF) | ((((b1 << 6) & 0x40) + (b2 & 0x3F)) & 0xFF)

    return unic


class Glyph:
    def __init__(self, index, char, code_point, font, font_size):
        """
        :param index: int
        :param char: str
        :param code_point: int
        :param font: ImageFont
        """
        self.char = char
        self.code_point = code_point
        self.index = index
        self.left, self.top, self.right, bottom = font.getbbox(char)
        self.width = font_size
        self.height = font_size
        self.data = None
        self.pad = 0

    def set_data(self, lines):
        self.data = '[\n\t\t\t\t{}\n\t\t\t]'.format('\n\t\t\t\t'.join(lines))

    def set_pad(self, pad):
        self.pad = pad

    def empty(self):
        return self.width * self.height == 0

    def size(self):
        return self.width, self.height

    def compile(self):
        return '0x{0.code_point:04X}: {{ \n\t\t\t"char": "{0.char}", "width": {0.width}, "height": {0.height}, "top": {0.top}, "left": {0.left}, "right": {0.right}, "pad": {0.pad}, \n\t\t\t"data": {0.data}, \n\t\t}},  # {0.char} '.format(self)


parser = argparse.ArgumentParser()
parser.add_argument("font", type=str, help="Name or path of the font to be compiled")
parser.add_argument("-name", type=str, required=True, help="Name for the generated bitmap font")
parser.add_argument("-size", type=int, required=True, help="The size in pixels of the compiled bitmap font")
parser.add_argument("-ranges", type=str, required=True, help="The Unicode character ranges to include in the bitmap font (i.e. 0-9,A-Z,À-ÿ)")
parser.add_argument("-fg", type=int, required=False, default=0, help="The foreground color, 0-255, defaults to 0 (black)")
parser.add_argument("-bg", type=int, required=False, default=255, help="The background color, 0-255, defaults to 255 (white)")
args = parser.parse_args()

if args.ranges == '*':
    with open('zh-hans3500.txt', 'r', encoding='utf8') as fr:
        lines = ''.join([l.strip() for l in fr.readlines()])
        code_point_ranges = list(map(lambda r: r.split(' ', 1), list(lines)))
elif args.ranges == 'city':
    with open('zh-city.txt', 'r', encoding='utf8') as fr:
        lines = ''.join([l.strip() for l in fr.readlines()])
        code_point_ranges = list(map(lambda r: r.split(' ', 1), list(lines)))
elif args.ranges == 'lunar':
    with open('zh-lunar.txt', 'r', encoding='utf8') as fr:
        lines = ''.join([l.strip() for l in fr.readlines()])
        code_point_ranges = list(map(lambda r: r.split(' ', 1), list(lines)))
elif args.ranges == 'birth':
    with open('zh-birth.txt', 'r', encoding='utf8') as fr:
        lines = ''.join([l.strip() for l in fr.readlines()])
        code_point_ranges = list(map(lambda r: r.split(' ', 1), list(lines)))
else:
    code_point_ranges = list(map(lambda r: r.split('-', 1), args.ranges.split(',')))
font_path = args.font  # dir/to/SmileySans-Oblique.ttf
font_name = args.name  # smiley24px
font_size = args.size
fg_color = args.fg
bg_color = args.bg

output_file_name = "{}/{}.py".format(path.dirname(font_path), font_name)
font_cname = "FONT_{}".format(font_name.upper().replace(".", "_").replace("-", "_").replace(" ", "_"))

print("Building font '{}' at size {}px with ranges {}".format(font_path, font_size, args.ranges))

font = ImageFont.truetype(font_path, font_size)  # TTF: TrueType Font
# https://stackoverflow.com/questions/27631736/meaning-of-top-ascent-baseline-descent-bottom-and-leading-in-androids-font
# https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
ascent, descent = font.getmetrics()

font_tables = list(map(lambda table: table.cmap.keys(), TTFont(font_path)['cmap'].tables))
def fontHasCodePoint(codePoint: int) -> bool:
    for table in font_tables:
        if codePoint in table:
            return True
    return False

output_lines = []
output_glyphs = []

byte_count = 0
for code_point in code_point_ranges:
    i = 0
    uni = None
    char_bytes = ''.join(code_point).encode('utf8')
    while i < len(char_bytes):
        utfbytes = encode_get_utf8_size(char_bytes[i])
        uni = encode_utf8_to_unicode(char_bytes[i:i + utfbytes])
        i += utfbytes
    glyph = Glyph(byte_count, ''.join(code_point), uni, font, font_size)
    if not fontHasCodePoint(uni) and uni != 0xFFFD:
        print("Warning: Font does not contain code point '{}' (U+{:04X})".format(uni, code_point))
    elif glyph.empty():
        print("Skipping whitespace char U+{:04X}".format(uni))
    else:
        output_glyphs.append(glyph)
        image = Image.new("1", glyph.size(), bg_color)
        draw = ImageDraw.Draw(image)
        draw.text((-glyph.left, -glyph.top), ''.join(code_point), font=font, fill=fg_color)
        # image.show() # for checking th char
        char_output_lines, char_byte_count, width, height, pad = compile_image(image)
        glyph.set_data(char_output_lines)
        glyph.set_pad(pad)
        output_lines.append("// '{}'".format(uni))
        output_lines += char_output_lines
        byte_count += char_byte_count

print("Output size: {}".format(byte_count))
print("Writing to file '{}'".format(output_file_name))

with open(output_file_name, mode="w", encoding="utf8") as of:
    of.writelines([
        '"""\n',
        ' This is a generated source file.\n',
        ' Original font: {}\n'.format(font_path),
        ' font size: {}px\n'.format(font_size),
        ' Code point ranges: {}\n'.format(args.ranges),
        '"""\n\n',

        '{} = {{\n'.format(font_cname),
        '   "glyphs": {\n',
        *map(lambda glyph: "        {}\n".format(glyph.compile()), output_glyphs),
        '   },\n',
        '   "ascent": {},\n'.format(ascent),
        '   "descent": {},\n'.format(descent),
        '   "space_width": {},\n'.format(round(font.getlength(" "))),
        '}\n\n',
    ])

print("Done")

