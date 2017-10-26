'''
#-------------------------------------------------------------------------------
# Name:        Building_Animator.py
# Purpose:     Animates several floors of a building by slowly rotating.
#
# Author:      Blake Harcourt - Blakeharcourt@hotmail.com
#
# Created:     24/10/2017
# Copyright:   (c) Blake Harcourt 2017
# Licence:     See attached License text file.
#-------------------------------------------------------------------------------
# Instructions:
# 1. Open the 'Building_Animation.cej' scene.
# 2. Run this python script.
# 3. Press the 'start' button that will appear in a UI box.
# 4. Script will automatically select the one building in the scene and start animating.
# 5. To stop animating close the UI box.
#-------------------------------------------------------------------------------
# Notes:
# 1. This script is currently set up to only work with one building at a time.
# 2. It reads a shape attribute called "Animate" which must be set to true.
#-------------------------------------------------------------------------------
'''

#IMPORTS
try:
    from scripting import *
    from math import *
    from java.awt import *
    from java.awt.event import  *
    import threading
    import time
    import profile
    import random
    raise Exception('Import', 'Import Errors:')
except Exception, inst:
    print type(inst)
    print inst.args
    print inst   


#VARIABLES ----------------------------------------------------------------------------------
ce = CE()               # get a CityEngine instance
Buildings = []          #A list of all buildings animated in the scene
Animate = False         #Is the program currently animating
Run = ""                #An Animation Thread

#WINDOW LISTENER ---------------------------------------------------------------------------
class Listener(WindowAdapter):
    
    #On window closed - stops the animation thread
    def windowClosing(self, e):
        global Animate
        print("Closing window") 
        Animate = False
        e.getSource().dispose()
        
    #On window deactivated - restores focus to the UI window
    def windowDeactivated(self, e):
        e.getSource().setAlwaysOnTop(False);
        e.getSource().setAlwaysOnTop(True);
        print("focus lost");

#ANIMATION -------------------------------------------------------------------------------

#Changes an objects attributes given an object, rule and a value(amount)
def Attribute_Changer(Object,Rule, Amount):
    ce.setAttribute(Object, Rule, Amount) 

#Animation loop
def Animation_Update_Loop():
    global Run
    global Animate
    global threads

    #Repeat the animation loop every 0.1 seconds
    Run = threading.Timer(0.1, Animation_Update_Loop)
    if (Animate == True):
        Run.start()
     
     #Loop through all buildings and change their values
    for C in Buildings:    
        
        #Get the rotations for the current building
        Rotate_1 = ce.getAttribute(C, '/ce/rule/Rotate_1')
        Rotate_2 = ce.getAttribute(C, '/ce/rule/Rotate_2')
        Rotate_3 = ce.getAttribute(C, '/ce/rule/Rotate_3')
        Rotate_4 = ce.getAttribute(C, '/ce/rule/Rotate_4')
        Rotate_5 = ce.getAttribute(C, '/ce/rule/Rotate_5')
        
        #Change the rotations
        NewRotate_1 = Rotate_1 + 1
        NewRotate_2 = Rotate_2 - 2
        NewRotate_3 = Rotate_3 + 2
        NewRotate_4 = Rotate_4 - 2
        NewRotate_5 = Rotate_5 + 2
        
        #Start the rotation threads for each of the values - Any move, rotate, scale, regenerate commands should be moved to a seperate thread to avoid blocking UI
        t1 = threading.Thread(target = Attribute_Changer, args = (C, '/ce/rule/Rotate_1',NewRotate_1 ))
        t1.start()
        
        t1 = threading.Thread(target = Attribute_Changer, args = (C, '/ce/rule/Rotate_2',NewRotate_2 ))
        t1.start() 
              
        t1 = threading.Thread(target = Attribute_Changer, args = (C, '/ce/rule/Rotate_3',NewRotate_3 ))
        t1.start()   
          
        t1 = threading.Thread(target = Attribute_Changer, args = (C, '/ce/rule/Rotate_4',NewRotate_4 ))
        t1.start()   
          
        t1 = threading.Thread(target = Attribute_Changer, args = (C, '/ce/rule/Rotate_5',NewRotate_5 ))
        t1.start()   
        

#Selects objects by an attribute and a value, returns list of objects
def selectByAttribute(attr, value):
    objects = ce.getObjectsFrom(ce.scene)
    selection = []
    for o in objects:
        attrvalue = ce.getAttribute(o, attr)
        if attrvalue  ==  value:
            selection.append(o)
        
    ce.setSelection(selection)
    return selection

#On start button pressed
def Start(event):
    global Buildings
    global Run
    global Animate
    
    print("Starting the animation thread")
    Animate = True #SET TO TRUE HERE OR ANIMATION WILL NEVER START
    Run = threading.Timer(1.0, Animation_Update_Loop)   #Starts the animation loop 1 second after button has been pressed
    Run.start()
    
    #Get building objects with an attribute called 'Animate' set to True
    print("Getting building object")
    MyLot = selectByAttribute("Animate",True)
    for M in MyLot:
        Buildings.append(M)
    
    print("Animation engine running...")

#DIALOG --------------------------------------------------------------------------------
class DiaButton(Button):
    dialog = None
    tfield = None

def dialog():
    frame = Frame("BuildingFrame")
    frame.setAlwaysOnTop(True);
    dia = Dialog(frame, "Building Animator", False)
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