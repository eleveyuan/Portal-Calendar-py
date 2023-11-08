import argparse
import os.path as path

from PIL import Image

from compiler import compile_image


parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, help="Path of the image to be compiled")
parser.add_argument("-dir", type=str, required=False, default='./', help="dir of result lists to be saved")
args = parser.parse_args()

image_path = args.path  # '/dir/foo-bar.gif'
image_name = path.basename(path.splitext(image_path)[0])  # 'foo-bar'
output_filename = "{}.py".format(path.splitext(image_path)[0])
image_cname = "IMG_{}".format(image_name.upper().replace(".", "_").replace("-", "_").replace(" ", "_"))  # 'IMG_FOO_BAR'
image_dir = args.dir

image = Image.open(image_path)
print("Loaded file '{}'".format(image_name))

output_lines, byte_count, width, height, pad = compile_image(image)

print("Output size: {}".format(byte_count))
print("Writing to file '{}'".format(output_filename))

with open(path.join(image_dir, output_filename), mode="w", encoding="utf8") as of:
    of.writelines([
        '"""\n',
        ' This is a generated source file.\n',
        ' Original image: {}\n'.format(image_path),
        '"""\n\n',

        '{} = {{\n'.format(image_cname),

        '   "data": [\n        {}\n    ],\n'.format('\n        '.join(output_lines)),
        '   "width": {},\n'.format(width),
        '   "height": {},\n'.format(height),
        '   "pad": {}\n'.format(pad),
        '}\n\n',

    ])

print("Done")
