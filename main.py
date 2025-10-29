from pyray import *
from raylib import KEY_DOWN, KEY_UP, KEY_RIGHT, KEY_LEFT, KEY_SPACE
import random
#Données fixées
Hertz=6
SIDE = 40
WIDTH = 20
HEIGHT=10
MOOVE=[(1,0),(-1,0),(0,1),(0,-1)] #right,left, down, up
snake_init=[
        [1,1],
        [2,1],
        [3,1]
    ]
vitesse_init=MOOVE[0]
FRUIT_init=[WIDTH//2,HEIGHT//2]


#VARIABLES GLOBALES
snake=snake_init
Higherscore=0
Score=0
FRUIT=FRUIT_init
perdu=False
vitesse=vitesse_init

def initiateur_variable():
    '''Remet à l'état initial les variables qui doivent l'être pour recommencer une partie'''
    global snake, perdu, vitesse
    snake=snake_init
    perdu=False
    vitesse=vitesse_init

def orientation():
    '''Renvoie le vecteur de déplacement élémentaire en accord avec la dernière touche enfoncée'''
    global vitesse
    if is_key_pressed(KEY_DOWN): 
        vitesse=MOOVE[2]
    if is_key_pressed(KEY_UP):
        vitesse=MOOVE[3]
    if is_key_pressed(KEY_RIGHT):
        vitesse=MOOVE[0]
    if is_key_pressed(KEY_LEFT):
        vitesse=MOOVE[1]
    return vitesse  

def new_position_fruit(): 
    '''Calcul des coordonnées du nouveau fruit'''
    global FRUIT
    FRUIT=[
        random.randint(0,WIDTH-1),
        random.randint(0,HEIGHT-1)
        ]
    
def animation():
    '''Calcule le nouveau serpent, implémente le score et change
      le fruit si nécessaire, vérifie si le joueur a perdu'''
    global snake
    vx, vy = vitesse
    hx, hy=snake[-1]
    new_head=[hx+vx,hy+vy]

    if new_head==FRUIT:
            new_position_fruit()
            modification_score(1)
    else : 
        snake=snake[1:]
    snake=snake + [new_head]
    condition_perte(new_head,snake)
    
def modification_score(indicateur):
    '''Mets à jour le score et le meilleur score, en prenant en compte le poids du succès
    réalisé avec indicateur qui est nul si défaite, et non nul si un fruit ou superfruit est mangé'''
    global Higherscore, Score
    if indicateur>0:
        Score=Score+indicateur
    if indicateur==0 :
        Higherscore=max(Higherscore,Score)
        Score=0

def dessin_game_page():
    '''fonction qui dessine la page game'''
    begin_drawing()
    clear_background(BLACK)
    draw_rectangle(FRUIT[0]*SIDE,FRUIT[1]*SIDE,SIDE,SIDE,RED)
    draw_text("Score="+Strscore,SIDE,SIDE,20,WHITE)
    for i, (x, y) in enumerate(snake) :  #permet de retourner l'indice puis les valeurs
        color= BLUE if i==len(snake)-1 else GREEN
        draw_rectangle(x*SIDE+1,y*SIDE+1,SIDE-2,SIDE-2,color)
    end_drawing()

def dessin_gameover_page():
    '''fonction qui dessine la page gameover'''
    begin_drawing()
    clear_background(BLACK)
    draw_text("Score="+Strscore,SIDE,SIDE,20,WHITE)
    draw_text("Higher score="+Strhigherscore,SIDE,2*SIDE,20,WHITE)
    draw_text('GAME OVER',SIDE*WIDTH//8,SIDE*HEIGHT//3,100,RED)
    draw_text('Press the space bar to restart the game !',SIDE*WIDTH//8,2*SIDE*HEIGHT//3,20,WHITE)
    end_drawing()

def condition_perte(new_head,snake):
    '''Regarde si le joueur a perdu et modifie la variable 'perdu' si c'est le cas'''
    global perdu
    if new_head[1]>=HEIGHT or new_head[1]<0 or new_head[0]<0 or new_head[0]>=WIDTH : 
        perdu=True
    elif new_head in snake[:-1]:
        perdu=True

#CODE DU JEU
init_window(SIDE*WIDTH,SIDE*HEIGHT, "Mon jeu")
set_target_fps(Hertz)

while not window_should_close():

    while not perdu :

        #optimisation_prise_en_compe_clic
        vitesse=orientation()
        #ANIMATION_futur_serpent et condition de perte
        animation()
        #optimisation_prise_en_compe_clic
        vitesse=orientation()
        #DESSIN PAGE GAME
        Strscore=str(Score)
        dessin_game_page()

    #Page Game Over
    modification_score(0)
    Strhigherscore=str(Higherscore)
    dessin_gameover_page()
    #Retour au jeu
    if is_key_pressed(KEY_SPACE):
        initiateur_variable()
close_window()
