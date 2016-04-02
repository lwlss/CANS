from CANS_functions import *
import pandas as pd

# Timepoints at which we would like to simulate cell densities (& remaining nutrients)
t=np.linspace(0,4.5,100)

nrow,ncol=5,5

# Initial conditions
C0=0.001
N0=0.23

# Parameter value
r=[3 for x in range(0,nrow*ncol)]
r[5]=5
r[8]=5
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
        ax[row,col].scatter(dat.ExptTime,esoln[:,i],c="blue")
        ax[row,col].plot(t,soln[:,i],c="black")
        ax[row,col].plot(t,soln[:,i+(nrow*ncol)],c="blue")
        ax[row,col].set_ylim([-0.02,0.3])
        ax[row,col].text(3.6, 0.275, 'R{r:02d}C{c:02d}'.format(r=row+1,c=col+1))
        ax[row,col].text(3.6, 0.255, 'SqErr: %.3f'%se)

##with open(r"C:\Users\Vicky\Desktop\blanktextfile.txt", "w") as fp:
##     soln=odeint(f,C+N,t)
##     for row in range(nrow):
##         for col in range(ncol):
##             i=convertij((row,col),ncol)
##             g = soln[:,i]
##             print type(g)
##        print t,soln[:,i+(nrow*ncol)]
##             fp.write("%i\t%i\t%i") % (i, t, g) 
##     fp.write("%s\n%s\n" % p)
##fp.write(("%s\t%.15f\t%i\t%i\n") % (p[0], p[1][0], p[1][1], p[1][2]))

# Plotting results
fig,ax=plt.subplots(nrow,ncol,figsize=(20,10)) #nrow, ncol
for row in range(nrow):
    for col in range(ncol):
        i=convertij((row+1,col+1),ncol)
        ax[row,col].plot(t,soln[:,i],c="black")
        ax[row,col].plot(t,soln[:,i+(nrow*ncol)],c="blue")
        ax[row,col].set_xlabel('Time since inoculation (d)')
        ax[row,col].set_ylabel('Population size (AU)')
plt.show()

print(setot)

