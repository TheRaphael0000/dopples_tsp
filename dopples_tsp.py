import itertools
import numpy as np
from collections import defaultdict
from python_tsp.exact import solve_tsp_dynamic_programming
from pprint import pprint

temples = {
    "START": (-2, 0),
    "ECAFLIP": (1, -5),
    "ENIRIPSA": (7, 1),
    "IOP": (1, 3),
    "CRA": (0, 3),
    "FECA": (12, 5),
    "SACRIEUR": (-3, -4),
    "SADIDA": (-1, 9),
    "OSAMODAS": (8, 2),
    "ENUTROF": (-1, -4),
    "SRAM": (-4, 0),
    "XÉLOR": (3, 1),
    "PANDAWA": (4, -2),
    "ROUBLARD": (3, 3),
    "ZOBAL": (1, -8),
    "STEAMER": (9, 1),
    "HELIOTROPE": (4, 0),
    "HUPPERMAGE": (-4, -2),
    "OUGINAK": (12, 3),
}

zaaps = {
    "Village d'Amakna": (-2, 0),
    "Bord de la forêt maléfique": (-1, 13),
    # "Coin des Bouftou": (5, 7),
    # "Port de Madrestam": (7, -4),
}


def manhattan_distance(a, b):
    return sum(abs(a[i] - b[i]) for i in range(len(a)))


zaap_to_temple = defaultdict(lambda: np.inf)
for (t, t_pos), (zaap, zaap_pos) in itertools.product(temples.items(), zaaps.items()):
    d = manhattan_distance(t_pos, zaap_pos)
    if d < zaap_to_temple[t]:
        zaap_to_temple[t] = d

pprint(zaap_to_temple)


temples_dist = {}

# if its shorter to use the haversack + zaap, use it
for (t1, t1_pos), (t2, t2_pos) in itertools.combinations(temples.items(), 2):
    d = manhattan_distance(t1_pos, t2_pos)
    temples_dist[(t1, t2)] = min(d, zaap_to_temple[t2])
    temples_dist[(t2, t1)] = min(d, zaap_to_temple[t1])

id_to_name = dict(enumerate(temples.keys()))
name_to_id = dict((v, k) for k, v in id_to_name.items())


# create the distance matrix
temples_dist_matrix = np.empty(shape=tuple(2 * [len(temples)]))

for t1, t2 in itertools.product(temples, temples):
    t1_, t2_ = name_to_id[t1], name_to_id[t2]
    if t1 == t2:
        temples_dist_matrix[t1_, t2_] = 0
    else:
        temples_dist_matrix[t1_, t2_] = temples_dist[(t1, t2)]


pprint(temples_dist_matrix)

# don't need to end at the start
temples_dist_matrix[:, 0] = 0

permutation_, distance = solve_tsp_dynamic_programming(temples_dist_matrix)

permutation = [id_to_name[p] for p in permutation_]

pprint(permutation)
pprint(distance)
