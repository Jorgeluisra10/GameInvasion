import pygame
import random
import math
from pygame import mixer


# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800,600))

# Titulo e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("extraterrestre.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load('wepik-export-20231001051249ixuw.png')

# Agregar música
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)


# Variables del Jugador
img_jugador = pygame.image.load("astronave.png")
jugador_x = 368
jugador_y = 520
jugador_x_cambio = 0

# Variables del Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 10

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("ovni.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(2)
    enemigo_y_cambio.append(50)

# Variables de la bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 520
bala_x_cambio = 0
bala_y_cambio = 10
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font('boston.ttf', 32)
texto_X = 10
texto_y = 10


# Texto final de Juego
fuente_final = pygame.font.Font('CutOutsFLF.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render('JUEGO TERMINADO', True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (210, 270))



#Función mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255,255,255))
    pantalla.blit(texto, (x,y))

# Función Jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

# Función Enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# Función disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

# Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # Imagen fondo
    pantalla.blit(fondo, (0,0))

    # Iterar eventos
    for evento in pygame.event.get():

        # Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento Presionar teclas
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -2
            elif evento.key == pygame.K_RIGHT:
                jugador_x_cambio = +2
            elif evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                nueva_bala = {
                "x": jugador_x,
                "y": jugador_y,
                "velocidad": -2
                }
                balas.append(nueva_bala)
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)


        # Evento Soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicación del jugador
    jugador_x += jugador_x_cambio


    # Mantener dentro de bordes del jugador
    if jugador_x <= 3:
        jugador_x = 3
    elif jugador_x >= 734:
        jugador_x = 734


    # Modificar ubicación del enemigo
    for e in range(cantidad_enemigos):

        # Fin juego
        if enemigo_y[e] > 465:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    # Mantener dentro de bordes del enemigo
        if enemigo_x[e] <= 0:
                enemigo_x_cambio[e] = 2
                enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 734:
               enemigo_x_cambio[e] = -2
               enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e],
        bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound('golpe.mp3')
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala

    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala,(bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)


    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_X, texto_y)

    # Actualizar
    pygame.display.update()
