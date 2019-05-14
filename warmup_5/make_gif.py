import sys
import imageio

n = int(sys.argv[2])
start = sys.argv[1]

filenames = []
for i in range(n):
    if i < 10:
        for j in range(3): filenames.append(start + str(i) + '.png')
    else:
        filenames.append(start + str(i) + '.png')

images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('./plot.gif', images)
