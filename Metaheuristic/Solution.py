import numpy as np

class Solution :
  def __init__(self,trajet,cout,distances) :
    self.trajet = trajet
    self.cout = cout
    distance_route = {}
    for k in trajet.keys() :
      distance_route[k] = np.sum([distances[i][j] for i,j,q in trajet[k]])
    self.distance_route = distance_route
    index = {}
    K = len(trajet.keys())
    for k in range(1,K+1) :
      charge =  np.sum([q for i,j,q in trajet[k]])
      index[k] = charge / distance_route[k]
    self.fitness = index