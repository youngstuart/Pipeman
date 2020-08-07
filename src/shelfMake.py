from shelfBase import _shelf
import maya.cmds as mc

#Test function
class customShelf(_shelf):
    def build(self):
        self.addButon(label="button1")
        self.addButon("button2")
        self.addButon("popup")
        p = mc.popupMenu(b=1)
        self.addMenuItem(p, "popupMenuItem1")
        self.addMenuItem(p, "popupMenuItem2")
        sub = self.addSubMenu(p, "subMenuLevel1")
        self.addMenuItem(sub, "subMenuLevel1Item1")
        sub2 = self.addSubMenu(sub, "subMenuLevel2")
        self.addMenuItem(sub2, "subMenuLevel2Item1")
        self.addMenuItem(sub2, "subMenuLevel2Item2")
        self.addMenuItem(sub, "subMenuLevel1Item2")
        self.addMenuItem(p, "popupMenuItem3")
        self.addButon("button3")
customShelf()