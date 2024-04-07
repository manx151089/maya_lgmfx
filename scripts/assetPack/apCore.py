import maya.cmds as cmds
import maya.OpenMaya as om

def createCustomPointNode(referenceFile="",transform=[0,0,0],rotation=[0,0,0],scale=[1,1,1]):
    cpn = cmds.createNode('customPointNode')
    print(cpn)
    cmds.setAttr(cpn+'.referenceFile',referenceFile,type="string")
    cmds.setAttr(cpn+'.transform',transform[0],transform[1],transform[2])
    cmds.setAttr(cpn+'.scale',scale[0],scale[1],scale[2])
    cmds.setAttr(cpn+'.rotation',rotation[0],rotation[1],rotation[2])
    if referenceFile is not "":
        name = referenceFile.split('/')[-1].split('_V')[0]
        cmds.rename(cpn,name)
    return cpn
def createCustomPointNodeFromDict(dict={}):
    rFile="D:/test/assetPack_dept_element_V001.abc"
    if 'referenceFile' in dict.keys():
        if dict['referenceFile'] is not '':
            rFile=dict['referenceFile']
        else:
            print('blank reference file')
    else:
        print("No reference file found")
    cpn = createCustomPointNode(referenceFile=rFile)
    return cpn
def unpackSelectedAssetPacks():
    pass
createCustomPointNodeFromDict()