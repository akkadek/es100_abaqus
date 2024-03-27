# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

def create_square(density, E, poisson, yieldstr, plasticstr, material_name, job_name):
    # make part
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.25, 0.0), point2=(
        -0.25, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
        addUndoState=False, entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 0.0), 
        ))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='sheet', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['sheet'].BaseShellExtrude(depth=0.50, sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    
    # material properties
    mdb.models['Model-1'].Material(name=material_name)
    mdb.models['Model-1'].materials[material_name].Density(table=((density, ), ))
    mdb.models['Model-1'].materials[material_name].Elastic(table=((E, poisson), 
        ))
    mdb.models['Model-1'].materials[material_name].Plastic(table=((yieldstr, plasticstr), ))
    
    # make assembly
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='sheet-1', part=
        mdb.models['Model-1'].parts['sheet'])
    
    #create section and assign material
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material=material_name, name='Section-1', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=0.01, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].parts['sheet'].Set(faces=
        mdb.models['Model-1'].parts['sheet'].faces.findAt(((-0.08333333, 0.0, 
        0.33333333), )), name='Set-sheet')
    mdb.models['Model-1'].parts['sheet'].SectionAssignment(offset=0.0, offsetField=
        '', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['sheet'].sets['Set-sheet'], sectionName=
        'Section-1', thicknessAssignment=FROM_SECTION)
   

    # create step
    mdb.models['Model-1'].StaticStep(initialInc=0.01, name='Step-1', nlgeom=ON, 
        previous='Initial')
    mdb.models['Model-1'].steps['Step-1'].setValues(maxInc=0.01, maxNumInc=300)
    
    # field output request
    #mdb.models['Model-1'].FieldOutputRequest(createStepName='Step-1', 
    #    layupLocationMethod=SPECIFIED, layupNames=('sheet-1.CompositeLayup-1', ), 
    #    name='F-Output-2', outputAtPlyBottom=False, outputAtPlyMid=True, 
    #    outputAtPlyTop=False, rebar=EXCLUDE, variables=('S', 'MISES', 'HSNFTCRT', 
    #    'HSNFCCRT', 'HSNMTCRT', 'HSNMCCRT'))
    
    # boundary conditions and load
    mdb.models['Model-1'].rootAssembly.Set(edges=
        mdb.models['Model-1'].rootAssembly.instances['sheet-1'].edges.findAt(((
        0.250, 0.0, 0.125), )), name='Set-1')
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-1'], u1=0.0, 
        u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0)
    mdb.models['Model-1'].rootAssembly.Set(edges=
        mdb.models['Model-1'].rootAssembly.instances['sheet-1'].edges.findAt(((
        -0.250, 0.0, 0.125), )), name='Set-2')
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
        'BC-2', region=mdb.models['Model-1'].rootAssembly.sets['Set-2'], u1=0.01, 
        u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)

    # mesh
    mdb.models['Model-1'].parts['sheet'].setElementType(elemTypes=(ElemType(
        elemCode=S4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT), ElemType(elemCode=S3, elemLibrary=STANDARD)), 
        regions=(mdb.models['Model-1'].parts['sheet'].faces.findAt(((-0.08333333, 
        0.0, 0.33333333), )), ))
    mdb.models['Model-1'].parts['sheet'].seedPart(deviationFactor=00.1, 
        minSizeFactor=0.01, size=0.010)
    mdb.models['Model-1'].parts['sheet'].generateMesh()
    mdb.models['Model-1'].rootAssembly.regenerate()
    
    # create job    
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name=job_name, nodalOutputPrecision=
        SINGLE, numCpus=8, numDomains=8, queue=None, resultsFormat=ODB, scratch='', 
        type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    #mdb.jobs[job_name].submit(consistencyChecking=OFF)

    
    # Save by kak3375 on 2024_01_31-17.35.05; build 2021 2020_03_06-09.50.37 167380



# name, density (kg/m^3), young's mod (Pa), poisson, yield stress (Pa), plastic strain
materials = [['job_sheet_polystyrene', 1050, 2960000000, 0.21, 34900000, 0, 'polystyrene'],
             ['job_sheet_304steel', 8000, 193000000000, 0.29, 205000000, 0, 'steel'], 
             ['job_sheet_6061aluminum', 2700, 69000000000, 0.33, 55000000, 0, 'aluminum'],
             ['job_sheet_PolycarbonatePlastic', 1200, 2310000000, 0.36, 62700000, 0, 'plastic'], 
             ['job_sheet_carbonFiber', 1750, 200000000000, 0.26]]



for i in range(3, 4):
    density = materials[i][1]
    E = materials[i][2]
    poisson = materials[i][3]
    yieldstr = materials[i][4]
    plasticstr = materials[i][5]
    material_name = materials[i][6]
    job_name = materials[i][0]
    
    create_square(density, E, poisson, yieldstr, plasticstr, material_name, job_name)
    
    #pathName = job_name + '.odb'
    # odb = odbAccess.openOdb(path=pathName)
    
    #odb = openOdb(path='{}.odb'.format(pathName))
    #odb.close()