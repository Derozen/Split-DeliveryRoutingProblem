from Models.linearsolver import solver
from preprocess.dataextraction import extraire_data
from Metaheuristic.geneticalgo import genetic_algo_routes


# data = extraire_data('Instances/Case0.txt')
# output_file = 'outputs/Output0.txt'
# solver(data,output_file)


#Testez l'lgorithme géntique pour case 9
genetic_algo_routes('Instances/Case9.txt','outputs/Output9.txt')