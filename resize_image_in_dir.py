import re
import sys
import os
import glob

from PIL import Image

def crop_images_in_dir(in_dir):
	dirs = os.listdir(in_dir)
	for d in dirs:
		imgs = glob.glob(os.path.join(in_dir,d,'*.jpg'))
		for img in imgs:
			new_image_path = img.replace('jpegs_256','jpegs_256_341')
			im = Image.open(img)
			im.resize((256,341),Image.ANTIALIAS).save(new_image_path)


if __name__ == '__main__':
	crop_images_in_dir('/home/yunfeng/ucf101/jpegs_256')

