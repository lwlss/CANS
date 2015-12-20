from pymc import *
import numpy as np

def logistic(x0,r,K,t):
    '''Vectorised logistic model'''
    return(K*x0*np.exp(r*t)/(K+x0*(np.exp(r*t)-1)))

# Simulate some observation times and experimental data, with measurement error
K_true=1.0
r_true=1.0
x0_true=0.001
tau_true=0.1
t_exp=np.linspace(0,15,100)
x_exp=logistic(x0_true,r_true,K_true,t_exp)
x_obs=np.random.normal(x_exp,sqrt(1/tau_true))

# Specify priors for model parameters (stochastic nodes)
r=Normal('r',1.5,1/2.0)
K=Normal('K',2,1/2.5)
x0=Normal('x0',0,1/0.1)
tau=Normal('tau',0,1/2.0)

# Deterministic nodes in the model (output from logistic model in this case)
@deterministic(plot=False)
def logisticmodel(x0=x0,r=r,K=K):
    return(logistic(x0,r,K,t_exp))

obs=Normal('obs',mu=logisticmodel,value=x_obs,observed=True)

# Need to add function closure so that t_exp can be a variable
