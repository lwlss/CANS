<?xml version="1.0" encoding="UTF-8"?>
<!-- generated with COPASI 4.16 (Build 104) (http://www.copasi.org) at 2016-06-29 20:31:30 UTC -->
<?oxygen RNGSchema="http://www.copasi.org/static/schema/CopasiML.rng" type="xml"?>
<COPASI xmlns="http://www.copasi.org/static/schema" versionMajor="4" versionMinor="16" versionDevel="104" copasiSourcesModified="0">
  <ListOfFunctions>
    <Function key="Function_13" name="Mass action (irreversible)" type="MassAction" reversible="false">
      <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
   <rdf:Description rdf:about="#Function_13">
   <CopasiMT:is rdf:resource="urn:miriam:obo.sbo:SBO:0000041" />
   </rdf:Description>
   </rdf:RDF>
      </MiriamAnnotation>
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
<b>Mass action rate law for first order irreversible reactions</b>
<p>
Reaction scheme where the products are created from the reactants and the change of a product quantity is proportional to the product of reactant activities. The reaction scheme does not include any reverse process that creates the reactants from the products. The change of a product quantity is proportional to the quantity of one reactant.
</p>
</body>
      </Comment>
      <Expression>
        k1*PRODUCT&lt;substrate_i&gt;
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_81" name="k1" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_79" name="substrate" order="1" role="substrate"/>
      </ListOfParameterDescriptions>
    </Function>
    <Function key="Function_14" name="Mass action (reversible)" type="MassAction" reversible="true">
      <MiriamAnnotation>
<rdf:RDF xmlns:CopasiMT="http://www.copasi.org/RDF/MiriamTerms#" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
   <rdf:Description rdf:about="#Function_14">
   <CopasiMT:is rdf:resource="urn:miriam:obo.sbo:SBO:0000042" />
   </rdf:Description>
   </rdf:RDF>
      </MiriamAnnotation>
      <Comment>
        <body xmlns="http://www.w3.org/1999/xhtml">
<b>Mass action rate law for reversible reactions</b>
<p>
Reaction scheme where the products are created from the reactants and the change of a product quantity is proportional to the product of reactant activities. The reaction scheme does include a reverse process that creates the reactants from the products.
</p>
</body>
      </Comment>
      <Expression>
        k1*PRODUCT&lt;substrate_i&gt;-k2*PRODUCT&lt;product_j&gt;
      </Expression>
      <ListOfParameterDescriptions>
        <ParameterDescription key="FunctionParameter_62" name="k1" order="0" role="constant"/>
        <ParameterDescription key="FunctionParameter_39" name="substrate" order="1" role="substrate"/>
        <ParameterDescription key="FunctionParameter_67" name="k2" order="2" role="constant"/>
        <ParameterDescription key="FunctionParameter_71" name="product" order="3" role="product"/>
      </ListOfParameterDescriptions>
    </Function>
  </ListOfFunctions>
  <Model key="Model_6" name="NoName" simulationType="time" timeUnit="d" volumeUnit="l" areaUnit="m²" lengthUnit="m" quantityUnit="#" type="deterministic" avogadroConstant="6.02214179e+23">
    <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#Model_6">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2016-06-29T20:37:06Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

    </MiriamAnnotation>
    <ListOfCompartments>
      <Compartment key="Compartment_2" name="c1" simulationType="fixed" dimensionality="0">
      </Compartment>
    </ListOfCompartments>
    <ListOfMetabolites>
      <Metabolite key="Metabolite_1533" name="C0" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1529" name="C1" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1525" name="C2" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1521" name="C3" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1517" name="C4" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1513" name="C5" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1509" name="C6" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1505" name="C7" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1501" name="C8" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1497" name="N0" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1493" name="N1" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1489" name="N2" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1485" name="N3" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1481" name="N4" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1477" name="N5" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1473" name="N6" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1469" name="N7" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
      <Metabolite key="Metabolite_1465" name="N8" simulationType="reactions" compartment="Compartment_2">
        <InitialExpression>
          &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
        </InitialExpression>
      </Metabolite>
    </ListOfMetabolites>
    <ListOfModelValues>
      <ModelValue key="ModelValue_387" name="C_0" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_387">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2016-06-29T20:37:18Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_386" name="N_0" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_386">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2016-06-29T20:37:20Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_385" name="kn" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_385">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2016-06-29T20:37:19Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_384" name="b0" simulationType="fixed">
        <MiriamAnnotation>
<rdf:RDF
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="#ModelValue_384">
    <dcterms:created>
      <rdf:Description>
        <dcterms:W3CDTF>2016-06-29T20:37:14Z</dcterms:W3CDTF>
      </rdf:Description>
    </dcterms:created>
  </rdf:Description>
</rdf:RDF>

        </MiriamAnnotation>
      </ModelValue>
      <ModelValue key="ModelValue_383" name="b1" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_382" name="b2" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_381" name="b3" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_380" name="b4" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_379" name="b5" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_378" name="b6" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_377" name="b7" simulationType="fixed">
      </ModelValue>
      <ModelValue key="ModelValue_376" name="b8" simulationType="fixed">
      </ModelValue>
    </ListOfModelValues>
    <ListOfReactions>
      <Reaction key="Reaction_1839" name="Growth_4" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1481" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1517" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1517" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4294" name="k1" value="40.742"/>
        </ListOfConstants>
        <KineticLaw function="Function_13">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_380"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1481"/>
              <SourceParameter reference="Metabolite_1517"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1838" name="Growth_0" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1497" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1533" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1533" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4293" name="k1" value="45.5543"/>
        </ListOfConstants>
        <KineticLaw function="Function_13">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_384"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1497"/>
              <SourceParameter reference="Metabolite_1533"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1837" name="Growth_1" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1493" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1529" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1529" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4292" name="k1" value="47.044"/>
        </ListOfConstants>
        <KineticLaw function="Function_13">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_383"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1493"/>
              <SourceParameter reference="Metabolite_1529"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1836" name="Growth_2" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1489" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1525" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1525" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4291" name="k1" value="46.1197"/>
        </ListOfConstants>
        <KineticLaw function="Function_13">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_382"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1489"/>
              <SourceParameter reference="Metabolite_1525"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1835" name="Growth_3" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1485" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1521" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1521" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4290" name="k1" value="43.2198"/>
        </ListOfConstants>
        <KineticLaw function="Function_13">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_381"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1485"/>
              <SourceParameter reference="Metabolite_1521"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1834" name="Growth_5" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1477" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1513" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1513" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4289" name="k1" value="49.8545"/>
        </ListOfConstants>
        <KineticLaw function="Function_13">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_379"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1477"/>
              <SourceParameter reference="Metabolite_1513"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1833" name="Growth_6" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1473" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1509" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1509" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_4288" name="k1" value="45.2705"/>
        </ListOfConstants>
        <KineticLaw function="Function_13">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_378"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1473"/>
              <SourceParameter reference="Metabolite_1509"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1832" name="Growth_7" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1469" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1505" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1505" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1847" name="k1" value="46.1567"/>
        </ListOfConstants>
        <KineticLaw function="Function_13">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_377"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1469"/>
              <SourceParameter reference="Metabolite_1505"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1831" name="Growth_8" reversible="false" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1465" stoichiometry="1"/>
          <Substrate metabolite="Metabolite_1501" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1501" stoichiometry="2"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1848" name="k1" value="61.8591"/>
        </ListOfConstants>
        <KineticLaw function="Function_13">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_81">
              <SourceParameter reference="ModelValue_376"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_79">
              <SourceParameter reference="Metabolite_1465"/>
              <SourceParameter reference="Metabolite_1501"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1830" name="Diff_0_1" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1497" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1493" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1849" name="k1" value="6.66883"/>
          <Constant key="Parameter_1850" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1497"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1493"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1829" name="Diff_0_3" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1497" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1485" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1851" name="k1" value="6.66883"/>
          <Constant key="Parameter_1852" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1497"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1485"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1828" name="Diff_1_2" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1493" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1489" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1853" name="k1" value="6.66883"/>
          <Constant key="Parameter_1854" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1493"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1489"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1827" name="Diff_1_4" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1493" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1481" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1855" name="k1" value="6.66883"/>
          <Constant key="Parameter_1856" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1493"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1481"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1826" name="Diff_2_5" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1489" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1477" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1857" name="k1" value="6.66883"/>
          <Constant key="Parameter_1858" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1489"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1477"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1825" name="Diff_3_4" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1485" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1481" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1859" name="k1" value="6.66883"/>
          <Constant key="Parameter_1860" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1485"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1481"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1824" name="Diff_3_6" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1485" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1473" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1861" name="k1" value="6.66883"/>
          <Constant key="Parameter_1862" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1485"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1473"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1823" name="Diff_4_5" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1481" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1477" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1863" name="k1" value="6.66883"/>
          <Constant key="Parameter_1864" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1481"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1477"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1822" name="Diff_4_7" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1481" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1469" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1865" name="k1" value="6.66883"/>
          <Constant key="Parameter_1866" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1481"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1469"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1821" name="Diff_5_8" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1477" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1465" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1867" name="k1" value="6.66883"/>
          <Constant key="Parameter_1868" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1477"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1465"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1820" name="Diff_6_7" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1473" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1469" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1869" name="k1" value="6.66883"/>
          <Constant key="Parameter_1870" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1473"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1469"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
      <Reaction key="Reaction_1819" name="Diff_7_8" reversible="true" fast="false">
        <ListOfSubstrates>
          <Substrate metabolite="Metabolite_1469" stoichiometry="1"/>
        </ListOfSubstrates>
        <ListOfProducts>
          <Product metabolite="Metabolite_1465" stoichiometry="1"/>
        </ListOfProducts>
        <ListOfConstants>
          <Constant key="Parameter_1871" name="k1" value="6.66883"/>
          <Constant key="Parameter_1872" name="k2" value="6.66883"/>
        </ListOfConstants>
        <KineticLaw function="Function_14">
          <ListOfCallParameters>
            <CallParameter functionParameter="FunctionParameter_62">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_39">
              <SourceParameter reference="Metabolite_1469"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_67">
              <SourceParameter reference="ModelValue_385"/>
            </CallParameter>
            <CallParameter functionParameter="FunctionParameter_71">
              <SourceParameter reference="Metabolite_1465"/>
            </CallParameter>
          </ListOfCallParameters>
        </KineticLaw>
      </Reaction>
    </ListOfReactions>
    <ListOfModelParameterSets activeSet="ModelParameterSet_0">
      <ModelParameterSet key="ModelParameterSet_0" name="Initial State">
        <ModelParameterGroup cn="String=Initial Time" type="Group">
          <ModelParameter cn="CN=Root,Model=NoName" value="0" type="Model" simulationType="time"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Compartment Sizes" type="Group">
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1]" value="1" type="Compartment" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Species Values" type="Group">
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C0]" value="0.001860615615095808" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C1]" value="0.001860615615095808" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C2]" value="0.001860615615095808" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C3]" value="0.001860615615095808" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C4]" value="0.001860615615095808" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C5]" value="0.001860615615095808" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C6]" value="0.001860615615095808" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C7]" value="0.001860615615095808" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C8]" value="0.001860615615095808" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N0]" value="0.06234861064845275" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N1]" value="0.06234861064845275" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N2]" value="0.06234861064845275" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N3]" value="0.06234861064845275" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N4]" value="0.06234861064845275" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N5]" value="0.06234861064845275" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N6]" value="0.06234861064845275" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N7]" value="0.06234861064845275" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N8]" value="0.06234861064845275" type="Species" simulationType="reactions">
            <InitialExpression>
              &lt;CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue&gt;
            </InitialExpression>
          </ModelParameter>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Initial Global Quantities" type="Group">
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[C_0]" value="0.001860615615095808" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[N_0]" value="0.06234861064845275" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[kn]" value="2.53641138605161" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[b0]" value="29.81396447813013" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[b1]" value="30.4510541986608" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[b2]" value="27.98375334844317" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[b3]" value="22.38973192910318" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[b4]" value="21.26493973508206" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[b5]" value="34.74555704220679" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[b6]" value="23.06606280195167" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[b7]" value="24.69650953636499" type="ModelValue" simulationType="fixed"/>
          <ModelParameter cn="CN=Root,Model=NoName,Vector=Values[b8]" value="45.4495327181632" type="ModelValue" simulationType="fixed"/>
        </ModelParameterGroup>
        <ModelParameterGroup cn="String=Kinetic Parameters" type="Group">
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Growth_4]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Growth_4],ParameterGroup=Parameters,Parameter=k1" value="21.26493973508206" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[b4],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Growth_0]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Growth_0],ParameterGroup=Parameters,Parameter=k1" value="29.81396447813013" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[b0],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Growth_1]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Growth_1],ParameterGroup=Parameters,Parameter=k1" value="30.4510541986608" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[b1],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Growth_2]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Growth_2],ParameterGroup=Parameters,Parameter=k1" value="27.98375334844317" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[b2],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Growth_3]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Growth_3],ParameterGroup=Parameters,Parameter=k1" value="22.38973192910318" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[b3],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Growth_5]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Growth_5],ParameterGroup=Parameters,Parameter=k1" value="34.74555704220679" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[b5],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Growth_6]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Growth_6],ParameterGroup=Parameters,Parameter=k1" value="23.06606280195167" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[b6],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Growth_7]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Growth_7],ParameterGroup=Parameters,Parameter=k1" value="24.69650953636499" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[b7],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Growth_8]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Growth_8],ParameterGroup=Parameters,Parameter=k1" value="45.4495327181632" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[b8],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_0_1]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_0_1],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_0_1],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_0_3]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_0_3],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_0_3],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_1_2]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_1_2],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_1_2],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_1_4]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_1_4],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_1_4],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_2_5]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_2_5],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_2_5],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_3_4]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_3_4],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_3_4],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_3_6]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_3_6],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_3_6],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_4_5]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_4_5],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_4_5],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_4_7]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_4_7],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_4_7],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_5_8]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_5_8],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_5_8],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_6_7]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_6_7],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_6_7],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
          <ModelParameterGroup cn="CN=Root,Model=NoName,Vector=Reactions[Diff_7_8]" type="Reaction">
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_7_8],ParameterGroup=Parameters,Parameter=k1" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
            <ModelParameter cn="CN=Root,Model=NoName,Vector=Reactions[Diff_7_8],ParameterGroup=Parameters,Parameter=k2" value="2.53641138605161" type="ReactionParameter" simulationType="assignment">
              <InitialExpression>
                &lt;CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue&gt;
              </InitialExpression>
            </ModelParameter>
          </ModelParameterGroup>
        </ModelParameterGroup>
      </ModelParameterSet>
    </ListOfModelParameterSets>
    <StateTemplate>
      <StateTemplateVariable objectReference="Model_6"/>
      <StateTemplateVariable objectReference="Metabolite_1481"/>
      <StateTemplateVariable objectReference="Metabolite_1493"/>
      <StateTemplateVariable objectReference="Metabolite_1485"/>
      <StateTemplateVariable objectReference="Metabolite_1477"/>
      <StateTemplateVariable objectReference="Metabolite_1469"/>
      <StateTemplateVariable objectReference="Metabolite_1473"/>
      <StateTemplateVariable objectReference="Metabolite_1489"/>
      <StateTemplateVariable objectReference="Metabolite_1465"/>
      <StateTemplateVariable objectReference="Metabolite_1497"/>
      <StateTemplateVariable objectReference="Metabolite_1517"/>
      <StateTemplateVariable objectReference="Metabolite_1521"/>
      <StateTemplateVariable objectReference="Metabolite_1513"/>
      <StateTemplateVariable objectReference="Metabolite_1505"/>
      <StateTemplateVariable objectReference="Metabolite_1529"/>
      <StateTemplateVariable objectReference="Metabolite_1533"/>
      <StateTemplateVariable objectReference="Metabolite_1501"/>
      <StateTemplateVariable objectReference="Metabolite_1509"/>
      <StateTemplateVariable objectReference="Metabolite_1525"/>
      <StateTemplateVariable objectReference="Compartment_2"/>
      <StateTemplateVariable objectReference="ModelValue_387"/>
      <StateTemplateVariable objectReference="ModelValue_386"/>
      <StateTemplateVariable objectReference="ModelValue_385"/>
      <StateTemplateVariable objectReference="ModelValue_384"/>
      <StateTemplateVariable objectReference="ModelValue_383"/>
      <StateTemplateVariable objectReference="ModelValue_382"/>
      <StateTemplateVariable objectReference="ModelValue_381"/>
      <StateTemplateVariable objectReference="ModelValue_380"/>
      <StateTemplateVariable objectReference="ModelValue_379"/>
      <StateTemplateVariable objectReference="ModelValue_378"/>
      <StateTemplateVariable objectReference="ModelValue_377"/>
      <StateTemplateVariable objectReference="ModelValue_376"/>
    </StateTemplate>
    <InitialState type="initialState">
      0 0.06234861064845275 0.06234861064845275 0.06234861064845275 0.06234861064845275 0.06234861064845275 0.06234861064845275 0.06234861064845275 0.06234861064845275 0.06234861064845275 0.001860615615095808 0.001860615615095808 0.001860615615095808 0.001860615615095808 0.001860615615095808 0.001860615615095808 0.001860615615095808 0.001860615615095808 0.001860615615095808 1 0.001860615615095808 0.06234861064845275 2.53641138605161 29.81396447813013 30.4510541986608 27.98375334844317 22.38973192910318 21.26493973508206 34.74555704220679 23.06606280195167 24.69650953636499 45.4495327181632 
    </InitialState>
  </Model>
  <ListOfTasks>
    <Task key="Task_13" name="Steady-State" type="steadyState" scheduled="false" updateModel="false">
      <Report reference="Report_0" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="JacobianRequested" type="bool" value="1"/>
        <Parameter name="StabilityAnalysisRequested" type="bool" value="1"/>
      </Problem>
      <Method name="Enhanced Newton" type="EnhancedNewton">
        <Parameter name="Resolution" type="unsignedFloat" value="1e-09"/>
        <Parameter name="Derivation Factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Use Newton" type="bool" value="1"/>
        <Parameter name="Use Integration" type="bool" value="1"/>
        <Parameter name="Use Back Integration" type="bool" value="1"/>
        <Parameter name="Accept Negative Concentrations" type="bool" value="0"/>
        <Parameter name="Iteration Limit" type="unsignedInteger" value="50"/>
        <Parameter name="Maximum duration for forward integration" type="unsignedFloat" value="1000000000"/>
        <Parameter name="Maximum duration for backward integration" type="unsignedFloat" value="1000000"/>
      </Method>
    </Task>
    <Task key="Task_1" name="Time-Course" type="timeCourse" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="500"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="5"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Continue on Simultaneous Events" type="bool" value="1"/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_2" name="Scan" type="scan" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="Subtask" type="unsignedInteger" value="1"/>
        <ParameterGroup name="ScanItems">
        </ParameterGroup>
        <Parameter name="Output in subtask" type="bool" value="1"/>
        <Parameter name="Adjust initial conditions" type="bool" value="0"/>
      </Problem>
      <Method name="Scan Framework" type="ScanFramework">
      </Method>
    </Task>
    <Task key="Task_3" name="Elementary Flux Modes" type="fluxMode" scheduled="false" updateModel="false">
      <Report reference="Report_1" target="" append="1" confirmOverwrite="1"/>
      <Problem>
      </Problem>
      <Method name="EFM Algorithm" type="EFMAlgorithm">
      </Method>
    </Task>
    <Task key="Task_4" name="Optimization" type="optimization" scheduled="false" updateModel="false">
      <Report reference="Report_2" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Subtask" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <ParameterText name="ObjectiveExpression" type="expression">
          
        </ParameterText>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
      </Problem>
      <Method name="Random Search" type="RandomSearch">
        <Parameter name="Number of Iterations" type="unsignedInteger" value="100000"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_5" name="Parameter Estimation" type="parameterFitting" scheduled="false" updateModel="false">
      <Report reference="Report_3" target="fit_report_p15_test_zone_5_5_3x3.txt" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Maximize" type="bool" value="0"/>
        <Parameter name="Randomize Start Values" type="bool" value="0"/>
        <Parameter name="Calculate Statistics" type="bool" value="1"/>
        <ParameterGroup name="OptimizationItemList">
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="7.162006228704914e-09"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[C_0],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="0.00186062"/>
            <Parameter name="UpperBound" type="cn" value="7.162006228704914e-03"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="3.258543118273325e-02"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[N_0],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="0.06234861064845275"/>
            <Parameter name="UpperBound" type="cn" value="1.30341724730933e-01"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[b0],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="29.81396447813013"/>
            <Parameter name="UpperBound" type="cn" value="1e+05"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[b1],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="30.4510541986608"/>
            <Parameter name="UpperBound" type="cn" value="1e+05"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[b2],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="27.98375334844317"/>
            <Parameter name="UpperBound" type="cn" value="1e+05"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[b3],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="22.38973192910318"/>
            <Parameter name="UpperBound" type="cn" value="1e+05"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[b4],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="21.26493973508206"/>
            <Parameter name="UpperBound" type="cn" value="1e+05"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[b5],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="34.74555704220679"/>
            <Parameter name="UpperBound" type="cn" value="1e+05"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[b6],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="23.06606280195167"/>
            <Parameter name="UpperBound" type="cn" value="1e+05"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[b7],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="24.69650953636499"/>
            <Parameter name="UpperBound" type="cn" value="1e+05"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[b8],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="45.4495327181632"/>
            <Parameter name="UpperBound" type="cn" value="1e+05"/>
          </ParameterGroup>
          <ParameterGroup name="FitItem">
            <ParameterGroup name="Affected Cross Validation Experiments">
            </ParameterGroup>
            <ParameterGroup name="Affected Experiments">
            </ParameterGroup>
            <Parameter name="LowerBound" type="cn" value="0"/>
            <Parameter name="ObjectCN" type="cn" value="CN=Root,Model=NoName,Vector=Values[kn],Reference=InitialValue"/>
            <Parameter name="StartValue" type="float" value="2.53641138605161"/>
            <Parameter name="UpperBound" type="cn" value="10"/>
          </ParameterGroup>
        </ParameterGroup>
        <ParameterGroup name="OptimizationConstraintList">
        </ParameterGroup>
        <Parameter name="Steady-State" type="cn" value="CN=Root,Vector=TaskList[Steady-State]"/>
        <Parameter name="Time-Course" type="cn" value="CN=Root,Vector=TaskList[Time-Course]"/>
        <Parameter name="Create Parameter Sets" type="bool" value="0"/>
        <ParameterGroup name="Experiment Set">
          <ParameterGroup name="Experiment">
            <Parameter name="Data is Row Oriented" type="bool" value="1"/>
            <Parameter name="Experiment Type" type="unsignedInteger" value="1"/>
            <Parameter name="File Name" type="file" value="p15_test_zone_5_5_3x3.csv"/>
            <Parameter name="First Row" type="unsignedInteger" value="1"/>
            <Parameter name="Key" type="key" value="Experiment_1"/>
            <Parameter name="Last Row" type="unsignedInteger" value="11"/>
            <Parameter name="Normalize Weights per Experiment" type="bool" value="1"/>
            <Parameter name="Number of Columns" type="unsignedInteger" value="10"/>
            <ParameterGroup name="Object Map">
              <ParameterGroup name="0">
                <Parameter name="Role" type="unsignedInteger" value="3"/>
              </ParameterGroup>
              <ParameterGroup name="1">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C0],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="2">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C1],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="3">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C2],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="4">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C3],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="5">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C4],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="6">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C5],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="7">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C6],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="8">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C7],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
              <ParameterGroup name="9">
                <Parameter name="Object CN" type="cn" value="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C8],Reference=Concentration"/>
                <Parameter name="Role" type="unsignedInteger" value="2"/>
              </ParameterGroup>
            </ParameterGroup>
            <Parameter name="Row containing Names" type="unsignedInteger" value="1"/>
            <Parameter name="Separator" type="string" value="&#x09;"/>
            <Parameter name="Weight Method" type="unsignedInteger" value="1"/>
          </ParameterGroup>
        </ParameterGroup>
        <ParameterGroup name="Validation Set">
          <Parameter name="Weight" type="unsignedFloat" value="1"/>
          <Parameter name="Threshold" type="unsignedInteger" value="5"/>
        </ParameterGroup>
      </Problem>
      <Method name="Genetic Algorithm" type="GeneticAlgorithm">
        <Parameter name="Number of Generations" type="unsignedInteger" value="1000"/>
        <Parameter name="Population Size" type="unsignedInteger" value="50"/>
        <Parameter name="Random Number Generator" type="unsignedInteger" value="1"/>
        <Parameter name="Seed" type="unsignedInteger" value="0"/>
      </Method>
    </Task>
    <Task key="Task_6" name="Metabolic Control Analysis" type="metabolicControlAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_4" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_13"/>
      </Problem>
      <Method name="MCA Method (Reder)" type="MCAMethod(Reder)">
        <Parameter name="Modulation Factor" type="unsignedFloat" value="1e-09"/>
        <Parameter name="Use Reeder" type="bool" value="1"/>
        <Parameter name="Use Smallbone" type="bool" value="1"/>
      </Method>
    </Task>
    <Task key="Task_7" name="Lyapunov Exponents" type="lyapunovExponents" scheduled="false" updateModel="false">
      <Report reference="Report_5" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="ExponentNumber" type="unsignedInteger" value="3"/>
        <Parameter name="DivergenceRequested" type="bool" value="1"/>
        <Parameter name="TransientTime" type="float" value="0"/>
      </Problem>
      <Method name="Wolf Method" type="WolfMethod">
        <Parameter name="Orthonormalization Interval" type="unsignedFloat" value="1"/>
        <Parameter name="Overall time" type="unsignedFloat" value="1000"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_8" name="Time Scale Separation Analysis" type="timeScaleSeparationAnalysis" scheduled="false" updateModel="false">
      <Report reference="Report_6" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="1"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
      </Problem>
      <Method name="ILDM (LSODA,Deuflhard)" type="TimeScaleSeparation(ILDM,Deuflhard)">
        <Parameter name="Deuflhard Tolerance" type="unsignedFloat" value="1e-06"/>
      </Method>
    </Task>
    <Task key="Task_9" name="Sensitivities" type="sensitivities" scheduled="false" updateModel="false">
      <Report reference="Report_7" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="SubtaskType" type="unsignedInteger" value="1"/>
        <ParameterGroup name="TargetFunctions">
          <Parameter name="SingleObject" type="cn" value=""/>
          <Parameter name="ObjectListType" type="unsignedInteger" value="7"/>
        </ParameterGroup>
        <ParameterGroup name="ListOfVariables">
          <ParameterGroup name="Variables">
            <Parameter name="SingleObject" type="cn" value=""/>
            <Parameter name="ObjectListType" type="unsignedInteger" value="41"/>
          </ParameterGroup>
        </ParameterGroup>
      </Problem>
      <Method name="Sensitivities Method" type="SensitivitiesMethod">
        <Parameter name="Delta factor" type="unsignedFloat" value="0.001"/>
        <Parameter name="Delta minimum" type="unsignedFloat" value="1e-12"/>
      </Method>
    </Task>
    <Task key="Task_10" name="Moieties" type="moieties" scheduled="false" updateModel="false">
      <Problem>
      </Problem>
      <Method name="Householder Reduction" type="Householder">
      </Method>
    </Task>
    <Task key="Task_11" name="Cross Section" type="crosssection" scheduled="false" updateModel="false">
      <Problem>
        <Parameter name="StepNumber" type="unsignedInteger" value="100"/>
        <Parameter name="StepSize" type="float" value="0.01"/>
        <Parameter name="Duration" type="float" value="1"/>
        <Parameter name="TimeSeriesRequested" type="bool" value="1"/>
        <Parameter name="OutputStartTime" type="float" value="0"/>
        <Parameter name="Output Event" type="bool" value="0"/>
        <Parameter name="Continue on Simultaneous Events" type="bool" value="0"/>
        <Parameter name="LimitCrossings" type="bool" value="0"/>
        <Parameter name="NumCrossingsLimit" type="unsignedInteger" value="0"/>
        <Parameter name="LimitOutTime" type="bool" value="0"/>
        <Parameter name="LimitOutCrossings" type="bool" value="0"/>
        <Parameter name="PositiveDirection" type="bool" value="1"/>
        <Parameter name="NumOutCrossingsLimit" type="unsignedInteger" value="0"/>
        <Parameter name="LimitUntilConvergence" type="bool" value="0"/>
        <Parameter name="ConvergenceTolerance" type="float" value="1e-06"/>
        <Parameter name="Threshold" type="float" value="0"/>
        <Parameter name="DelayOutputUntilConvergence" type="bool" value="0"/>
        <Parameter name="OutputConvergenceTolerance" type="float" value="1e-06"/>
        <ParameterText name="TriggerExpression" type="expression">
          
        </ParameterText>
        <Parameter name="SingleVariable" type="cn" value=""/>
      </Problem>
      <Method name="Deterministic (LSODA)" type="Deterministic(LSODA)">
        <Parameter name="Integrate Reduced Model" type="bool" value="0"/>
        <Parameter name="Relative Tolerance" type="unsignedFloat" value="1e-06"/>
        <Parameter name="Absolute Tolerance" type="unsignedFloat" value="1e-12"/>
        <Parameter name="Max Internal Steps" type="unsignedInteger" value="10000"/>
      </Method>
    </Task>
    <Task key="Task_0" name="Linear Noise Approximation" type="linearNoiseApproximation" scheduled="false" updateModel="false">
      <Report reference="Report_8" target="" append="1" confirmOverwrite="1"/>
      <Problem>
        <Parameter name="Steady-State" type="key" value="Task_13"/>
      </Problem>
      <Method name="Linear Noise Approximation" type="LinearNoiseApproximation">
      </Method>
    </Task>
  </ListOfTasks>
  <ListOfReports>
    <Report key="Report_0" name="Steady-State" taskType="steadyState" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Steady-State]"/>
      </Footer>
    </Report>
    <Report key="Report_1" name="Elementary Flux Modes" taskType="fluxMode" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Footer>
        <Object cn="CN=Root,Vector=TaskList[Elementary Flux Modes],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_2" name="Optimization" taskType="optimization" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Problem=Optimization,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Optimization],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_3" name="Parameter Estimation" taskType="parameterFitting" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Description"/>
        <Object cn="String=\[Function Evaluations\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Value\]"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="String=\[Best Parameters\]"/>
      </Header>
      <Body>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Function Evaluations"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Value"/>
        <Object cn="Separator=&#x09;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,Reference=Best Parameters"/>
      </Body>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Parameter Estimation],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_4" name="Metabolic Control Analysis" taskType="metabolicControlAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Metabolic Control Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_5" name="Lyapunov Exponents" taskType="lyapunovExponents" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Lyapunov Exponents],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_6" name="Time Scale Separation Analysis" taskType="timeScaleSeparationAnalysis" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Time Scale Separation Analysis],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_7" name="Sensitivities" taskType="sensitivities" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Sensitivities],Object=Result"/>
      </Footer>
    </Report>
    <Report key="Report_8" name="Linear Noise Approximation" taskType="linearNoiseApproximation" separator="&#x09;" precision="6">
      <Comment>
        Automatically generated report.
      </Comment>
      <Header>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Description"/>
      </Header>
      <Footer>
        <Object cn="String=&#x0a;"/>
        <Object cn="CN=Root,Vector=TaskList[Linear Noise Approximation],Object=Result"/>
      </Footer>
    </Report>
  </ListOfReports>
  <ListOfPlots>
    <PlotSpecification name="Concentrations, Volumes, and Global Quantity Values" type="Plot2D" active="1">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="[C0]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C0],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[C1]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C1],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[C2]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C2],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[C3]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C3],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[C4]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C4],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[C5]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C5],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[C6]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C6],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[C7]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C7],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[C8]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[C8],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[N0]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N0],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[N1]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N1],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[N2]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N2],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[N3]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N3],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[N4]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N4],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[N5]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N5],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[N6]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N6],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[N7]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N7],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="[N8]" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="auto"/>
          <Parameter name="Recording Activity" type="string" value="during"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Model=NoName,Reference=Time"/>
            <ChannelSpec cn="CN=Root,Model=NoName,Vector=Compartments[c1],Vector=Metabolites[N8],Reference=Concentration"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
    <PlotSpecification name="Parameter Estimation Result" type="Plot2D" active="1">
      <Parameter name="log X" type="bool" value="0"/>
      <Parameter name="log Y" type="bool" value="0"/>
      <ListOfPlotItems>
        <PlotItem name="Experiment,[C0](Measured Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="3"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Color" type="string" value="#FF0000"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Measured Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C0](Fitted Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="#FF0000"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Fitted Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C0](Weighted Error)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="2"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
          <Parameter name="Color" type="string" value="#FF0000"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Weighted Error"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C1](Measured Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="3"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Color" type="string" value="#0000FF"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[1],Reference=Measured Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C1](Fitted Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="#0000FF"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[1],Reference=Fitted Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C1](Weighted Error)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="2"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
          <Parameter name="Color" type="string" value="#0000FF"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[1],Reference=Weighted Error"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C2](Measured Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="3"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Color" type="string" value="#00E600"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[2],Reference=Measured Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C2](Fitted Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="#00E600"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[2],Reference=Fitted Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C2](Weighted Error)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="2"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
          <Parameter name="Color" type="string" value="#00E600"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[2],Reference=Weighted Error"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C3](Measured Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="3"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Color" type="string" value="#00BEF0"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[3],Reference=Measured Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C3](Fitted Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="#00BEF0"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[3],Reference=Fitted Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C3](Weighted Error)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="2"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
          <Parameter name="Color" type="string" value="#00BEF0"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[3],Reference=Weighted Error"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C4](Measured Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="3"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Color" type="string" value="#F000FF"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[4],Reference=Measured Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C4](Fitted Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="#F000FF"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[4],Reference=Fitted Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C4](Weighted Error)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="2"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
          <Parameter name="Color" type="string" value="#F000FF"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[4],Reference=Weighted Error"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C5](Measured Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="3"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Color" type="string" value="#F0C800"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[5],Reference=Measured Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C5](Fitted Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="#F0C800"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[5],Reference=Fitted Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C5](Weighted Error)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="2"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
          <Parameter name="Color" type="string" value="#F0C800"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[5],Reference=Weighted Error"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C6](Measured Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="3"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Color" type="string" value="#FF0000"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[6],Reference=Measured Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C6](Fitted Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="#FF0000"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[6],Reference=Fitted Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C6](Weighted Error)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="2"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
          <Parameter name="Color" type="string" value="#FF0000"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[6],Reference=Weighted Error"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C7](Measured Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="3"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Color" type="string" value="#0000FF"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[7],Reference=Measured Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C7](Fitted Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="#0000FF"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[7],Reference=Fitted Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C7](Weighted Error)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="2"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
          <Parameter name="Color" type="string" value="#0000FF"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[7],Reference=Weighted Error"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C8](Measured Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="3"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="1"/>
          <Parameter name="Color" type="string" value="#00E600"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[8],Reference=Measured Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C8](Fitted Value)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="0"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Color" type="string" value="#00E600"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[8],Reference=Fitted Value"/>
          </ListOfChannels>
        </PlotItem>
        <PlotItem name="Experiment,[C8](Weighted Error)" type="Curve2D">
          <Parameter name="Line type" type="unsignedInteger" value="2"/>
          <Parameter name="Line subtype" type="unsignedInteger" value="0"/>
          <Parameter name="Line width" type="unsignedFloat" value="1"/>
          <Parameter name="Symbol subtype" type="unsignedInteger" value="2"/>
          <Parameter name="Color" type="string" value="#00E600"/>
          <Parameter name="Recording Activity" type="string" value="after"/>
          <ListOfChannels>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[0],Reference=Independent Value"/>
            <ChannelSpec cn="CN=Root,Vector=TaskList[Parameter Estimation],Problem=Parameter Estimation,ParameterGroup=Experiment Set,ParameterGroup=Experiment,Vector=Fitted Points[8],Reference=Weighted Error"/>
          </ListOfChannels>
        </PlotItem>
      </ListOfPlotItems>
    </PlotSpecification>
  </ListOfPlots>
  <GUI>
  </GUI>
  <SBMLReference file="p15_test_5_5_3x3_from_compmodelbc_argv_5_b_guess_35.xml">
    <SBMLMap SBMLid="C0" COPASIkey="Metabolite_1533"/>
    <SBMLMap SBMLid="C1" COPASIkey="Metabolite_1529"/>
    <SBMLMap SBMLid="C2" COPASIkey="Metabolite_1525"/>
    <SBMLMap SBMLid="C3" COPASIkey="Metabolite_1521"/>
    <SBMLMap SBMLid="C4" COPASIkey="Metabolite_1517"/>
    <SBMLMap SBMLid="C5" COPASIkey="Metabolite_1513"/>
    <SBMLMap SBMLid="C6" COPASIkey="Metabolite_1509"/>
    <SBMLMap SBMLid="C7" COPASIkey="Metabolite_1505"/>
    <SBMLMap SBMLid="C8" COPASIkey="Metabolite_1501"/>
    <SBMLMap SBMLid="C_0" COPASIkey="ModelValue_387"/>
    <SBMLMap SBMLid="Diff_0_1" COPASIkey="Reaction_1830"/>
    <SBMLMap SBMLid="Diff_0_3" COPASIkey="Reaction_1829"/>
    <SBMLMap SBMLid="Diff_1_2" COPASIkey="Reaction_1828"/>
    <SBMLMap SBMLid="Diff_1_4" COPASIkey="Reaction_1827"/>
    <SBMLMap SBMLid="Diff_2_5" COPASIkey="Reaction_1826"/>
    <SBMLMap SBMLid="Diff_3_4" COPASIkey="Reaction_1825"/>
    <SBMLMap SBMLid="Diff_3_6" COPASIkey="Reaction_1824"/>
    <SBMLMap SBMLid="Diff_4_5" COPASIkey="Reaction_1823"/>
    <SBMLMap SBMLid="Diff_4_7" COPASIkey="Reaction_1822"/>
    <SBMLMap SBMLid="Diff_5_8" COPASIkey="Reaction_1821"/>
    <SBMLMap SBMLid="Diff_6_7" COPASIkey="Reaction_1820"/>
    <SBMLMap SBMLid="Diff_7_8" COPASIkey="Reaction_1819"/>
    <SBMLMap SBMLid="Growth_0" COPASIkey="Reaction_1838"/>
    <SBMLMap SBMLid="Growth_1" COPASIkey="Reaction_1837"/>
    <SBMLMap SBMLid="Growth_2" COPASIkey="Reaction_1836"/>
    <SBMLMap SBMLid="Growth_3" COPASIkey="Reaction_1835"/>
    <SBMLMap SBMLid="Growth_4" COPASIkey="Reaction_1839"/>
    <SBMLMap SBMLid="Growth_5" COPASIkey="Reaction_1834"/>
    <SBMLMap SBMLid="Growth_6" COPASIkey="Reaction_1833"/>
    <SBMLMap SBMLid="Growth_7" COPASIkey="Reaction_1832"/>
    <SBMLMap SBMLid="Growth_8" COPASIkey="Reaction_1831"/>
    <SBMLMap SBMLid="N0" COPASIkey="Metabolite_1497"/>
    <SBMLMap SBMLid="N1" COPASIkey="Metabolite_1493"/>
    <SBMLMap SBMLid="N2" COPASIkey="Metabolite_1489"/>
    <SBMLMap SBMLid="N3" COPASIkey="Metabolite_1485"/>
    <SBMLMap SBMLid="N4" COPASIkey="Metabolite_1481"/>
    <SBMLMap SBMLid="N5" COPASIkey="Metabolite_1477"/>
    <SBMLMap SBMLid="N6" COPASIkey="Metabolite_1473"/>
    <SBMLMap SBMLid="N7" COPASIkey="Metabolite_1469"/>
    <SBMLMap SBMLid="N8" COPASIkey="Metabolite_1465"/>
    <SBMLMap SBMLid="N_0" COPASIkey="ModelValue_386"/>
    <SBMLMap SBMLid="b0" COPASIkey="ModelValue_384"/>
    <SBMLMap SBMLid="b1" COPASIkey="ModelValue_383"/>
    <SBMLMap SBMLid="b2" COPASIkey="ModelValue_382"/>
    <SBMLMap SBMLid="b3" COPASIkey="ModelValue_381"/>
    <SBMLMap SBMLid="b4" COPASIkey="ModelValue_380"/>
    <SBMLMap SBMLid="b5" COPASIkey="ModelValue_379"/>
    <SBMLMap SBMLid="b6" COPASIkey="ModelValue_378"/>
    <SBMLMap SBMLid="b7" COPASIkey="ModelValue_377"/>
    <SBMLMap SBMLid="b8" COPASIkey="ModelValue_376"/>
    <SBMLMap SBMLid="c1" COPASIkey="Compartment_2"/>
    <SBMLMap SBMLid="kn" COPASIkey="ModelValue_385"/>
  </SBMLReference>
</COPASI>
