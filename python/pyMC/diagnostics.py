import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 12})
from scipy.stats import gaussian_kde
import numpy as np
import pymc as mc
import pandas as pd
from pandas.tools.plotting import scatter_matrix as scatmat
#import seaborn as sb

def summarisePred(p,conf=0.95):
    lowerperc=100.0*(1.0-conf)/2.0
    upperperc=100.0-lowerperc
    res={}
    res['low']=[np.percentile(p.trace[:,i],lowerperc) for i in range(p.shape[0])]
    res['med']=[np.percentile(p.trace[:,i],50.0) for i in range(p.shape[0])]
    res['up']=[np.percentile(p.trace[:,i],upperperc) for i in range(p.shape[0])]
    return(res)

def predictPlots(M,splitPlots=False):
    mc.Matplot.plot(M.pred,format="pdf")
    if splitPlots:
        for i in range(0,M.pred.shape[0]):
            Matplot.plot(M.pred.trace[:,i],"pred_%01d"%i,format="pdf")

def comparePosteriors(M1,M2,sim,main="",lab1="",lab2="",lwd=2,show=False,simulated=True):
    fig,ax=plt.subplots(1,2,figsize=(21,14))
    pd.Series(M1.r.trace[:]).plot(kind="kde",ax=ax[0],color="blue",label=lab1,lw=lwd)
    pd.Series(M2.r.trace[:]).plot(kind="kde",ax=ax[0],color="red",label=lab2,lw=lwd)
    ax[0].set_xlabel('r')
    if simulated: ax[0].axvline(sim.r_true,linestyle="dashed",color="black",label="True value",lw=lwd)
    pd.Series(M1.K.trace[:]).plot(kind="kde",ax=ax[1],color="blue",label=lab1,lw=lwd)
    pd.Series(M2.K.trace[:]).plot(kind="kde",ax=ax[1],color="red",label=lab2,lw=lwd)
    ax[1].set_xlabel('K')
    if simulated: ax[1].axvline(sim.K_true,linestyle="dashed",color="black",label="True value",lw=lwd)
    ax[1].legend()
    plt.suptitle(main)
    if show:
        plt.show()

def comparePosteriors2(Mlist,labs,clist,main="",lwd=2,show=False,inocVal=0.001):
    fig,ax=plt.subplots(2,2,figsize=(21,21))
    for M in Mlist:
        nodenames=[x.__name__ for x in M._variables_to_tally]
        nodenames=[n for n in nodenames if n not in ["pred","tau"]]
        if "v" not in nodenames:
            M.v_vals=1.0
        else:
            M.v_vals=M.v.trace[:]
        if "x0" not in nodenames:
            M.x0_vals=inocVal
        else:
            M.x0_vals=M.x0.trace[:]
        M.mdr=mdr(M.K.trace[:],M.r.trace[:],M.x0_vals,M.v_vals)
        M.mdp=mdp(M.K.trace[:],M.r.trace[:],M.x0_vals,M.v_vals)
        M.mdrmdp=M.mdr*M.mdp        
    
    for i,M in enumerate(Mlist):
        scol=clist[i]
        pd.Series(M.r.trace[:]).plot(kind="kde",ax=ax[0,0],color=scol,label=labs[i],lw=lwd)
        pd.Series(M.K.trace[:]).plot(kind="kde",ax=ax[0,1],color=scol,label=labs[i],lw=lwd)
        pd.Series(M.mdr[:]).plot(kind="kde",ax=ax[1,0],color=scol,label=labs[i],lw=lwd,xlim=[0,20])
        pd.Series(M.mdrmdp[:]).plot(kind="kde",ax=ax[1,1],color=scol,label=labs[i],lw=lwd,xlim=[0,50])

    ax[0,0].set_xlabel('r')
    ax[0,1].set_xlabel('K')
    ax[1,0].set_xlabel('MDR')
    ax[1,1].set_xlabel('MDRMDP')
    ax[1,1].legend()
    plt.suptitle(main)
    if show:
        plt.show()

def posteriorPriorPlots(M,sim,par,bnum=50,show=True,main="",lwd=2,simulated=True):
    nodenames=[x.__name__ for x in M._variables_to_tally]
    pred=summarisePred(M.pred)
    fig,ax=plt.subplots(2,3,figsize=(21,14))

    ax[0,0].scatter(sim.t_exp,sim.x_obs,color="blue")
    if simulated: ax[0,1].scatter(sim.t_exp,sim.x_exp,color="red")
    ax[0,0].plot(sim.t_pred,pred["med"],color="blue",lw=lwd)
    ax[0,0].plot(sim.t_pred,pred["low"],color="blue",linestyle="dashed",lw=lwd)
    ax[0,0].plot(sim.t_pred,pred["up"],color="blue",linestyle="dashed",lw=lwd)
    ax[0,0].set_xlabel('Time since inoculation (d)')
    ax[0,0].set_ylabel('Population size (AU)')
    ax[0,0].set_ylim([min(pred["low"]),max(pred["up"])])

    if 'x0' in nodenames: 
        x0_pdf=gaussian_kde(M.trace('x0')[:])
        x0_min,x0_max=np.percentile(M.trace('x0')[:],[0,100])
        x0_range=np.linspace(par.x0_min,par.x0_max,500)
        x0_dens=x0_pdf(x0_range)
        ax[0,1].hist(M.trace('x0')[:],bins=np.linspace(par.x0_min,par.x0_max,bnum),normed=True,color="skyblue")
        ax[0,1].plot(x0_range,x0_dens,'r',color="blue",lw=lwd)
        if simulated: ax[0,1].axvline(sim.x0_true,linestyle="dashed",color="black",lw=lwd)
        ax[0,1].set_xlabel('x0 (AU)')
        ax[0,1].set_ylabel('Density')
        yval=1.0/(par.x0_max-par.x0_min)
        ax[0,1].vlines([par.x0_min,par.x0_max],0,yval,color="red",lw=lwd)
        ax[0,1].hlines(yval,par.x0_min,par.x0_max,color="red",lw=lwd)

    if 'v' in nodenames: 
        v_pdf=gaussian_kde(M.trace('v')[:])
        v_min,v_max=np.percentile(M.trace('v')[:],[0,100])
        v_range=np.linspace(par.v_min,par.v_max,500)
        v_dens=v_pdf(v_range)
        ax[0,2].hist(M.trace('v')[:],bins=np.linspace(par.v_min,par.v_max,bnum),normed=True,color="skyblue")
        ax[0,2].plot(v_range,v_dens,'r',color="blue",lw=lwd)
        if simulated: ax[0,2].axvline(sim.v_true,linestyle="dashed",color="black",lw=lwd)
        ax[0,2].set_xlabel('v')
        ax[0,2].set_ylabel('Density')
        yval=1.0/(par.v_max-par.v_min)
        ax[0,2].vlines([par.v_min,par.v_max],0,yval,color="red",lw=lwd)
        ax[0,2].hlines(yval,par.v_min,par.v_max,color="red",lw=lwd)

    r_pdf=gaussian_kde(M.trace('r')[:])
    r_min,r_max=np.percentile(M.trace('r')[:],[0,100])
    r_range=np.linspace(par.r_min,par.r_max,500)
    r_dens=r_pdf(r_range)    
    ax[1,0].hist(M.trace('r')[:],bins=np.linspace(par.r_min,par.r_max,bnum),normed=True,color="skyblue")
    ax[1,0].plot(r_range,r_dens,'r',color="blue",lw=lwd)
    ax[1,0].set_xlabel('r (1/d)')
    ax[1,0].set_ylabel('Density')
    yval=1.0/(par.r_max-par.r_min)
    ax[1,0].vlines([par.r_min,par.r_max],0,yval,color="red",lw=lwd)
    ax[1,0].hlines(yval,par.r_min,par.r_max,color="red",lw=lwd)
    if simulated: ax[1,0].axvline(sim.r_true,linestyle="dashed",color="black",lw=lwd)

    K_pdf=gaussian_kde(M.trace('K')[:])
    K_min,K_max=np.percentile(M.trace('K')[:],[0,100])
    K_range=np.linspace(par.K_min,par.K_max,500)
    K_dens=K_pdf(K_range)    
    ax[1,1].hist(M.trace('K')[:],bins=np.linspace(par.K_min,par.K_max,bnum),normed=True,color="skyblue")
    ax[1,1].plot(K_range,K_dens,'r',color="blue",lw=lwd)
    ax[1,1].set_xlabel('K (AU)')
    ax[1,1].set_ylabel('Density')
    yval=1.0/(par.K_max-par.K_min)
    ax[1,1].vlines([par.K_min,par.K_max],0,yval,color="red",lw=lwd)
    ax[1,1].hlines(yval,par.K_min,par.K_max,color="red",lw=lwd)
    if simulated: ax[1,1].axvline(sim.K_true,linestyle="dashed",color="black",lw=lwd)
    
    tau_pdf=gaussian_kde(M.trace('tau')[:])
    tau_min,tau_max=np.percentile(M.trace('tau')[:],[0,100])
    tau_range=np.linspace(par.tau_min,par.tau_max,500)
    tau_dens=tau_pdf(tau_range)
    ax[1,2].hist(M.trace('tau')[:],bins=np.linspace(par.tau_min,par.tau_max,bnum),normed=True,color="skyblue")
    ax[1,2].plot(tau_range,tau_dens,'r',color="blue",lw=lwd)
    ax[1,2].set_xlabel('tau')
    ax[1,2].set_ylabel('Density')
    yval=1.0/(par.tau_max-par.tau_min)
    ax[1,2].vlines([par.tau_min,par.tau_max],0,yval,color="red",lw=lwd)
    ax[1,2].hlines(yval,par.tau_min,par.tau_max,color="red",lw=lwd)
    if simulated: ax[1,2].axvline(sim.tau_true,linestyle="dashed",color="black",lw=lwd)
    plt.suptitle(main)
    if show:
        plt.show()

def plotCorrs(M,main="",maxsamp=3000,show=True):
    '''Plot scatterplot matrix showing correlation between posterior samples for each variable'''
    mxsmp=min(maxsamp,M.r.trace.length())
    nodenames=[x.__name__ for x in M._variables_to_tally]
    nodenames=[n for n in nodenames if n not in ["pred","tau"]]
    
    M_df=pd.DataFrame()
    for n in nodenames:
        M_df[n]=getattr(M,n).trace[0:mxsmp]
    scat=scatmat(M_df,diagonal="kde")
    plt.suptitle(main)
    if show:
        plt.show()
