from pyray import *
from raylib import KEY_DOWN, KEY_UP, KEY_RIGHT, KEY_LEFT, KEY_SPACE, KEY_V, KEY_B, KEY_N
import random

#Données fixées
Hertz=6 #fréquence d'avancement du serpent
SIDE = 40
WIDTH = 20
HEIGHT=10
MOOVE=[(1,0),(-1,0),(0,1),(0,-1)] #right,left, down, up : les mouvements autorisés
snake_init=[
        [1,1],
        [2,1],
        [3,1]
    ]
vitesse_init=MOOVE[0]
FRUIT_init=[WIDTH//2,HEIGHT//2]
Score_min_MegaFruit=5 #score minimal pour que le MegaFruit commence à apparaître

#VARIABLES GLOBALES
snake=snake_init
Higherscore=0
Score=0
FRUIT=FRUIT_init
perdu=False
start=False
Mode_megafruit=False
Mode_death_by_edge=True
Mode_death_by_obstacle=False
vitesse=vitesse_init #vecteur de changement de position
queue_en_attente=0 #Mesure du nombre de cases à rajouter au serpent

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

def activation_mega_fruit():
    '''fonction qui donne les coordonnées et le poids du super fruit
    ainsi que le temps avant apparition et disparition'''
    global MEGAFRUIT,VALEUR_Megafruit, MF_Timer_app, MF_Timer_disp 
    MEGAFRUIT=[
        random.randint(0,WIDTH-1),
        random.randint(0,HEIGHT-1)
        ]
    VALEUR_Megafruit=random.randint(2,5)
    MF_Timer_app=random.randint(10*Hertz,40*Hertz)
    #ici on diminue le temps de disp du MF en fonction du poids
    MF_Timer_disp=random.randint(30,40)+MF_Timer_app-3*VALEUR_Megafruit

def mange_mega_fruit_donc_nouveau_serpent():
    '''stocke la taille de la queue à ajouter, implémente le score,
      et relance le processus d'apparition d'un mega fruit'''
    global queue_en_attente,Score
    Score= Score + VALEUR_Megafruit
    queue_en_attente=VALEUR_Megafruit
    activation_mega_fruit()

def animation():
    '''Calcule le nouveau serpent, implémente le score et change
      le fruit si nécessaire, vérifie si le joueur a perdu'''
    global snake, queue_en_attente
    vx, vy = vitesse
    hx, hy=snake[-1]
    #pour gérer la différence suivant l'activation du mode Mode_death_by_edge
    if Mode_death_by_edge : 
        new_head=[hx+vx,hy+vy]
    else : 
        new_head=[(hx+vx)%WIDTH,(hy+vy)%HEIGHT]
    #Pour détected si le megafruit est mangé
    if Mode_megafruit and Score>=Score_min_MegaFruit: 
        if new_head==MEGAFRUIT : 
            mange_mega_fruit_donc_nouveau_serpent()
    #gestion du cas où le fruit est mangé
    if new_head==FRUIT:
            new_position_fruit()
            modification_score(1)
    else : 
        #ici la variable queue représente le nombre d'élement à rajouter à la queue
        if queue_en_attente>0: 
            queue_en_attente=queue_en_attente-1
        else :
            #seulement s'il n'y a aucun élément à rajouter, on enlève le dernier point 
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

def maj_parametres_homepage():
    '''fonction qui détecte les choix de modes de l'utilisateur quand il est sur le menu home'''
    global Mode_death_by_edge, Mode_death_by_obstacle, Mode_megafruit
    if is_key_pressed(KEY_V):
        Mode_megafruit=not(Mode_megafruit)
    if is_key_pressed(KEY_B):
        Mode_death_by_obstacle=not(Mode_death_by_obstacle)
    if is_key_pressed(KEY_N):
        Mode_death_by_edge=not(Mode_death_by_edge)

def dessin_home_page():
    '''fonction qui dessine la page d'accueil en fonction des paramètre choisis'''
    begin_drawing()
    clear_background(BLACK)
    draw_text('SNAKE',SIDE*WIDTH//4,SIDE*HEIGHT//6,130,YELLOW)
    draw_text('Press the space bar to start the game !',SIDE*WIDTH//8,7*SIDE*HEIGHT//8,25,WHITE)
    color= GREEN if Mode_megafruit else RED
    draw_text('SUPER FRUIT (V)',SIDE*WIDTH//8,4*SIDE*HEIGHT//8,20,color)
    color= GREEN if Mode_death_by_obstacle else RED
    draw_text('OBSTACLE (B)',SIDE*WIDTH//8,5*SIDE*HEIGHT//8,20,color)
    color= GREEN if Mode_death_by_edge else RED
    draw_text('DEATH ON EDGE (N)',SIDE*WIDTH//8,6*SIDE*HEIGHT//8,20,color)
    end_drawing()

def dessin_game_page():
    '''fonction qui dessine la page game'''
    begin_drawing()
    clear_background(BLACK)
    draw_rectangle(FRUIT[0]*SIDE,FRUIT[1]*SIDE,SIDE,SIDE,RED)
    if Mode_megafruit and Score>=Score_min_MegaFruit :
        if MF_Timer_app<=0 and MF_Timer_disp>=0:
            draw_rectangle(MEGAFRUIT[0]*SIDE,MEGAFRUIT[1]*SIDE,SIDE,SIDE,YELLOW)
            draw_text(str(VALEUR_Megafruit),MEGAFRUIT[0]*SIDE+5,MEGAFRUIT[1]*SIDE+5,40,RED)
        if MF_Timer_disp<0 :
            activation_mega_fruit()
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
    while not start and not window_should_close(): 
        dessin_home_page()
        maj_parametres_homepage()
        if is_key_pressed(KEY_SPACE):
            start=True
    start=True
    if Mode_megafruit : 
            activation_mega_fruit()
    while not perdu :
        if Mode_megafruit and Score>=Score_min_MegaFruit : 
            MF_Timer_app=MF_Timer_app-1
            MF_Timer_disp=MF_Timer_disp-1
        
        #optimisation_prise_en_compte_clic
        vitesse=orientation()
        #ANIMATION_futur_serpent et condition de perte
        animation()
        #optimisation_prise_en_compte_clic
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
