from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, lpSum, value, LpStatus
from Models.variables import get_params
import numpy as np
# import os
def solver(data,output_file) :
    # Définir le problème
    problem = LpProblem("Minimisation_multiple_variables", LpMinimize)
    cas,coefficients, contraintes, constante_eq,constante_inf = get_params(data) 
    # Définir les variables
    num_variables = len(cas)
    variables = [LpVariable(f"x{i+1}", lowBound=0, upBound=1, cat=LpInteger) for i in range(num_variables)]

    # Définir la fonction objectif
    # Coefficients de la fonction objectif
    problem += lpSum(coefficients[i] * variables[i] for i in range(num_variables)), "Objectif"

    # Ajouter les contraintes
    for j in range(len(constante_inf)) :
        problem += lpSum(contraintes[j][i] * variables[i] for i in range(num_variables)) <= constante_inf[j], f"Contrainte_inf_{j}"
    # Pour les contraintes d'égalité
    start_idx = len(constante_inf)
    for j in range(len(constante_eq)):
        idx = j + len(contraintes) - len(constante_eq)  # Utiliser le bon index dans contraintes
        problem += lpSum(contraintes[idx][i] * variables[i] for i in range(num_variables)) == constante_eq[j], f"Contrainte_eq_{j}"


    # Résoudre le problème
    status = problem.solve()


    if status == 1:  # Si une solution est trouvée
        print("Statut de la solution:", problem.status)
        print("Valeur optimale de z:", value(problem.objective))
        z = value(problem.objective)
        solutions = []
        print("Valeur optimale de z:", z)
        for t, var in enumerate(variables):
            if value(var) != 0 :
                m,i,j,q = cas[t]
                solutions.append((m,i,j,q))
        trajet = {}
        departs = {m: [] for m,i,j,q in solutions}
        for m,i,j,q in solutions :
            if m not in trajet.keys() :
                trajet[m] = f"Route {m+1}: {i} - {j} ({q}) "
                departs[m].append(j)
            elif i in departs[m] and j!=0 :
                trajet[m] += f"- {j} ({q}) "
                departs[m].append(j)
            elif i in departs[m] and j==0 :
                trajet[m] += f"- {j}"
        lines = []
        for d in  trajet.values():
            lines.append(d)
        total_cost = f'Total cost: {z}'
        n_deliveries = f'Number of deliveries: {len(trajet.keys())}'
        lines.append(total_cost)
        lines.append(n_deliveries)
        loads = [int(np.sum([q for k,i,j,q in solutions if k==m])) for m in trajet.keys()]
        t_loads = 'Trucks loads:'
        for l in loads :
            t_loads += f' {l}'
        lines.append(t_loads)
        with open(output_file,'w') as f:
            f.write('\n'.join(lines))
        for p in solutions:
            print(p)

    else:
        print("Aucune solution optimale trouvée.")
        print(status)
        print("Statut:", LpStatus[status])