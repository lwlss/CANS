import numpy as np


from cans2.plate import Plate
from cans2.model import CompModel, CompModelBC, IndeModel
from cans2.guesser import Guesser
from cans2.cans_funcs import gauss_list
from cans2.plotter import Plotter


def sim_and_fit(rows, cols, times, plate_model, true_params, fit_model,
                b_guess, C_doubt=1e3, N_doubt=2.0,
                area_ratio=1.0, C_ratio=1e-5,):
    """Simulate a Plate and carry out a quick fit.

    Return a Plate containing the estimates in Cultures.

    plate_model : CANS Model instance to simulate values for the plate.

    true_params : np.array of all parameters required for comp_model
    ordered according to comp_model.params and with culture level
    parameters supplied for all cultures.

    fit_model : (str) "log_eq" or "imag_neighs" for logistic equivalent or
    imaginary neighbour model.

    b_guess : Guess for parameter b. One guess for all cultures. The
    quick fit aims to improve upon this.

    See Guesser.quick_fit_log_eq documentation for information on
    C_doubt and N_doubt and how the

    See Guesser documentation for area_ratio and C_ratio.

    """
    plate = Plate(rows, cols)
    plate.times = times
    plate.sim_params = true_params
    # set_sim_data also sets rr_model with the simulated params.
    plate.set_sim_data(plate_model, noise=False)

    plotter = Plotter(plate_model)
    plotter.plot_est_rr(plate, plate.sim_params, sim=True)

    guesser = Guesser(plate, plate_model,
                      area_ratio=area_ratio, C_ratio=C_ratio)

    if fit_model == "log_eq":
        quick_guess = guesser.quick_fit_log_eq(b_guess, C_doubt=C_doubt)

    elif fit_model == "imag_neighs":
        message = "Imaginary neighbour quick fitting not yet implemented."
        raise ValueError(message)
    return quick_guess, guesser


model = CompModelBC()
rows = 3
cols = 3
times = np.linspace(0, 5, 11)
true_params = {"N_0": 0.1, "NE_0": 0.15, "kn": 1.0}
true_params["C_0"] = true_params["N_0"]/10000
bs = gauss_list(rows*cols, mean=50.0, var=15.0, negs=False)
# Make a np.array of true params.
true_params = np.array([true_params[p] for p in model.params[:model.b_index]]
                       + list(bs))
quick_fit_kwargs = {
    "rows": rows,
    "cols": cols,
    "times": times,
    "plate_model": model,
    "true_params": true_params,
    "fit_model": "log_eq",
    "b_guess": 45.0,
    "C_doubt": 1e3,
    "N_doubt": 2.0,
    # Guess of edge_area/internal_area. Only required for CompModelBC and
    # ignored for CompModel.
    "area_ratio": 1.0,
    "C_ratio": 1e-6,    # Guess of init_cells/final_cells.
}

quick_guess, quick_guesser = sim_and_fit(**quick_fit_kwargs)
# Need to add in a kn guess.

quick_guess = np.delete(quick_guess, model.params.index("kn"))

inde_model = IndeModel()
plotter = Plotter(model)
plotter.plot_culture_fits(quick_guesser.plate, inde_model, sim=True)
