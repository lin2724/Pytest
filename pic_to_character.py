from PIL import Image


def test():
    im = Image.open('other/test.jpg')
    print im.format
    # im.show()
    out = im.point(lambda i: i * 2.2)
    out.show()
    pass

if __name__ == '__main__':
    test()