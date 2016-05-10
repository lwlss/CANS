import numpy as np

from scipy.integrate import odeint

from cans.cans import gauss_list


def inde_model(params):
    """Return a function for running the inde model.

    Args
    ----
    params : list
        Model parameters
    neighbourhood : list
        A list of tuples of neighbour indices for each culture.
    """
    # Separate out plate and culture level parameters.
    r_params = params
    # odeint requires times argument in cans_growth function.
    def inde_growth(amounts, times):
        """Return cans rates given current amounts and times."""
        # Cannot have negative amounts.
        np.maximum(0, amounts, out=amounts)
        # An iterator of values for variables/terms appearing in the model.
        vals = zip(*[iter(amounts)]*2, r_params)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for C, N, r in vals for rate in (r*N*C, -r*N*C)]
        return rates
    return inde_growth


def comp_model(params, neighbourhood):
    """Return a function for running the competition model.

    Args
    ----
    params : list
        Model parameters
    neighbourhood : list
        A list of tuples of neighbour indices for each culture.
    """
    # Separate out plate and culture level parameters.
    kn = params[0]
    r_params = params[1:]
    # odeint requires times argument in cans_growth function.
    def comp_growth(amounts, times):
        """Return model rates given current amounts and times."""
        # Cannot have negative amounts.
        np.maximum(0, amounts, out=amounts)
        # Amounts of nutrients and signal.
        nutrients = amounts[1::2]
        # Sums of nutrient and signal diffusion for each culture.
        N_diffusions = [sum([nutrient - nutrients[j] for j in neighbourhood[i]])
                        for i, nutrient in enumerate(nutrients)]
        # An iterator of values for variables/terms appearing in the model.
        vals = zip(*[iter(amounts)]*2, r_params, N_diffusions)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for C, N, r, Ndiff in vals for rate
                 in (r*N*C, -r*N*C - kn*Ndiff)]
        return rates
    return comp_growth


class Model:
    def __init__(self, model, r_index, params, species):
        self.model = model
        self.r_index = r_index
        self.params = params    # A list of parameter names
        self.species = species

    # Require the neighbourhood and no_cultures from the plate but not
    # any other data.
    def solve(self, plate, params):
        no_species = len(self.species)
        init_amounts = np.tile(params[:no_species], plate.no_cultures)
        # Might be cheaper to pass neighbourhood for the independent
        # model but do nothing with it. However, the comparison below
        # is more explicit.
        if 'kn' in self.params:
            growth_func = self.model(params[no_species:], plate.neighbourhood)
        else:
            growth_func = self.model(params[no_species:])
        sol = odeint(growth_func, init_amounts, plate.times)
        return np.maximum(0, sol)


    def gen_params(self, plate, mean=1.0, var=0.0):
        """Generate and return a np.array of parameter values.

        Useful for simulations and initial guesses in fitting.

        """
        # C(t=0), N(t=0)
        params = [0.005, 1.0]
        if 'kn' in self.params:
            params.append(0.0)
        if var:
            # Need to import function from some module
            r = gauss_list(plate.no_cultures, mean=mean, var=var, negs=False)
        else:
            r = [mean]*plate.no_cultures
        # C(t=0), N(t=0), kn (if present), r0, r1,...
        params = np.array(params + r)
        return params

        
class CompModel(Model):
    def __init__(self):
        self.model = comp_model
        self.r_index = 3
        self.params = ['C(t=0)', 'N(t=0)', 'kn', 'rs']
        self.species = ['C', 'N']


class IndeModel(Model):
    def __init__(self):
        self.model = inde_model
        self.r_index = 2
        self.params = ['C(t=0)', 'N(t=0)', 'rs']
        self.species = ['C', 'N']


if __name__ == '__main__':
    comp_mod = CompModel()
    inde_mod = IndeModel()
    print(inde_mod.model)
    print(comp_mod.model)
