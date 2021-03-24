import os
import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import shutil

def getBounds(image):

	data = np.asarray(image)

	data = np.transpose(data)
	data = np.swapaxes(data, 1, 2)

	data = data[0]

	ymin = 0
	ymax = len(data)-1
	trow = np.sum(data[0])*10

	for row in range(len(data)):
		if np.sum(data[row]) > trow and ymin == 0:
			ymin = row

	for row in range(len(data)):
		if ymax == len(data)-1 and np.sum(data[len(data)-row-1]) > trow:
			ymax = len(data)-row-1

	data = np.transpose(data)

	xmin = 0
	xmax = len(data)-1
	tcol = np.sum(data[0])*10

	for col in range(len(data)):
		if np.sum(data[col]) > tcol and xmin == 0:
			xmin = col

	for col in range(len(data)):
		if xmax == len(data)-1 and np.sum(data[len(data)-col-1]) > tcol:
			xmax = len(data)-col-1

	return ((xmin,ymin),(xmax,ymax))

def saveAnno(folder, imNum, nMasks, bList, imBreadth, imHeight):
	with open('./' + folder + '/Annotation/' + imNum + '.txt', 'w') as f:
		f.write('# Compatible with PASCAL Annotation Version 1.00\n')
		f.write('Image filename : "'+folder+'/PNGImages/'+imNum+'.png"\n')
		f.write('Image size (X x Y x C) : '+str(imBreadth)+' x '+str(imHeight)+' x 3\n')
		f.write('Database : '+'"'+folder+'"\n')
		f.write('Objects with ground truth : '+str(nMasks)+' { ')
		for i in range(nMasks):
			f.write('"d" ')
		f.write('}\n')
		f.write('# Note there may be some objects not included in the ground truth list for they are severe-occluded\n')
		f.write('# or have very small size.\n')
		f.write('# Top left pixel co-ordinates : (0, 0)\n')
		for i in range(nMasks):
			f.write('# Details for defect '+str(i+1)+' ("d")\n')
			f.write('Original label for object '+str(i+1)+' "d" : "d"\n')
			f.write('Bounding box for object '+str(i+1)+' "d" (Xmin, Ymin) - (Xmax, Ymax) : '+repr(bList[i][0])+' - '+repr(bList[i][1])+'\n')
			f.write('Pixel mask for object '+str(i+1)+' "d" : "'+folder+'/Masks/'+imNum+'_mask.png"\n')
			f.write('\n')

def main():

	# Making Annotation

	# shutil.rmtree('./OASIS/Annotation/')
	folder = 'debug'
	os.mkdir('./' + folder + '/')
	os.mkdir('./' + folder + '/Annotation/')

	imageLen = len(glob.glob('./masks/*'))
	flag = True

	for i in range(imageLen):

		masks = glob.glob('./masks/'+str(i).zfill(int(np.log10(imageLen)+1))+'/*')

		imNum = str(i).zfill(int(np.log10(imageLen)+1))
		nMasks = len(masks)

		bList = []

		for mask in masks:

			im = Image.open(mask)

			bList.append(getBounds(im))

		saveAnno(folder,imNum, nMasks, bList, imBreadth=256, imHeight=256)

	# Making masks

	# shutil.rmtree('./OASIS/Masks/')
	os.mkdir('./' + folder + '/Masks/')

	imageLen = len(glob.glob('./masks/*'))

	for i in range(imageLen):

		masks = glob.glob('./masks/'+str(i).zfill(int(np.log10(imageLen)+1))+'/*')

		imNum = str(i).zfill(int(np.log10(imageLen)+1))
		nMasks = len(masks)

		for val, mask in enumerate(masks):

			im = Image.open(mask)

			imData = np.asarray(im)

			data = np.copy(imData)

			data = np.transpose(data)
			data = np.swapaxes(data, 1, 2)[0]

			tval = 200
			data[data <= tval] = 0
			data[data > tval] = (val+1)

			if val == 0:
				maskNet = data
			else:
				maskNet = maskNet + data

		print(maskNet.shape)
		img = Image.fromarray(maskNet)

		img.save('./' + folder + '/Masks/'+imNum+'_mask.png')

		if i==5:

			print("Displaying image.")
			plt.imshow(maskNet)
			plt.colorbar()
			plt.show()

	# Saving images

	# shutil.rmtree('./OASIS/PNGImages/')
	os.mkdir('./' + folder + '/PNGImages/')

	imageLen = len(glob.glob('./images/*'))

	for i in range(imageLen):

		name = str(i).zfill(int(np.log10(imageLen)+1))+'.png'

		im = np.asarray(Image.open('./images/'+name))
		im = np.transpose(im)
		im = np.swapaxes(im, 1, 2)[:3]

		print(im.shape)

		im = np.swapaxes(im, 1, 2)
		im = np.transpose(im)

		Image.fromarray(im).save('./' + folder + '/PNGImages/'+name, mode='RGB')

	print("End of script.")

if __name__ == '__main__':

	# im = Image.open('OASIS/Masks/02_mask.png')
	# plt.imshow(im)
	# plt.colorbar()
	# plt.show()

	# im = np.asarray(Image.open('OASIS/PNGImages/02.png'))
	# print(im.shape)
	# plt.imshow(im)
	# plt.show()

	main()