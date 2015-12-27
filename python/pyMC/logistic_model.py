from pymc import *
import numpy as np

def logistic(x0,r,K,t):
    '''Vectorised logistic model'''
    return(K*x0*np.exp(r*t)/(K+x0*(np.exp(r*t)-1)))

# Simulate some observation times and experimental data, with measurement error
K_true=0.6
r_true=2.5
x0_true=0.001
tau_true=500.0
t_exp=np.linspace(0,5,10)
t_pred=np.linspace(0,max(t_exp),100)
x_exp=logistic(x0_true,r_true,K_true,t_exp)
x_obs=np.random.normal(x_exp,sqrt(1.0/tau_true))

# Stochastic modes in the model (prior specifications)
r_min,r_max=0.0,10.0
r=Uniform('r',r_min,r_max)
K_min,K_max=0.0,1.0
K=Uniform('K',K_min,K_max)
#x0_min,x0_max=0.0,0.1
#x0=Uniform('x0',x0_min,x0_max)
tau_min,tau_max=0,5000
tau=Uniform('tau',tau_min,tau_max)

# Deterministic nodes in the model (output from logistic model in this case)
##@deterministic(plot=False)
##def logisticobs(x0=x0,r=r,K=K):
##    return(logistic(x0,r,K,t_exp))
##
##@deterministic(plot=False)
##def logisticpred(x0=x0,r=r,K=K):
##    return(logistic(x0,r,K,t_pred))

@deterministic(plot=False)
def logisticobsfix(r=r,K=K):
    return(logistic(x0_true,r,K,t_exp))

@deterministic(plot=False)
def logisticpredfix(r=r,K=K):
    return(logistic(x0_true,r,K,t_pred))

pred=Normal('pred',mu=logisticpredfix,tau=tau)
obs=Normal('obs',mu=logisticobsfix,tau=tau,value=x_obs,observed=True)
