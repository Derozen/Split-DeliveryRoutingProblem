import numpy as np
def extraire_data(file):
  with open(file, 'r') as f:
    data = f.readlines()
  data = [x.strip() for x in data]
  data = [x.split(' ') for x in data]
  data = [[int(x) for x in gx if x!=''] for gx in data]
  n = data[0][0] # the number of customer 
  Q = data[0][1] #the maximum capacity of each vehicule
  quantités = data[1] #the demand of each customers
  data = data[2:]
  data = [g for g in data if g != []]
  data = np.array( data)
  distances = np.zeros((n+1, n+1))  #the distance matrix between each node including the clients and the factory. it's a symmetrical
  #matrix where each element of the  diagonal is 0
  for i in range(n+1):
    for j in range(n+1):
      distances[i][j] = int(np.linalg.norm(data[i] - data[j]) + 0.5)
  data = {'n':n,'Q':Q,'distances':distances,'quantités':quantités}
  return data