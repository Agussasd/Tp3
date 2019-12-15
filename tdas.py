class _Nodo:
	def __init__(self, dato, prox = None):
		self.dato = dato
		self.prox = prox

class PilaVaciaError(Exception):
	pass

class Pila:
	def __init__(self):
		self.items = []

	def apilar(self, x):
		self.items.append(x)
	
	def desapilar(self):
		if self.esta_vacia():
			raise PilaVaciaError()
		return self.items.pop()
	
	def esta_vacia(self):
		return len(self.items) == 0

	def ver_tope(self):
		while not self.esta_vacia():
			return self.items[-1]

	def ver_pila(self):
		return self.items[::-1]

class Cola:
	def __init__(self):
		self.items = []

	def encolar(self, x):
		self.items.append(x)
	
	def desencolar(self):
		if self.esta_vacia():
			raise ValueError("La cola esta vacia")
		return self.items.pop(0)
	
	def esta_vacia(self):
		return len(self.items) == 0

	def ver_frente(self):
		while not self.esta_vacia():
			return self.items[-1]

	def ver_cola(self):
		return self.items[::-1]

	def __len__(self):
		len = 0
		for elemento in self.items:
			len += 1
		return len


class ListaEnlazada:
	def __init__(self):
		self.prim = None
		self.len = 0

	def append(self, dato):
		if self.prim == None:
			self.prim = _Nodo(dato, None)
		else:
			act = self.prim
			while act.prox != None:
				act = act.prox
			act.prox = _Nodo(dato, None)

	def __str__(self):
		act = self.prim
		l = []
		while act != None:
			l.append(act.dato)
			act = act.prox
		return str(l)

	def __len__(self):
		act = self.prim
		n = 0
		while act != None:
			n += 1
			act = act.prox
		return n