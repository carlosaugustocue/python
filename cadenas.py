# .count()
# .capitalize()
# .title()
# .swapcase()
# .replace(,)
# .split()
# .strip()
# .lstrip()
# .rstrip()
# .find()
# .index()
# eval()	#Este y el siguiente son super métodos
# exec()

name = "Carlos"
print(type(name))
# -----------------------------------------------------------
# las comillas triples son sensibles a los saltos de línea
message = """Este es un mensaje
con saltos de línea"""
print(message)
# -----------------------------------------------------------
# Indexación
print(name[0])
print(name[1])
# -----------------------------------------------------------
# Concatenacion
first_name = "Carlos"
last_name = "Aranzazu"
full_name = first_name + " " + last_name
print(full_name)
# -----------------------------------------------------------
# Repetición
print("Hola " * 5)
# -----------------------------------------------------------
# Longitud
print(len(name))
# -----------------------------------------------------------
print(first_name)
print(first_name.capitalize())
print(first_name.title())   # Capitaliza cada palabra
print(first_name.swapcase())    # Invierte mayúsculas y minúsculas
# -----------------------------------------------------------
print(first_name.strip())    # Elimina espacios en blanco
print(first_name.lstrip())   # Elimina espacios en blanco a la izquierda
print(first_name.rstrip())   # Elimina espacios en blanco a la derecha
# -----------------------------------------------------------

