from display import *
from matrix import *
from gmath import *

def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def brokenTriangle(x0, y0, z0, x1, y1, z1, x2, y2, z2, screen, color):
  xMin = x0
  zMin = z0
  if x1 < xMin:
    xMin = x1
    zMin = z1
  if x2 < xMin:
    xMin = x2
    zMin = z2
  xMax = x0
  zMax = z0
  if x1 > xMax:
    xMax = x1
    zMax = z1
  if x2 > xMin:
    xMax = x2
    zMax = z2
  drawLineHorizontal(int(round(xMin)), int(round(xMax)), int(round(y0)), zMin, zMax, screen, color)

def fillPolygon(x0, y0, z0, x1, y1, z1, x2, y2, z2, screen, color):
  points = [[x0, y0, z0], [x1, y1, z1], [x2, y2, z2]]
  selectionSort(points)
  b = [int(round(x)) for x in points[0]]
  m = [int(round(x)) for x in points[1]]
  t = [int(round(x)) for x in points[2]]
  if b[1] == m[1] and b[1] == t[1]:
    brokenTriangle(x0, y0, z0, x1, y1, z1, x2, y2, z2, screen, color)
    return
  b[2],m[2],t[2] = points[0][2],points[1][2],points[2][2]
  xStart,xEnd = b[0],b[0]
  zStart,zEnd = b[2],b[2]
  if t[1] != b[1]:
    dxStart = (t[0] - b[0]) * 1.0 / (t[1] - b[1])
    dzStart = (t[2] - b[2]) * 1.0 / (t[1] - b[1])
  if b[1] != m[1]:
    dxEnd = (m[0] - b[0]) * 1.0 / (m[1] - b[1])
    dzEnd = (m[2] - b[2]) * 1.0 / (m[1] - b[1])
  else:
    dxEnd = (t[0] - m[0]) * 1.0 / (t[1] - m[1])
    dzEnd = (t[2] - m[2]) * 1.0 / (t[1] - m[1])
  for y in range(b[1], t[1] + 1):
    if y == m[1]:
      xEnd = m[0]
      zEnd = m[2]
      if t[1] != m[1]:
        dxEnd = (t[0] - m[0]) * 1.0 / (t[1] - m[1])
        dzEnd = (t[2] - m[2]) * 1.0 / (t[1] - m[1])
    drawLineHorizontal(int(round(xStart)), int(round(xEnd)), y, zStart, zEnd, screen, color)
    xStart += dxStart
    xEnd += dxEnd
    zStart += dzStart
    zEnd += dzEnd


def selectionSort(ary):
  for i in range(len(ary)):
    lowestIndex = i
    lowestValue = ary[i][1]
    for j in range(i, len(ary)):
      if ary[j][1] < lowestValue:
        lowestValue = ary[j][1]
        lowestIndex = j
    ary[i],ary[lowestIndex] = [x for x in ary[lowestIndex]],[x for x in ary[i]]


def draw_polygons( polygons, screen, color ):
    if len(polygons) < 2:
        print('Need at least 3 points to draw')
        return

    point = 0
    while point < len(polygons) - 2:
        p1 = polygons[point]
        p2 = polygons[point + 1]
        p3 = polygons[point + 2]
        normal = calculate_normal(polygons, point)[:]
        #print normal
        if normal[2] > 0:
            #fillPolygon(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2], p3[0], p3[1], p3[2], screen, colorList[point % len(colorList)])
            # draw_line( int(polygons[point][0]),
            #            int(polygons[point][1]),
            #            int(polygons[point+1][0]),
            #            int(polygons[point+1][1]),
            #            screen, color)
            # draw_line( int(polygons[point+2][0]),
            #            int(polygons[point+2][1]),
            #            int(polygons[point+1][0]),
            #            int(polygons[point+1][1]),
            #            screen, color)
            # draw_line( int(polygons[point][0]),
            #            int(polygons[point][1]),
            #            int(polygons[point+2][0]),
            #            int(polygons[point+2][1]),
            #            screen, color)
            fillPolygon(p1[0], p1[1], p1[2], p2[0], p2[1], p2[2], p3[0], p3[1], p3[2], screen, colorList[point % len(colorList)])
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])


def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def drawLineHorizontal(x0, x1, y, z0, z1, screen, color):
  if x0 > x1: drawLineHorizontal(x1, x0, y, z1, z0, screen, color)
  if x1 != x0: dz = 1.0 * (z1 - z0) / (x1 - x0)
  z = z0
  for x in range(x0, x1 + 1):
    plot(screen, color, x, y, z)
    z += z0

def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line