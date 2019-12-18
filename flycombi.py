#!/usr/bin/python3

import csv
import sys
from grafo import Grafo
from biblioteca import dijkstra, bfs,  mst_prim, orden_topologico, random_walk, ciclo_vacaciones

#peso = [int(tiempo_promedio), int(precio), int(cant_vuelos)]

"""Terminado hasta ahora: camino_mas 🟌
						  camino_escalas 🟌
						  itinerario 🟌🟌
						  nueva_aerolinea 🟌🟌
						  vacaciones 🟌🟌🟌
						  centralidad_aprox 🟌
"""

#aeropuertos.csv formato: ciudad,codigo_aeropuerto,latitud,longitud
#vuelos.csv formato aeropuerto_i,aeropuerto_j,tiempo_promedio,precio,cant_vuelos_entre_aeropuertos

COMANDOS = ["camino_mas", "camino_escalas", "itinerario", "nueva_aerolinea", "centralidad_aprox", "vacaciones"]

def vacaciones(vuelos, aeropuertos, origen, k):
	n = int(k)
	visitados = []
	for a_origen in aeropuertos[origen]:
		if ciclo_vacaciones(vuelos, a_origen, a_origen, visitados, n, 0):
			break
	if len(visitados) == 0:
		print("No se encontro recorrido")
		return
	visitados.append(a_origen)
	print(" -> ".join(visitados))

def centralidad_aprox(vuelos, k):
	n = int(k)
	centralidad = {}
	for v in vuelos:
		centralidad[v] = 0
	for i in range(1500):
		recorrido = random_walk(vuelos, 500)
		for v in recorrido:
			centralidad[v] += 1
	centralidades_ordenadas = sorted(centralidad, key=lambda i: centralidad[i])
	centralidades_ordenadas.reverse()
	print(", ".join(centralidades_ordenadas[:n]))

def nueva_aerolinea(vuelos, archivo):
	"""Recibe los vuelos y un archivo a escribir y debe devolver un archivo nuevo con una aerolinea que conecte a todos los aeropuertos con el minimo costo (peso)"""
	mst = mst_prim(vuelos) #Necesito un arbol de tendido minimo porque me piden que el peso tiene que ser el minimo posible
	with open(archivo, 'w') as archivo:
		for v in mst:
			visitados = set()
			for w in mst.adyacentes(v):
				if w in visitados: 
					continue
				archivo.write('{},{},{},{},{}\n'.format(v, w, mst.peso(v, w)[0], mst.peso(v, w)[1], mst.peso(v, w)[2]))
				visitados.add(w)
	print('OK')

def itinerario(aeropuertos, vuelos, archivo):
	"""Imprime el orden en el que deben visitarse las ciudades que se pasan como archivo, y el camino minimo en tiempo"""
	grafo = Grafo(True)
	with open(archivo, "r") as archivo:
		archivo_csv = csv.reader(archivo)
		ciudades = next(archivo_csv)
		for ciudad in ciudades:
			grafo.agregar_vertice(ciudad)
		for linea in archivo_csv:
			grafo.agregar_arista(linea[0], linea[1], None)
	itinerario = orden_topologico(grafo) #Utilizo orden topologico porque los vuelos deben realizarse en cierto orden
	orden_visita = ", ".join(itinerario)
	print(orden_visita) #Imprimo el recorrido
	for ciudad in range(len(itinerario) - 1):
		origen = itinerario[ciudad]
		destino = itinerario[ciudad + 1]
		camino_minimo = camino_escalas(aeropuertos, vuelos, origen, destino)
		if camino_minimo != None:
			print(camino_minimo) #Imprimo el camino en escalas
	
def camino_escalas(aeropuertos, vuelos, origen, destino):
	"""Similar a camino_mas, pero en este caso la lista es segun la menor cantidad de escalas"""
	minimo = []
	for aeropuerto_origen in aeropuertos[origen]:
		for aeropuerto_destino in aeropuertos[destino]:
			padre, orden = bfs(vuelos, aeropuerto_origen, aeropuerto_destino)
			if len(minimo) == 0 or (orden[aeropuerto_destino] < (minimo[0])[minimo[3]]):
				minimo = (orden, padre, aeropuerto_origen, aeropuerto_destino)
	camino = [minimo[3]]
	while camino[0] != minimo[2]:
		aer = (minimo[1])[camino[0]]
		camino.insert(0, aer)
	resultado = " -> ".join(camino)
	print(resultado)

def camino_mas(aeropuertos, vuelos, filtro, origen, destino):
	"""Imprime una lista en orden para ir desde el origen hasta el destino, segun el tipo de filtro que interese (barato o rapido)"""
	minimo = []
	for aeropuerto_origen in aeropuertos[origen]:
		for aeropuerto_destino in aeropuertos[destino]:
			dist, padre = dijkstra(vuelos, aeropuerto_origen, aeropuerto_destino, 1 if filtro == "barato" else 0) #Uso esta funcion para encontrar el camino_minimo, si el filtro es barato el peso es 1, en otro caso 0
			if len(minimo) == 0 or (dist[aeropuerto_destino] < (minimo[0])[minimo[3]]):
				minimo = (dist, padre, aeropuerto_origen, aeropuerto_destino)
	camino = [minimo[3]]
	while minimo[2] != camino[0]:
		aer = (minimo[1])[camino[0]]
		camino.insert(0, aer)
	resultado = " -> ".join(camino)
	print(resultado)

def listar_operaciones():
	for comando in COMANDOS:
		print(comando)

def procesar_aeropuertos():
	aeropuertos = {}
	with open(sys.argv[1]) as archivo:
		archivo_csv = csv.reader(archivo)
		for linea in archivo_csv:
			aeropuertos[linea[0]] = aeropuertos.get(linea[0], []) + [linea[1]]
	return aeropuertos

def procesar_vuelos():
	vuelos = Grafo()
	with open(sys.argv[2]) as archivo:
		archivo_csv = csv.reader(archivo)
		for origen, destino, tiempo_promedio, precio, cant_vuelos in archivo_csv:
			peso = [int(tiempo_promedio), int(precio), int(cant_vuelos)]
			vuelos.agregar_arista(origen, destino, peso)	
	return vuelos

def procesar_comandos(comandos, parametros, aeropuertos, vuelos):
	if comandos[0] == "camino_mas":
		return camino_mas(aeropuertos, vuelos, parametros[0], parametros[1], parametros[2])
	if comandos[0] == "camino_escalas":
		return camino_escalas(aeropuertos, vuelos, parametros[0], parametros[1])
	if comandos[0] == "itinerario":
		return itinerario(aeropuertos, vuelos, parametros[0])
	if comandos[0] == "nueva_aerolinea":
		return nueva_aerolinea(vuelos, parametros[0])
	if comandos[0] == "centralidad_aprox":
		return centralidad_aprox(vuelos, parametros[0])
	if comandos[0] == "vacaciones":
		return vacaciones(vuelos, aeropuertos, parametros[0], parametros[1])

def main():
	aeropuertos = procesar_aeropuertos()
	vuelos = procesar_vuelos()
	for linea in sys.stdin:
		comandos = linea.rstrip("\n").split(" ")
		if(comandos[0]) == "listar_operaciones":
			listar_operaciones()
		parametros = " ".join(comandos[1:]).split(",")
		procesar_comandos(comandos, parametros, aeropuertos, vuelos)

main()
