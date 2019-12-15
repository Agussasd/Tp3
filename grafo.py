import random

class Grafo:
	def __init__(self, dirigido = False):
		self.vertices = {}
		self.dirigido = dirigido
		self.cantidad = 0

	def agregar_vertice(self, vertice):
		if vertice not in self.vertices:
			self.vertices[vertice] = {} #Aca irian los adyacentes
		self.cantidad += 1

	def borrar_vertice(self, vertice):
		if not self.dirigido:
			if vertice in self.vertices:
				for v in self.vertices[v]:
					self.vertices[v].pop(vertice)
		self.vertices.pop(vertice)
		for vertice in self.vertices.values():
			vertice.pop(v, None)
		self.cantidad -= 1

	def ver_vertices(self): 
		return self.vertices

	def agregar_arista(self, v, ady, peso = 1):
		self.agregar_vertice(v)
		self.agregar_vertice(ady)
		self.vertices[v][ady] = peso
		if not self.dirigido:
			self.vertices[ady][v] = peso

	def eliminar_arista(self, v, ady):
		if v in self.vertices:
			if ady in self.vertices[v]:
				self.vertices[v].pop(ady)
				if not self.dirigido:
					self.vertices[ady].pop(v)

	def adyacentes(self, vertice):
		return list(self.vertices[vertice])

	def vertice_random(self):
		return random.choice(list(self.vertices.keys()))

	def peso(self, vertice, adyacente):
		return self.vertices[vertice][adyacente]

	def obtener_cantidad(self):
		return self.cantidad

	def __repr__(self):
		return "{}".format(self.vertices)

	def __iter__(self):
		return iter(self.vertices)
