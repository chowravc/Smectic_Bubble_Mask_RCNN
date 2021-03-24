# Importing Packages
import bpy
import sys
import os
import numpy as np
import random as r
import glob as g

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

# Importing useful python scripts
from capCreator import *
from wallCreator import *
from bubbleCreator import *
from spotCreator import *
from lightUtils import *
from materialUtils import *
from intersectionCheck import *


# CHANGE CODE HERE-----

# If true, separate masks for each island will be produced
# If false, front and back masks will be produced
insanceSegmentation = True

# Resolution of rendered masks
res = (256, 256)

# END OF CHANGE CODE-----


# Deleting wall used to add emission in last script
bpy.data.objects["ChangeEmissionToRed100OnMe"].select_set(True)
bpy.ops.object.delete()

# Finding out number of images to produce
numberOfImages = len(g.glob("./angles/*"))

os.mkdir('./masks/')

# Creating separate masks for each island in each image
if insanceSegmentation:

    # For each image
    for k in range(numberOfImages):

        # Deciding name of image
        nameID = str(k).zfill(len(str(numberOfImages)))

        # Creating a number of randomly decided caps.

        # Number of random caps to create.
        number = len(open("./angles/"+nameID+".txt", "r").read().splitlines())

        # Radius of the sphere the cap will be on.
        radius = 1

        # Location of the cap.
        location = (0, 0, 0)

        # If on first image, access these materials as variables
        if k == 0:

            # Cap materials
            frontCapMaterial = bpy.data.materials["frontCapMaterial"]

            # Material of wall
            materialName = "wallMaterial"
            materialColor = (0, 0, 0)
            createMaterial(materialName, materialColor, removeShader=True)
            wallMaterial = bpy.data.materials[materialName]

        # Read information on each cap in image
        capAngles = open("./angles/"+nameID+".txt", "r").read().splitlines()
        capPhis = open("./phis/"+nameID+".txt", "r").read().splitlines()
        capThetas = open("./thetas/"+nameID+".txt", "r").read().splitlines()

        # Creating walls
        if k == 0:
            createWall("Wall0", (2, -2, -10), (-5, -2, -10), (-5, -2, 10), (2, -2, 10), wallMaterial)
            createWall("Wall1", (2, 2, -10), (-5, 2, -10), (-5, 2, 10), (2, 2, 10), wallMaterial)
            createWall("Wall2", (-5, -2, -10), (-5, 2, -10), (-5, 2, 10), (-5, -2, 10), wallMaterial)

            # Creating and linking camera
            bpy.ops.object.camera_add(location=(3, 0, 0), rotation=(np.pi/2, 0, np.pi/2))

        # Saving masks for each cap
        for i in range(number):

            for j in range(number):

                # Creating 'masking' caps
                # Cap size parameter (Choose cap size between 0 and 10)
                cSize = float(capAngles[j])

                # Euler angles of the cap.
                euler = (float(capThetas[j]), float(capPhis[j]), 0)
        
                # Name the cap.
                name = "Cap" + str(j).zfill(len(str(number)))

                if j == i:
                    # Creating cap
                    createCap(radius, cSize, euler, location, name, frontCapMaterial)
                    fname = name
                else:
                    # Creating cap
                    createCap(radius, cSize, euler, location, name, wallMaterial)

            # Changing camera size and activating
            bpy.data.cameras['Camera'].lens = 45
            bpy.context.scene.camera = bpy.data.objects['Camera']
            
            # Deselect all
            bpy.ops.object.select_all(action='DESELECT')

            # Setting render path
            if i == 0:
                os.mkdir('./masks/' + nameID + "/")

            bpy.context.scene.render.filepath = os.getcwd() + '/masks/' + nameID + "/" + fname + '.png'

            # Rendering Scene
            # Get the scene
            scene = bpy.data.scenes["Scene"]

            # Set render resolution
            scene.render.resolution_x = res[0]
            scene.render.resolution_y = res[1]
            scene.render.resolution_percentage = 100
            bpy.ops.render.render(write_still = True)

            # Deselect all
            bpy.ops.object.select_all(action='DESELECT')

            for j in range(number):
                # Deleting caps

                # Name the cap.
                name = "Cap" + str(j).zfill(len(str(number)))

                # Deleting all caps
                bpy.data.objects[name].select_set(True)
                bpy.ops.object.delete()

                # Deselect all
                bpy.ops.object.select_all(action='DESELECT')



print("")
print("Reached end of script 3. Check if correct masks were created. Don't save Blender file while closing. Thanks!")
print("")