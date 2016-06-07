"""Convert model to SBML. Addapted from: http://sbml.org/Software/libSBML/5.13.0/docs//python-api/libsbml-python-creating-model.html"""
import sys
from libsbml import *

import numpy as np
from cans2.plate import Plate
from cans2.model import CompModel


def check(value, message):
   """If 'value' is None, prints an error message constructed using
   'message' and then exits with status code 1.  If 'value' is an integer,
   it assumes it is a libSBML return status code.  If the code value is
   LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
   prints an error message constructed using 'message' along with text from
   libSBML explaining the meaning of the code, and exits with status code 1.

   http://sbml.org/Software/libSBML/5.13.0/docs/
   /python-api/libsbml-python-creating-model.html
   """
   if value == None:
     raise SystemExit('LibSBML returned a null value trying to '
                      + message + '.')
   elif type(value) is int:
     if value == LIBSBML_OPERATION_SUCCESS:
       return
     else:
       err_msg = 'Error encountered trying to ' + message + '.' \
                 + 'LibSBML returned error code ' + str(value) + ': "' \
                 + OperationReturnValue_toString(value).strip() + '"'
       raise SystemExit(err_msg)
   else:
     return

# Simulate a plate with data and parameters.
plate1 = Plate(2, 2)
plate1.times = np.linspace(0, 5, 11)
params = {
    "C_0": 1e-6,
    "N_0": 0.1,
    "kn": 1.5
}
plate1.set_sim_data(CompModel(), r_mean=40.0, r_var=15.0, custom_params=params)

# writeSBMLToFile(d, filename)


def create_model():
    """Return an SBML model given a plate and model.

    http://sbml.org/Software/libSBML/5.13.0/docs/
    /python-api/libsbml-python-creating-model.html

    """
    try:
        document = SBMLDocument(3, 1)
    except ValueError:
        raise SystemExit("Could not create SBMLDocument object")


    # Create a time unit of day.
    day = model.createUnitDefinition()
    check(day, "create unit definition")
    check(day.setId("day"), "set unit difinition id")
    unit = day.createUnit()
    check(unit, "create unit on day")
    # Requires all four of these.
    check(unit.setKind(UNIT_KIND_SECOND), "set unit kind")
    check(unit.setExponent(1), "Set unit exponent")
    check(unit.setScale(0), "set unit scale")
    check(unit.setMultiplier(86400), "set unit multiplier")


    model = document.createModel()
    check(model, "create model")
    check(model.setTimeUnits("day"), "set model-wide time units")
    # Should these two be dimensionless?
    check(model.setExtentUnits("dimensionless"), "set model units of extent")
    check(model.setSubstanceUnits("dimensionless"), "set model substance units")
    # check(model.setExtentUnits("mole"), "set model units of extent")
    # check(model.setSubstanceUnits("mole"), "set model substance units")


    # Not sure whether to use one compartment or a compartment for
    # each culture. Attempting to use dimensionless unit sizes and one
    # compartment. Not sure how all of this affects ODEs yet.
    c1 = model.createCompartment()
    check(c1, "create compartment")
    check(c1.setId("c1"), "set compartment id")
    # 'constant' refers to size
    check(c1.setConstant(True), "set compartment 'constant'")
    check(c1.setSize(1), "set compartment 'size'")
    check(c1.setSpatialDimensions(3), "set compartment dimensions")
    check(c1.setUnits("dimensionless"), "set compartment dimensions")


    def create_species():
        # for i in len(plate.no_cultures):
        # for species in comp_model.species:
        s = model.createSpecies()
        # s.setId('
