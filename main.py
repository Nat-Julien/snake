from pyray import *
SIDE = 40
WIDTH = 20
HEIGHT=10
snake=[
        [1,1],
        [2,1],
        [3,1]
    ]
init_window(SIDE*WIDTH,SIDE*HEIGHT, "Mon jeu")
set_target_fps(10)
vitesse=[1,0]
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    #ANIMATION
    
    vx, vy = vitesse
    hx, hy=snake[-1]
    new_head=[hx+vx,hy+vy]
    snake= snake[1:]+[new_head]
    
    
    #Dessin
    for i, (x, y) in enumerate(snake) :  #permet de retourner l'indice puis les valeurs
        color= GREEN if i==len(snake)-1 else DARKGREEN
        draw_rectangle(x*SIDE+1,y*SIDE+1,SIDE-2,SIDE-2,color)
    
    end_drawing()

close_window()
