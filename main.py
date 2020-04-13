from display import *
from draw import *
from parser import *
from matrix import *
import math
from random import randint

def makeNColors(n):
  colors = []
  for i in range(n):
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    colors.append([r, b, g])
  return colors

def testColors(n):
  colors = makeNColors(n)
  f = open("main.py", "a")
  f.write("\n#")
  f.write(str(colors))
  f.close()
  matrix = []
  row = int(n ** .5) + 1
  radius = XRES / row / 2
  for i in range(row):
    for x in range(row):
      if row * i + x >= n: return
      color = colors[row * i + x]
      cx = x * radius * 2 + radius
      cy = i * radius * 2 + radius
      add_sphere(matrix, cx, cy, 0, radius, steps_3d)
      draw_polygons(matrix, screen, color)
      matrix.clear()

screen = new_screen()
screen1 = new_screen()
color = [ 0, 0, 0 ]
edges = []
polygons = []
transform = new_matrix()
scriptFile = "script"
f = open(scriptFile, "r")
filename = f.readlines()[-1].replace("\n", "")
parse_file(scriptFile, edges, polygons, transform, screen, DRAW_COLOR)
