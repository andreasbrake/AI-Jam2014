from PIL import Image
import scipy
import numpy as np
import glob

im = Image.open('./data/1_2_.gif')

test_image = np.array(im.getdata())
test_image.resize((243, 320))

images = []

for image in glob.glob('./data/1_*_.gif'):
	image = Image.open(image)
	images.append(np.array(image.getdata()))

images = np.array(images)

mean_image = np.uint8(np.mean(images, 0))

mean_image.resize((243, 320))

#diff_image = np.subtract(test_image, mean_image)

out = Image.fromarray(mean_image)
out.save('test.gif','GIF')