import numpy as np


from cans2.rank import correlate_ests


from cans2.parser import get_genes
from cans2.process import find_best_fits


best_no_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModel/*.json",
                                     num=2, key="obj_fun"))
best_bc = np.array(find_best_fits("../../results/p15_fits/full_plate/CompModelBC/*.json",
                                  num=2, key="obj_fun"))
print(best_bc)

genes = get_genes("data/p15/ColonyzerOutput.txt")
print(genes)


correlate_ests(genes, ("CompModelBC_1", best_bc[0]),
               ("CompModelBC_2", best_bc[1]))
