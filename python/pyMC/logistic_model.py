import random
import time
import datetime
import pymc as mc
import numpy as np
import pandas as pd
from scipy.integrate import odeint
from diagnostics import *
import os
from pymc.Matplot import plot

def mdr(x0,r,K,v):
    '''Vectorised Maximum Doubling Rate for generalised logistic model.
Recover value for logistic model by setting v=1.'''
    return(np.divide((r*v),np.log(1.0-(np.power(2.0,v)-1.0)/(np.power(2.0,v)*np.power(np.divide(x0,K),v)-1.0))))

def mdp(x0,K):
    '''Vectorised Maximum Doubling Potential for generalised logistic and logistic models.'''
    return(np.log(np.divide(K,x0))/np.log(2.0))    

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
    if genLog:
        v=mc.Uniform('v',par.v_min,par.v_max)
    r=mc.Uniform('r',par.r_min,par.r_max)
    K=mc.Uniform('K',par.K_min,par.K_max)
    tau=mc.Uniform('tau',par.tau_min,par.tau_max)

    print("Building model...")
    # Deterministic nodes in the model (output from logistic model in this case)
    if fixInoc and not genLog:
        @mc.deterministic(plot=False)
        def logisticobs(r=r,K=K):
            return(logfun(inocVal,r,K,sim.t_exp))

        @mc.deterministic(plot=False)
        def logisticpred(r=r,K=K):
            return(logfun(inocVal,r,K,sim.t_pred))
    if not fixInoc and not genLog:
        @mc.deterministic(plot=False)
        def logisticobs(x0=x0,r=r,K=K):
            return(logfun(x0,r,K,sim.t_exp))

        @mc.deterministic(plot=False)
        def logisticpred(x0=x0,r=r,K=K):
            return(logfun(x0,r,K,sim.t_pred))
    if fixInoc and genLog:
        @mc.deterministic(plot=False)
        def logisticobs(r=r,K=K,v=v):
            return(glogistic(inocVal,r,K,sim.t_exp,v))

        @mc.deterministic(plot=False)
        def logisticpred(r=r,K=K,v=v):
            return(glogistic(inocVal,r,K,sim.t_pred,v))
    if not fixInoc and genLog:
        @mc.deterministic(plot=False)
        def logisticobs(x0=x0,r=r,K=K,v=v):
            return(glogistic(inocVal,r,K,sim.t_exp,v))

        @mc.deterministic(plot=False)
        def logisticpred(x0=x0,r=r,K=K,v=v):
            return(glogistic(inocVal,r,K,sim.t_pred,v))
    # Posterior predictive and measurement error models
    pred=mc.Normal('pred',mu=logisticpred,tau=tau)
    obs=mc.Normal('obs',mu=logisticobs,tau=tau,value=sim.x_obs,observed=True)

    print("Sampling from posterior...")
    if fixInoc and not genLog:
        M=mc.MCMC(dict({"r":r,"K":K,"tau":tau,"pred":pred,"obs":obs}))
    if not fixInoc and not genLog:
        M=mc.MCMC(dict({"x0":x0,"r":r,"K":K,"tau":tau,"pred":pred,"obs":obs}))
    if fixInoc and genLog:
        M=mc.MCMC(dict({"r":r,"K":K,"v":v,"tau":tau,"pred":pred,"obs":obs}))
    if not fixInoc and genLog:
        M=mc.MCMC(dict({"x0":x0,"r":r,"K":K,"v":v,"tau":tau,"pred":pred,"obs":obs}))
    M.sample(iter=iter, burn=burn, thin=thin,progress_bar=False)
    return(M)

def hierarchy_inf(data,par,iter=250000,burn=1000,thin=100):
    '''Learn about r and K in full hierarchy, learn about x0 separately for each column.'''
    priors={}
    x0=mc.Uniform('x0',par.x0_min,par.x0_max)
    tau=mc.Uniform('tau',par.tau_min,par.tau_max)

    priors["x0"]=x0
    priors["tau"]=tau
  
    r=mc.Uniform('r',par.r_min,par.r_max)
    r_delta=mc.Uniform('r_delta',0,(par.r_max-par.r_min)/2)
    
    K=mc.Uniform('K',par.K_min,par.K_max)
    K_delta=mc.Uniform('K_delta',0,(par.K_max-par.K_min)/2)
    
    priors["r"]=r
    priors["r_delta"]=r_delta
    priors["K"]=K
    priors["K_delta"]=K_delta

    grps=data.groupby("Gene")
    for grp in grps:
        grplab,reps=grp

        r_gen=mc.Uniform("r_{}".format(grplab),r-r_delta,r+r_delta)
        r_gen_delta=mc.Uniform("r_delta_{}".format(grplab),0,r_delta)
        K_gen=mc.Uniform("K_{}".format(grplab),K-K_delta,K+K_delta)
        K_gen_delta=mc.Uniform("K_delta_{}".format(grplab),0,K_delta)

        priors["r_{}".format(grplab)]=r_gen
        priors["r_delta_{}".format(grplab)]=r_gen_delta
        priors["K_{}".format(grplab)]=K_gen
        priors["K_delta_{}".format(grplab)]=K_gen_delta
        
        reps=reps.groupby("ID")
        for rep in reps:
            replab,repdf=rep
            r_rep=mc.Uniform("r_{0}_{1}".format(grplab,replab),r_gen-r_gen_delta,r_gen+r_gen_delta)
            K_rep=mc.Uniform("K_{0}_{1}".format(grplab,replab),K_gen-K_gen_delta,K_gen+K_gen_delta)
            @mc.deterministic(plot=False)
            def logisticobs(x0=x0,r=r_rep,K=K_rep):
                return(logistic(x0,r,K,repdf.ExptTime))
            obs=mc.Normal('obs_{0}_{1}'.format(grplab,replab),mu=logisticobs,tau=tau,value=repdf.Intensity,observed=True)
            priors["r_{0}_{1}".format(grplab,replab)]=r_rep
            priors["K_{0}_{1}".format(grplab,replab)]=K_rep
            priors['obs_{0}_{1}'.format(grplab,replab)]=obs
    M=mc.MCMC(priors)
    M.sample(iter=iter, burn=burn, thin=thin,progress_bar=False)
    return(M)

def hierarchy_inf_x0(data,par,iter=250000,burn=1000,thin=100):
    '''Learn about x0,r,K in full hierarchy'''
    priors={}
    tau=mc.Uniform('tau',par.tau_min,par.tau_max)
    priors["tau"]=tau

    x0=mc.Uniform('x0',par.x0_min,par.x0_max)
    x0_delta=mc.Uniform('x0_delta',0,(par.x0_max-par.x0_min)/2)
  
    r=mc.Uniform('r',par.r_min,par.r_max)
    r_delta=mc.Uniform('r_delta',0,(par.r_max-par.r_min)/2)
    
    K=mc.Uniform('K',par.K_min,par.K_max)
    K_delta=mc.Uniform('K_delta',0,(par.K_max-par.K_min)/2)

    priors["x0"]=x0
    priors["x0_delta"]=x0_delta
    priors["r"]=r
    priors["r_delta"]=r_delta
    priors["K"]=K
    priors["K_delta"]=K_delta

    grps=data.groupby("Gene")
    for grp in grps:
        grplab,reps=grp

        x0_gen=mc.Uniform("x0_{}".format(grplab),x0-x0_delta,x0+x0_delta)
        x0_gen_delta=mc.Uniform("x0_delta_{}".format(grplab),0,x0_delta)
        r_gen=mc.Uniform("r_{}".format(grplab),r-r_delta,r+r_delta)
        r_gen_delta=mc.Uniform("r_delta_{}".format(grplab),0,r_delta)
        K_gen=mc.Uniform("K_{}".format(grplab),K-K_delta,K+K_delta)
        K_gen_delta=mc.Uniform("K_delta_{}".format(grplab),0,K_delta)

        priors["x0_{}".format(grplab)]=x0_gen
        priors["x0_delta_{}".format(grplab)]=x0_gen_delta
        priors["r_{}".format(grplab)]=r_gen
        priors["r_delta_{}".format(grplab)]=r_gen_delta
        priors["K_{}".format(grplab)]=K_gen
        priors["K_delta_{}".format(grplab)]=K_gen_delta
        
        reps=reps.groupby("ID")
        for rep in reps:
            replab,repdf=rep
            x0_rep=mc.Uniform("x0_{0}_{1}".format(grplab,replab),x0_gen-x0_gen_delta,x0_gen+x0_gen_delta)
            r_rep=mc.Uniform("r_{0}_{1}".format(grplab,replab),r_gen-r_gen_delta,r_gen+r_gen_delta)
            K_rep=mc.Uniform("K_{0}_{1}".format(grplab,replab),K_gen-K_gen_delta,K_gen+K_gen_delta)
            @mc.deterministic(plot=False)
            def logisticobs(x0=x0_rep,r=r_rep,K=K_rep):
                return(logistic(x0,r,K,repdf.ExptTime))
            obs=mc.Normal('obs_{0}_{1}'.format(grplab,replab),mu=logisticobs,tau=tau,value=repdf.Intensity,observed=True)
            priors["x0_{0}_{1}".format(grplab,replab)]=x0_rep
            priors["r_{0}_{1}".format(grplab,replab)]=r_rep
            priors["K_{0}_{1}".format(grplab,replab)]=K_rep
            priors['obs_{0}_{1}'.format(grplab,replab)]=obs
    M=mc.MCMC(priors)
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

# Read in some real Colonyzer data for inference
class realData():
    def getSpot(self,row,col):
        self.filt=self.raw[(self.raw.Row==row)&(self.raw.Column==col)]
        self.t_exp=self.filt.ExptTime.values
        self.x_obs=self.filt.Intensity.values
    def __init__(self,row=1,col=1,fname="../../data/p15/RawData.txt",n_pred=5):
        self.raw=pd.read_csv(fname,sep="\t")
        self.getSpot(row,col)
        self.t_pred=np.linspace(0,max(self.t_exp),n_pred)

class par:
    '''Prior parameters (ranges for uniform distributions)'''
    r_min,r_max=0.0,10.0
    K_min,K_max=0.0,1.0
    x0_min,x0_max=0.0,0.1
    tau_min,tau_max=0,1500000
    v_min,v_max=0.1,10.0

def make_sure_path_exists(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
def P15():
    #data=sim(n_pred=50)
    #print(logistic(data.x0_true,data.r_true,data.K_true,data.t_pred))
    #print(logisticode(data.x0_true,data.r_true,data.K_true,data.t_pred))
    #data=[sim(n_pred=10) for x in range(1,4)]
    fname="../../data/p15/RawData.txt"
    raw=pd.read_csv(fname,sep="\t")
    raw=raw[~(raw.Row.isin([1,16]) & raw.Column.isin([1,24]))]
    #raw=raw[raw.Gene.isin(["MRE11","EXO1"])]
    dirname="AllStrains"
    make_sure_path_exists(dirname)
    print(fname)
    M=hierarchy_inf(raw,par,iter=101000,burn=1000,thin=1000)
    plot(M,path=dirname)

##if __name__ == "__main__":
##    colnum=1
##    print("Column {}".format(colnum))
##    fname="../../data/dilution/RawData.txt"
##    raw=pd.read_csv(fname,sep="\t")
##    raw=raw[raw.Column==colnum]
##    root="Dilutions"
##    make_sure_path_exists(root)
##    dirname=os.path.join(root,"C{0:02d}".format(colnum))
##    make_sure_path_exists(dirname)
##    M=hierarchy_inf_x0(raw,par,iter=7500,burn=500,thin=10)
##    plot(M,path=dirname)
##    df=pd.DataFrame()
##    genes=np.sort(raw.Gene.unique())
##    for gene in genes:
##        df["x0_{0}_C{1:02d}".format(gene,colnum)]=getattr(M,"r_"+gene).trace[:]
##        df["r_{0}_C{1:02d}".format(gene,colnum)]=getattr(M,"r_"+gene).trace[:]
##        df["K_{0}_C{1:02d}".format(gene,colnum)]=getattr(M,"K_"+gene).trace[:]
##    df["x0_C{0:02d}".format(colnum)]=getattr(M,"x0").trace[:]
##    df.to_csv(os.path.join(root,"C{0:02d}.txt".format(colnum)),sep="\t",index=False)
##    frac_r=float(np.sum(df["r_{0}_C{1:02d}".format(genes[0],colnum)]>df["r_{0}_C{1:02d}".format(genes[1],colnum)]))/len(df["r_{0}_C{1:02d}".format(genes[0],colnum)])
##    print("Probability that "+genes[0]+" is fitter than "+genes[1]+" in terms of r: "+str(frac_r))
##    frac_K=float(np.sum(df["K_{0}_C{1:02d}".format(genes[0],colnum)]>df["K_{0}_C{1:02d}".format(genes[1],colnum)]))/len(df["K_{0}_C{1:02d}".format(genes[0],colnum)])
##    print("Probability that "+genes[0]+" is fitter than "+genes[1]+" in terms of K: "+str(frac_K))  
    
    
    
    

