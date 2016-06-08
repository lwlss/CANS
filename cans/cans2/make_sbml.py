"""Convert model to SBML.

Addapted from: http://sbml.org/Software/libSBML/5.13.0/docs/
/python-api/libsbml-python-creating-model.html

See also the SBML Level 3 Version 1 Release 1 specifications.
http://sbml.org/Software/libSBML/docs/python-api/ \
libsbml-sbml-specifications.html

"""
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


def create_unit(model, id, kinds, exponents, scales, multipliers):
    """Create a new unit for the SBML Model.

    kinds, exponents, scalses, and multipliers are lists for each base
    unit in the new unit. E.g. for kilometers_per_second, you would
    require unit kinds of meter and second and the corresponding
    exponents scales and multipliers.

    """
    unit_def = model.createUnitDefinition()
    check(unit_def, "create unit definition")
    check(unit_def.setId(id), "set unit difinition id")
    for k, e, s, m in zip(kinds, exponents, scales, multipliers):
        unit = unit_def.createUnit()
        check(unit, "create unit on day")
        # Requires all four of these.
        check(unit.setKind(k), "set unit kind")
        check(unit.setExponent(e), "Set unit exponent")
        check(unit.setScale(s), "set unit scale")
        check(unit.setMultiplier(m), "set unit multiplier")


def create_compartment(model, id, constant=True, size=1, dims=3,
                       units="dimesionless"):
    """Create a new compartment for the SBML Model.

    "constant" is a boolean which determines whether the compartment
    size can vary during a simulation.

    """
    c = model.createCompartment()
    check(c, "create compartment")
    check(c.setId(id), "set compartment id")
    # 'constant' refers to size
    check(c.setConstant(constant), "set compartment 'constant'")
    check(c.setSize(size), "set compartment 'size'")
    check(c.setSpatialDimensions(dims), "set compartment dimensions")
    check(c.setUnits(units), "set compartment dimensions")


def create_a_species(model, species, culture_no, init_amount):
    """Add a species to the SBML Model."""
    s = model.createSpecies()
    check(s, "create species s")
    check(s.setId(species + str(culture_no)),
          "set species {0}{1} id".format(species, culture_no))
    check(s.setCompartment("c1"),
          "set species {0}{1} compartment".format(species, culture_no))
    # If "constant" and "boundaryCondition" both false,
    # species can be both a product and a reactant.
    check(s.setConstant(False),
          "set constant attr on {0}{1}".format(species, culture_no))
    check(s.setBoundaryCondition(False),
          "set boundary condition on {0}{1}".format(species, culture_no))
    check(s.setInitialAmount(init_amount),
          "set init amount for {0}{1}".format(species, culture_no))
    # May need to specify a different unit for amount.
    check(s.setSubstanceUnits("dimensionless"),
          "set substance units for {0}{1}".format(species, culture_no))
    # If False: unit of amount / unit of size. If True: unit of amount
    # only. I.e. desnity or amount?
    check(s.setHasOnlySubstanceUnits(True),
          "set hasOnlySubstanceUnits for {0}{1}".format(species, culture_no))


def create_species(model, plate, growth_model, params):
    """Create each specie in a growth model for each culture on a Plate.

    Species list is, e.g., C0, C1, ..., N0, N1, ... and can be
    retrieved with the method Model.getListOfSpecies(). Requires
    either plate.sim_params or plate.est_params as the params argument
    in order to set initial amounts.

    """
    for i, species in enumerate(growth_model.species):
        for n in range(plate.no_cultures):
            create_a_species(model, species, n, params[i])


def create_model(plate, growth_model, params):
    """Return an SBML model given a plate and model.

    http://sbml.org/Software/libSBML/5.13.0/docs/
    /python-api/libsbml-python-creating-model.html

    Requires either plate.sim_params or plate.est_params (or whatever
    attribute estimated parameters are assigned to) as the params argument.

    """
    try:
        document = SBMLDocument(3, 1)
    except ValueError:
        raise SystemExit("Could not create SBMLDocument object")

    model = document.createModel()
    check(model, "create model")
    create_unit(model, id="day", kinds=[UNIT_KIND_SECOND],
                exponents=[1], scales=[0], multipliers=[86400])
    check(model.setTimeUnits("day"), "set model-wide time units")
    # Dimensionless units are intended for rations where they will
    # cancel out. I use item rather than moles because we actually
    # have intensity measurements as a proxy for amounts and do not
    # know how they corresponds. Intensity output from Colonzyer is
    # given in arbitrary units.
    check(model.setExtentUnits("item"), "set model units of extent")
    check(model.setSubstanceUnits("item"), "set model substance units")
    # check(model.setExtentUnits("mole"), "set model units of extent")
    # check(model.setSubstanceUnits("mole"), "set model substance units")


    # Create units for other params.  Not necessarry but may help with
    # error   checking  of   mathematical  formula.   Units  are   not
    # heirarchical so must use second as a base.
    create_unit(model, id="per_day", kinds=[UNIT_KIND_SECOND], exponents=[-1],
                scales=[0], multipliers=[86400])


    # Not sure whether to use one compartment or a compartment for
    # each culture. Attempting to use dimensionless unit sizes and one
    # compartment. Not sure how all of this affects ODEs yet.
    create_compartment(model, "c1", constant=True, size=1, dims=3,
                       units="dimensionless")

    create_species(model, plate1, growth_model, params)
    print(list(model.getListOfSpecies()))

    # Create parameters
    create_params(model, plate, growth_model, params)

    # Create reactions

def create_params(model, plate, growth_model, params):
    # Create kn. This code is not very general but could be made more
    # general if units were specified for parameters in Model
    # difinitions in the model.py module of the cans package.

    #  May need to define new units per_day or item_per_day.
    create_param(model, "kn", constant=True, val=params[2], units="per_day")
    # Create r

def create_param(model, id, constant, val, units=None):
    """Create an SBML Model parameter.

    If "constant" is True then the parameter value cannot be changed
    by any construct except initialAssignment. Setting "constant"
    False does not mean that the value must change.

    Units is optional.

    """
    k = model.createParameter()
    check(k, "create parameter {0}".format(id))
    check(k.setId(id), "set parameter {0} id".format(id))
    check(k.setConstant(constant), "set parameter {0} 'constant'".format(id))
    check(k.setValue(val), "set parameter {0} value".format(id))
    if units is not None:
        check(k.setUnits("per_day"), "set parameter {0} units".format(id))


if __name__ == "__main__":
    # Simulate a plate with data and parameters.
    plate1 = Plate(2, 2)
    plate1.times = np.linspace(0, 5, 11)
    comp_model = CompModel()
    params = {
        "C_0": 1e-6,
        "N_0": 0.1,
        "kn": 1.5
    }
    plate1.set_sim_data(comp_model, r_mean=40.0, r_var=15.0,
                        custom_params=params)

    create_model(plate1, comp_model, plate1.sim_params)

    # writeSBMLToFile(d, filename)
