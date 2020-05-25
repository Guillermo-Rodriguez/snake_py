"""
	Tutorial original
	Hay similitudes y diferencias muy notorias. Hay funciones que reutilizan código repetido en el tutorial
	https://www.youtube.com/watch?v=bW0o4g4cg1g&list=PLuaRu05D7vP5ij2oZlGHatrF9ZUetf2VA
"""

import turtle
import time
import random

_pos = 0.1 		#tiempo de respiro del sitema entre fotogramas en esta declaración time.sleep(_pos) en el bucle principal
score = 0		#nuestra puntuación inicial dentro del juego
highScore = 0
w,h = 600, 600 	#Ancho y alto de la ventana
"""
	Banderas lógicas para limitar los movimientos de la serpiente como en el juego original
	debe limitar el movimiento contrario al actual ejem. Si se mueve hacia arriba no puede 
	volver sobre sí misma hacia abajo estas funciones no estaban definidas en el tutorial.
	En la declaracion como en el cambio de valor se hace usa declaracion múltiple 
"""
dirUp,dirDown,dirLeft,dirRight = True,True,True,True

"""
	Inicio de la declaración de los objetos del juego (spanglish every where XD)
	-------------------------------------------------
"""


#window config 
wn = turtle.Screen()
wn.title("Snake")
wn.bgcolor("black")
wn.setup(width = w, height = h)
wn.tracer(0)
turtle.resizemode("noresize")

#head snake
head = turtle.Turtle()
head.speed(0) 				#Al iniciar la ventana el objeto ya esta pintado
head.shape("square")		#Forma del objeto en este caso un cuadrado
head.color("white")			#Color del objeto
head.penup()				#Quitar el rastro de movimiento del objeto
head.goto(0,0)				#Posición del objeto (0,0) es el centro de la ventana
head.direction = "stop"		#Dirección inicial de movimiento del objeto 

#feed
feed = turtle.Turtle()
feed.speed(0)
feed.shape("circle")
feed.color("red")
feed.penup()
feed.goto(0,100)
feed.direction = "stop"

#body of the snake
segments = []

#text 

text = turtle.Turtle()
text.speed(0)
text.color("white")
text.penup()
text.hideturtle()
text.goto(0,260)
text.write("Score:0	High Score: 0", align = "center", font = ("Currier", 20, "normal"))

"""
	Fin de la declaración de los objetos del juego
	-------------------------------------------------
"""


"""
	Inicio de la declaración de funciones de movimiento de la serpiente
	-------------------------------------------------------------------
"""

#mov up
def _movUp():
	global dirUp,dirDown,dirLeft,dirRight
	if dirUp :
		dirDown,dirUp,dirLeft,dirRight = False,True,True,True
		head.direction = "up"

#mov down
def _movDown():
	global dirUp,dirDown,dirLeft,dirRight
	if dirDown :
		dirDown,dirUp,dirLeft,dirRight = True,False,True,True
		head.direction = "down"

#mov left
def _movLeft():
	global dirUp,dirDown,dirLeft,dirRight
	if dirLeft :
		dirDown,dirUp,dirLeft,dirRight = True,True,True,False
		head.direction = "left"

#mov right
def _movRight():
	global dirUp,dirDown,dirLeft,dirRight	
	if dirRight :
		dirDown,dirUp,dirLeft,dirRight = True,True,False,True
		head.direction = "right"

"""
	Fin de la declaración de funciones de movimiento de la serpiente
	-------------------------------------------------------------------
"""

#mov head
"""
	Según sea la dirección de la serpiente actualiza las 
	coordenadas de la cabeza como en un plano cartesiano
	obteniendo la coordenada y luego sumando o restando 20 px 
"""
def _mov():
	if head.direction == "up":
		y = head.ycor()
		head.sety(y + 20)

	if 	head.direction == "down":
		y = head.ycor()
		head.sety(y - 20)

	if 	head.direction == "left":
		x = head.xcor()
		head.setx(x - 20)

	if 	head.direction == "right":
		x = head.xcor()
		head.setx(x + 20)

#key listen
"""
	Objeto escucha del teclado por cada flecha del teclado
	existe una funcion de movimiento en la sección de movimiento
"""
wn.listen()
wn.onkeypress(_movUp, "Up")				
wn.onkeypress(_movDown, "Down")				
wn.onkeypress(_movLeft, "Left")				
wn.onkeypress(_movRight, "Right")


"""
	Intersección de la cabeza de la serpiente con la comida
	agrega nuevos segmentos al cuerpo y mueve la comida a una posición random
	entre los valores de los limites de la ventana simpre tomando referencia del plano cartesiano
"""
def _intersectionHeadSnake():
	global score,highScore
	if head.distance(feed) < 20:
		x = random.randint(-280,280)				
		y = random.randint(-280,280)
		feed.goto(x,y)	

		new_seg = turtle.Turtle()
		new_seg.speed(0)
		new_seg.shape("square")
		new_seg.color("grey")
		new_seg.penup()
		segments.append(new_seg)

		#update score
		score += 10

		if score > highScore:
			highScore = score
		#update text score	
		text.clear()	
		text.write("Score:{}	High Score:{}".format(score, highScore), 
			align = "center", font = ("Currier", 20, "normal"))

	totalSeg = len(segments)
	for i in range(totalSeg -1, 0, -1):
		x = segments[i -1].xcor()
		y = segments[i -1].ycor()
		segments[i].goto(x,y)

	if totalSeg > 0:
		x = head.xcor()
		y = head.ycor()
		segments[0].goto(x,y)

#choque con los limites de la ventana
def _intersectionHeadLimit():
	global score,highScore
	if head.xcor() > 280 or head.xcor() < -280 or head.ycor() > 280 or head.ycor() < -280 :
		time.sleep(1)
		head.goto(0,0)
		head.direction = "stop"
		_clearSegs()
		score = 0
		text.clear()	
		text.write("Score:{}	High Score:{}".format(score, highScore), 
			align = "center", font = ("Currier", 20, "normal"))

#intersection body snake
def _intersectionBody():
	global score, highScore
	for segment in segments:
		if segment.distance(head) < 20 :
			time.sleep(1)
			head.goto(0,0)
			head.direction = "stop"
			_clearSegs()
			score = 0
			text.clear()	
			text.write("Score:{}	High Score:{}".format(score, highScore), 
				align = "center", font = ("Currier", 20, "normal"))

"""
	Limpiar los segmentos del cuerpo de la serpiente.
	Eliminando los objetos turtle del vector o lista segments[]
"""
def _clearSegs():
	l = len(segments)
	for i in range(0,l):
		segments[i].hideturtle()
	segments.clear()	

while True:
	wn.update()
	_intersectionHeadLimit()
	_intersectionHeadSnake()
	_mov()
	_intersectionBody()
	time.sleep(_pos)