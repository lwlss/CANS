import time
import random
import inspyred


from cans2.plate import Plate


# Generator functions for evolutionary strategy.
def gen_random_uniform(random, args):
    """Generate random parameters between the bounds.

    random : A numpy RandomState object seeded with current system
    time upon instatiation.

    bounds : Contained in the args dict. A 2d array of lower and upper
    bounds for each parameter in the model.

    For all parameters values are sampled from a uniform distribution
    in linear space.

    """
    bounds = args.get("bounds")
    params = [random.uniform(l, h) for l, h in zip(bounds[:, 0], bounds[:, 1])]
    return params


def gen_random_uniform_log_C(random, args):
    """Generate random parameters between the bounds.

    random : A numpy RandomState object seeded with current system
    time upon instatiation.

    bounds : Contained in the args dict. A 2d array of lower and upper
    bounds for each parameter in the model.

    For the initial concentration of cells, the exponent is sampled
    over a uniform space and it is assumed that the mantissas of the
    lower and upper bounds are equal. For all other parameters,
    values are sampled from uniform distributions in linear space.

    """
    bounds = args.get("bounds")
    params = [random.uniform(l, h) for l, h in zip(bounds[:, 0], bounds[:, 1])]
    C_0_mantissa, C_0_exp = frexp_10(bounds[0])
    exponent = random.uniform(C_0_exp[0], C_0_exp[1])
    params[0] = C_0_mantissa[0]*10.0**exponent
    return params


def generete_params_from_guesses(random, args):
    """Generate parameters from imaginary neighbour guesses.

    These guesses are obtained from "quick" fits of a simplified
    "imaginary neighbour" model. The quick fits also also require
    starting guesses for the ratio of starting to final cell
    concentration, the ratio of edge to internal culture area, and an
    approximate magnitude of growth parameter b. These are sampled
    randomly from uniform distributions between the bounds. For the
    case of cell ratios samples are taken from the logspace.

    """
    # Random area_ratio and C_ratio.
    area_range = args.get("area_range")
    C_range = args.get("C_range")
    b_range = args.get("b_range")
    area_ratio = random.uniform(low=area_range[0], high=area_range[1])
    C_0_mantissa, C_0_exp = frexp_10(C_range)
    exponent = random.uniform(low=C_0_exp[0], high=C_0_exp[1])
    C_ratio = C_0_matissa[0]*10.0**exponent
    # Random uniform. We could use N(50, 50) (clipped above zero) and
    # could also randomize the mean and variance.
    b_guess = random.uniform(low=b_range[0], high=b_range[1])

    guess_kwargs = args.get("imag_neigh_kwargs")    # Obviously do not unpack.
    guess_kwargs["area_ratio"] = area_ratio
    guess_kwargs["C_ratio"] = C_ratio
    guess_kwargs["imag_neigh_params"][-2:] = [b_guess*1.5, b_guess]

    guess, guesser = fit_imag_neigh(**guess_kwargs)
    return guess


# args required for generate_params_from_guesses. Can set all of the
# below values.
def get_imag_neigh_args(plate, plate_model, C_ratio=1e-4, C_doubt=1e3,
                        b_guess=45.0, area_range=np.array([1.0, 2.0]),
                        b_range=np.array([0.0, 200.0])):
    # Create args needed for below function (to be passed in args).
    imag_neigh_kwargs = {
        "plate": plate,
        "plate_model": plate_model,
        "C_ratio": C_ratio,    # Guess of init_cells/final_cells.
        "kn_start": 0.0,
        "kn_stop": 2.0,
        "kn_num": 21,
        "area_ratio": 1.5,    # Initial dummy val.
        # ['kn1', 'kn2', 'b-', 'b+', 'b']
        "imag_neigh_params": np.array([1.0, 1.0, 0.0, b_guess*1.5, b_guess]),
        "no_neighs": None,    # If None calculated as np.ceil(C_f_max/N_0_guess).
    }
    args = {
        "area_range": area_range,
        "C_range": np.array([C_ratio/C_doubt, C_ratio*C_doubt]),
        "b_range": b_range,
        "imag_neigh_kwargs": imag_neigh_kwargs,
    }
    return args


# Functions for evaluating the candidates.

# Can we use the decorator @inspyred.ec.evaluator for this and maybe
# parallize? Alternatively, we could use each candidate as an initial
# guess for gradient fitting or generate each candidate from gradient
# fits.
def evaluate_fit(candidates, args):
    # Evaluate the objective function for each set of canditate
    # parameters and return this as the fitness. Here fitter and plate
    # are defined outside the scope of the function.
    fitter = args.get("cans_fitter")
    plate = args.get("plate")
    return [fitter._rr_obj(plate, cs) for cs in candidates]

# Can we use the decorator @inspyred.ec.evaluator for this and maybe
# parallize? Alternatively, we could use each candidate as an initial
# guess for gradient fitting or generate each candidate from gradient
# fits.
def evaluate_fit(candidates, args):
    # Evaluate the objective function for each set of canditate
    # parameters and return this as the fitness. Here fitter and plate
    # are defined outside the scope of the function.
    fitter = args.get("cans_fitter")
    plate = args.get("plate")
    return [fitter._rr_obj(plate, cs) for cs in candidates]



# @inspyred.ec.utilities.memoize(maxlen=100)
@inspyred.ec.evaluators.evaluator
def evaluate_with_grad_fit(candidate, args):
    """Gradient fitting using a candidate initial guess.

    For multiprocessing, args must be pickleable. Numpy arrays and (I
    assume) Swig/RoadRunner objects are not pickleable so I have to
    create new Plate objects. This has a low overhead compared to the
    minimization and is a lot easier than finding ways to pickle the
    objects/methods.

    """
    # plate_kwargs should be a dictionary of "rows", "cols", and the
    # subdictionary "data". "data" should contain "times", "c_meas",
    # and "empties" as lists not numpy arrays. We may have to convert
    # to numpy array in Plate.__init__.
    plate = Plate(**args.get("plate_kwargs"))
    model = args.get("model")
    plate.set_rr_model(model, candidate)
    # Now need to fit using.
    bounds = args.get("bounds")
    est = plate.fit_model(model, param_guess=candidate, bounds=bounds,
                          rr=True, minimizer_opts={"disp": False})
    candidate.fitted_params = list(est.x)
    return est.fun





# Also want to try a particle swarm
