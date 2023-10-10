from PIL import Image

OUTPUT_BYTES_PER_LINE = 20


def compile_image(image):
    image = image.convert(mode="1", dither=Image.NONE)
    output_lines = [""]
    byte_count = 0
    inline_count = 0
    pixel = image.load()
    width, height = image.size
    bitmap = []
    for h in range(height):
        for w in range(width):
            if pixel[w, h] > 0:
                bitmap.append('0')
            else:
                bitmap.append('1')
    bitmap = ''.join(bitmap)
    for x in range(len(bitmap) >> 3):
        temp = bitmap[8 * x: 8 * (x + 1)]
        if inline_count == OUTPUT_BYTES_PER_LINE:
            output_lines.append("")
            inline_count = 0
        output_lines[-1] += "0x{:02X},".format(int(temp, 2))
        byte_count += 1
        inline_count += 1
    return output_lines, byte_count