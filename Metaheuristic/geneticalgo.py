from .functions import get_routes
from .generate import genetic_algorithm, generate_solutions
from preprocess.dataextraction import extraire_data
import numpy as np
def genetic(populations,data,n_iter=5) :
  Routes = get_routes(populations)
  peuple = populations.copy()
  for iter in range(n_iter) :
    generation = genetic_algorithm(peuple,data)
    generation = sorted(generation, key=lambda x: x.cout)
    peuple = sorted(peuple, key=lambda x: x.cout)
    for nop in range(10) :
      old = peuple[nop]
      for Nn in range(len(generation)-10,len(generation)) :
        new = generation[Nn]
        if old.cout < new.cout :
          generation[Nn] = peuple[nop]
    peuple = generation
    print(f'iteration {iter}')
  return peuple

def genetic_algo_routes(file,output_file):
  data = extraire_data(file)
  populations = []
  for iter in range(100) :
    sol = generate_solutions(data)
    populations.append(sol)
  final =  genetic(populations,data,n_iter=5)
  final = sorted(final, key=lambda x: x.cout)
  sol = final[0]
  z = sol.cout
  cas = []
  print("Valeur optimale de z:",z )
  for m in sol.trajet.keys():
    for i,j,q in sol.trajet[m]:
      cas.append((m,i,j,q))
  description = {}
  departs = {m: [] for m,i,j,q in cas}
  for m,i,j,q in cas :
    if m not in description.keys() :
      description[m] = f"Route {m}: {i} - {j} ({q}) "
      departs[m].append(j)
    elif i in departs[m] and j!=0 :
      description[m] += f"- {j} ({q}) "
      departs[m].append(j)
    elif i in departs[m] and j==0 :
      description[m] += f"- {j}"
    lines = []
    for d in  description.values():
      lines.append(d)
    total_cost = f'Total cost: {z}'
    n_deliveries = f'Number of deliveries: {len(sol.trajet.keys())}'
    lines.append(total_cost)
    lines.append(n_deliveries)
    loads = [int(np.sum([q for i,j,q in sol.trajet[m]])) for m in sol.trajet.keys()]
    t_loads = 'Trucks loads:'
    for l in loads :
      t_loads += f' {l}'
    lines.append(t_loads)
    with open(output_file, 'w') as f:
      f.write('\n'.join(lines))