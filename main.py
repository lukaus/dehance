from PIL import Image
import matplotlib.pyplot as plt
import math
import sys


filename = "img.jpg"
scale = 20  # scale of each dice
divisions = 6 # or 12 maybe

print(sys.argv)
if len(sys.argv) > 1:
	print("Found arguments")
	if len(sys.argv) >= 2:
		filename = sys.argv[1]
	if len(sys.argv) >= 3:
		scale = int(sys.argv[2])
	if len(sys.argv) >= 4:
		divisions = int(sys.argv[3])


# Load image
img = Image.open(filename)
img = img.convert('L')


# sum pixels in each region
img_vals = [ ] # rows


row = 0 # current row
col = 0 # current col

print(f"\nScaling {img.size[1]} x {img.size[0]} to {int(math.floor(img.size[1]/scale))} x {int(math.floor(img.size[0]/scale))}") 


#if img.size[0] % scale != 0 or img.size[1] % scale != 0:
#	print(f"Error: Image is not subdividable in {scale} pixel increments. ({img.size[0]}x{img.size[1]})")
#	exit(-1)


for x in range(0, img.size[1], scale):
	img_vals.append( [] ) # col
	for y in range(0, img.size[0], scale):
		# Iterate over pixels of subregion
		darkness = 0
		for px in range(0, scale):
			for py in range(0, scale):
				if(y + py < img.size[0]) and (x+px < img.size[1]):
					darkness += img.getpixel((y+ py, x + px))
		darkness = int(darkness / (scale * scale))
		img_vals[int(x / scale)].append(darkness)
	print(f"[", end="")
	print('=' * (int((x+1)/img.size[1]*100)),end="")
	print('-' * ( 99 - int((x)/img.size[1]*100)),end="")
	print(f"]", end="\r")



# find distribution of light/dark regions 

all_points = []

for x in range(len(img_vals)):
	for y in range(len(img_vals[x])):
		all_points.append(img_vals[x][y])

all_points.sort()

itr = int(math.floor(len(all_points) / divisions))

indices = []
for x in range(0, len(all_points), itr):
	indices.append(all_points[x])

#print(indices)
print("")

# place calculate values for each region

img_map = []
for x in range(len(img_vals)):
	img_map.append([])
	for y in range(len(img_vals[x])):
		img_map[x].append(5)
		for i in range(len(indices)-1):
			if img_vals[x][y] < indices[i+1]:
				img_map[x][y] = i
				break


printval = [" ","·","░","▒","▓","█"]

im1 = Image.open("1.jpg")
im2 = Image.open("2.jpg")
im3 = Image.open("3.jpg")
im4 = Image.open("4.jpg")
im5 = Image.open("5.jpg")
im6 = Image.open("6.jpg")

dicevals = [im6, im5, im4, im3, im2, im1]

composite = Image.new("RGB", ( len(img_map[0])*scale, len(img_map)*scale ), color=(255, 255, 255))

for x in range(len(img_map)):
	for y in range(len(img_map[x])):
		print(printval[img_map[x][y]], end="")
		composite.paste(dicevals[img_map[x][y]].resize((scale, scale)), (y*scale, x*scale))

	print("")


# output image with dice images

composite.save("out.jpg", quality=100)
