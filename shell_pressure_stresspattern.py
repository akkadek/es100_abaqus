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
        'Part-1', originalInstances=SUPPRESS)

    # combine into set
    mdb.models['Model-1'].HomogeneousShellSection(idealization=NO_IDEALIZATION, 
        integrationRule=SIMPSON, material=material_name, name='Section-1', 
        nodalThicknessField='', numIntPts=5, poissonDefinition=DEFAULT, 
        preIntegrate=OFF, temperature=GRADIENT, thickness=thickness, thicknessField='', 
        thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
    mdb.models['Model-1'].parts['Part-1'].Set(faces=
        mdb.models['Model-1'].parts['Part-1'].faces.findAt(((x/2, y/2, z), ), 
        ((x, y/2, z/2), ), ((0.0, y/2, z/2), ), ((x/2, y/2, 0.0), ), 
        ((x/2, y, z/2), ), ), name='Set-1')
    mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=
        mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName=
        'Section-1', thicknessAssignment=FROM_SECTION)
   
    # mesh
    mdb.models['Model-1'].rootAssembly.regenerate()
    mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
        minSizeFactor=0.1, size=0.005)
    mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
        elemCode=S4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT), ElemType(elemCode=S3, elemLibrary=STANDARD)), 
        regions=(mdb.models['Model-1'].parts['Part-1'].faces.findAt(((x/2, y/2, 
        z), ), ((x, y/2, z/2), ), ((0.0, y/2, z/2), ), ((x/2, y/2, 0.0), ), 
        ((x/2, y, z/2), ), ), ))
    mdb.models['Model-1'].parts['Part-1'].generateMesh()
   
    # create step
    mdb.models['Model-1'].rootAssembly.regenerate()
    mdb.models['Model-1'].StaticStep(name='Step-1', nlgeom=ON, previous='Initial')
  
    # boundary conditions
    mdb.models['Model-1'].rootAssembly.Set(edges=
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
       x/2, 0.0, z), ), ((x, 0.0, z/2), ), ((0.0, 0.0, z/2), ), ((
        x/2, 0.0, 0.0), ), ), name='Set-1')
    # pressure
    mdb.models['Model-1'].EncastreBC(createStepName='Step-1', localCsys=None, name=
        'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-1'])
    mdb.models['Model-1'].rootAssembly.Surface(name='Surf-1', side2Faces=
        mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
        x/2, y, z/2), )))
    mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Step-1', 
        distributionType=UNIFORM, field='', magnitude=force, name='Load-1', region=
        mdb.models['Model-1'].rootAssembly.surfaces['Surf-1'])
    
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
materials = [['job_sheetpressure_polystyrene', 1050, 2960000000, 0.21, 34900000, 0, 'polystyrene'], 
             ['job_sheetpressure_304steel', 8000, 193000000000, 0.29, 205000000, 0, 'steel'], 
             ['job_sheetpressure_6061aluminum', 2700, 69000000000, 0.33, 55000000, 0, 'aluminum'],
             ['job_sheetpressure_PolycarbonatePlastic',  1200, 2310000000, 0.36, 62700000, 0, 'plastic'], 
             ['job_sheetcarbonFiber', 1750, 200000000000, 0.26]]



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
    