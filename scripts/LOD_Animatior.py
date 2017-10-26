'''
#-------------------------------------------------------------------------------
# Name:        Tree_Lod_Anim.py
# Purpose:     Switches tree LOD models based on a distance to camera.
#
# Author:      Blake Harcourt - Blakeharcourt@hotmail.com
#
# Created:     24/10/2017
# Copyright:   (c) Blake Harcourt 2017
# Licence:     See attached License text file.
#-------------------------------------------------------------------------------
# Instructions:
# 0. Open the "LOD_Animation.cej" scene
# 1. Run this python script to display the Tree LOD Anim UI panel. 
# 2. A UI box with a "start" button will appear on the screen. Note: Python can sometimes take a while to start the first time using it.
# 3. Select all the tree shapes in the viewport you want to LOD animate. (cntrl+A)
# 4. Press 'start', the tree shapes will now animate LODS depending on camera distance. - You can unselect the trees after this step
# 5. To stop LOD animating, simply close the UI box.
#-------------------------------------------------------------------------------
# Notes:
# 1. Trees must have a CGA rule that uses the attribute 'LOD_Level' to change shapes.
# 2. LOD levels start at 0, and move up incrementally. 1,2,3, etc.
# 3. LOD 0 is the highest LOD a model has.
# 4. Once the LOD animation has started all trees can be unselected and LODs will still be changed.
# 5. Trees must be selected before pressing start
# 6. This rule could very easily work for buildings or road rules. Just needs a LOD_Level attribute.
#-------------------------------------------------------------------------------
'''


#Imports
try:
    from scripting import *
    from math import *
    from java.awt import *
    from java.awt.event import  *
    import threading
    import time
    import profile
    import random
    raise Exception('Import', 'Import')
except Exception, inst:
    print type(inst)
    print inst.args
    print inst   

# get a CityEngine instance
ce = CE()


Tree_Group = []         #A list of all trees added in the scene
Animate = False         #Is the program currently animating
Run = ""                #An Animation Thread



#Class for the UI interaction listeners (Closing and Deactivated) ------------------------------------
class Listener(WindowAdapter):
    
    #Has the window been closed - stop animating if so
    def windowClosing(self, e):
        global Animate
        print("Closing window") 
        Animate = False
        e.getSource().dispose()
        
        
    #Make the UI panel always on top
    def windowDeactivated(self, e):
            e.getSource().setAlwaysOnTop(False);
            e.getSource().setAlwaysOnTop(True);
            print("focus lost");

#Changes the LOD of the tree -----------------------------------------------------------------------
def ChangeLod(Object, distance, Shape):

    #Get the current LOD level of the selected tree
    Current_LOD = int(ce.getAttribute(Shape, "/ce/rule/LOD_Level"))

    #Change it depending on distance and current level - Current distances are 200, 100 and 30
    if (distance > 200 and Current_LOD != 3 ):
        ce.setAttribute(Shape, "/ce/rule/LOD_Level", 3) 
    elif ((distance > 100 and distance < 200)   and Current_LOD != 2):
        ce.setAttribute(Shape, "/ce/rule/LOD_Level", 2)      
    elif ((distance > 30 and distance < 100)  and Current_LOD != 1):
        ce.setAttribute(Shape,"/ce/rule/LOD_Level", 1)       
    elif (distance < 30  and Current_LOD != 0):
        ce.setAttribute(Shape, "/ce/rule/LOD_Level", 0)   

#infinite update loop
def Tree_Update_Loop():
    global Run
    global Animate
    global threads

    #Rerun the loop every 1 second
    Run = threading.Timer(1.0, Tree_Update_Loop)
    if (Animate == True):
        Run.start()
     
    #Get the camera position
    CameraPos = ce.get3DViews()[0].getCameraPosition()

    #Loop through each tree
    for C in Tree_Group:    
        
        #Get the tree position
        Pos_Tree = C.Get_Tree_Pos()
        Shape_Tree = C.Get_Tree_Shape()
        
        #Calculate the deltas for XYZ between the camera and the tree
        deltaX =  Pos_Tree[0] - CameraPos[0]
        deltaY =  Pos_Tree[1] - CameraPos[1]
        deltaZ =  Pos_Tree[2] - CameraPos[2] 
        
        #Calculate the distance between camera and tree
        distance =  sqrt(deltaX * deltaX + deltaY * deltaY + deltaZ * deltaZ);
        
        #Note: - Lod could potentially be set by calculating the camera view frustrum instead of just using distance to camera.
        
        #Update the LOD in a new thread
        t1 = threading.Thread(target = ChangeLod, args = (C, distance, Shape_Tree ))
        t1.start()

#On start button pressed event
def Start(event):
    global Tree_Group
    global Run
    global Animate
    
    print("Starting the animation thread")
    Animate = True #SET TO TRUE HERE OR ANIMATION WILL NEVER START!
    Run = threading.Timer(1.0, Tree_Update_Loop)
    Run.start()
    
    #Get all selected trees
    selectedShapes = ce.getObjectsFrom(ce.selection, ce.isShape)
    
    #Add all trees to the Tree_Group and cache their positions
    for S in selectedShapes:
        T = Tree(ce.getPosition(S), S)  #Cache the tree position as it never changes
        Tree_Group.append(T)            #Add it to the tree group
    
    print("LOD Animation engine running...")
    print("Num trees = " + str(len(Tree_Group)))
    if (len(Tree_Group) == 0):
        print("No trees were selected to animate. Close the UI panel, select all trees, and start again." )


#Class containing tree position and tree CE shape ------------------------------------------------
class Tree:
    def __init__(self, Pos, Shape):
        self.Pos = Pos
        self.Shape = Shape
        
    #Returns an array of the tree position [X,Y,Z]
    def Get_Tree_Pos(self):
        return self.Pos
     
    #Returns the tree CE Shape
    def Get_Tree_Shape(self):
        return self.Shape

#DIALOG ------------------------------------------------------------------------------------------
class DiaButton(Button):
    dialog = None
    tfield = None

def dialog():
    frame = Frame("LOD_Frame")
    frame.setAlwaysOnTop(True);
    dia = Dialog(frame, "LOD Animator", False)
    dia.setSize(550,500)

    l = Listener()
    dia.addWindowListener(l)

    b1 = DiaButton("Start", actionPerformed=Start)
    dia.add(b1)

    layout = GridLayout(5,2)
    dia.setLayout(layout)
    dia.pack()
    dia.show()
    
dialog()
