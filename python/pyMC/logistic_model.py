import pymc as mc
import numpy as np
import multiprocessing as mp
from scipy.integrate import odeint
import random
from diagnostics import *

def logistic(x0,r,K,t):
    '''Vectorised logistic model'''
    return(K*x0*np.exp(r*t)/(K+x0*(np.exp(r*t)-1)))

# Solution of dx/dt = r*x*(1-(x/K)^v)
def glogistic(x0,r,K,t,v=1.0):
    '''Vectorised generalised logistic growth model'''
    return(K/(1+(-1+(K/x0)**v)*np.exp(-r*v*t))**(1/v))

# Define function specifying what ODE is
# y is a list of variables (only one variable in this case: C)
# t is a list of times at which we will calculate variables
def logisticode(x0,r,K,t):
    rc = r/K
    def f(y,t):
        C,N=y
        dC=rc*C*N
        dN=-rc*C*N
        return([dC,dN])
    iconds=[x0,K-x0]
    return(odeint(f,iconds,t))

# To convert from N-C competition model to logistic model, think about matching rates at t=0
# Competition:
# dC/dt @t0 = rc*C0*N0
# Logistic
# dC/dt @t0 = rl*C0*(1-C0/K)
# In order for growth curves to be identical:
# rc*C0*N0 = rl*C0*(1-C0/K)
# -> rc = rl*(1-C0/K)/N0
# Also need same population size at steady-state:
# Logistic carrying capacity is initial pop size plus increase from nutrient consumption
# K=C0+N0
# -> N0=K-C0
# Therefore:
# rc = rl*(1-C0/K)/(K-C0)
# -> rc = rl/K

# Simulate some observation times and experimental data, with measurement error
class sim():
    rnd=np.random
    '''Parameters used for generating simulated data, together with simulated data'''
    def __init__(self,x0=0.001,r=2.5,K=0.6,tau=300.0,v=1.0,tmax=5,n_exp=10,n_pred=10):
        self.seed = random.randint(0,4294967295)
        self.K_true=K
        self.r_true=r
        self.x0_true=x0
        self.v_true=v
        self.tau_true=tau
        self.t_exp=np.linspace(0,tmax,n_exp)
        self.t_pred=np.linspace(0,tmax,n_pred)
        self.x_exp=glogistic(self.x0_true,self.r_true,self.K_true,self.t_exp,self.v_true)
        self.rnd.seed(self.seed)
        self.x_obs=self.rnd.normal(self.x_exp,np.sqrt(1.0/self.tau_true))

data=sim()
print(logistic(data.x0_true,data.r_true,data.K_true,data.t_pred))
print(logisticode(data.x0_true,data.r_true,data.K_true,data.t_pred))


# Stochastic nodes in the model (prior specifications)
class par:
    '''Prior parameters (ranges for uniform distributions)'''
    r_min,r_max=0.0,10.0
    K_min,K_max=0.0,1.0
    x0_min,x0_max=0.0,0.1
    tau_min,tau_max=0,5000

def inference(sim,par,iter=250000,burn=1000,thin=100,fixInoc=False,genLog=False):
    print("Building priors...")
    if not fixInoc:
        x0=mc.Uniform('x0',par.x0_min,par.x0_max)
    r=mc.Uniform('r',par.r_min,par.r_max)
    K=mc.Uniform('K',par.K_min,par.K_max)
    tau=mc.Uniform('tau',par.tau_min,par.tau_max)

    print("Building model...")
    # Deterministic nodes in the model (output from logistic model in this case)
    if fixInoc:
        @mc.deterministic(plot=False)
        def logisticobs(r=r,K=K):
            return(logistic(sim.x0_true,r,K,sim.t_exp))

        @mc.deterministic(plot=False)
        def logisticpred(r=r,K=K):
            return(logistic(sim.x0_true,r,K,sim.t_pred))
    else:
        @mc.deterministic(plot=False)
        def logisticobs(x0=x0,r=r,K=K):
            return(logistic(x0,r,K,sim.t_exp))

        @mc.deterministic(plot=False)
        def logisticpred(x0=x0,r=r,K=K):
            return(logistic(x0,r,K,sim.t_pred))

    # Posterior predictive and measurement error models
    pred=mc.Normal('pred',mu=logisticpred,tau=tau)
    obs=mc.Normal('obs',mu=logisticobs,tau=tau,value=sim.x_obs,observed=True)

    print("Sampling from posterior...")
    if fixInoc:
        M=mc.MCMC(dict({"r":r,"K":K,"tau":tau,"pred":pred,"obs":obs}))
    else:
        M=mc.MCMC(dict({"x0":x0,"r":r,"K":K,"tau":tau,"pred":pred,"obs":obs}))
    M.sample(iter=iter, burn=burn, thin=thin,progress_bar=False)
    return(M)

def makeRes(fixInoc):
    return(inference(data,par,2500,1000,100,fixInoc))

#p=mp.Pool(2)
#Mvals=p.map(makeRes,[False,True])

#M=inference(sim,par,iter=2500,burn=1000,thin=100,fixInoc=False)
#Mfix=inference(sim,par,iter=2500,burn=1000,thin=100,fixInoc=True)

# Diagnostic and posterior plots
#mc.Matplot.plot(M)
#mc.Matplot.plot(Mfix)

#predictPlots(M,splitPlots=False)
#predictPlots(Mfix,splitPlots=False)

#posteriorPriorPlots(M,sim,par,50)
#posteriorPriorPlots(Mfix,sim,par,50)
