"""Convert model to SBML. Addapted from: http://sbml.org/Software/libSBML/5.13.0/docs//python-api/libsbml-python-creating-model.html"""
import sys
from libsbml import *

import numpy as np
from cans2.plate import Plate
from cans2.model import CompModel


def check(value, message):
    """If 'value' is None, prints an error message constructed using
    'message' and then exits with status code 1.  If 'value' is an
    integer, it assumes it is a libSBML return status code.  If the
    code value is LIBSBML_OPERATION_SUCCESS, returns without further
    action; if it is not, prints an error message constructed using
    'message' along with text from libSBML explaining the meaning of
    the code, and exits with status code 1.

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

def create_model():
    """Return an SBML model given a plate and model.

    http://sbml.org/Software/libSBML/5.13.0/docs/
    /python-api/libsbml-python-creating-model.html

    """
    try:
        document = SBMLDocument(3, 1)
    except ValueError:
        raise SystemExit("Could not create SBMLDocument object")

    model = document.createModel()
    check(model, "create model")

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

    create_species(model, plate1, comp_model)
    print(list(model.getListOfSpecies()))


def create_species(model, plate, comp_model):
    for i, specie in enumerate(comp_model.species):
        for n in range(plate.no_cultures):
            create_specie(model, specie, n, plate.sim_params[i])


def create_specie(model, specie, culture_no, init_amount):
    s = model.createSpecies()
    check(s, "create species s")
    check(s.setId(specie + str(culture_no)),
          "set species {0}{1} id".format(specie, culture_no))
    check(s.setCompartment("c1"),
          "set species {0}{1} compartment".format(specie, culture_no))
    # If "constant" and "boundaryCondition" both false,
    # species can be both a product and a reactant.
    check(s.setConstant(False),
          "set constant attr on {0}{1}".format(specie, culture_no))
    check(s.setBoundaryCondition(False),
          "set boundary condition on {0}{1}".format(specie, culture_no))
    check(s.setInitialAmount(init_amount),
          "set init amount for {0}{1}".format(specie, culture_no))
    # May need to specify a different unit for amount.
    check(s.setSubstanceUnits("dimensionless"),
          "set substance units for {0}{1}".format(specie, culture_no))
    # Density/conc. or amount? Not sure which one to use. False is density.
    check(s.setHasOnlySubstanceUnits(False),
          "set hasOnlySubstanceUnits for {0}{1}".format(specie, culture_no))


# Simulate a plate with data and parameters.
plate1 = Plate(2, 2)
plate1.times = np.linspace(0, 5, 11)
comp_model = CompModel()
params = {
    "C_0": 1e-6,
    "N_0": 0.1,
    "kn": 1.5
}
plate1.set_sim_data(CompModel(), r_mean=40.0, r_var=15.0, custom_params=params)

# writeSBMLToFile(d, filename)

create_model()


