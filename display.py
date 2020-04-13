from subprocess import Popen, PIPE
from os import remove
from random import randint

#constant
XRES = 500
YRES = 500
MAX_COLOR = 255
RED = 0
GREEN = 1
BLUE = 2
TSTEP = .0001
steps_2d = 10000
steps_3d = 20
DEFAULT_COLOR = [255, 255, 255]
DRAW_COLOR = [0, 0, 0]

zbuffer = []
for i in range(YRES):
  row = [float("-inf")] * XRES
  zbuffer.append(row)

def makeNColors(n):
  colors = []
  for i in range(n):
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    colors.append([r, b, g])
  return colors

colorList = makeNColors(500)

def new_screen( width = XRES, height = YRES ):
    screen = []
    for y in range( height ):
        row = []
        screen.append( row )
        for x in range( width ):
            screen[y].append( DEFAULT_COLOR[:] )
    return screen

def plot(screen, color, x, y, z):
  newy = YRES - 1 - y
  if not ( x >= 0 and x < XRES and newy >= 0 and newy < YRES ): return
  if z <= zbuffer[newy][x]: return
  plotHelper(screen, color, x, y, z)

def plotHelper(screen, color, x, y, z):
    zbuffer[YRES - 1 - y][x] = z
    newy = YRES - 1 - y
    if ( x >= 0 and x < XRES and newy >= 0 and newy < YRES ):
        screen[newy][x] = color[:]

# def plot( screen, color, x, y ):
#     newy = YRES - 1 - y
#     if ( x >= 0 and x < XRES and newy >= 0 and newy < YRES ):
#         screen[newy][x] = color[:]

def clear_screen( screen ):
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            screen[y][x] = DEFAULT_COLOR[:]

def save_ppm( screen, fname ):
    f = open( fname, 'wb' )
    ppm = 'P6\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    f.write(ppm.encode())
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            f.write( bytes(pixel) )
    f.close()

def save_ppm_ascii( screen, fname ):
    f = open( fname, 'w' )
    ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    for y in range( len(screen) ):
        row = ''
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            row+= str( pixel[ RED ] ) + ' '
            row+= str( pixel[ GREEN ] ) + ' '
            row+= str( pixel[ BLUE ] ) + ' '
        ppm+= row + '\n'
    f.write( ppm )
    f.close()

def save_extension( screen, fname ):
    ppm_name = fname[:fname.find('.')] + '.ppm'
    save_ppm_ascii( screen, ppm_name )
    p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

def display( screen ):
    ppm_name = 'pic.ppm'
    save_ppm_ascii( screen, ppm_name )
    p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)
