import numpy as np
from .Solution import Solution
from .functions import route_mix, get_routes, select_element_with_proba
def generate_solutions(data,avance={}) :
    n = data['n']
    Q = data['Q']
    quantités = data['quantités']
    distances = data['distances']
    M = np.sum(quantités)//Q +1
    if avance == {} :
      A = 0 +Q
      stop = []
      S = M * Q
      f = quantités.copy()
      R = [i for i in range(1,n+1)]
      P = {}
      k = 1
      #y = [[0 for m in range(M)]for i in range(1,n+1)]
      #v = [[0 for m in range(M)]for i in range(1,n+1)]
      y = []
      v = []
    else:
      stop = []
      y = avance['y']
      v = avance['v']
      f = avance['f']
      R = avance['R']
      P = avance['P']
      k = avance['k']
      S = (M+1-k) * Q
      A = 0+Q
    rules = ['furthest','closest','highest_demand','smallest_demand','median','random',
             'furthest_node_on_smallest_arc','furthest_Clarke_Wright']
    rules2 = ['round_up','round_down','full']
    rule2 =  np.random.choice(rules2)
    rule =   np.random.choice(rules)
    print(rule)
    print(rule2)
    def round_(x,rule2) :
      if rule2 == 'round_down' :
        return np.floor(x)
      elif rule2 == 'round_up' :
        return np.ceil(x)
      elif rule2 == 'full' :
        return x
    def control_1(rule):
      if rule == 'furthest' :
        if R == []:
          stop.append(1)
          print('stop')
        else :
          if len(R)== 1:
            return R[0]
          else:
            nodes_ranked = sorted(R, key=lambda x: distances[0][x], reverse=True)
            return nodes_ranked[0]
      elif rule == 'closest' :
        if R == []:
          stop.append(1)
          print('stop')
        else :
          if len(R)== 1:
            return R[0]
          else:
            nodes_ranked = sorted(R, key=lambda x: distances[0][x])
            return nodes_ranked[0]
      elif rule == 'highest_demand' :
        if R == []:
          stop.append(1)
          print('stop')
        else :
          if len(R)== 1:
            return R[0]
          else:
            return np.argmax(f)+1
      elif rule == 'smallest_demand' :
        if R == []:
          stop.append(1)
          print('stop')
        else :
          if len(R)== 1:
            return R[0]
          else:
            demand = sorted(R, key=lambda x: f[x-1])
            return demand[0]
      elif rule == 'median' :
        if R == []:
          stop.append(1)
          print('stop')
        else :
          if len(R)%2 == 0 :
            nodes_ranked = sorted(R, key=lambda x: distances[0][x])
            mediane = len(R)//2
            return nodes_ranked[mediane-1]
          else :
            nodes_ranked = sorted(R, key=lambda x: distances[0][x])
            mediane = len(R)//2
            return nodes_ranked[mediane]
      elif rule == 'random' :
        if R == []:
          stop.append(1)
          print('stop')
        else :
          if len(R)==1:
            return R[0]
          else:
            return np.random.choice(R)
      elif rule == 'furthest_node_on_smallest_arc' :
        if R == []:
          stop.append(1)
          print('stop')
        elif len(R) == 1 :
          return  R[0]
        elif len(R) == 2:
          smallest = sorted(R,key= lambda x: distances[0][x],reverse=True)
          return smallest[0]
        else :
          arcs = sorted([[i,j] for i in R for j in R if j!=i
          ], key=lambda x: distances[x[0]][x[1]])
          smallest = sorted(arcs[0],key= lambda x: distances[0][x],reverse=True)
          return smallest[0]

      elif rule == 'furthest_Clarke_Wright' :
        if R == []:
          stop.append(1)
          print('stop')

        elif len(R) == 1 :
          return  R[0]
        elif len(R) == 2:
          nodes_ranked = sorted(R, key=lambda x: distances[0][x], reverse=True)
          return nodes_ranked[0]
        else :
          savings = sorted([(i,j) for i in R for j in R if j!=i
          ], key=lambda x: distances[0][x[0]] - distances[x[0]][x[1]] + distances[0][x[1]],reverse=True)
          smallest = sorted(savings[0],key= lambda x: distances[0][x],reverse=True)
          return smallest[0]
    def control_2(b,k,rule2,M=M,Q=Q):
        if R == [] :
          print("stop")
          stop.append(1)
        elif len(R) == 1 :
          i = R[0]
          P[k].append(i)
          if f[i-1] <= b:
            R.remove(i)
            y[k-1][i-1] = 1
            v[k-1][i-1] = f[i-1]
            f[i-1] = 0
            stop.append(1)
          else :
            if b>0:
              y[k-1][i-1] = 1
              v[k-1][i-1] = b
              f[i-1] -= b
              S = (M+1-k)*Q
              A = round_(S/(M-k),rule2)

        else :
          nodes_ranked = sorted(R, key=lambda x: distances[P[k][-1]][x])
          i,j = R[0],R[1]
          if f[i-1]>b and f[j-1]<=b and b>0:# step 2.a
            if rule2 != 'full' :
              if b-f[j-1] <= A :
                y[k-1][j-1] = 1
                v[k-1][j-1] = f[j-1]
                R.remove(j)
                P[k].append(j)
                S = S - (b - f[j-1])
                A = round_(S/(M-k),rule2)
                f[j-1] = 0
              else :
                y[k-1][j-1] = 1
                v[k-1][j-1] = f[j-1]
                R.remove(j)
                P[k].append(j)
                b -= f[j-1]
                f[j-1] = 0
                control_2(b,k,rule2)
            else:
                y[k-1][j-1] = 1
                v[k-1][j-1] = f[j-1]
                R.remove(j)
                P[k].append(j)
                b -= f[j-1]
                f[j-1] = 0
                control_2(b,k,rule2)
#####################"
          elif f[i-1]<= b and f[j-1]>b : #step 2.b
            if rule2 != 'full' :
              if b-f[i-1] <= A :
                y[k-1][i-1] = 1
                v[k-1][i-1] = f[i-1]
                R.remove(i)
                P[k].append(i)
                S = S - (b - f[i-1])
                A = round_(S/(M-k))
                f[i-1] = 0
              else :
                y[k-1][i-1] = 1
                v[k-1][i-1] = f[i-1]
                R.remove(i)
                P[k].append(i)
                b -= f[i-1]
                f[i-1] = 0
                control_2(b,k,rule2)
            else:
              y[k-1][i-1] = 1
              v[k-1][i-1] = f[i-1]
              R.remove(i)
              P[k].append(i)
              b -= f[i-1]
              f[i-1] = 0
              control_2(b,k,rule2)
#####################"
          elif f[i-1]<=b and f[j-1]<=b and f[i-1]+f[j-1]>b: #step 2.c
            if rule2!= 'full':
              if f[i-1]==b:
                y[k-1][i-1] = 1
                v[k-1][i-1] = f[i-1]
                R.remove(i)
                P[k].append(i)
                A = round_(S/(M-k),rule2)
                f[i-1] = 0
                print(f)
                print(i)
              else:
                if f[j-1]<b:
                  y[k-1][i-1] = 1
                  v[k-1][i-1] = f[i-1]
                  R.remove(i)
                  P[k].append(i)
                  y[k-1][j-1] = 1
                  v[k-1][j-1] = b-f[i-1]
                  A = round_(S/(M-k),rule2)
                  f[i-1] = 0
                  f[j-1] -= v[k-1][j-1]
                  P[k].append(j)
                  print(f)
                  print(i)
                  print(j)
                else:
                  y[k-1][i-1] = 1
                  v[k-1][i-1] = f[i-1]
                  R.remove(i)
                  P[k].append(i)
                  A = round_(S/(M-k),rule2)
                  f[i-1] = 0
            else:
              if f[i-1]<b:
                y[k-1][i-1] = 1
                v[k-1][i-1] = f[i-1]
                R.remove(i)
                P[k].append(i)
                y[k-1][j-1] = 1
                v[k-1][j-1] = b-f[i-1]
                f[i-1] = 0
                f[j-1] -= v[k-1][j-1]
                print(f)
                print(i)
                print(j)
                P[k].append(j)
              else:
                y[k-1][i-1] = 1
                v[k-1][i-1] = f[i-1]
                R.remove(i)
                P[k].append(i)
                f[i-1] = 0
#####################"
          elif f[i-1]<=b and f[j-1]<=b and f[i-1]+f[j-1]<=b: #step 2.d
            if rule2!= 'full':
              if b- f[i-1] - f[j-1] <= A:
                y[k-1][i-1] = 1
                v[k-1][i-1] = f[i-1]
                R.remove(i)
                R.remove(j)
                P[k].append(i)
                P[k].append(j)
                y[k-1][j-1] = 1
                v[k-1][j-1] = f[j-1]
                S -= (b- f[i-1] - f[j-1])
                A = round_(S/(M-k),rule2)
                f[i-1] = 0
                f[j-1] = 0
                print(f)
                print(i)
                print(j)
              else :
                y[k-1][i-1] = 1
                v[k-1][i-1] = f[i-1]
                R.remove(i)
                R.remove(j)
                P[k].append(i)
                P[k].append(j)
                y[k-1][j-1] = 1
                v[k-1][j-1] = f[j-1]
                b -= (f[i-1] + f[j-1])
                f[i-1] = 0
                f[j-1] = 0
                print(f)
                print(i)
                print(j)
                control_2(b,k,rule2)
            else:
              y[k-1][i-1] = 1
              v[k-1][i-1] = f[i-1]
              R.remove(i)
              R.remove(j)
              P[k].append(i)
              P[k].append(j)
              y[k-1][j-1] = 1
              v[k-1][j-1] = f[j-1]
              b -= (f[i-1] + f[j-1])
              f[i-1] = 0
              f[j-1] = 0
              print(f)
              print(i)
              print(j)
              control_2(b,k,rule2)
          elif f[i-1]>b and f[j-1]>b and b>0: #step 2.e
            y[k-1][i-1] = 1
            v[k-1][i-1] = b
            f[i-1] -= b
            print(f'f{i} non complet')
            P[k].append(i)



    while R!= [] :
      P[k] = []
      b = Q
      i = control_1(rule)
      if stop != [] :
        print('pause')
        break
      P[k].append(i)
      y.append([0 for i in range(n)])
      v.append([0 for i in range(n)])
      if f[i-1] > Q:
        y[k-1][i-1] = 1
        v[k-1][i-1] = Q
        f[i-1] -= Q
        A = round_(S/(M-k),rule2)
        S = S - Q
        k += 1
        b -= Q
        print(f)
        print(i)
      else:
        if rule2 != 'full':
          if Q-f[i-1]<=A :
            y[k-1][i-1] = 1
            v[k-1][i-1] = f[i-1]
            R.remove(i)
            S = S - (Q - f[i-1])
            if k<M:
              A = round_(S/(M-k),rule2)
            f[i-1] = 0
            k += 1
            # on revient a l'étape 1
            print(f)
            print(i)
            #print("Back to 1")
          else :
            y[k-1][i-1] = 1
            v[k-1][i-1] = f[i-1]
            R.remove(i)
            b -= f[i-1]
            f[i-1] = 0
            print(f)
            print(i)
            control_2(b,k,rule2)
            print(f"route {k}")
            k+=1
            if stop != [] or R== [] :
              break
        else:
          y[k-1][i-1] = 1
          v[k-1][i-1] = f[i-1]
          R.remove(i)
          b -= f[i-1]
          f[i-1] = 0
          control_2(b,k,rule2)
          print(f"route {k}")
          k+=1
          if stop != [] or R== [] :
            break

    if np.sum(f)!= 0:
      print(f'R est {R}')
    trajet = {}
    for t in range(1,k) :
      if len(P[t]) == 0 :
        continue
      elif len(P[t]) == 1 :
        point = P[t][0]
        trajet[t] = [(0,point,v[t-1][point-1]),(point,0,0)]
      else :
        point = P[t][0]
        trajet[t] = [(0,point,v[t-1][point-1])]
        for i in range(1,len(P[t])) :
          point2 = P[t][i]
          point1 = P[t][i-1]
          trajet[t].append((point1,point2,v[t-1][point2-1]))
        trajet[t].append((P[t][-1],0,0))
    cout = 0
    for t in range(1,k) :
      for i,j,q in trajet[t] :
        cout += distances[i][j]
      if j!=0 and q == 0:
        print('alerte alerte alerte alerte')
        print(i,j,q)
        print(rule)
        print(rule2)
    print(len(trajet.keys())-k)
    #print(cout)
    return Solution(trajet,cout,distances)




def genetic_algorithm(populations,data,pop_gen=70) :
    Routes = get_routes(populations)
    n = data['n']
    Q = data['Q']
    quantités = data['quantités']
    distances = data['distances']
    routes = Routes.copy()

  #for iter in range(n_iter) :
    generation = []
    Select_routes = []
#######
    def gener_gene(data) :
      n = data['n']
      Q = data['Q']
      quantités = data['quantités']
      distances = data['distances']
      R = [i for i in range(1,n+1)]
      P = {}
      f=quantités.copy()
      v=[]
      y=[]
#######
      if routes != [] :
        current_route = select_element_with_proba(routes)
##########
        print(f'route est {current_route}')
        print(f'Routes sont {routes}')
        if route_mix(Select_routes+[current_route[0]],data) :
          routes.remove(current_route)
          current_route = current_route[0]
          P[len(P.keys())+1] = [j for i,j,q in current_route if j!=0]
          k = len(P.keys())
          v.append([0 for i in range(n)])
          y.append([0 for i in range(n)])
          for i,j,q in current_route :
              if j!=0 :
                f[j-1] -= q
                v[k-1][j-1] = q
                y[k-1][j-1] = 1
                if f[j-1]==0 :
                  R.remove(j)
          Select_routes.append(current_route)
##########
          if routes != [] :
            for fois in range(len(routes)) :
              current_route = select_element_with_proba(routes)
              if route_mix(Select_routes+[current_route[0]],data) :
                routes.remove(current_route)
                current_route = current_route[0]
                Select_routes.append(current_route)
                m = len(P.keys())+1
                v.append([0 for i in range(n)])
                y.append([0 for i in range(n)])
                P[m] = [j for i,j,q in current_route if j!=0]
                for i,j,q in current_route :
                  if j!=0 :
                    f[j-1] -= q
                    v[m-1][j-1] = q
                    y[m-1][j-1] = 1
                    if f[j-1] ==0:
                      print( Select_routes[:-1])
                      print(current_route)
                      R.remove(j)
  ##########
            if np.sum(f) > 0:
              avance = {}
              avance['y'] = y
              avance['v'] = v
              avance['P'] = P
              avance['R'] = R
              avance['f'] = f
              avance['k'] = len(P.keys()) +1
              generation.append(generate_solutions(data,avance=avance))
              print('solution générée')
            else :
              K = len(P.keys())
              trajet = {}
              for t in range(1,K+1) :
                if len(P[t]) == 0 :
                  continue
                elif len(P[t]) == 1 :
                  point = P[t][0]
                  trajet[t] = [(0,point,v[t-1][point-1]),(point,0,0)]
                else :
                  point = P[t][0]
                  trajet[t] = [(0,point,v[t-1][point-1])]
                  for i in range(1,len(P[t])) :
                    point2 = P[t][i]
                    point1 = P[t][i-1]
                    trajet[t].append((point1,point2,v[t-1][point2-1]))
                  trajet[t].append((P[t][-1],0,0))
              cout = 0
              for t in range(1,k) :
                for i,j,q in trajet[t] :
                  cout += distances[i][j]
              generation.append(Solution(trajet,cout,f))
##########
        else :
          routes.remove(current_route)
          current_route = current_route[0]
          Select_routes.append(current_route)
          P[len(P.keys())+1] = [j for i,j,q in current_route if j!=0]
          k = len(P.keys())
          v.append([0 for i in range(n)])
          y.append([0 for i in range(n)])
          for i,j,q in current_route :
              if j!=0 :
                f[j-1] -= q
                v[k-1][j-1] = q
                y[k-1][j-1] = 1
                if f[j-1]==0 :
                  R.remove(j)
          avance = {}
          avance['y'] = y
          avance['v'] = v
          avance['P'] = P
          avance['R'] = R
          avance['f'] = f
          avance['k'] = k
          generation.append(generate_solutions(data,avance=avance))
#######
##########
      else :
        generation.append(generate_solutions(data))

#######
    for it in range(pop_gen) :
      gener_gene(data)
      print(len(generation))
    print(len(generation))
    return generation



