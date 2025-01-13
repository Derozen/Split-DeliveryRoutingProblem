import numpy as np

def select_element_with_proba(liste,Pg=0.2):
  liste_proba = [Pg]
  reste = 1-Pg
  nombre = len(liste)
  if nombre == 1 :
    return liste[0]
  else:
    random_number = np.random.uniform(0,1)
    if random_number <= Pg :
      return liste[0]
    else:
      np.random.randint(1,nombre)
      return liste[np.random.randint(1,nombre)]

def get_routes(populations) :
  Paths = []
  for sol in populations :
    Paths += [(route,sol.fitness[i]) for i,route in sol.trajet.items()]
  Paths = sorted(Paths, key=lambda x: x[1],reverse=True)
  Routes = []
  for path,fitness in Paths :
    if (path,fitness) not in Routes :
      Routes.append((path,fitness))
  Routes = sorted(Routes, key=lambda x: x[1],reverse=True)
  return Routes

def route_mix(rs,data):
  n = data['n']
  Q = data['Q']
  quantités = data['quantités']
  d = [0 for i in range(n)]
  s = 0
  for r in rs :
    for i,j,q in r :
      d[j-1] += q
  for i in range(n) :
    if d[i] > quantités[i] :
      s +=1
  if s == 0 :
    return True
  else :
    return False
