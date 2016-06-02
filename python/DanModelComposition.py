import compiler
import numpy as np

def comp_model_AC(params, neighbourhood,ODE=False):
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
    b = params[1:]

    N_diffs=["kn*({}*N[{}]-".format(len(neighbourhood[i]),i)+"("+"+".join(["N[{}]".format(j) for j in neighbourhood[i]])+"))" for i in range(len(b))]
    C_expressions=["b[{}]*C[{}]*N[{}]".format(i,i,i) for i in range(len(b))]
    N_expressions=["-b[{}]*C[{}]*N[{}]+".format(i,i,i)+N_diffs[i] for i in range(len(b))]

    C_ODEs=["dC[{}]/dt = ".format(i)+C_exp for i,C_exp in enumerate(C_expressions)]
    N_ODEs=["dN[{}]/dt = ".format(i)+N_exp for i,N_exp in enumerate(N_expressions)]
    All_ODEs=C_ODEs+N_ODEs

    C_compiled=[compiler.compile(C_exp,'<string>', 'eval') for C_exp in C_expressions]
    N_compiled=[compiler.compile(N_exp,'<string>', 'eval') for N_exp in N_expressions]
    
    # odeint requires times argument in cans_growth function.
    def comp_growth(amounts, times):
        """Return model rates given current amounts and times."""
        # There must be a way to avoid having to do this...
        # Currently, some kind of variable scope problem occurs without it (or similar)...
        aaaaaaargh=b+[kn]
        # Cannot have negative amounts.
        amounts=np.maximum(0, amounts)
        # Amounts of nutrients and signal.
        C = amounts[0:len(amounts)/2]
        N = amounts[len(amounts)/2:]

        C_rates = [eval(C_comp) for C_comp in C_compiled]
        N_rates = [eval(N_comp) for N_comp in N_compiled]
        return (C_rates+N_rates)
    if ODE:
        return (All_ODEs)
    else:
        return (comp_growth)

params=[1.0,1.2,1.5,1.7]
neighbourhood=[(0,1),(1,2),(1,2,1)]
amounts=[1,2,3,4,5,6]
growth=comp_model_AC(params,neighbourhood)
res=growth(amounts,[])
print(res)

odes=comp_model_AC(params,neighbourhood,True)
for ode in odes:
    print(ode)

# When "amounts" is not a numpy array this fails:
# np.maximum(0, amounts, out=amounts)
# Whereas this typecasts correctly:
# amounts=np.maximum(0,amounts)





