import numpy as np
import csv


def write_c_meas(plate, outfile=""):
    """Write times and cell observations as csv.

    This can be imported in COPASI and used in the objective functions
    of parameter estimations.
    """
    r1 = ["Time"] + ["C{0}".format(i) for i in range(plate.no_cultures)]
    data = []
    data.append(r1)
    c_array = np.reshape(plate.c_meas, (len(plate.times), plate.no_cultures))
    for i, time in enumerate(plate.times):
        data.append([time] + list(c_array[i]))
    with open(outfile, 'wb') as f:
        writer = csv.writer(f, delimiter="\t")
        for r in data:
            writer.writerow(r)


if __name__ == "__main__":
    from cans2.plate import Plate
    from cans2.model import CompModel
    from cans2.plotter import Plotter

    outdir = "sbml_models/sim_3x3/"
    c_meas_path = outdir + "c_meas.csv"
    sbml_path = outdir + "sim_3x3.xml"

    rows = 3
    cols = 3

    comp_model = CompModel()
    comp_plotter = Plotter(comp_model)

    plate1 = Plate(rows, cols)
    plate1.times = np.linspace(0, 5, 11)

    true_params = {'N_0': 0.1, 'kn': 0.5}
    true_params['C_0'] = true_params['N_0']/100000.0
    plate1.set_sim_data(comp_model, b_mean=100.0, b_var=50.0,
                        custom_params=true_params)

    # comp_plotter.plot_est(plate1, plate1.sim_params, sim=True)

    plate1.set_rr_model(comp_model, plate1.sim_params, outfile=sbml_path)
    print(plate1.rr.model.getFloatingSpeciesInitConcentrations())

    write_c_meas(plate1, c_meas_path)
    print(np.reshape(plate1.c_meas, (len(plate1.times), plate1.no_cultures)))




    # Output SBML model and

    # plate1.est = plate1.fit_model(comp_model, minimizer_opts={"disp": True},
    #                               rr=True, sel=True)
