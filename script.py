import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )
    systems= [tmp]

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print symbols
    for command in commands:
        polygons = []
        if command['op'] == 'push':
            systems.append( [x[:] for x in systems[-1]] )


        elif command['op'] == 'pop':
            systems.pop()

        elif command['op'] == 'sphere':
            add_sphere(polygons,
                       float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                       float(command['args'][3]), step_3d)
            matrix_mult( systems[-1], polygons )

            if command['constants'] == None:
                reflect = '.white'
            else:
                reflect = command['constants']

            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)

        elif command['op'] == 'torus':
            add_torus(polygons,
                      float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                      float(command['args'][3]), float(command['args'][4]), step_3d)
            matrix_mult( systems[-1], polygons )

            if command['constants'] == None:
                reflect = '.white'
            else:
                reflect = command['constants']

            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)

        elif command['op'] == 'box':
            add_box(polygons,
                    float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                    float(command['args'][3]), float(command['args'][4]), float(command['args'][5]))
            matrix_mult( systems[-1], polygons )

            if command['constants'] == None:
                reflect = '.white'
            else:
                reflect = command['constants']

            draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)

        elif command['op'] == 'circle':
            add_circle(edges,
                       float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                       float(command['args'][3]), step)
            matrix_mult( systems[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif command['op'] == 'hermite' or command['op'] == 'bezier':
            add_curve(edges,
                      float(command['args'][0]), float(command['args'][1]),
                      float(command['args'][2]), float(command['args'][3]),
                      float(command['args'][4]), float(command['args'][5]),
                      float(command['args'][6]), float(command['args'][7]),
                      step, line)
            matrix_mult( systems[-1], edges )
            draw_lines(edges, screen, zbuffer, color)
            edges = []


        elif command['op'] == 'line':
            add_edge( edges,
                      float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                      float(command['args'][3]), float(command['args'][4]), float(command['args'][5]) )
            matrix_mult( systems[-1], edges )
            draw_lines(eges, screen, zbuffer, color)
            edges = []

        elif command['op'] == 'scale':
            t = make_scale(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]


        elif command['op'] == 'move':
            t = make_translate(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]


        elif command['op'] == 'rotate':
            theta = float(command['args'][1]) * (math.pi / 180)
            if command['args'][0] == 'x':
                t = make_rotX(theta)
            elif command['args'][0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif command['op'] == 'display' or command['op'] == 'save':
            if command['op'] == 'display':
                display(screen)
            else:
                save_extension(screen, command['args'][0]+".png")
        #print command
