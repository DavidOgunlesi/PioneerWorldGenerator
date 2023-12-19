"""
World generator creates a X by X map of tiles, each tile has a type.
Turns this map into an csv file.
"""

from perlin_noise import PerlinNoise
from typing import List, Tuple
import random
import csv
import os
import math
from enum import Enum

# enum for tile types
class Tile(Enum):
    EMPTY = "◾"
    STONE = "🌫️"
    ORE = "🌑"
    TREE = "🟤"
    BUSH = "🌿"
    ROCK = "🪨"
    RIVER = "🌊"


def IndexToCoordinates(width, idx: int) -> Tuple[int, int]:
    x = idx % width
    y = idx // width
    return x, y

def CoordinatesToIndex(width, x: int, y: int) -> int:
    return x + y * width

def FillWithPerlinNoise(map: List[float], scale: Tuple[float, float] = None, octaves: int = 1, persistence: float = 0.5, lacunarity: float = 2, seed: int = 1):
    noiseMaps = []
    for i in range(octaves):
        noiseMaps.append(PerlinNoise(octaves=i+1, seed=seed))
    
    for i in range(len(map)):
        x, y = IndexToCoordinates(scale[0], i)
        currPers = 1
        currScale = scale
        
        for noiseMap in noiseMaps:
            val = noiseMap([x / currScale[0], y / currScale[1]]) * currPers  
            # val *= (self.scapeAttribute.maxValue - self.scapeAttribute.minValue)
            # val += self.scapeAttribute.minValue
            map[i] += val # min(val, self.scapeAttribute.maxValue)
            currPers *= persistence
            currScale = currScale[0] / lacunarity, currScale[1] / lacunarity
            
        map[i] += 0.5
            
def GenerateMountains(symbolMap: List[float], threshold: float = 0.5):
    width = int(math.sqrt(len(symbolMap)))
    map = [0] * width ** 2
    
    FillWithPerlinNoise(map, (width, width), octaves=5, persistence= 0.5, lacunarity=2, seed=random.randint(0, 1000))

    for i in range(len(map)):
        if map[i] > threshold:
            map[i] = 0
        else:
            map[i] = 1
            symbolMap[i] = Tile.STONE.value
            
    return map

def GenerateOre(symbolMap: List[float], seedChance: float = 0.01, orePatchGrowthChance: float = 0.5, orePatchGrowthRadius: int = 10, orePatchGrowthIterations: int = 10):
    width = int(math.sqrt(len(symbolMap)))
    map = [0] * width ** 2
            
    for i in range(len(symbolMap)):
        if symbolMap[i] == Tile.STONE.value and random.random() < seedChance:
            symbolMap[i] = Tile.ORE.value
            
            for _ in range(orePatchGrowthIterations):
                x, y = IndexToCoordinates(width, i)
                x += random.randint(-orePatchGrowthRadius, orePatchGrowthRadius)
                y += random.randint(-orePatchGrowthRadius, orePatchGrowthRadius)
                if x < 0 or y < 0 or x >= width or y >= width: continue
                symbolMap[CoordinatesToIndex(width, x,  y)] = Tile.ORE.value
                map[CoordinatesToIndex(width, x,  y)] = 1
                if random.random() > orePatchGrowthChance: break
            
    return map

def GenerateFoliage(symbolMap: List[float], treeGrowthChance: float = 0.1, foliageGrowthChance: float = 0.5, rockChance: float = 0.1):
    width = int(math.sqrt(len(symbolMap)))
    map = [0] * width ** 2
            
    for i in range(len(symbolMap)):
        
        if symbolMap[i] == Tile.EMPTY.value and random.random() < treeGrowthChance:
            symbolMap[i] = Tile.TREE.value
            map[i] = 1
            continue
            
        if symbolMap[i] == Tile.EMPTY.value and random.random() < foliageGrowthChance:
            symbolMap[i] = Tile.BUSH.value
            map[i] = 0.2
            continue
            
        if symbolMap[i] == Tile.EMPTY.value and random.random() < rockChance:
            symbolMap[i] = Tile.ROCK.value
            map[i] = 0.5
            continue
            
    return map

def GenerateRiver(symbolMap: List[float], riverWidth: float):
    width = int(math.sqrt(len(symbolMap)))
    map = [0] * width ** 2
    # choose start and end points for river (random side of map)
    sides = [(0, random.randint(0, width)), (width, random.randint(0, width)), (random.randint(0, width), 0), (random.randint(0, width), width)]
    
    riverStart = sides[random.randint(0, 3)]
    riverEnd = sides[random.randint(0, 3)]
    
    while riverStart == riverEnd:
        riverEnd = sides[random.randint(0, 3)]
    
    t = 0
    
    def LerpTuple(a: Tuple[int, int], b: Tuple[int, int], t: float) -> Tuple[int, int]:
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    
    controlPoint1 = (random.randint(0, width), random.randint(0, width))
    controlPoint2 = (random.randint(0, width), random.randint(0, width))
    # make beizer curve
    riverPoints = []
    for i in range(0,100):
        t = i / 100
        l1 = LerpTuple(riverStart, controlPoint1, t)
        l2 = LerpTuple(controlPoint1, controlPoint2, t)
        l3 = LerpTuple(controlPoint2, riverEnd, t)
        l4 = LerpTuple(l1, l2, t)
        l5 = LerpTuple(l2, l3, t)
        l6 = LerpTuple(l4, l5, t)
        riverPoints.append(l6)
        
    def Distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)    
    
    for i in range(len(symbolMap)):
        for point in riverPoints:
            if Distance(point, IndexToCoordinates(width, i)) < riverWidth:
                map[i] = 1
                symbolMap[i] = Tile.RIVER.value
                break
    
    return map
    
    
