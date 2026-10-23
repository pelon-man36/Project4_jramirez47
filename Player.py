from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task

class Player(SphereCollideObject):
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str,
            texPath: str, posVec: Vec3, posHpr: Vec3, scaleVec: float):
        super(Player, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 8)
        self.taskMgr = taskMgr
        self.accept = accept
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setHpr(posHpr)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

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
    
    def setKeyBindings(self):
        # key bindings for ship movement
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