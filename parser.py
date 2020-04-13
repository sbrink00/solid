import sys
from matrix import *
from draw import *
from display import *
from transformations import *

#add new transformation by multiplyint it after current matrix.

def genLines(file):
  f = open(file, "r")
  lines = f.readlines()
  for i in range(len(lines)): lines[i] = lines[i][:-1]
  if sys.argv[-1] == "nodisplay": lines = [x for x in lines if x != "display"]
  f.close()
  return lines

stack = newStack()

def parse_file(file, edge, polygons, transform, screen, color):
  global stack
  lines = genLines(file)
  ident(transform)
  x = 0
  while x < len(lines):
    if lines[x] == "line":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_edge(edge, p[0], p[1], p[2], p[3], p[4], p[5])
      matrix_mult(stack[-1], edge)
      draw_lines(edge, screen, DRAW_COLOR)
      del edge[:]
      x += 1
    elif lines[x] == "circle":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_circle(edge, p[0], p[1], p[2], p[3], 10000)
      matrix_mult(stack[-1], edge)
      draw_lines(edge, screen, DRAW_COLOR)
      del edge[:]
      x += 1
    elif lines[x] == "triangle":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_polygon(polygons, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
      matrix_mult(stack[-1], polygons)
      draw_polygons(polygons, screen, DRAW_COLOR)
      del polygons[:]
      x += 1
    elif lines[x] == "hermite":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_hermite(edge, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
      matrix_mult(stack[-1], edge)
      draw_lines(edge, screen, DRAW_COLOR)
      del edge[:]
      x += 1
    elif lines[x] == "bezier":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_bezier(edge, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
      matrix_mult(stack[-1], edge)
      draw_lines(edge, screen, DRAW_COLOR)
      del edge[:]
      x += 1
    elif lines[x] == "torus":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_torus(polygons, p[0], p[1], p[2], p[3], p[4], steps_3d)
      matrix_mult(stack[-1], polygons)
      draw_polygons(polygons, screen, DRAW_COLOR)
      del polygons[:]
      x += 1
    elif lines[x] == "sphere":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_sphere(polygons, p[0], p[1], p[2], p[3], steps_3d)
      matrix_mult(stack[-1], polygons)
      draw_polygons(polygons, screen, DRAW_COLOR)
      del polygons[:]
      x += 1
    elif lines[x] == "box":
      p = [int(y) for y in lines[x + 1].split(" ")]
      add_box(polygons, p[0], p[1], p[2], p[3], p[4], p[5])
      matrix_mult(stack[-1], polygons)
      draw_polygons(polygons, screen, DRAW_COLOR)
      del polygons[:]
      x += 1
    elif lines[x] == "ident":
      ident(transform)
    elif lines[x] == "scale":
      f = [int(y) for y in lines[x + 1].split(" ")]
      s = []
      scale(s, f[0], f[1], f[2])
      transform_mult(stack[-1], s)
      stack[-1] = deepcopy(s)
      x += 1
    elif lines[x] == "move":
      f = [int(y) for y in lines[x + 1].split(" ")]
      move = []
      translate(move, f[0], f[1], f[2])
      transform_mult(stack[-1], move)
      stack[-1] = deepcopy(move)
      x += 1
    elif lines[x] == "rotate":
      f = lines[x + 1].split(" ")
      r = []
      rotate(r, f[0], int(f[1]))
      transform_mult(stack[-1], r)
      stack[-1] = deepcopy(r)
      x += 1
    elif lines[x] == "push":
      push(stack)
    elif lines[x] == "pop":
      pop(stack)
    elif lines[x] == "apply":
      matrix_mult(transform, edge)
      matrix_mult(transform, polygons)
    elif lines[x] == "display":
      display(screen)
    elif lines[x] == "clear":
      edge.clear()
    elif lines[x] == "save":
      save_extension(screen, lines[x + 1])
      print("File name: " + lines[x + 1])
      return
      x += 1
    elif lines[x] == "stop":
      return
    x += 1
