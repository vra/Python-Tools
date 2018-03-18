from PIL import Image




def crop_images_from_list(image_list, ext):
	with open(image_list, 'r') as image_list_file:
		for line in image_list_file:
			image_path = line.split(' ')[0]
			box = line.split(' ')[1:5]
			box = tuple([int(i) for i in box])
			with Image.open(image_path) as im:
				im.crop(box).resize((171,128),Image.ANTIALIAS).save(image_path.rstrip('.jpg')+ext+'.jpg')

if __name__ == '__main__':
	crop_images_from_list('../lists/split01/trainlist01_frm.txt.crop.rcnn_cut','_crop')

