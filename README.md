Le Split Delivery Vehicle Routing Problem (SD-VRP) est une variante du problème de tournées de
véhicules à capacité limitée (CVRP), qui est l’un des problèmes les plus étudiés dans le domaine
de l’optimisation combinatoire et des sciences de la logistique. Contrairement au CVRP, où
chaque client doit être servi par un seul véhicule, le SD-VRP permet à un client d’être livré par
plusieurs véhicules, à condition que la totalité de sa demande soit satisfaite. C’est un outil
puissant pour résoudre des problèmes logistiques complexes dans un large éventail de contextes
industriels. En permettant une flexibilité accrue dans la répartition des demandes et l’utilisation
des ressources, il contribue à réduire les coûts, améliorer l’efficacité et répondre aux besoins
croissants en matière de transport durable.
Ces caractéristiques rend le SD-VRP particulièrement pertinent dans des contextes où :
− La demande de certains clients dépasse la capacité d’un seul véhicule.
− Les itinéraires doivent être optimisés pour réduire les coûts ou maximiser l'efficacité tout en
répondant à des contraintes de capacités.

Il est une approche innovante pour résoudre les problèmes logistiques complexes où la flexibilité
dans la livraison est essentielle. Voici quelques avantages et applications pratiques du SD-VRP :
− Réduction des coûts logistiques : En permettant de partager la demande d’un client entre
plusieurs véhicules, le SD-VRP minimise les trajets inutiles ou sous-optimaux, réduisant ainsi
les coûts de transport.
− Amélioration de l’efficacité des livraisons : L’utilisation de plusieurs véhicules pour un même
client permet d’adapter la logistique à des situations complexes, comme des zones
géographiques éloignées ou une forte densité de clients.
− Gestion des ressources limitées : Dans des contextes où la flotte de véhicules est restreinte,
le SD-VRP optimise l’utilisation des ressources en répartissant efficacement les livraisons.
− Flexibilité face à des contraintes opérationnelles : Les entreprises peuvent mieux gérer les
demandes variables ou imprévues, notamment lors de pics saisonniers ou dans des
environnements urbains congestionnés.


Le problème “Split Delivery Vehicle Routing Problem”
Le Split Delivery Vehicle Routing Problem (SD-VRP) est une relaxation du problème classique de
tournée de véhicules à capacité limitée (CVRP), où chaque client peut être servi par plus d’un
véhicule.
Données d’entrée :
− Localisation :
o Le dépôt est situé au nœud 0.
o Un ensemble de n clients {1, ..., n}, représentés par leurs coordonnées.
− Une flotte de M véhicules {1, ..., M} est disponible.
o Chaque véhicule a une capacité maximale Q.
− Chaque client est associé à une demande qᵢ, qui doit être entièrement satisfaite.
Coût :
− Une matrice D spécifie le coût ou la distance entre chaque paire de nœuds (à calculer via
les coordonnées).
Toutes les distances sont euclidiennes. Les coordonnées des nœuds dans les fichiers d’entrée
permettent de calculer les distances entre les clients et le dépôt. La distance entre deux nœuds i
et j est calculée selon la formule de distance euclidienne adaptée, suivante :
![image](https://github.com/user-attachments/assets/a7c467d4-e0f4-4175-b123-23c6ecb480a3)

Format des fichiers d’entrée
Chaque instance du SD-VRP est stockée dans un fichier texte suivant un format structuré précis.
Structure du fichier d’entrée :
− Première ligne : Deux paramètres :
o n : Nombre total de clients.
o Q : Capacité maximale de chaque véhicule.
− Deuxième ligne : Les demandes de chaque client (quantité à livrer). Liste des demandes,
séparées par des espaces.
− Lignes suivantes, les coordonnées des nœuds :
o La première ligne, parmi elles, correspond aux coordonnées du dépôt.
o Les lignes suivantes indiquent les coordonnées de chaque client, une ligne par
client.
Exemple de fichier d’entrée (Case0) :
Si nous avons 3 clients et une capacité de véhicule de 10, avec des demandes respectives de 4, 5,
et 6 unités, le fichier pourrait ressembler à ceci :
3 10
4 5 6
0 0
2 3
4 5
6 7
− Première ligne : Il y a 3 clients, et la capacité des véhicules est de 10.
− Deuxième ligne : Les demandes des clients sont 4, 5, et 6 unités.
− Troisième ligne et suivantes : Coordonnées des nœuds :
o Le dépôt est situé au point (0, 0).
o Les clients sont situés respectivement aux points (2, 3), (4, 5), et (6, 7).

Afin de resoudre ce problème, j'ai utilisé deux méthodes, la modelisation linéaire (pour Case0) et un algrithme genetique ( metaheuristique).
Activez l'environnement virtuel

env\Scripts\activate

Installez ensuite  les dépendances 


pip install -r requirements.txt


Vous pouvez tester la solution sur test.py

Source :
A Genetic Algorithm for the Split Delivery Vehicle Routing Problem by Joseph Hubert Wilck IV1 , Tom M. Cavalier2 : https://www.scirp.org/journal/paperinformation?paperid=19939
 
A Construction Heuristic for the Split Delivery Vehicle Routing Problem Joseph Hubert Wilck IV1, Tom M. Cavalier2 : https://www.scirp.org/journal/paperinformation?paperid=19928
