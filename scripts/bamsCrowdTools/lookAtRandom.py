


from glm.Qtpy.Qt import QtWidgets
try:
   app = QtWidgets.QApplication([])
except:
   app = None
def getSelected():
    cp=cmds.ls(sl=True,o=True,s=True)
    #cpSh=cmds.listRelatives(cp[0],shapes=True)
    #a=cmds.ls(a,s=True)
    print ("shapeNodeName>>>",(cp[0]))
    selectedEntity=cmds.glmLayoutTool(cp=str(cp[0]),gse=True)
    print type(selectedEntity)
    return str(selectedEntity)
    
from glm.layout.layout import *

myEntity=getSelected()
filePaths = list()

from maya_crowd.entities import *
def lookAtRandomiser(tp_keyValue_x=100.0,tp_keyValue_y=60.0,tp_keyValue_z=30.0,tpn_keyValue_x=175.0,tpn_keyValue_y=0,tpn_keyValue_z=175.0,offset=30,frameOffsetRandom=30):
    selected_entity=getSelected()
    print ("success")
    print ("imported>>",selected_entity)
    selnode=cmds.ls(sl=True,o=True,s=True)[0]
    print selnode
    if(selnode is not None):    
        cp=CacheProxyNode(selnode)
        filePaths.append(cp.layout_file)
        
        for filePath in filePaths:
            fileHandle = openLayoutFile(filePath)
            print "layoutFile{}".format(filePath)
            if (fileHandle is not None):
                rootId = getRootId(fileHandle)
                
                previousRootNode = getNodeById(fileHandle, rootId)
            
                # create a selector, linked after root and automatically set as root instead
                createSelectorNode = createSelector(fileHandle, selected_entity, previousRootNode)
            
                
                lookatOperatorNode = createOperator(fileHandle, "LookAt", createSelectorNode)
                a=list()
                keyFrames=[[]]
                keyValues=[[]]
                lis=listNodeAttributes(lookatOperatorNode,a)
                nodeAttr=setNodeAttribute(lookatOperatorNode, 'boneName',keyFrames,[u'cwd_neck_C_head']) # takes an empty attributeNameList list() and feed it, or return False
                time=cmds.currentTime( query=True )
                
                keyFrames=[]
                keyValues=[[[tp_keyValue_x,tp_keyValue_y,tp_keyValue_z]]]
                nodeAttr=setNodeAttribute(lookatOperatorNode, 'targetPosition',keyFrames,keyValues) 
                keyFrames=[]
                keyValues=[[[tpn_keyValue_x,tpn_keyValue_y,tpn_keyValue_z]]]
                nodeAttr=setNodeAttribute(lookatOperatorNode, 'targetPositionNoise',keyFrames,keyValues) 
                keyFrames=[time-offset,time,time+offset]
                keyValues=[[0.0],[1.0],[0.0]]
                nodeAttr=setNodeAttribute(lookatOperatorNode, 'weight',keyFrames,keyValues)
                keyFrames=[]
                keyValues=[[frameOffsetRandom]]
                nodeAttr=setNodeAttribute(lookatOperatorNode, 'weightFramesNoise',keyFrames,keyValues)
                print lis,a
                print "/n",time,nodeAttr,keyFrames,keyValues
                #getNodeAttribute(operatorNode, attributeName, keyFrames, keyValues) # returns None on error
                #setNodeAttribute(operatorNode, attributeName, keyFrames, keyValues)#
            
main_window = cmds.loadUI(uiFile = "/projects/pony/prod/ldCrowd/ldCrowd_s0010/tasks/crowd/maya/scripts/ui/lookAtUi.ui")
cmds.showWindow(main_window)

def uiLookAtRandom():
    tp_keyValue_x = float(cmds.textField("direction_x", query=True, text=True))
    tp_keyValue_y = float(cmds.textField("direction_y", query=True, text=True))
    tp_keyValue_z = float(cmds.textField("direction_z", query=True, text=True))
    tpn_keyValue_x = float(cmds.textField("noise_x", query=True, text=True))
    tpn_keyValue_y = float(cmds.textField("noise_y", query=True, text=True))
    tpn_keyValue_z = float(cmds.textField("noise_z", query=True, text=True))
    offset = int(cmds.textField("frameLength", query=True, text=True))
    frameOffsetRandom = int(cmds.textField("frameOffsetRandom", query=True, text=True))
    
    lookAtRandomiser(tp_keyValue_x,tp_keyValue_y,tp_keyValue_z,tpn_keyValue_x,tpn_keyValue_y,tpn_keyValue_z,offset)
    print tp_keyValue_x,tp_keyValue_y,tp_keyValue_z,tpn_keyValue_x,tpn_keyValue_y,tpn_keyValue_z,offset,frameOffsetRandom
    