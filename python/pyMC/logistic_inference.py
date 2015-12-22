import logistic_model
from pymc import MCMC
M = MCMC(logistic_model)
M.sample(iter=100000, burn=5000, thin=1000)

from pylab import hist, show
hist(M.trace('x0')[:])
show()
