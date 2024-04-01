from bams_client import BamsClient
from bams_client.filters import Filters
from pathresolver import bpm
import maya.mel as mel
# This creates your client object to work with.
#bc = BamsClient()
# Once you have this you can start to operate on the database..
#filter_cls = Filters()

#x=path_manager.templates_from_path('/projects/pony/prod/ldCrowd/')
gmoDict={}
from pymel.core import *
def filterRefresh():
    import glob
    filtName=cmds.textFieldGrp(myFilt,q=True,text=True)
    print ">>",filtName
    searchString="/projects/pony/prod/ldCrowd/*/tasks/crowd/maya/"+filtName+".gmo"
    x=glob.glob(searchString)
    print x
    global gmoDict
    gmoDict={}
    cmds.textScrollList(gmos,e=True,ra=True)
    for each in x:
        
        key=each.split("/")[-1]
        gmoDict[key]=each
        cmds.textScrollList(gmos,e=True,append=each.split("/")[-1])
    #return gmoDict
        
def addClip():
    val=cmds.textFieldGrp(gmofilepath,q=True,text=True)        
    mel.eval('glmMotionClipCmd;')
    node=cmds.ls(sl=True)
    print node
    print node[0],val
    setAttr(node[0]+".motionFile",val,type="string")

names=os.listdir("/projects/pony/prod/ldCrowd/")

def updategmofile():
    a=cmds.textScrollList(gmos,q=True,selectItem=True)
    global gmoDict
    #print a,gmoDict
    #print gmoDict.get(a[0])
    cmds.textFieldGrp(gmofilepath,e=True,text=gmoDict.get(a[0]))

    

cmds.window("gmoLister",title="gmo Lister")
clm1=cmds.columnLayout()
myFilt=cmds.textFieldGrp(parent=clm1, label='filter', text='type filter to get started',cc="filterRefresh()" )

gmos=cmds.textScrollList(parent=clm1, numberOfRows=8, allowMultiSelection=True,
                        append=names,
                        showIndexedItem=4,
                        sc="updategmofile()" )
                        
gmofilepath=cmds.textFieldGrp(parent=clm1, label='gmofile', text='Editable',cc="" )
cmds.button(parent=clm1,label="oye",c="addClip()")
cmds.showWindow()
#addClip()
print gmoDict
