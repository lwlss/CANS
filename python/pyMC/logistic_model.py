import random
import time
import datetime
import pymc as mc
import numpy as np
import pandas as pd
from scipy.integrate import odeint
from diagnostics import *

def logistic(x0,r,K,t):
    '''Vectorised logistic model'''
    return(K*x0*np.exp(r*t)/(K+x0*(np.exp(r*t)-1)))

# Solution of dx/dt = r*x*(1-(x/K)^v)
def glogistic(x0,r,K,t,v=1.0):
    '''Vectorised generalised logistic growth model'''
    return(K/(1+(-1+(K/x0)**v)*np.exp(-r*v*t))**(1/v))

def logisticode(x0,r,K,t):
    '''Set of ODEs equivalent to logistic model. Population consumes nutrients, self-limiting when nutrients exhausted.'''
    rc = r/K
    # Define function specifying ODE
    # y: list of species values (C first, then N)
    # t: list of times at which we will calculate variables
    def f(y,t):
        C,N=y
        dC=rc*C*N
        dN=-rc*C*N
        return([dC,dN])
    iconds=[x0,K-x0]
    res=odeint(f,iconds,t)
    # Return C results only, to match logistic output
    return(res[:,0])

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

def inference(sim,par,iter=250000,burn=1000,thin=100,fixInoc=False,inocVal=0.0,genLog=False,logfun=logistic):
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
            return(logfun(inocVal,r,K,sim.t_exp))

        @mc.deterministic(plot=False)
        def logisticpred(r=r,K=K):
            return(logfun(inocVal,r,K,sim.t_pred))
    else:
        @mc.deterministic(plot=False)
        def logisticobs(x0=x0,r=r,K=K):
            return(logfun(x0,r,K,sim.t_exp))

        @mc.deterministic(plot=False)
        def logisticpred(x0=x0,r=r,K=K):
            return(logfun(x0,r,K,sim.t_pred))

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

def sinceStart(start):
    '''Returns a string reporting nicely formatted time since start (s)'''
    raws=time.time()-start
    m,s=divmod(raws,60)
    h,m=divmod(m,60)
    d,h=divmod(h,24)
    w,d=divmod(d,7)

    labs=["week","day","hour","min","sec"]
    vals=[w,d,h,m,s]
    string=""
    for (i,val) in enumerate(vals):
        if(val>0): string+="{} {} ".format(int(round(val)),labs[i]+"s")
    return(string.rstrip())

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

# Read in some read Colonyzer data for inference
class realData():
    def getSpot(self,row,col):
        self.filt=self.raw[(self.raw.Row==row)&(self.raw.Column==col)]
        self.t_exp=self.filt.ExptTime.values
        self.x_obs=self.filt.Intensity.values
    def __init__(self,row=1,col=1,fname="../../data/RawData.txt",n_pred=5):
        self.raw=pd.read_csv(fname,sep="\t")
        self.getSpot(row,col)
        self.t_pred=np.linspace(0,max(self.t_exp),n_pred)

if __name__ == "__main__":      
    data=sim(n_pred=50)
    print(logistic(data.x0_true,data.r_true,data.K_true,data.t_pred))
    print(logisticode(data.x0_true,data.r_true,data.K_true,data.t_pred))
