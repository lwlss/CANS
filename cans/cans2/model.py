import numpy as np


from scipy.integrate import odeint


from cans2.cans_funcs import gauss_list, stdout_redirected, get_mask


# Need to generealize to allow power to be specified
def power_model(params):
    """Simplified model for (hopefully) guessing r params.

    Constains a power series as an approximation of diffusion.

    """
    k1 = params[0]
    k2 = params[1]
    k3 = params[2]
    k4 = params[3]
    k5 = params[4]
    r = params[5]
    def growth(amounts, times):
        print(times)
        np.maximum(0, amounts, out=amounts)
        rates = [r*amounts[0]*amounts[1],
                 -r*amounts[0]*amounts[1] + k1 + k2*times + k3*times*times
                 + k3*times**4 + k4*times**5]
        return rates
    return growth


def neighbour_model(params, no_neighs=2):
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
                 # Factor of no_neighs in diffusion terms is for the
                 # number of each pair of identical neighbours (zero
                 # and fast growers).
                 -r[2]*N[1]*C[1] - no_neighs*kn[0]*(N[1] - N[0]) - no_neighs*kn[1]*(N[1] - N[2]),
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
    def growth(amounts, times):
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
    return growth


def comp_model(params, neighbourhood, mask, neigh_nos):
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
    r = np.asarray(params[1:])
    # odeint requires times argument in cans_growth function.
    def growth(amounts, times):
        """Return model rates given current amounts and times."""
        # Cannot have negative amounts.
        np.maximum(0, amounts, out=amounts)
        # Amounts of nutrients and signal.
        C, N = np.split(amounts, 2)

        # Sum of nutrient diffusion for each culture. This is the
        # slowest part but I can't think of anything faster.
        N_diffs = neigh_nos*N - np.sum(mask*N, axis=1)

        C_rates = r*C*N
        N_rates = -C_rates - kn*N_diffs
        rates = np.append(C_rates, N_rates)
        return rates
    return growth


class Model(object):
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
        init_amounts = np.repeat(params[:self.no_species], plate.no_cultures)

        # init_amounts = np.tile(params[:self.no_species], plate.no_cultures)
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
                                     plate.neighbourhood, plate.mask,
                                     plate.neigh_nos)
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
        self.params = ['C_0', 'N_0', 'kn', 'r']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Competition Model'



class IndeModel(Model):
    def __init__(self):
        self.model = inde_model
        self.r_index = 2
        self.params = ['C_0', 'N_0', 'r']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Independent Model'


class PowerModel(Model):
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
    def __init__(self, no_neighs):
        """Only suitable for single cultures."""
        self.model = neighbour_model
        self.r_index = 6
        # Could actually fix C_0 and N_0 with init guess.
        self.params = ['C_0', 'N_0', 'kn1', 'kn2', 'r-', 'r+', 'r']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Neighbour model'
        self.no_neighs = no_neighs

    def solve(self, plate, params, times=None):
        # Can't inherit becuase tiling of intitial amounts needs to be
        # different (3 for only one culture) and need to pass the
        # number of each type of neighbour to the growth fuction.
        init_amounts = np.tile(params[:self.no_species], 3)
        growth_func = self.model(params[self.no_species:], self.no_neighs)
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
