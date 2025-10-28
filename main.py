from pyray import *
from raylib import KEY_DOWN, KEY_UP, KEY_RIGHT, KEY_LEFT, KEY_SPACE
import random

#VARIABLES GLOBALES
SIDE = 40
WIDTH = 20
HEIGHT=10
FRUIT=[WIDTH//2,HEIGHT//2]
MOOVE=[(1,0),(-1,0),(0,1),(0,-1)] #right,left, down, up
snake=[
        [1,1],
        [2,1],
        [3,1]
    ]
perdu=False

#CODE DU JEU
init_window(SIDE*WIDTH,SIDE*HEIGHT, "Mon jeu")
set_target_fps(6)
vitesse=MOOVE[0]
while not window_should_close():
    Score=0

    while not perdu :
    

        #ANIMATION
    
        vx, vy = vitesse
        hx, hy=snake[-1]
        new_head=[hx+vx,hy+vy]

        if is_key_pressed(KEY_DOWN): 
            vitesse=MOOVE[2]
        if is_key_pressed(KEY_UP):
            vitesse=MOOVE[3]
        if is_key_pressed(KEY_RIGHT):
            vitesse=MOOVE[0]
        if is_key_pressed(KEY_LEFT):
            vitesse=MOOVE[1]

        if new_head==FRUIT:
            FRUIT=[
                random.randint(0,WIDTH-1),
                random.randint(0,HEIGHT-1)
            ]
            score+=1
        else : 
            snake=snake[1:]
        snake= snake + [new_head]

        #CONDITIONS DE FIN DE PARTIE
        if new_head[1]>=HEIGHT or new_head[1]<0 or new_head[0]<0 or new_head[0]>=WIDTH : 
            perdu=True
        elif new_head in snake[:-1]:
            perdu = True

        #DESSIN
        begin_drawing()
        clear_background(BLACK)

        draw_rectangle(FRUIT[0]*SIDE,FRUIT[1]*SIDE,SIDE,SIDE,RED)

        for i, (x, y) in enumerate(snake) :  #permet de retourner l'indice puis les valeurs
            color= DARKGREEN if i==len(snake)-1 else GREEN
            draw_rectangle(x*SIDE+1,y*SIDE+1,SIDE-2,SIDE-2,color)
    
        end_drawing()


    
    begin_drawing()
    clear_background(BLACK)
    draw_text('GAME OVER',SIDE*WIDTH//8,SIDE*HEIGHT//3,100,RED)
    draw_text('Appuyer sur la barre espace pour recommencer',SIDE*WIDTH//8,2*SIDE*HEIGHT//3,20,WHITE)
    end_drawing()
    if is_key_pressed(KEY_SPACE):
        perdu=False
        snake=[
                [1,1],
                [2,1],
                [3,1]
        ]
        vitesse=MOOVE[0]
close_window()
