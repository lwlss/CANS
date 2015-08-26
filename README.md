# CANS
#### Competition-based model of growth of cell populations on solid agar surfaces

![Yeast growing on agar surface](http://farm6.staticflickr.com/5310/5658435523_c2e43729f1_b.jpg "Yeast on agar")

During Quantiatitive Fitness Analysis ([QFA](http://research.ncl.ac.uk/qfa/)) of microbial cultures, we analyse the way cultures grow on solid agar surfaces.  Basically, we inoculate cells onto an agar surface, and repeatedly photograph the agar plates as the populations grow, analysing images (using the [Colonyzer](http://research.ncl.ac.uk/colonyzer/) software) to estimate changes in cell density over time.  Usually we assume that cultures grow independently, and this is a good assumption during the early part of the growth phase.  However, later in the growth phase, it seems likely that competition between cultures will become important.  This model attempts to account for that competition.

CANS models are ODEs which we solve using the odeint function in Python.

On the way to developing a full-blown competition model, we developed some simpler versions, using the same tools:

##### Exponential model
C is number of cells
C0 is the initial condition (number of cells at t=0)
r is the rate parameter

Assuming [mass-action kinetics](https://en.wikipedia.org/wiki/Law_of_mass_action) and assuming that the number of cells is continuous, we model the cell dynamics as a simple first order reaction in a well-stirred vessel:

  C -> 2C
  rate = r*C

The reaction above can be written in ODE form:

  dC/dt = r * C
  C(0) = C0



##### Nutrient limited model

##### Compeition model

##### Competition model with signalling (full CANS model)


#### TODO:
* Add description of models to .md file
* Read in some actual QFA data
* Plot multiple growth curves on a single page (array plot)
* Fit models to data (parameter inference) 
* Compare inferred paramter values from competition model with values from regular QFA








