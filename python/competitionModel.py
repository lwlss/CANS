from CANS_functions import *
import pandas as pd
import scipy.optimize as opt

# Timepoints at which we would like to simulate cell densities (& remaining nutrients)
t=np.linspace(0,4.5,100)

nrow,ncol=16,24

# Initial conditions
C0=0.001
N0=0.23

# Parameter value
r=[3 for x in range(0,nrow*ncol)]
k=0.05

# Initial conditions
C=[C0 for x in range(0,nrow*ncol)]
N=[N0 for x in range(0,nrow*ncol)]

# Define function specifying what ODE is
# y is a list of variables (only one variable in this case: C)
# t is a list of times at which we will calculate variables
f=makeModelComp(nrow,ncol,r,k)
soln=odeint(f,C+N,t)

# Read in some real data
data=pd.read_csv("..\data\p15\ColonyzerOutput.txt",sep="\t")
data=data[(data.Column<=ncol)&(data.Row<=nrow)]
data["ID"]=['R{r:02d}C{c:02d}'.format(r=row,c=col) for row,col in zip(data.Row,data.Column)]
dmat=data.pivot("ExptTime","ID","Intensity")
# Simulate from model at times corresponding to expt. obs. only
et=data.ExptTime.unique()
et.sort()
esoln=odeint(f,C+N,et)[:,0:(nrow*ncol)]

def calcErr(C,N,r,k,dmat):
    '''Given set of model parameters & data, calulates the squared error between model prediction and observed data.'''
    f=makeModelComp(nrow,ncol,r,k)
    esoln=odeint(f,C+N,et)[:,0:(nrow*ncol)]
    return(np.sqrt(np.square(esoln-dmat).sum().sum()))

def makeLeastSquares(dmat):
    '''Set up an objective function with a vector of arguments for least squares optimisation of CANS model, given data dmat'''
    nrow=len(set([x[0:3] for x in dmat.columns]))
    ncol=len(set([x[4:] for x in dmat.columns]))
    def ObjFun(x):
      Cvals=[x[0] for i in range(nrow*ncol)]
      Nvals=[x[1] for i in range(nrow*ncol)]
      rvals=x[2:(2+nrow*ncol)]
      k=x[2+nrow*ncol]
      return(calcErr(Cvals,Nvals,rvals,k,dmat))
    return(ObjFun)

Obj=makeLeastSquares(dmat)
print(Obj([C[0]]+[N[0]]+r+[k]))

startTime = int(round(time.time()))

res=opt.minimize(
    Obj,
    x0=[C[0]]+[N[0]]+r+[k],
    args=(),
    method='BFGS',
    jac=None,
    tol=None,
    callback=None,
    options={'disp': False, 'gtol': 1e-02, 'eps': 0.0001, 'return_all': False, 'maxiter': 1000, 'norm': np.inf}
)

endTime = int(round(time.time()))

print(endTime-startTime)

print(res.nit)

C=[res.x[0] for i in range(nrow*ncol)]
N=[res.x[1] for i in range(nrow*ncol)]
r=res.x[2:(2+nrow*ncol)]
k=res.x[2+nrow*ncol]
f=makeModelComp(nrow,ncol,r,k)
soln=odeint(f,C+N,t)

# Plotting results
fig,ax=plt.subplots(nrow,ncol,figsize=(20,10))
setot=0
for row in range(nrow):
    for col in range(ncol):
        dat=data[(data.Column==(col+1))&(data.Row==(row+1))]
        i=convertij((row+1,col+1),ncol)
        se=sum([(x-y)**2 for x,y in zip(dat.Intensity,soln[:,i])])
        setot+=se
        ax[row,col].scatter(dat.ExptTime,dat.Intensity,c="red")
        #ax[row,col].scatter(dat.ExptTime,esoln[:,i],c="blue")
        ax[row,col].plot(t,soln[:,i],c="black")
        ax[row,col].plot(t,soln[:,i+(nrow*ncol)],c="blue")
        ax[row,col].set_ylim([-0.02,0.3])
        ax[row,col].text(2.6, 0.275, 'R{r:02d}C{c:02d}'.format(r=row+1,c=col+1))
        ax[row,col].text(2.6, 0.255, 'SqErr: %.3f'%se)

