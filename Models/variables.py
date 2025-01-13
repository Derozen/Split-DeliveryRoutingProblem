from preprocess.dataextraction import extraire_data
import numpy as np
def get_params(data):
    n,quantités,distances,Q = data['n'],data['quantités'],data['distances'],data['Q']
    M = np.sum(quantités)//Q +1

    cas = []
    coefficients = []
    for m in range(M):
        for j in range(1,n+1):
            if quantités[j-1]<=Q :
                for q in range(1,quantités[j-1]+1):
                    cas.append((m,0,j,q))
            else :
                for q in range(1,Q+1):
                    cas.append((m,0,j,q))
        for i in range(1,n+1):
            for j in range(1,n+1):
                if j!=i :
                    if quantités[j-1]<=Q :
                        for q in range(1,quantités[j-1]):
                            cas.append((m,i,j,q))
                    else :
                        for q in range(1,Q):
                            cas.append((m,i,j,q))
        for i in range(1,n+1):
            cas.append((m,i,0,0))

    total = len(cas)
    for m,i,j,q in cas :
        coefficients.append(distances[i][j])

    print(f'Le total de variables est: {total}')
    contraintes = []
    contraintes_2 = []
    constante_inf = []
    constante_eq = []
    for vehicule in range(M) :
        for depart in range(n+1) :
            c = [0 for i in range(total)]
            for t,(m,i,j,q) in enumerate(cas):
                if m == vehicule and i == depart :
                    c[t] = 1
            contraintes.append(c)
            constante_inf.append(1)
    ##
        for arriv in range(n+1) :
            h = [0 for i in range(total)]
            for t,(m,i,j,q) in enumerate(cas):
                if m == vehicule and j==arriv:
                    h[t] = 1
            contraintes.append(h)
            constante_inf.append(1)
    #
    #depart de i = 0
        for dep in range(1,n+1) :
            d = [0 for i in range(total)]
            for t,(m,i,j,q) in enumerate(cas):
                if m == vehicule and i == dep :
                    d[t] = 1
                elif m == vehicule and i == 0 :
                    d[t] = -1
            contraintes.append(d)
            constante_inf.append(0)
    #
    # Somme des i d'arrivee = somme des i de depart
        for point in range(n+1) :
            d = [0 for i in range(total)]
            for t,(m,i,j,q) in enumerate(cas):
                if m == vehicule and i == point :
                    d[t] = 1
                elif m == vehicule and j == point :
                    d[t] = -1
            contraintes_2.append(d)
            constante_eq.append(0)
    #arrivee à j = 0
        d = [0 for i in range(total)]
        for t,(m,i,j,q) in enumerate(cas):
            if m == vehicule and i == 0 :
                d[t] = 1
            elif m == vehicule and j == 0 :
                d[t] = -1
        contraintes_2.append(d)
        constante_eq.append(0)
    #
    # le vehicule ne passe pas 2 fois entre les memes arcs
        for point in range(1,n) :
            for point2 in range(point+1,n+1) :
                d = [0 for i in range(total)]
                for t,(m,i,j,q) in enumerate(cas):
                    if m == vehicule and i == point and j == point2 :
                        d[t] = 1
                    elif m == vehicule and i == point2 and j == point :
                        d[t] = 1
                contraintes.append(d)
                constante_inf.append(1)
        #
        d = [0 for i in range(total)]
        for t,(m,i,j,q) in enumerate(cas):
            if m == vehicule :
                d[t] = q
        contraintes.append(d)
        constante_inf.append(Q)
    ###
    contraintes += contraintes_2
    ###
    for client in range(1,n+1) :
        d = [0 for i in range(total)]
        for t,(m,i,j,q) in enumerate(cas):
            if j == client :
                d[t] = q
        contraintes.append(d)
        constante_eq.append(quantités[client-1])


    return cas,coefficients, contraintes, constante_eq,constante_inf