'''
#-------------------------------------------------------------------------------
# Name:        Traffic_Animator.py
# Purpose:     Animates cars along road segments
#
# Author:      Blake Harcourt - Blakeharcourt@hotmail.com
#
# Created:     24/10/2017
# Copyright:   (c) Blake Harcourt 2017
# Licence:     See attached License text file.
#-------------------------------------------------------------------------------
# Instructions:
# 1. Open the "Traffic_Animation.cej" scene
# 2. Run this python script to display the Car Anim UI panel. 
# 3. A UI box with a "start" button will appear on the screen. Note: Python can sometimes take a while to start the first time using it.
# 4. Select a node on a road segment
# 5. Press start, the python console will display "Animation engine ready..." when it's ready for traffic to be added
# 6. Press "Add Car" button to add a car on the road.
# 7. Cars will automatically start moving and rotating along the road.
# 8. Press "Add Car" button to continue adding cars.
# 9. To stop animating cars simply close the Car Anim UI panel.
#-------------------------------------------------------------------------------
# Notes:
# 1. All cars are added to a 'Vehicles' layer
# 2. Too many cars will slow down the animation system considerably
# 3. Roads must be straight segments - Cannot currently follow curves
# 4. Roads must be flat - Cannot current follow height changes if curved
# 5. There is no type of collision detection between cars
# 6. Only run one instance of this script at a time
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
    raise Exception('Import', 'Import')
except Exception, inst:
    print type(inst)
    print inst.args
    print inst   

# get a CityEngine instance
ce = CE()


Cars = []               #A list of all cars added in the scene
Animate = False         #Is the program currently animating
Run = ""                #An Animation Thread
V_Layer = None          #The Vehicle layer


#Animation loop to move cars
def Car_Update_Loop():
    global Run
    global Animate
    global threads
    
    #Rerun the loop every 0.01 seconds
    Run = threading.Timer(0.01, Car_Update_Loop)
    if (Animate == True):
        Run.start()
        #profile.runctx('map(lambda C: C.Update_Self(), Cars)', globals(), locals()) - Uncomment to profile Update_Self function
        map(lambda C: C.Update_Self(), Cars)

#Listener for window close and focus
class Listener(WindowAdapter):
    
    #Stops animation if the window is closed
    def windowClosing(self, e):
        global Animate
        print("Closing window") 
        Animate = False
        e.getSource().dispose()
        
    #Makes the UI window always on top
    def windowDeactivated(self, e):
            e.getSource().setAlwaysOnTop(False);
            e.getSource().setAlwaysOnTop(True);
            print("focus lost");
    
#On start pressed
def Start(event):
    global Cars
    global Run
    global Animate
    global V_Layer
    
    print("Starting the animation thread")
    Animate = True #SET TO TRUE HERE OR ANIMATION WILL NEVER START
    Run = threading.Timer(1.0, Car_Update_Loop)
    Run.start()
    
    #Get Selected Start Node
    print("Getting Start Node")
    StartNode = getObjectsFrom(ce.selection(), ce.isGraphNode)[0]
    print(StartNode)
    
    print("Creating new vehicles layer")
    V_Layer = ce.addStaticModelLayer('Vehicles')    #Tried a few different methods of animation, and static model layers gave the best results for more than 1 vehicle animating

    print("Animation engine ready...")

#Creates a new car instance and adds to scene
def AddAnotherCarThread():
    
    #Get the selected node
    StartNode = getObjectsFrom(ce.selection(), ce.isGraphNode)[0]
    print("Attempting car creation")

    #Create a new car
    v = Anim_Car(StartNode)
    Cars.append(v)  #Add to the cars list
    
    #Reselects the original node
    ce.setSelection(StartNode)

#On add car pressed
def AddAnotherCar(event):
    t = threading.Thread(target=AddAnotherCarThread)
    t.start()

#HELPER FUNCTIONS ------------------------------------------------------------------
#Returns a list of segments from a node ID  (OID)
def Get_Touching_Segments_From_Node_ID(NOD_ID):
    Node = ce.findByOID(NOD_ID)
    segments = ce.getObjectsFrom(Node, ce.isGraphSegment)
    return segments

#Returns a list of segments from a node
def Get_Touching_Segments_From_Node(Node):
    segments = ce.getObjectsFrom(Node, ce.isGraphSegment)
    return segments

#Returns a list of nodes on a segment from a segment ID (OID)
def Get_Nodes_From_Segment_ID(SEG_ID):
    Segment = ce.findByOID(SEG_ID)
    Nodes = ce.getObjectsFrom(Segment, ce.isGraphNode)
    return Nodes

#Unused: Easy print for an array - Useful for console print statements
def Print_Array(Array):
    i = 0
    for A in Array:
        print(str(i) + ": " + ce.getOID(A))
        i = i + 1
 
#Unused: Stops all car animations     
def Stop_Everything():
     global Animate
     Animate = False
     
#Given a list of objects, it returns a random selection
def ReturnRandomFromList(ListOfObjects):
    random_index = random.randrange(0,len(ListOfObjects))
    SelectedObj = ListOfObjects[random_index]
    return SelectedObj

#Given a list of segments, it removes the current segment and returns the remaining - Used for choosing the next segment if more then 1 option available
def ReturnRandomSegmentFromList(Car, ListOfObjects):
    X = ListOfObjects
    for o in ListOfObjects:
        if (ce.getOID(o) == ce.getOID(Car.CurrentSegment)):
            X.remove(o)    
    random_index = random.randrange(0,len(X))
    SelectedObj = X[random_index]
    return SelectedObj

#VECTOR FUNCTIONS ------------------------------------------------------------------
#Subtracts two vectors [X,Y,Z] - returns vector
def SubtractTwoVectors(Vec1, Vec2): 
     R1 = Vec1[0] - Vec2[0]
     R2 = Vec1[1] - Vec2[1]
     R3 = Vec1[2] - Vec2[2]
     NewArray = [R1, R2, R3]
     return NewArray
 
 #Adds two vectors [X,Y,Z] - returns vector
def AddTwoVectors(Vec1, Vec2): 
     R1 = Vec1[0] + Vec2[0]
     R2 = Vec1[1] + Vec2[1]
     R3 = Vec1[2] + Vec2[2]
     NewArray = [R1,R2,R3]
     return NewArray
   
#Divides a vector [X,Y,Z] by a value - returns vector
def DivideAVector(Vec1, Value):
     R1 = Vec1[0] / Value
     R2 = Vec1[1] / Value
     R3 = Vec1[2] / Value
     NewArray = [R1,R2,R3]
     return NewArray     
    
#Multiplies a vector [X,Y,Z] by a value - returns vector 
def MultiplyAVector(Vec1, Value):
     R1 = Vec1[0] * Value
     R2 = Vec1[1] * Value
     R3 = Vec1[2] * Value
     NewArray = [R1,R2,R3]
     return NewArray    
 
#Calculates the magnitude of a vector [X,Y,Z] - returns value
def CalculateMagnitude(Vec):
    Mag = (Vec[0] * Vec[0]) + (Vec[1] * Vec[1]) + (Vec[2] * Vec[2])
    SquareRoot = sqrt(Mag)
    return SquareRoot

#CAR FUNCTIONS ------------------------------------------------------------------

#Moves a given object to a position
def func1(Car,Pos):
    ce.move(Car, Pos)

#Rotates a given object by an amount
def func2(Car,Rot):
    ce.rotate(Car, Rot)








#ANIMATED CAR CLASS ------------------------------------------------
class Anim_Car:
    
    def __init__(self, Starting_Node):
        self.CurrentNode = Starting_Node    #The node the car started on
        self.CurrentSegment = None  #The current road segment the car is on
        self.NextNode = None    #The node the car is targeting
        self.speed = 1      #The speed of the car
        self.MyShape = None #The current CE shape the car belongs to
        self.Rotation = 0   #Starting rotation at 0
        self.Ready = True   #Is the car animation state ready to change
        
        #Cached Variables - These are reset only when a new node is reached
        #Caching these variables was done to avoid using CE 'get' methods every frame
        self.CachedCurrentNode = None   #The position of the starting node
        self.CachedNextNode = None  #The position of the target node
        self.CachedCurrentPos = None    #The cars current position
        
        #Create Shape - Import the DAE car object
        settings = DAEImportSettings()
        settings.setScale(0.5)
        settings.setOffset([0,0,0])
        Layer = ce.importFile(ce.toFSPath("models/Blue Car.dae"), settings) 

        #Get the car from the street layer
        streetlayer = ce.getObjectsFrom(ce.scene, ce.isStaticModelLayer, ce.withName("'Blue Car'"))[0]
        A = ce.getObjectsFrom(streetlayer, ce.isShape, ce.withName("'Blue Car.dae'"))[0]

        #Copy it and delete the original
        l = ce.copy ( A, True, V_Layer )[0]

        #Delete the original layer
        ce.delete(streetlayer)

        #Get the object
        oid = ce.getOID( l )
        object = ce.findByOID(oid)
        self.MyShape = object

        #Set starting positions and starting info
        self.Set_Pos_From_Node(Starting_Node)
        self.Get_Starting_Segment(Starting_Node)
        
        #Cache the data
        self.CachedCurrentPos = ce.getPosition(self.MyShape)
        self.CachedCurrentNode = ce.getPosition(self.CurrentNode)
        self.CachedNextNode = ce.getPosition(self.NextNode)
        
        print("Car creation finished")
        

    #Update function to move and rotate the car
    def Update_Self(self):
        if (self.IsReady() == True):     
            start = time.time()   
               
            #profile.runctx('self.Move_Car()', globals(), locals())     -Uncomment to profile Move_Cars function
            self.Move_Car()
            self.Rotate_Car()  
            
    #Is the car ready to be moved again - movement/rotation animation has finished             
    def IsReady(self):
        return self.Ready    

    #Unused - Sets the car to a position of 0,0,1000          
    def New_Pos(self):
        position = [0,0,1000]
        ce.setPosition(self.MyShape, position)
        
    #Gets a new segment OID given a Node
    def Get_Starting_Segment(self, Node):
        
        print("Get segment from node")
        segments = ce.getObjectsFrom(Node, ce.isGraphSegment)
        
        print("Set current segment - just choose a random")
        self.CurrentSegment = ReturnRandomFromList(segments)

        OID = ce.getOID(self.CurrentNode)
        print(OID)
        
        #Get the next node that isnt the starting node as the destination - A segment can only have 2 nodes
        Nodes = ce.getObjectsFrom(self.CurrentSegment, ce.isGraphNode)
        if (Nodes[0] == self.CurrentNode):
            self.NextNode = Nodes[1]
        else:
            self.NextNode = Nodes[0]
            
    #Sets the car position to a node position
    def Set_Pos_From_Node(self, Node):
        Verts = ce.getVertices(Node)
        ce.setPosition(self.MyShape, Verts)        
        
    #Returns a nodes position vector [X,Y,Z]
    def Get_Pos_From_Node(self, Node):
        Verts = ce.getVertices(Node)   
        return Verts
        
    #Set the position of an object to a vector [X,Y,Z]
    def Set_Pos(self, PositionArray):
       position = [PositionArray[0],PositionArray[1],PositionArray[2]]
       ce.setPosition(self.MyShape, position)   
   
    #Runs the moveTowards function and then sends a translate vector to a threaded function
    def Move_Car(self):   
        self.Ready = False  #Car is currently being moved so turn ready to false
        self.speed = 20     #Generic speed chosen for car

        #Get the current position
        OriginalPos = self.CachedCurrentPos

        #New Movement Function - Needs to be in a thread
        self.CachedCurrentPos = self.MoveTowards(self.CachedCurrentPos, self.CachedNextNode, 0.01*self.speed)
        
        #Move the shape (Is move quicker than set position ?)    
        X = OriginalPos[0] - self.CachedCurrentPos[0]
        Y = OriginalPos[1] - self.CachedCurrentPos[1]
        Z = OriginalPos[2] - self.CachedCurrentPos[2]
        
        #Create a translate vector
        t = [-X,Y,-Z]
        
        #Start a thread to move the car
        t1 = threading.Thread(target = func1, args = (self.MyShape, t))
        t1.start()       
        
    #Rotates the car to face the next node    
    def Rotate_Car(self):

        #Calculate the rotation between Starting Node and Finish Node
        Node1 = self.CachedCurrentNode
        Node2 = self.CachedNextNode

        #Calculate Distance
        Dist = sqrt(((Node2[2] - Node1[2])**2) + ((Node2[0] - Node1[0])**2))
        
        #Calcualte deltas DX DY
        DX = (Node2[0] - Node1[0])
        DY = (Node2[2] - Node1[2])            

        #Calculate Bearing
        myradians = atan2(DY, DX)
        mydegrees = (degrees(myradians) + 180)%360
        
        #Difference Between Current Bearing and Desired Bearing
        Difference = self.Rotation - mydegrees
        self.Rotation = mydegrees

        #Rotate the car in a thread if difference between current and desired angle is greater than 0
        if (Difference != 0):
            r = [0,Difference,0]
            #ce.rotate(self.MyShape, r)
            t1 = threading.Thread(target = func2, args = (self.MyShape, r))
            t1.start()
        self.Ready = True   #Car has finished moving and rotating and is now ready to be updated next frame
        
    # Moves the car at the same constant speed towards a node, if it reaches the target node, it switches to a new node   
    def MoveTowards(self, CurrentVec, TargetVec, MaxDistDelta):

        a = SubtractTwoVectors(TargetVec, CurrentVec)
        magnitude = CalculateMagnitude(a)
        
        #AT TARGET POINT
        if (magnitude <= MaxDistDelta or magnitude == 0):
            
         #Get the new segment
         TouchingSegments = Get_Touching_Segments_From_Node(self.NextNode)
         
         #Remove the current segment from the list
         self.CurrentSegment = ReturnRandomSegmentFromList(self, TouchingSegments)

         #Set the current node to the next node
         self.CurrentNode = self.NextNode
 
         #Get the next node that isnt the starting node as the destination - A segment can only have 2 nodes
         Nodes = ce.getObjectsFrom(self.CurrentSegment, ce.isGraphNode)
         if (ce.getOID(Nodes[0]) == ce.getOID(self.CurrentNode)):
            self.NextNode = Nodes[1]
         else:
            self.NextNode = Nodes[0]        
         
         #Cache the new positions
         self.CachedCurrentNode = self.Get_Pos_From_Node(self.CurrentNode)
         self.CachedNextNode = self.Get_Pos_From_Node(self.NextNode)
         
         return TargetVec
        else:
            return AddTwoVectors(CurrentVec, MultiplyAVector(DivideAVector(a,magnitude),MaxDistDelta))
        
    #Updates the attributes of a car object - currently unused as was very slow to update attributes
    def UpdateAttributes(self):
        ce.setAttribute(self.MyShape, 'Current_Node', self.CurrentNode)    
        ce.setAttribute(self.MyShape, 'Current_Segment', self.CurrentSegment)  
        ce.setAttribute(self.MyShape, 'Next_Node', self.NextNode)  
        ce.setAttribute(self.MyShape, 'Speed', self.speed)  
        ce.setAttribute(self.MyShape, 'Rotation', self.Rotation)  

#DIALOG --------------------------------------------------------------------------------
class DiaButton(Button):
    dialog = None
    tfield = None

def dialog():
    frame = Frame("MeasureFrame")
    frame.setAlwaysOnTop(True);
    dia = Dialog(frame, "Traffic Animator", False)
    dia.setSize(550,500)

    l = Listener()
    dia.addWindowListener(l)

    b1 = DiaButton("Start", actionPerformed=Start)
    dia.add(b1)

    b3 = DiaButton("Add Car", actionPerformed=AddAnotherCar)
    dia.add(b3)
    b3.dialog = dia
    
    layout = GridLayout(5,2)
    dia.setLayout(layout)
    dia.pack()
    dia.show()
    
try:   
     dialog()
except Exception, inst:
    print type(inst)
    print inst.args
    print inst           
        
        
        
        
        
        
        
        
        
        
        
        
        