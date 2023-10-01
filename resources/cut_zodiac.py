from PIL import Image


def cut_pic(image):
    width, height = image.size
    item_width = int(width / 3)
    item_height = int(height / 4)

    # cut picture roughly
    box_list = []
    for i in range(4):
        for j in range(3):
            if j == 0:
                box_list.append((j * item_width, i * item_height, (j + 1) * item_width, (i + 1) * item_height))
            elif j == 1:
                box_list.append((j * item_width, i * item_height, (j + 1) * item_width + 20, (i + 1) * item_height))
            elif j == 2:
                box_list.append((j * item_width + 20, i * item_height, (j + 1) * item_width, (i + 1) * item_height))
    img_list = [image.crop(box) for box in box_list]

    # cut picture precisely
    res_img_list = []
    for img in img_list:
        w, h = img.size
        red, green, blue, alpha = img.split()

        y_top = 0
        y_bottom = 0
        for i in range(h):
            x = 0
            for j in range(w):
                if alpha.getpixel((j, i)) == 0:
                    x += 1
            if x == w and y_top < h/2:
                y_top += 1
            if x == w and y_bottom > h/2:
                break
            y_bottom += 1

        x_left = 0
        x_right = 0
        for i in range(w):
            x = 0
            for j in range(h):
                if alpha.getpixel((i, j)) == 0:
                    x += 1
            if x == h and x_left < w / 2:
                x_left += 1
            if x == h and x_right > w / 2:
                break
            x_right += 1

        left, right, top, bottom = x_left, x_right, y_top, y_bottom
        print(img.size, left, right, top, bottom)
        res_img_list.append(img.crop((left, top, right, bottom)))

    return res_img_list


def save_img(img_list, path='./'):
    idx = 1
    max_width = 0
    max_height = 0
    for img in img_list:
        if img.width > max_width:
            max_width = img.width
        if img.height > max_height:
            max_height = img.height
        img.save(path + str(idx) + '.png', 'PNG')
        img.save(path + str(idx) + '.bmp', 'BMP')
        idx += 1
    print('max_width={}, max_height={}'.format(max_width, max_height))


img = Image.open('zodiac.png')
img_list = cut_pic(img)
save_img(img_list)
