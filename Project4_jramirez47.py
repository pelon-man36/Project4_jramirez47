from direct.showbase.ShowBase import ShowBase
import SpaceJamClasses as spaceJamClasses
import DefensePaths as defensePaths
from panda3d.core import *
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
import CollideObjectBase as collideObjectBase
import sys

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setScene()
        fullCycle = 60

        for j in range(fullCycle):
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.Station, nickName, j, fullCycle, 2)

        self.circleX = defensePaths.createCircleX(self)
        self.circleZ = defensePaths.createCircleZ(self)
        self.circleY = defensePaths.createCircleY(self)

        self.setCamera()
        self.setKeyBindings()


        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
    
        #self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
        #self.cTrav.addCollider(self.Player.collisionNode, self.pusher)
        #self.showCollisions()
        self.cTrav.showCollisions(self.render)


    def setScene(self):
        self.Player = spaceJamClasses.Player(self.loader, "./Assets/Spaceships/ship.obj", self.render,
            "Player", "./Assets/Spaceships/ship_TEX.tga", (0, 400, 0), (180, 0, 0), 5)

        self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render,
            "Universe", "./Assets/Universe/Universe.jpg", (0, 0, 0), 15000)

        self.Planet1 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet1", "./Assets/Planets/Planet1.jpg", (-1500, 5000, 350), 100)

        self.Planet2 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet2", "./Assets/Planets/Planet2.png", (4000, 3000, 400), 100)

        self.Planet3 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet3", "./Assets/Planets/Planet3.png", (-4000, -2000, -400), 100)

        self.Planet4 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet4", "./Assets/Planets/Planet4.png", (-2000, 1000, 450), 100)

        self.Planet5 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet5", "./Assets/Planets/Planet5.png", (0, 0, 5000), 100)

        self.Planet6 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render,
            "Planet6", "./Assets/Planets/Planet6.png", (2000, 6000, 0), 100)

        self.Station = spaceJamClasses.SpaceStation(self.loader, "./Assets/Space_Station/SpaceStation1B/spaceStation.egg",
            self.render, "SpaceStation", (5000, 4000, 70), 50)
        

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Spaceships/DroneDefender/DroneDefender.obj",
            self.render, droneName, "./Assets/Spaceships/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Spaceships/DroneDefender/DroneDefender.obj",
            self.render, droneName, "./Assets/Spaceships/DroneDefender/octotoad1_auv.png", position, 10)

    def setCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Player.modelNode)
        self.camera.setFluidPos(0, 4, -30)
        self.camera.setHpr(180, 90, 0)

    def Upwards(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveUpwards, "upward-thrust")
        else:
            self.taskMgr.remove("upward-thrust")

    def Downwards(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveDownwards, "downward-thrust")
        else:
            self.taskMgr.remove("downward-thrust")

    def Forward(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveForward, "forward-thrust")
        else:
            self.taskMgr.remove("forward-thrust")

    def Backward(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveBackward, "backward-thrust")
        else:
            self.taskMgr.remove("backward-thrust")

    def Leftward(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveLeftward, "leftward-thrust")
        else:
            self.taskMgr.remove("leftward-thrust")

    def Rightward(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.MoveRightward, "rightward-thrust")
        else:
            self.taskMgr.remove("rightward-thrust")
    
    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, "left-turn")
        else:
            self.taskMgr.remove("left-turn")

    def RightTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, "right-turn")
        else:
            self.taskMgr.remove("right-turn")
    
    def MoveUpwards(self, task):
        rate = .5
        self.Player.modelNode.setP(self.Player.modelNode.getP() - rate)
        return task.cont

    def MoveDownwards(self, task):
        rate = .5
        self.Player.modelNode.setP(self.Player.modelNode.getP() + rate)
        return task.cont

    def MoveForward(self, task):
        speed = 5
        trajectory = self.render.getRelativeVector(self.Player.modelNode, Vec3.up())
        trajectory.normalize()
        self.Player.modelNode.setFluidPos(self.Player.modelNode.getPos() + trajectory * speed)
        return task.cont

    def MoveBackward(self, task):
        speed = 5
        trajectory = self.render.getRelativeVector(self.Player.modelNode, Vec3.up())
        trajectory.normalize()
        self.Player.modelNode.setFluidPos(self.Player.modelNode.getPos() - trajectory * speed)
        return task.cont

    def MoveLeftward(self, task):
        rate = .5
        self.Player.modelNode.setR(self.Player.modelNode.getR() + rate)
        return task.cont

    def MoveRightward(self, task):
        rate = .5
        self.Player.modelNode.setR(self.Player.modelNode.getR() - rate)
        return task.cont
    
    def ApplyLeftTurn(self, task):
        # half a degree every frame
        rate = .5
        self.Player.modelNode.setH(self.Player.modelNode.getH() - rate)
        return task.cont

    def ApplyRightTurn(self, task):
        # half a degree every frame
        rate = .5
        self.Player.modelNode.setH(self.Player.modelNode.getH() + rate)
        return task.cont

    def quit(self):
        sys.exit()
    
    def setKeyBindings(self):
        # key bindings for ship movement
        self.accept("escape", self.quit)
        self.accept("arrow_up", self.Upwards, [1])
        self.accept("arrow_up-up", self.Upwards, [0])
        self.accept("arrow_down", self.Downwards, [1])
        self.accept("arrow_down-up", self.Downwards, [0])
        self.accept("w", self.Forward, [1])
        self.accept("w-up", self.Forward, [0])
        self.accept("s", self.Backward, [1])
        self.accept("s-up", self.Backward, [0])
        self.accept("a", self.Leftward, [1])
        self.accept("a-up", self.Leftward, [0])
        self.accept("d", self.Rightward, [1])
        self.accept("d-up", self.Rightward, [0])
        self.accept("arrow_left", self.LeftTurn, [1])
        self.accept("arrow_left-up", self.LeftTurn, [0])
        self.accept("arrow_right", self.RightTurn, [1])
        self.accept("arrow_right-up", self.RightTurn, [0])







app = MyApp()
app.run()