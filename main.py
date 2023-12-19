import worldGenerator as wg
import random

worldSize = (200, 200)
symbolMap = [wg.Tile.EMPTY.value] * worldSize[0] * worldSize[1]

wg.GenerateMountains(symbolMap, threshold = 0.3)
wg.GenerateOre(symbolMap, seedChance = 0.01, orePatchGrowthChance = 0.9, orePatchGrowthRadius = 2, orePatchGrowthIterations = 20)
wg.GenerateRiver(symbolMap, riverWidth = 6)
map = wg.GenerateFoliage(symbolMap, treeGrowthChance = 0.01, foliageGrowthChance = 0.5, rockChance = 0.005)

# # add edge to map
# for p in range(worldSize[0]):
#     symbolMap[p] = "⬛"
#     symbolMap[p + (worldSize[0] * (worldSize[1] - 1))] = "⬛"

# convert to csv
symbolMap = [symbolMap[i:i+worldSize[0]] for i in range(0, len(symbolMap), worldSize[0])]
with open('map.txt', "w", encoding="utf-8") as f:
    for row in symbolMap:
        f.write("".join(row) + "\n")

with open('map.csv', "w", encoding="utf-8") as f:
    for row in symbolMap:
        f.write(",".join(row).replace(wg.Tile.EMPTY.value, "") + "\n")

# display the map using matplotlib
import matplotlib.pyplot as plt

# # turn map into 2d array
# map = [map[i:i+worldSize[0]] for i in range(0, len(map), worldSize[0])]
# # show array as image
# plt.imshow(map, cmap='gray', vmin=0, vmax=1)

# plt.show()

# # turn map into 2d array
# map2 = [map2[i:i+worldSize[0]] for i in range(0, len(map2), worldSize[0])]
# # show array as image
# plt.imshow(map2, cmap='gray', vmin=0, vmax=1)

# # show the plot
# plt.show()
