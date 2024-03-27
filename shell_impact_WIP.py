
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

import numpy as np
import odbAccess
from abaqus import *
from abaqusConstants import *
from connectorBehavior import *


def create_box(dim_xyz, thickness, density, E, poisson, yieldstr, plasticstr, material_name, force, job_name):    
    Mdb()
    #x = 0.150 (6in), y = 0.075(3in), z=0.100 (4 in)
    x = dim_xyz[0]
    y = dim_xyz[2]
    z = dim_xyz[1]
    # top
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(x, z))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='six_four', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['six_four'].BaseShell(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    
    #end cap 1
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(y, z))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='three_four_pt1', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['three_four_pt1'].BaseShell(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    
    #end cap 2
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(y, z))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='three_four_pt2', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['three_four_pt2'].BaseShell(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    
    #side 1
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(x, y))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='three_six_pt1', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['three_six_pt1'].BaseShell(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    
    #side 2
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(x, y))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='thee_six_pt2', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['thee_six_pt2'].BaseShell(sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    
    # create material
    mdb.models['Model-1'].Material(name=material_name)
    mdb.models['Model-1'].materials[material_name].Density(table=((density, ), ))
    mdb.models['Model-1'].materials[material_name].Elastic(table=((E,poisson), 
        ))
    mdb.models['Model-1'].materials[material_name].Plastic(table=((yieldstr, plasticstr), ))

    #assembly
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='six_four-1', 
        part=mdb.models['Model-1'].parts['six_four'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='thee_six_pt2-1'
        , part=mdb.models['Model-1'].parts['thee_six_pt2'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name=
        'three_four_pt1-1', part=mdb.models['Model-1'].parts['three_four_pt1'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name=
        'three_four_pt2-1', part=mdb.models['Model-1'].parts['three_four_pt2'])
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name=
        'three_six_pt1-1', part=mdb.models['Model-1'].parts['three_six_pt1'])
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('three_six_pt1-1', )
        , vector=(0.0, 0.0, 0.1))
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(0.1, 0.0, 
        0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('six_four-1', ))
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('six_four-1', ), 
        vector=(0.0, y, 0.0))
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 0.0, 
        0.1), axisPoint=(0.0, 0.0, 0.0), instanceList=('three_four_pt2-1', ))
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 0.1, 
        0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('three_four_pt2-1', ))
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('three_four_pt2-1', 
        ), vector=(x, 0.0, 0.0))
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 0.0, 
        0.1), axisPoint=(0.0, 0.0, 0.0), instanceList=('three_four_pt1-1', ))
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 0.1, 
        0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('three_four_pt1-1', ))

    #combine assembly
    mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, 
        instances=(mdb.models['Model-1'].rootAssembly.instances['six_four-1'], 
        mdb.models['Model-1'].rootAssembly.instances['thee_six_pt2-1'], 
        mdb.models['Model-1'].rootAssembly.instances['three_four_pt1-1'], 
        mdb.models['Model-1'].rootAssembly.instances['three_four_pt2-1'], 
        mdb.models['Model-1'].rootAssembly.instances['three_six_pt1-1']), name=
        'chassis', originalInstances=SUPPRESS)

    # combine into set, assign material
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material=material_name, name='Section-1', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=thickness/4, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].parts['chassis'].Set(faces=
        mdb.models['Model-1'].parts['chassis'].faces.findAt(((x/2, y/2, z), ), 
        ((x, y/2, z/2), ), ((0.0, y/2, z/2), ), ((x/2, y/2, 0.0), ), 
        ((x/2, y, z/2), ), ), name='Set-1')
    mdb.models['Model-1'].parts['chassis'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['chassis'].sets['Set-1'], sectionName=
        'Section-1', thicknessAssignment=FROM_SECTION)
    
    #create surface for the outser surface of the chassis
    mdb.models['Model-1'].parts['chassis'].Surface(name='chassis_outer', 
        side1Faces=mdb.models['Model-1'].parts['chassis'].faces.findAt(((x/2, 
        y/2, z), ), ((0.0, y/2, z/2), ), ((x/2, y, z/2), ), (
        (x, y/2, z/2), ), ((x/2, y/2, 0.0), ), ))
   
     #create the weight
    radius = 0.05 # diameter of weight was 140 mm
    height = 0.01/2 # height of weight was 20 mm
     
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
    mdb.models['Model-1'].sketches['__profile__'].ConstructionLine(point1=(0.0, 
        -0.5), point2=(0.0, 0.5))
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 0.0))
    mdb.models['Model-1'].sketches['__profile__'].FixedConstraint(entity=
        mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 0.0), 
        ))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, height), point2=(
        radius, height))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(radius, height), point2=(
        radius, -height))
    mdb.models['Model-1'].sketches['__profile__'].Line(point1=(radius, -height), 
        point2=(0.0, -height))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='weight', type=
        DISCRETE_RIGID_SURFACE)
    mdb.models['Model-1'].parts['weight'].BaseShellRevolve(angle=360.0, 
        flipRevolveDirection=OFF, sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
     
    mdb.models['Model-1'].parts['weight'].ReferencePoint(point=
        mdb.models['Model-1'].parts['weight'].vertices.findAt((0.0, height, 0.0), ))
    
    #add inertia to the weight so that it can collide
    mdb.models['Model-1'].parts['weight'].engineeringFeatures.PointMassInertia(
        alpha=0.0, composite=0.0, i11=1.0, i22=1.0, i33=1.0, mass=1.0, name=
        'Inertia-1', region=Region(referencePoints=(
        mdb.models['Model-1'].parts['weight'].referencePoints[2], )))
    
    #add the weight to the assembly
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='weight-1', 
        part=mdb.models['Model-1'].parts['weight'])
    mdb.models['Model-1'].rootAssembly.translate(instanceList=('weight-1', ), 
        vector=(x/2, y*1.1, z/2))
           
    # mesh
    mdb.models['Model-1'].rootAssembly.regenerate()
    mdb.models['Model-1'].parts['chassis'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.01, size=0.0025)
    mdb.models['Model-1'].parts['chassis'].setElementType(elemTypes=(ElemType(
        elemCode=S4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT), ElemType(elemCode=S3, elemLibrary=STANDARD)), 
        regions=(mdb.models['Model-1'].parts['chassis'].faces.findAt(((x/2, y/2, 
        z), ), ((x, y/2, z/2), ), ((0.0, y/2, z/2), ), ((x/2, y/2, 0.0), ), 
        ((x/2, y, z/2), ), ), ))
    mdb.models['Model-1'].parts['chassis'].generateMesh()
    
    #mesh the weight
    mdb.models['Model-1'].parts['weight'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=0.005)
    mdb.models['Model-1'].parts['weight'].setElementType(elemTypes=(ElemType(
        elemCode=R3D4, elemLibrary=STANDARD), ElemType(elemCode=R3D3, 
        elemLibrary=STANDARD)), regions=(
        mdb.models['Model-1'].parts['weight'].faces.findAt(((radius/2, height, 
        0), ), ((radius, 0, 0), ), ((radius/2, -height, 0), ), ), ))
    mdb.models['Model-1'].parts['weight'].generateMesh()
    mdb.models['Model-1'].rootAssembly.regenerate()
   
    # create step
    mdb.models['Model-1'].ExplicitDynamicsStep(improvedDtMethod=ON, name=
        'Step-smash', previous='Initial', timePeriod=0.15)
    
    
    # boundary conditions
    mdb.models['Model-1'].rootAssembly.Set(edges=
        mdb.models['Model-1'].rootAssembly.instances['chassis-1'].edges.findAt(((
        x/2, 0.0, z), ), ((x, 0.0, z/2), ), ((0.0, 0.0, z/2), ), ((
        x/2, 0.0, 0.0), ), ), name='Set-1')    
    mdb.models['Model-1'].EncastreBC(createStepName='Step-smash', localCsys=None, name=
        'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-1'])
    
    #interaction property
    mdb.models['Model-1'].ContactProperty('IntProp-1')
    mdb.models['Model-1'].ContactExp(createStepName='Step-smash', name='Int-1')
    mdb.models['Model-1'].interactions['Int-1'].includedPairs.setValuesInStep(
        stepName='Step-smash', useAllstar=ON)
    mdb.models['Model-1'].interactions['Int-1'].contactPropertyAssignments.appendInStep(
        assignments=((GLOBAL, SELF, 'IntProp-1'), ), stepName='Step-smash')
    mdb.models['Model-1'].rootAssembly.Set(faces=
        mdb.models['Model-1'].rootAssembly.instances['weight-1'].faces.findAt(((
        x/2, y*1.1+height, z/2), ), ((x/2 + radius, y*1.1, z/2), ), ((x/2, y*1.1-height, z/2), ), ), 
        name='b_Set-2')
    mdb.models['Model-1'].RigidBody(bodyRegion=
        mdb.models['Model-1'].rootAssembly.sets['b_Set-2'], name='Constraint-1', 
        refPointRegion=Region(referencePoints=(
        mdb.models['Model-1'].rootAssembly.instances['weight-1'].referencePoints[2], 
        )))
    
    #apply velocity to weight
    mdb.models['Model-1'].rootAssembly.Set(name='Set-5', referencePoints=(
        mdb.models['Model-1'].rootAssembly.instances['weight-1'].referencePoints[2], 
        ))
    mdb.models['Model-1'].Velocity(distributionType=MAGNITUDE, field='', name=
        'Predefined Field-1', omega=0.0, region=
        mdb.models['Model-1'].rootAssembly.sets['Set-5'], velocity2=-1.0)
    
    # set boundary conditions to weight so it doesn't rotate while falling
    mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName=
        'Step-smash', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=
        None, name='BC-weight', region=Region(referencePoints=(
        mdb.models['Model-1'].rootAssembly.instances['weight-1'].referencePoints[2], 
        )), u1=0.0, u2=UNSET, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0)
    
    # create job
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
        multiprocessingMode=DEFAULT, name=job_name, nodalOutputPrecision=SINGLE, 
        numCpus=8, numDomains=8, numGPUs=0, queue=None, resultsFormat=ODB, scratch=
        '', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
 

# dimensions is 6in x 4 in x 3 in (roughly 150x100x75 mm^3)
dim_xyz = [0.150, 0.100, 0.075] #in meters
thickness = 0.003 #1/4 in is roughly 6.35 mm, so 1/8 in is approximated as 3mm
force = 20 #2.5 lbs is roughly 1 kg but I am going to do 2 kg and estimate gravity to be 10 m/s^2, so force in N will be 20 N


# name, density (kg/m^3), young's mod (Pa), poisson, yield stress (Pa), plastic strain
#NOTE: have to change the above value for thickness for _quarterthick job for polycarbonate below
materials = [['job_sheetimpact_304steel', 8000, 193000000000, 0.29, 205000000, 0, 'steel'], 
             ['job_sheetimpact_6061aluminum', 2700, 69000000000, 0.33, 55000000, 0, 'aluminum'],
             ['job_sheetimpact_polystyrene', 1050, 2960000000, 0.21, 34900000, 0, 'polystyrene'], 
             ['job_sheetimpact_PolycarbonatePlastic_quarterthick', 1200, 2310000000, 0.36, 62700000, 0, 'plastic'], 
             ['job_sheetimpact_PolycarbonatePlastic', 1200, 2310000000, 0.36, 62700000, 0, 'plastic']]



for i in range(3, 4):
    density = materials[i][1]
    E = materials[i][2]
    poisson = materials[i][3]
    yieldstress = materials[i][4]
    plasticstrain = materials[i][5]
    material_name = materials[i][6]
    job_name = materials[i][0]
    
    create_box(dim_xyz, thickness, density, E, poisson, yieldstress, plasticstrain, material_name, force, job_name)
    #odb = openOdb(path='{}.odb'.format(job_name))
    #odb.close()
    