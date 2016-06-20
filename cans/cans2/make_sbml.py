"""Convert model to SBML.

Addapted from:
(Michael Hucka) "Tutorial: creating a simple model"
http://sbml.org/Software/libSBML/5.13.0/docs//python-api/libsbml-python-creating-model.html
http://sbml.org/Software/libSBML/docs/python-api/create_simple_model_8py-example.html

See also the SBML Level 3 Version 1 Release 1 specifications.
http://sbml.org/Software/libSBML/docs/python-api/libsbml-sbml-specifications.html

There is one explicit reference to a species (N) in the function
create_spcecies. This is done to assign initial amounts at boundaries.

"""
import sys
from libsbml import *


def check(value, message):
    """If 'value' is None, prints an error message constructed using
    'message' and then exits with status code 1.  If 'value' is an
    integer, it assumes it is a libSBML return status code.  If the
    code value is LIBSBML_OPERATION_SUCCESS, returns without further
    action; if it is not, prints an error message constructed using
    'message' along with text from libSBML explaining the meaning of
    the code, and exits with status code 1.

    (Michael Hucka) "Tutorial: creating a simple model"
    http://sbml.org/Software/libSBML/5.13.0/docs//python-api/libsbml-python-creating-model.html
    http://sbml.org/Software/libSBML/docs/python-api/create_simple_model_8py-example.html

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
                       units="volume"):
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
    check(c.setUnits(units), "set compartment units")


def create_params(model, plate, growth_model, params):
    """Create plate and culture level parameters.

    Values provided in the params argument should be ordered according
    to the names in growth_model.params. growth_model.param_index is
    the index of the first parameter in growth_model.params that is
    not an amount. growth_model.b_index is the index of the first
    culture level parameter in growth_model.params.

    """
    pi = growth_model.param_index
    bi = growth_model.b_index
    # Create params for init amounts.
    for i, init_amount in enumerate(growth_model.params[:pi]):
        create_param(model, init_amount, constant=True, val=params[i],
                     units="item")
    # Plate level parameters (excluding init amounts).
    for i, param in enumerate(growth_model.params[pi:bi]):
        create_param(model, param, constant=True, val=params[pi + i])
    # Culture level parameters.
    for i, param in enumerate(growth_model.params[bi:]):
        first_index = bi + i*plate.no_cultures
        for j in range(plate.no_cultures):
            create_param(model, param + str(j), constant=True,
                         val=params[first_index + j])


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
        check(k.setUnits(units), "set parameter {0} units".format(id))


def create_a_species(model, species, culture_no, compartment="c1",
                     units="item", has_only_substance_units=True,
                     constant=False, bc=False):
    """Add a species to the SBML Model."""
    s = model.createSpecies()
    check(s, "create species s")
    check(s.setId(species + str(culture_no)),
          "set species {0}{1} id".format(species, culture_no))
    check(s.setCompartment(compartment),
          "set species {0}{1} compartment".format(species, culture_no))
    # If "constant" and "boundaryCondition" both false,
    # species can be both a product and a reactant.
    check(s.setConstant(constant),
          "set constant attr on {0}{1}".format(species, culture_no))
    check(s.setBoundaryCondition(bc),
          "set boundary condition on {0}{1}".format(species, culture_no))

    # Now setting with InitialAssignment in assign_init_vals().
    # check(s.setInitialAmount(init_amount),
    #       "set init amount for {0}{1}".format(species, culture_no))

    # May need to specify a different unit for amount.
    check(s.setSubstanceUnits(units),
          "set substance units for {0}{1}".format(species, culture_no))
    # If False: unit of amount / unit of size. If True: unit of amount
    # only. I.e. desnity or amount?
    check(s.setHasOnlySubstanceUnits(has_only_substance_units),
          "set hasOnlySubstanceUnits for {0}{1}".format(species, culture_no))


def create_species(model, plate, growth_model, params):
    """Create each species in a growth model for each culture on a Plate.

    Species list is, e.g., C0, C1, ..., N0, N1, ... and can be
    retrieved with the method Model.getListOfSpecies(). Requires
    either plate.sim_params or plate.est_params as the params argument
    in order to set initial amounts.

    """
    for i, species in enumerate(growth_model.species):
        for n in range(plate.no_cultures):
            # Now setting with InitialAssignment in assign_init_vals().
            # if species == "N" and n in plate.edges:
            #     # Different N_0 for cultures at the boundaries in some
            #     # models.
            #     print(model.getParameter("C_0").getValue())
            #     # Need to reference the SBML parameter
            #     init_amount = params[i+1]
            # else:
            #     init_amount = params[i]
            create_a_species(model, species, n, units="item")


def assign_init_vals(model, plate, growth_model):
    """Assign initial values to species.

    Assignment using an InitialAssignment object allows assignment
    using rules. The alternative, directly assigning values to the
    species with e.g. setInitialAmount(val), does not allow this. In
    our case we wish to reference initial amount parameters in the
    initial assignment. This way we should be able to fit initial
    amounts that belong to more than one culture collectively in
    COPASI.

    """
    # How does the initial assigment know which species it references?
    for i in range(plate.no_cultures):
        for s, bc in zip(growth_model.species, growth_model.species_bc):
            init = model.createInitialAssignment()
            check(init, "Create InitialAssignment for {0}".format(s + str(i)))
            check(init.setSymbol(s + str(i)),
                  "Set symbol for {0}".format(s + str(i)))

            if i in plate.edges and bc:    # String or empty string.
                math_ast = parseL3Formula(bc)
                check(math_ast, "create AST for {0}".format(s + str(i)))
            else:
                init_param = growth_model.params[growth_model.species.index(s)]
                math_ast = parseL3Formula(init_param)

            check(init.setMath(math_ast), "set math for {0}".format(s + str(i)))


def create_reactions(model, plate, growth_model):
    for reaction in growth_model.reactions:
        if reaction["neighs"]:
            create_two_culture_reactions(model, plate, reaction)
        elif not reaction["neighs"]:
            create_one_culture_reactions(model, plate, reaction)


def create_one_culture_reactions(model, plate, reaction):

    """Create reactions with species from only one culture.

    Intended for growth type reactions rather than diffusion.
    """
    for i in range(plate.no_cultures):
        # The single culture indices must be supplied in a tuple so
        # that a general function, which can handle reactions with
        # species from more than one culture, can be used to format
        # names.
        create_reaction(model, reaction, (i,))


def create_two_culture_reactions(model, plate, reaction):
    """Intended for diffusion type reactions."""
    if reaction["reversible"]:
        # Only inculde higher neighbours so that reactions are not
        # counted twice.
        neighs = [tuple(j for j in plate.neighbourhood[i] if i<j)
                  for i in range(plate.no_cultures)]
    elif not reaction["reversible"]:
        neighs = plate.neighbourhood

    for i in range(plate.no_cultures):
        for j in neighs[i]:
            create_reaction(model, reaction, (i, j))


def create_reaction(model, reaction, indices):
    """Create a reaction.

    Species can come from more than one culture with culture indices
    passed in the indices tuple.
    """
    r = init_reaction(model, reaction["name"].format(*indices),
                      reversible=reaction["reversible"])
    for stoich, reactant in reaction["reactants"]:
        create_reactant(r, stoich, reactant.format(*indices))
    for stoich, product in reaction["products"]:
        create_product(r, stoich, product.format(*indices))

    math_ast = parseL3Formula(reaction["rate"].format(*indices))
    check(math_ast, "create AST for " + reaction["name"].format(*indices))

    kinetic_law = r.createKineticLaw()
    check(kinetic_law,
          "create kinetic law for " + reaction["name"].format(*indices))
    check(kinetic_law.setMath(math_ast),
          "set math on kinetic law for " + reaction["name"].format(*indices))


def init_reaction(model, id, reversible=False, fast=False):
    r = model.createReaction()
    check(r, "create reaction")
    check(r.setId(id), "set reaction {0} id".format(id))
    # Reversibility is actually determined by the rate equation and it
    # is up to the programmer to make sure that this attribute is
    # consistant with it.
    check(r.setReversible(reversible),
          "set reaction {0} reversibility flag".format(id))
    # "If a model does not distinguish between time scales, the fast
    # attribute should be set to 'false' for all reactions." - from
    # SBML L3V1R1 specification. Our hypothesis is that diffusion
    # occurs quickly enough to affect growth so "fast" should be False
    # for all.
    check(r.setFast(fast), "set reaction {0} speed".format(id))
    return r


def create_reactant(reaction, stoich, species_id):
    """Add a reactant to a libsbml Reaction."""
    r_id = reaction.getId()
    reactant_in_r = "reactant {0} in reaction {1}".format(species_id, r_id)
    R_ref = reaction.createReactant()
    check(R_ref, "create {0} reactant".format(species_id))
    check(R_ref.setSpecies(species_id), "assign " + reactant_in_r)
    # "constant" dictates whether the stochiometry can be changed
    # during a reaction.
    check(R_ref.setConstant(False), "set 'constant' on " + reactant_in_r)
    check(R_ref.setStoichiometry(stoich),
          "set stoichiometry for " + reactant_in_r)


def create_product(reaction, stoich, species_id):
    """Add a product to a libsbml Reaction."""
    r_id = reaction.getId()
    prod_in_r = "product {0} in reaction {1}".format(species_id, r_id)
    P_ref = reaction.createProduct()
    check(P_ref, "create {0} product".format(species_id))
    check(P_ref.setSpecies(species_id), "assign " + prod_in_r)
    # "constant" dictates whether the stochiometry can be changed
    # during a reaction.
    check(P_ref.setConstant(False), "set 'constant' on " + prod_in_r)
    check(P_ref.setStoichiometry(stoich), "set stoichiometry for " + prod_in_r)


def create_sbml(plate, growth_model, params, outfile=""):
    """Return an SBML model given a plate and model.

    http://sbml.org/Software/libSBML/5.13.0/docs/
    /python-api/libsbml-python-creating-model.html

    Requires either plate.sim_params or plate.est_params (or whatever
    attribute estimated parameters are assigned to) as the params
    argument.

    If outfile ends with the suffix ".gz", the xml file is compressed.

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

    # Intensity measurments output by Colonzyer are given in arbitrary
    # units so use item (rather than moles) for substance amounts.
    check(model.setExtentUnits("item"), "set model units of extent")
    check(model.setSubstanceUnits("item"), "set model substance units")

    # Removed to make more general. Let units for kinitic parameters
    # be automatically generated from other units.  # Create units for
    # kinetic parameters. Not necessarry but may help # with error
    # checking of mathematical formula. Units are not # heirarchical
    # so must use second as a base rather than day.
    # create_unit(model, id="per_day", kinds=[UNIT_KIND_SECOND],
    # exponents=[-1], scales=[0], multipliers=[86400])
    # create_unit(model, id="day_per_item", kinds=[UNIT_KIND_SECOND,
    # UNIT_KIND_ITEM], exponents=[1, -1], scales=[0, 0],
    # multipliers=[86400, 1])

    # Use one compartment for all species and reactions.
    create_compartment(model, "c1", constant=True, size=1, dims=0,
                       units="dimensionless")

    create_params(model, plate, growth_model, params)
    create_species(model, plate, growth_model, params)

    # Assing rulebased initial values to species
    assign_init_vals(model, plate, growth_model)

    create_reactions(model, plate, growth_model)

    if outfile:
        writeSBMLToFile(document, outfile)

    # Return a text string containing the SBML document in xml format.
    return writeSBMLToString(document)


if __name__ == "__main__":
    import numpy as np


    from cans2.plate import Plate
    from cans2.model import CompModelBC, CompModel
    from cans2.plotter import Plotter


    # Simulate a plate with data and parameters.
    rows = 3
    cols = 3
    plate1 = Plate(rows, cols)
    plate1.times = np.linspace(0, 5, 11)
    comp_model = CompModelBC()
    params = {
        "C_0": 1e-6,
        "N_0": 0.1,
        "kn": 1.5
    }
    plate1.set_sim_data(comp_model, b_mean=40.0, b_var=15.0,
                        custom_params=params)

    # Convert comp model to SBML.
    sbml = create_sbml(plate1, comp_model, plate1.sim_params,
                        outfile="sbml_models/simulated_{0}x{1}_test_plate_bc.xml".format(rows, cols))

    comp_model_ir = CompModel(rev_diff=False)
    sbml = create_sbml(plate1, comp_model_ir, plate1.sim_params,
                        outfile="sbml_models/simulated_{0}x{1}_test_plate_ir.xml".format(rows, cols))

    # # Plot a cans model simulation to compare.
    # comp_plotter = Plotter(CompModel())
    # comp_plotter.plot_est(plate1, plate1.sim_params,
    #                       title="CompModel Simulated Growth (SciPy)", sim=True,
    #                       filename="sbml_models/plots/cans_{0}x{1}_sim.pdf".format(rows, cols))

    # Should try loading the model in Copasi and simulating/solving
    # with libRoadRunner when I think it is finished.
