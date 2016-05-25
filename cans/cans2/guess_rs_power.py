import numpy as np
#import matplotlib.pyplot as plt


from cans2.model import IndeModel, CompModel, GuessModel
from cans2.guesser import Guesser
from cans2.plate import Plate
from cans2.plotter import Plotter
#from cans2.cans_funcs import gauss_list
from cans2.zoning import resim_zone


inde_model = IndeModel()
comp_model = CompModel()
#guess_model = GuessModel()
comp_guesser = Guesser(comp_model)
inde_plotter = Plotter(IndeModel())
comp_plotter = Plotter(CompModel())
