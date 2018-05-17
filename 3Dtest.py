import pygame
import random
import math
import time
import sys
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os, inspect
from pygame.transform import scale

from pygame.locals import *

from sys import platform as _platform

if _platform == "win32":
    scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) # compatible interactive Python Shell
    scriptDIR  = os.path.dirname(scriptPATH)
    assets = os.path.join(scriptDIR,"aa.obj")

from objloader import *
# Define some colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
GREEN2= [100, 255, 100]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]
BROWN = [136, 66, 29]
BROWN2 = [136, 100, 60]
YELLOW= [255,255,0]

#REPERE 3D
# axe X => vers la droite comme d'habitude
# axe Y => vertical vers le haut
# aze Z => profondeur, orienté vers l'arrière, ainsi lorsque z=-10 l'objet est devant la caméra

ix = (1,0,0)
iy = (0,1,0)
iz = (0,0,1)
mix = (-1,0,0)
miy = (0,-1,0)
miz = (0,0,-1)
######################################################################################
#
#  les fonctions ci dessous ne doivent pas etre modifiées ou alors à vos risques et péril
#
######################################################################################

#init de la vue 3D
pygame.init()
display = (800,600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
glEnable(GL_DEPTH_TEST)
FOV = 45 #idem que dans les jeux
ratio = (display[0]/display[1])
dist_min = 0.1
dist_max = 100 # au dela les objets ne sont plus affichés - vous pouvez modifier cette distance
gluPerspective(FOV, ratio, dist_min, dist_max)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

# en opengl les couleurs sont entre 0 et 1
def OpenGLColor(Couleur):
    (R,V,B) = Couleur
    return (R/255,V/255,B/255)

# cree un parallélogramme OPENGL plongé en 3D ceci dans le repère local
# A est un coin du rectangle
# u et v sont les vecteurs qui définissent les bords parallèles

def Face(Couleur,A,u,v):
    (Ax,Ay,Az) = A
    (ux,uy,uz) = u
    (vx,vy,vz) = v
    A1 = A
    A2 = (Ax+ux,Ay+uy,Az+uz)
    A3 = (Ax+ux+vx,Ay+uy+vy,Az+uz+vz)
    A4 = (Ax+vx,Ay+vy,Az+vz)
    glBegin(GL_QUADS)
    glColor3fv(OpenGLColor(Couleur))
    glVertex3fv( A1 )
    glVertex3fv( A2 )
    glVertex3fv( A3 )
    glVertex3fv( A4  )
    glEnd()


# cree un triangle isocèle plongé en 3D ceci dans le repère local
# A est un le milieu de la base du rectangle
# demibase est la direction de la base et hauteur la direction de la hauteur
def TriangleIsocele(Couleur, A, demibase,hauteur):
    (Ax,Ay,Az) = A
    (lx,ly,lz) = demibase
    (hx,hy,hz) = hauteur
    A1 = (Ax-lx,Ay-ly,Az-lz)
    A2 = (Ax+hx,Ay+hy,Az+hz)
    A3 = (Ax+lx,Ay+ly,Az+lz)
    glBegin(GL_TRIANGLES)
    glColor3fv(OpenGLColor(Couleur))
    glVertex3fv( A1 )
    glVertex3fv( A2 )
    glVertex3fv( A3 )
    glEnd()

#crée une ligne dans la scène
def Lines(Couleur,P1,P2):
    glBegin(GL_LINES)
    glColor3fv(Couleur)
    glVertex3fv(P1)
    glVertex3fv(P2)
    glEnd()

#dessine les trois axes dans le repere local
# X,Y,Z couleurs => R V B
def AxesRepere(longueur):
    L = longueur
    P = (.1,.1,.1)
    Lines(RED,P,(L,0,0))
    Lines(GREEN,P,(0,L,0))
    Lines(BLUE,P,(0,0,L))


def OpenGLRepereCamera(): #ne pas toucher
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix();
    glRotatef(rotdegres, 0, 1, 0)
    glTranslatef(player_x, -player_y, player_z)

#################################################################################
#
#   A partir d'ici, vous pouvez modifier ou vous inspirez des fonctions existantes
#   pour créer de nouvelles fonctions  !!!
#
#################################################################################




# un cube qui bouge !! et qui tourne
def RotatingCube():
    glPushMatrix(); # cree un sous repère
    theta = (time.time()*10)%360
    h =  (time.time())%10
    glTranslatef(-1,h,-10)     # translation par rapport au repère parent
    glRotatef(theta, 0, 1, 0)  # rotation autours de l'axe Y du repère parent
    glScale(2,2,2)             # zoom autours des axes du repere parent
    Cube()
    AxesRepere(2)              # desine les axes du repere local
    glPopMatrix();             # revient au repère parent et oublie le repère courant

#Crée les 6 faces d'un cube, un coin du cube touche le point (0,0,0)
# il n'est pas centré !

def Cube():
    Face(YELLOW, (0,0,0),ix,iz)
    Face(GREEN, (0,0,0),ix,iy)
    Face(BLUE,  (0,0,0),iy,iz)
    Face(RED,   (1,1,1),mix,miz)
    Face(BROWN, (1,1,1),mix,miy)
    Face(YELLOW,(1,1,1),miy,miz)


BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
GREEN2= [100, 255, 100]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]
BROWN = [136, 66, 29]
BROWN2 = [136, 100, 60]
YELLOW= [255,255,0]

def TupleChange(x):
    ix = ()
    for i in range(0,len(x)):
        ix = ix + (x[i]*(-1),)
    return ix

def Rect(x,y,z, a,b,c,d,e,f, Couleur):
    ix = TupleChange(x)
    iy = TupleChange(y)
    iz = TupleChange(z)
    Face(Couleur, (a,b,c),x,z)
    Face(Couleur, (a,b,c),x,y)
    Face(Couleur, (a,b,c),y,z)
    Face(Couleur, (d,e,f),ix,iz)
    Face(Couleur, (d,e,f),ix,iy)
    Face(Couleur, (d,e,f),iy,iz)

def Box():
    glPushMatrix(); # cree un sous repère
    if _platform == "win32":
        obj = OBJ(assets,swapyz = True)
    elif _platform == "win64":
        obj = OBJ("aa.obj",swapyz = True)
#    theta = (time.time()*10)%360
#    h =  (time.time())%10

    glTranslatef(5,5,5)     # translation par rapport au repère parent
#    glRotatef(0, 0, 0, 0)  # rotation autours de l'axe Y du repère parent
    glScale(2,2,2)             # zoom autours des axes du repere parent

#    AxesRepere(2)              # desine les axes du repere local
    glCallList(obj.gl_list)
    glPopMatrix();             # revient au repère parent et oublie le repère courant


def Arbre2(a,b,c): #y,z,x
    Rect((1,0,0),(0,2,0),(0,0,1),a+1,b,c+1,a+2,b+2,c+2,BROWN)
    Rect((2,0,0),(0,3,0),(0,0,2),a,b+2,c+1,a+2,b+5,c+3,GREEN)
    Rect((2,0,0),(0,1,0),(0,0,4),a,b+3,c,a+2,b+4,c+4,GREEN)
    Rect((4,0,0),(0,1,0),(0,0,2),a-1,b+3,c+1,a+3,b+4,c+3,GREEN)

#inspirez vous de cette fonction pour créer un décors !
# crée un damier, mais peut servir de relief
def Sol():
    for x in range(-40,40,4) :
        for z in range(20,-40,-4):
            couleur = BLUE
            if (x+z)%8 == 0 : couleur = RED
            Face( couleur, (x, 0,z), (4,0,0) , (0,0,4)  )

#positionne au hasard des arbres dans la scène
Arbres = []
for i in range(30) :
    x = random.randint(-40,40)
    z = random.randint(-40,0)
    Arbres.append((x,z))

#dessine les arbres
def Foret():
    for P in Arbres:
        (x,z) = P
        TriangleIsocele( GREEN , (x, 1,z),  (1,0,0),(0,5,0) )
        TriangleIsocele( GREEN2, (x, 1 ,z), (0,0,1),(0,5,0) )
        Face( BROWN,  (x-0.5, 0, z), (1,0,0),(0,1,0) )
        Face( BROWN2, (x, 0, z-0.5), (0,0,1),(0,1,0) )




# description de la position et de l'orientation du joueur dans la scène
# le joueur est au dessus du sol
player_z = -10
player_y = 1.8  #hauteur des yeux du joueur par rapport au sol 1.8m
player_x = 0
rotdegres = 0


# LOAD OBJECT AFTER PYGAME INIT
if _platform == "win32":
    obj = OBJ(assets,swapyz = True)
elif _platform == "win64":
    obj = OBJ("aa.obj",swapyz = True)

clock = pygame.time.Clock()

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded


# Loop until the user clicks the close button.
done = False

rx, ry = (0,0)
tx, ty = (0,0)
zpos = 5
rotate = move = False
# -------- Main Program Loop -----------
while not done:
   # EVENEMENTS
   # détecte le clic sur le bouton close de la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT):
            # elif e.key == K_F4 and bool(e.mod & KMOD_ALT):
            sys.exit()

    # LOGIQUE
    KeysPressed = pygame.key.get_pressed()

    speed = 1
    rotrad = math.radians(rotdegres)
    dir_cam_x = math.sin(rotrad)
    dir_cam_z = -math.cos(rotrad)


    if KeysPressed[pygame.K_DOWN]:
       player_x   += dir_cam_x * speed
       player_z   += dir_cam_z * speed

    if KeysPressed[pygame.K_UP]:
       player_x   -= dir_cam_x * speed
       player_z   -= dir_cam_z * speed

    if KeysPressed[pygame.K_LEFT]:    rotdegres -= 10
    if KeysPressed[pygame.K_RIGHT]:   rotdegres += 10
    if KeysPressed[pygame.K_ESCAPE]:  done = True

    OpenGLRepereCamera();

    # DESSIN
    Sol()
    Cube()
    RotatingCube()
    Foret()
    Box()
    AxesRepere(5)
    Arbre2(0,0,0)
    #print(rotdegres,dir_cam_x,dir_cam_z)

    # commande affichage

    glPopMatrix();
    glCallList(obj.gl_list)
    glLoadIdentity()
    pygame.display.flip()
    pygame.time.wait(25)
# Close everything down
pygame.quit()
