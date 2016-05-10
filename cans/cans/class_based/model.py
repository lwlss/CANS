def inde_model():
    pass

def comp_model():
    pass


class Model:

    def __init__(self, model, r_index, params):
        self.model = model
        self.r_index = r_index
        self.params = params    # A list of parameter names


    def solve(self, plate, params):
        init_amounts = np.tile(params[:r_index], plate.no_cultures)
        rate_func = self.model(params[r_index:], plate.neighbourhood)
        sol = odeint.(rate_func, init_amounts, plate.times)
        return np.maximum(0, sol)


    def gen_params(self, plate, mean=1.0, var=0.0):
    """Return a np.array of parameter values."""
        # C(t=0), N(t=0)
        params = [0.005, 1.0]
        if kn in self.params:
            params.append(0.0)
        if var:
            # Need to import function
            r = gauss_list(plate.no_cultures, mean=mean, var=var, negs=False)
        else:
            r = [mean]*plate.no_cultures
        # C(t=0), N(t=0), (kn), r0, r1,...
        params = np.array(params + r)
        return params

        
class CompModel(Model):

    def __init__(self):
        self.model = comp_model
        self.r_index = 3
        self.params = params['C(t=0)', 'N(t=0)', 'kn', 'rs']


class IndeModel(Model):

    def __init__(self):
        self.model = inde_model
        self.r_index = 2
        self.params = params['C(t=0)', 'N(t=0)', 'rs']
