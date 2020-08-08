from shelfBase import _shelf
import maya.cmds as mc

#Test function
class customShelf(_shelf):
    def build(self):
        self.addButon(label="Pipeman")
        self.addButon(label="Update", command="import update;update.onMayaDroppedPythonFile(None)")
        
#customShelf()