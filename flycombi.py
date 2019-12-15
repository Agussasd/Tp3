import csv
import sys
from grafo import Grafo
from biblioteca import dijkstra, bfs, centralidad_biblioteca, mst_prim, orden_topologico
from heapq import heapify, heappush, heappop #Heappush encola, heappop desencola del heap

#peso = [int(tiempo_promedio), int(precio), int(cant_vuelos)]


"""Terminado hasta ahora: camino_mas 🟌
						  camino_escalas 🟌
						  itinerario 🟌🟌
						  centralidad 🟌🟌🟌 (Falla)
						  nueva_aerolinea 🟌🟌
"""

#aeropuertos.csv formato: ciudad,codigo_aeropuerto,latitud,longitud
#vuelos.csv formato aeropuerto_i,aeropuerto_j,tiempo_promedio,precio,cant_vuelos_entre_aeropuertos

COMANDOS = ["listar_operaciones", "camino_mas", "camino_escalas", "centralidad", "itinerario", "nueva_aerolinea"]


def nueva_aerolinea(vuelos, archivo):
	"""Recibe los vuelos y un archivo a escribir y debe devolver un archivo nuevo con una aerolinea que conecte a todos los aeropuertos con el minimo costo (peso)"""
	mst = mst_prim(vuelos) #Necesito un arbol de tendido minimo porque me piden que el peso tiene que ser el minimo posible
	with open(archivo, "w") as archivo:
		visitados = []
		for v in mst:
			visitados.append(v)
			for w in mst.adyacentes(v):
				if w in visitados:
					continue
				tiempo_promedio, precio, cant_vuelos = mst.peso(v, w)
				linea = ",".join([v, w, str(tiempo_promedio), str(precio), str(cant_vuelos)])
				archivo.write(linea + "\n")
	print("OK")

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
	
def centralidad(vuelos, k): #k la cantidad de aeropuertos mas importantes a mostrar
	"""Tendira que imprimir los aeropuertos mas importantes, pero no funciona del todo bien"""
	n = int(k)
	centralidades = centralidad_biblioteca(vuelos)
	#print(centralidades)
	centralidades_ordenadas = sorted(centralidades, key=lambda i: centralidades[i]) #Ordeno el diccionario por valor, lo saque de stack overflow asi que esto puede ser lo q este fallando
	centralidades_ordenadas.reverse()
	#print("\n" * 2)
	#print(centralidades_ordenadas)
	for i in range(n):
		print(centralidades_ordenadas[i], end = ", ")
	
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
		#print(camino)
		aer = (minimo[1])[camino[0]]
		camino.insert(0, aer)
		#print(camino)
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
		#print(camino)
		aer = (minimo[1])[camino[0]]
		camino.insert(0, aer)
		#print(camino)
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
	if comandos[0] == "centralidad":
		return centralidad(vuelos, parametros[0])
	if comandos[0] == "itinerario":
		return itinerario(aeropuertos, vuelos, parametros[0])
	if comandos[0] == "nueva_aerolinea":
		return nueva_aerolinea(vuelos, parametros[0])

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
