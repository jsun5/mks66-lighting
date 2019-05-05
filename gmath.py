import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(light[0])
    normalize(view)
    amb=calculate_ambient(ambient,areflect)
    dif=calculate_diffuse(light,dreflect,normal)
    spe=calculate_specular(light,sreflect,view,normal)
    
    total = [int( amb[0]+dif[0]+spe[0] ),
             int( amb[1]+dif[1]+spe[1] ),
             int( amb[2]+dif[2]+spe[2] )]
             
    limit_color(total)
    return total
    
    
def calculate_ambient(alight, areflect):
    return [alight[0]*areflect[0],
            alight[1]*areflect[1],
            alight[2]*areflect[2]]
    

def calculate_diffuse(light, dreflect, normal):
    if dot_product(light[0],normal) > 0:
        return [light[1][0]*dreflect[0]*dot_product(light[0],normal),
                light[1][1]*dreflect[1]*dot_product(light[0],normal),
                light[1][2]*dreflect[2]*dot_product(light[0],normal)]
    else:
        return [0,0,0]

def calculate_specular(light, sreflect, view, normal):
    init = [(2*dot_product(light[0],normal)*normal[0]) - light[0][0],
            (2*dot_product(light[0],normal)*normal[1]) - light[0][1],
            (2*dot_product(light[0],normal)*normal[2]) - light[0][2]]
    
    if(dot_product(init,view)>0):
        return [sreflect[0]*light[1][0]*(dot_product(init,view)**SPECULAR_EXP),
                sreflect[1]*light[1][1]*(dot_product(init,view)**SPECULAR_EXP),
                sreflect[2]*light[1][2]*(dot_product(init,view)**SPECULAR_EXP)]
    else:
        return [0,0,0]

def limit_color(color):
    for i in range(len(color)):
        if color[i]<0:color[i]=0
        elif color[i]>255:color[i]=255

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
