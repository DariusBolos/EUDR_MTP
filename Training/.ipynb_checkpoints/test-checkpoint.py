import matplotlib.pyplot as plt
centroid = (-91.08638941901245, 16.52295242422859)
radius = 0.43
fig, ax = plt.subplots()
c1 = plt.Circle(centroid, radius, color='g')
ax.add_patch(c1)
#plt.show()