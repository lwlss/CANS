import numpy as np


from scipy.integrate import odeint


from cans2.cans_funcs import gauss_list, stdout_redirected


def guess_model(params):
    """Simplified model for (hopefully) guessing r params.

    Constains a constant k as an approximation for diffusion.

    """
    k = params[0]
    r = params[1]
    def guess_growth(amounts, times):
        np.maximum(0, amounts, out=amounts)
        rates = [r*amounts[0]*amounts[1], -r*amounts[0]*amounts[1] + k]
        return rates
    return guess_growth


def power_model2(params):
    """Simplified model for (hopefully) guessing r params.

    Constains a constant k as an approximation for diffusion.

    """
    k1 = params[0]
    k2 = params[1]
    r = params[2]
    def guess_growth(amounts, times):
        print(times)
        np.maximum(0, amounts, out=amounts)
        rates = [r*amounts[0]*amounts[1],
                -r*amounts[0]*amounts[1] + k1 + k2*times]
        return rates
    return guess_growth


def power_model3(params):
    """Simplified model for (hopefully) guessing r params.

    Constains a constant k as an approximation for diffusion.

    """
    k1 = params[0]
    k2 = params[1]
    k3 = params[2]
    r = params[3]
    def guess_growth(amounts, times):
        print(times)
        np.maximum(0, amounts, out=amounts)
        rates = [r*amounts[0]*amounts[1],
                 -r*amounts[0]*amounts[1] + k1 + k2*times + k3*times*times]
        return rates
    return guess_growth


def power_model5(params):
    """Simplified model for (hopefully) guessing r params.

    Constains a constant k as an approximation for diffusion.

    """
    k1 = params[0]
    k2 = params[1]
    k3 = params[2]
    k4 = params[3]
    k5 = params[4]
    r = params[5]
    def guess_growth(amounts, times):
        print(times)
        np.maximum(0, amounts, out=amounts)
        rates = [r*amounts[0]*amounts[1],
                 -r*amounts[0]*amounts[1] + k1 + k2*times + k3*times*times
                 + k3*times**4 + k4*times**5]
        return rates
    return guess_growth


def neighbour_model(params):
    """Model for guessing r for single cultures.

    Fast and slow growing neighbours (intended to have r bounded) with
    different diffusion constants.

    """
    kn = params[:2]
    r = params[2:]
    def growth(amounts, times):
        np.maximum(0, amounts, out=amounts)
        C = amounts[::2]
        N = amounts[1::2]
        rates = [r[0]*N[0]*C[0],
                 -r[0]*N[0]*C[0] - kn[0]*(N[0] - N[1]),
                 r[2]*N[1]*C[1],
                 -r[2]*N[1]*C[1] - kn[0]*(N[1] - N[0]) - kn[1]*(N[1] - N[2]),
                 r[1]*N[2]*C[2],
                 -r[1]*N[2]*C[2] - kn[1]*(N[2] - N[1])]
        return rates
    return growth


def inde_model(params):
    """Return a function for running the inde model.

    Args
    ----
    params : list
        Model parameters
    """
    # Separate out plate and culture level parameters.
    r_params = params
    # odeint requires times argument in cans_growth function.
    def inde_growth(amounts, times):
        """Return cans rates given current amounts and times."""
        # Cannot have negative amounts.
        np.maximum(0, amounts, out=amounts)
        # An iterator of values for variables/terms appearing in the model.
        vals = zip(r_params, *[iter(amounts)]*2)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for r, C, N in vals for rate in (r*N*C, -r*N*C)]
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
        vals = zip(r_params, N_diffusions, *[iter(amounts)]*2)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for r, Ndiff, C, N, in vals for rate
                 in (r*N*C, -r*N*C - kn*Ndiff)]
        return rates
    return comp_growth


class Model:
    def __init__(self, model, r_index, params, species):
        self.model = model
        self.r_index = r_index
        self.params = params    # A list of parameter names
        self.species = species
        self.no_species = len(self.species)


    # Require the neighbourhood and no_cultures from the plate but not
    # any other data. Optional times is for simulations. If worried
    # about speed can create different solve methods with and
    # without the extra argument.
    def solve(self, plate, params, times=None):
        init_amounts = np.tile(params[:self.no_species], plate.no_cultures)
        # Set C(t=0) to zero for empty locations.
        for index in plate.empties:
            init_amounts[self.no_species*index] = 0.0
        # For alternative approach without using (0,0) bounds can
        # insert r=0 values according to indices in empties. In this
        # approach the r values would be absent from the params so
        # would have to be inserted rather than replaced. These would
        # then have to be reentered in the final result from the
        # minimizer as nan in order for placings to correspond.

        # Might be cheaper to pass neighbourhood for the independent
        # model but do nothing with it. However, the comparison with
        # 'kn' below is more explicit.
        if 'kn' in self.params:
            growth_func = self.model(params[self.no_species:],
                                     plate.neighbourhood)
        else:
            growth_func = self.model(params[self.no_species:])
        # Optional smooth times for simulations/fits.
        if times is None:
            with stdout_redirected():    # Redirect lsoda warnings
                sol = odeint(growth_func, init_amounts, plate.times)
        else:
            with stdout_redirected():    # Redirect lsoda warnings
                sol = odeint(growth_func, init_amounts, times)
        return np.maximum(0, sol)


    def gen_params(self, plate, mean=1.0, var=0.0):
        """Generate and return a np.array of parameter values.

        Useful for simulations and initial guesses in fitting.

        """
        # C(t=0), N(t=0)
        params = [0.005, 1.0]    # Might be better to set defaults in
                                 # model __init__.
        if 'kn' in self.params:
            params.append(0.0)
        if var:
            # Need to import function from cans functional modules.
            r = gauss_list(plate.no_cultures, mean=mean, var=var, negs=False)
        else:
            r = [mean]*plate.no_cultures
        # C(t=0), N(t=0), kn (if present), r0, r1,...
        params = np.array(params + r)    # Can remove r params according to the empties.
        return params

        
class CompModel(Model):
    def __init__(self):
        self.model = comp_model
        self.r_index = 3
        self.params = ['C_0', 'N_0', 'kn', 'rs']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Competition Model'


class IndeModel(Model):
    def __init__(self):
        self.model = inde_model
        self.r_index = 2
        self.params = ['C_0', 'N_0', 'rs']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Independent Model'


class GuessModel(Model):
    def __init__(self):
        """Only suitable for single cultures."""
        self.model = guess_model
        self.r_index = 3
        # Could actually fix C_0 and N_0 with init guess.
        self.params = ['C_0', 'N_0', 'k', 'r']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Guess Model'


class PowerModel2(Model):
    def __init__(self):
        """Only suitable for single cultures."""
        self.model = power_model2
        self.r_index = 4
        # Could actually fix C_0 and N_0 with init guess.
        self.params = ['C_0', 'N_0', 'k1', 'k2', 'r']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Power Model 2'


class PowerModel3(Model):
    def __init__(self):
        """Only suitable for single cultures."""
        self.model = power_model3
        self.r_index = 5
        # Could actually fix C_0 and N_0 with init guess.
        self.params = ['C_0', 'N_0', 'k1', 'k2', 'k3', 'r']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Power Model 3'


class PowerModel5(Model):
    def __init__(self):
        """Only suitable for single cultures."""
        self.model = power_model5
        self.r_index = 7
        # Could actually fix C_0 and N_0 with init guess.
        self.params = ['C_0', 'N_0', 'k1', 'k2', 'k3', 'k4', 'k5', 'r']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Power Model 5'


class NeighModel(Model):
    def __init__(self):
        """Only suitable for single cultures."""
        self.model = neighbour_model
        self.r_index = 6
        # Could actually fix C_0 and N_0 with init guess.
        self.params = ['C_0', 'N_0', 'kn1', 'kn2', 'r-', 'r+', 'r']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Neighbour model'


    def solve(self, plate, params, times=None):
        init_amounts = np.tile(params[:self.no_species], 3)
        growth_func = self.model(params[self.no_species:])
        if times is None:
            with stdout_redirected():    # Redirect lsoda warnings
                sol = odeint(growth_func, init_amounts, plate.times)
        else:
            with stdout_redirected():    # Redirect lsoda warnings
                sol = odeint(growth_func, init_amounts, times)
        return np.maximum(0, sol)


if __name__ == '__main__':
    comp_mod = CompModel()
    inde_mod = IndeModel()
    print(inde_mod.model)
    print(comp_mod.model)
