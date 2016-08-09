import numpy as np
import sys
if sys.version_info[0] == 2:
    import roadrunner
# import time

from scipy.integrate import odeint


from cans2.cans_funcs import gauss_list, get_mask


# Need to generealize to allow power to be specified
def power_model(params):
    """Simplified model for (hopefully) guessing b params.

    Constains a power series as an approximation of diffusion.
    """
    k1 = params[0]
    k2 = params[1]
    k3 = params[2]
    k4 = params[3]
    k5 = params[4]
    b = params[5]
    def growth(amounts, times):
        np.maximum(0, amounts, out=amounts)
        rates = [b*amounts[0]*amounts[1],
                 -b*amounts[0]*amounts[1] + k1 + k2*times + k3*times*times
                 + k3*times**4 + k4*times**5]
        return rates
    return growth


def neighbour_model(params, no_neighs=2):
    """Model for guessing b for single cultures.

    Fast and slow growing neighbours (intended to have b bounded) with
    different diffusion constants.

    """
    kn = params[:2]
    b = params[2:]
    def growth(amounts, times):
        np.maximum(0, amounts, out=amounts)
        C = amounts[::2]
        N = amounts[1::2]
        rates = [b[0]*N[0]*C[0],
                 -b[0]*N[0]*C[0] - kn[0]*(N[0] - N[1]),
                 b[2]*N[1]*C[1],
                 # Factor of no_neighs in diffusion terms is for the
                 # number of each pair of identical neighbours (zero
                 # and fast growers).
                 -b[2]*N[1]*C[1] - no_neighs*kn[0]*(N[1] - N[0]) - no_neighs*kn[1]*(N[1] - N[2]),
                 b[1]*N[2]*C[2],
                 -b[1]*N[2]*C[2] - kn[1]*(N[2] - N[1])]
        return rates
    return growth


def inde_model(params, plate):
    """Return a function for running the inde model.

    Args
    ----
    params : list
        Model parameters

    Nothing is done with the passes plate. It is there for constitancy
    with comp_model which needs attributes from the plate for rate
    calculations. This way we can have one model.solve method.

    """
    # Separate out plate and culture level parameters.
    b_params = params
    # odeint requires times argument in cans_growth function.
    def growth(amounts, times):
        """Return cans rates given current amounts and times."""
        # Cannot have negative amounts.
        np.maximum(0, amounts, out=amounts)
        # An iterator of values for variables/terms appearing in the model.
        vals = zip(b_params, *[iter(amounts)]*2)
        # This will sometimes store negative amounts. This can
        # be corrected in the results returned by odeint if call
        # values are ALSO set to zero at the start of each
        # function call (see np.maximum() above).
        rates = [rate for b, C, N in vals for rate in (b*N*C, -b*N*C)]
        return rates
    return growth


def comp_model(params, plate):
    """Return a function for running the competition model.

    Args
    ----
    params : list
        Model parameters excluding intial amounts.
    plate : Plate
        A corresponding plate with attributes describing the neighbourhood.
    """
    # Separate out plate and culture level parameters.
    kn = params[0]
    b = np.asarray(params[1:])
    neighbourhood = plate.neighbourhood
    # Boolean array of neighbours for each culture. Rows are current
    # culture; cols are neighbours.
    mask = plate.mask
    neigh_nos = plate.neigh_nos
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

        C_rates = b*C*N
        N_rates = -C_rates - kn*N_diffs
        rates = np.append(C_rates, N_rates)
        return rates
    return growth


class Model(object):
    def __init__(self, model, b_index, params, species):
        self.model = model
        self.b_index = b_index
        self.params = params    # A list of parameter names
        self.species = species
        self.no_species = len(self.species)


    # Optional times is for simulations. For fits should be called
    # with plate.times.
    def solve(self, plate, params, times):
        init_amounts = np.repeat(params[:self.no_species], plate.no_cultures)
        # Set C(t=0) to zero for empty locations.
        init_amounts[list(plate.empties)] = 0.0
        growth_func = self.model(params[self.param_index:], plate)
        # mxhnil is the maximum number of messages to be printed.
        sol = odeint(growth_func, init_amounts, times,
                     atol=1.49012e-8, rtol=1.49012e-8, mxhnil=0)
        return np.maximum(0, sol)


    def rr_solve(self, plate, params):
        """Set SBML parameters and solve using RoadRunner.

        Return amounts of all species on the Plate.
        """
        # Initial amounts are assigned to all species using the
        # expressions in the InitialAssignments of the SBML model.
        plate.rr.model.setGlobalParameterValues(params)
        sol = plate.rr_solve()
        return sol


    def rr_solve_spline(self, plate, params):
        """Set SBML parameters and solve spline using RoadRunner.

        Return amounts of all species on the Plate.
        """
        # Initial amounts are assigned to all species using the
        # expressions in the InitialAssignments of the SBML model.
        plate.rr.model.setGlobalParameterValues(params)
        sol = plate.rr_solve_spline()
        return sol


    def rr_solve_selections(self, plate, params):
        """Set SBML parameters and solve using RoadRunner.

        Includes only the selected cultures in the solution. These are
        set by Plate method set_rr_timecourse_selections.

        """
        plate.rr.model.setGlobalParameterValues(params)
        sol = plate.rr_solve_selections()
        return sol


    # Could generalize for other culture level parameters.
    def gen_params(self, plate, mean=50.0, var=0.0):
        """Generate and return a np.array of parameter values.

        Useful for simulations and initial guesses in fitting.
        """
        plate_lvl = self.defaults
        if var:
            # From cans_funcs module
            b = gauss_list(plate.no_cultures, mean=mean, var=var, negs=False)
        else:
            b = [mean]*plate.no_cultures
        params = np.append(plate_lvl, b)
        return params

        
class CompModel(Model):
    def __init__(self, rev_diff=True):
        """Instantiate CompModel.

        If rev_diff is True use reversible reaction equations for
        diffusion.
        """
        self.model = comp_model
        self.b_index = 3
        self.param_index = 2    # First param that is not an amount.
        self.params = ['C_0', 'N_0', 'kn', 'b']
        # Default values of plate level params for simulations.
        self.defaults = [1e-6, 0.1, 0.1]
        self.species = ['C', 'N']
        # Do the species have different initial concentrations at
        # boundaries? Evaluates False for empty string.
        self.species_bc = ["", ""]
        self.no_species = len(self.species)
        self.name = "Competition Model"
        self.rr_solver = self.rr_solve
        # Define SBML model.
        self.reactions = [
            {
                "name": "Growth_{0}",
                "rate": "b{0} * C{0} * N{0}",
                "reactants": [(1, "N{0}"), (1, "C{0}")],
                "products": [(2, "C{0}")],
                "reversible": False,
                # True if species of neighbouring cultures are involved.
                "neighs": False,
                "internals": True,
                "edges": True,
            },
            {
                "name": "Diff_{0}_{1}",
                "rate": "kn * N{0} - kn * N{1}",
                "reactants": [(1, "N{0}")],
                "products": [(1, "N{1}")],
                "reversible": rev_diff,
                "neighs": True,
                "internals": True,
                "edges": True,
            }
        ]
        # Alternative irriversible representation of nutrient diffusion.
        if not rev_diff:
            self.reactions[1]["rate"] = "kn * N{0}"


class CompModelBC(Model):
    """Competition model with special treatment of boundaries.

    The extra parameter NE_0 is the initial amount of nutrients in
    edge cultures.
    """
    def __init__(self, rev_diff=True):
        # self.model =     # Not implemented in python yet
        self.b_index = 4
        self.param_index = 3    # First param that is not an amount.
        self.params = ["C_0", "N_0", "NE_0", "kn", "b"]
        # Default values of plate level params for simulations.
        self.defaults = [1e-6, 0.1, 0.2, 0.1]
        self.species = ["C", "N"]
        self.species_bc = ["", "NE_0"]
        self.no_species = len(self.species)
        self.name = "Competition Model BC"
        self.rr_solver = self.rr_solve
        self.reactions = [
            {
                "name": "Growth_{0}",
                "rate": "b{0} * C{0} * N{0}",
                "reactants": [(1, "N{0}"), (1, "C{0}")],
                "products": [(2, "C{0}")],
                "reversible": False,
                # True if species of neighbouring cultures are involved.
                "neighs": False,
                "internals": True,
                "edges": False,
            },
            {
                "name": "Diff_{0}_{1}",
                "rate": "kn * N{0}",
                "reactants": [(1, "N{0}")],
                "products": [(1, "N{1}")],
                "reversible": False,
                "neighs": True,
                "internals": True,
                "edges": False,
            },
            # Reactions just for boundaries:
            # {...,
            # "internals": False,
            # "edges": True,
            # ...}
            {
                "name": "Growth_{0}_bc",
                # Scale the amount of nutrients by the ratio N_0/NE_0
                # to make a concentration. Edge cultures have more
                # starting nutrients proportional to the greater area
                # belonging to them. I could
                "rate": "b{0} * C{0} * N{0} * N_0/NE_0",
                "reactants": [(1, "N{0}"), (1, "C{0}")],
                "products": [(2, "C{0}")],
                "reversible": False,
                # True if species of neighbouring cultures are involved.
                "neighs": False,
                "internals": False,
                "edges": True,
            },
            {
                "name": "Diff_{0}_{1}_bc",
                "rate": "kn * N{0} * N_0/NE_0",
                "reactants": [(1, "N{0}")],
                "products": [(1, "N{1}")],
                "reversible": False,
                "neighs": True,
                "internals": False,
                "edges": True,
            }

        ]


class IndeModel(Model):
    def __init__(self):
        self.model = inde_model
        self.b_index = 2
        self.param_index = 2    # First param that is not an amount.
        self.params = ['C_0', 'N_0', 'b']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Independent Model'


class PowerModel(Model):
    def __init__(self):
        """Only suitable for single cultures."""
        self.model = power_model5
        self.b_index = 7
        self.param_index = 2
        # Could actually fix C_0 and N_0 with init guess.
        self.params = ['C_0', 'N_0', 'k1', 'k2', 'k3', 'k4', 'k5', 'b']
        self.species = ['C', 'N']
        self.no_species = len(self.species)
        self.name = 'Power Model 5'


class ImagNeighModel(Model):
    def __init__(self, no_neighs):
        """Only suitable for single cultures."""
        self.model = neighbour_model
        self.b_index = 6
        self.param_index = 2
        # Could actually fix C_0 and N_0 with init guess.
        self.params = ['C_0', 'N_0', 'kn1', 'kn2', 'b-', 'b+', 'b']
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
            sol = odeint(growth_func, init_amounts, plate.times)
        else:
            sol = odeint(growth_func, init_amounts, times)
        return np.maximum(0, sol)


if __name__ == '__main__':
    comp_mod = CompModel()
    inde_mod = IndeModel()
    print(inde_mod.model)
    print(comp_mod.model)
    comp_mod_bc = CompModelBC()
    print(comp_mod_bc.__dict__)
    print(comp_mod_bc.rr_solver)
