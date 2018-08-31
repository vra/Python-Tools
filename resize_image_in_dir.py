""" Resize images to targe size. """
import argparse
import glob
import os
import re
import sys

from PIL import Image


def resize_images_in_dir(in_dir, out_dir, sizes):
    sizes = tuple(int(i) for i in sizes.split(','))
    dirs = os.listdir(in_dir)
    for d in dirs:
        print('==> processing dir %s' % d)
        imgs = glob.glob(os.path.join(in_dir, d, '*.jpg'))
        for img in imgs:
            new_image_path = img.replace(in_dir, out_dir)
            im = Image.open(img)
            im.resize(tuple(sizes), Image.ANTIALIAS).save(new_image_path)


def parse_commandline_args():
    """ function for commandline parameter parsing. """
    parser = argparse.ArgumentParser("Resize Images in Two Layer Folder.")
    parser.add_argument('-i', '--src', help="image directory", required=True)
    parser.add_argument('-o', '--out', help="target image directory", required=True)
    parser.add_argument('-r', '--size', help="target image resolution", required=True)

    args = parser.parse_args()
    return args


def main():
    """ main function. """
    args = parse_commandline_args()
    resize_images_in_dir(args.src, args.out, args.size)


if __name__ == '__main__':
    main()

