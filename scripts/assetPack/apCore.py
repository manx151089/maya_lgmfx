import maya.cmds as cmds
import maya.OpenMaya as om
import json
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
    keys = dict.keys()
    if 'referenceFile' in keys:
        if dict['referenceFile'] is not '':
            rFile=dict['referenceFile']
        else:
            print('blank reference file')
    else:
        print("No reference file found")
    transform = [0,0,0]
    rotation = [0,0,0]
    scale = [1,1,1]
    if "rotation" in keys:
        rotation = dict['rotation']
    if "transform" in keys:
        transform = dict['transform']
    if "scale" in keys:
        scale =dict['scale']
    cpn = createCustomPointNode(referenceFile=rFile,transform=transform,rotation=rotation,scale=scale)
    return cpn


def jsonFileToDict(filepath):
    """
    Converts a JSON file to a Python dictionary.
    Args:
        filepath (str): Path to the JSON file.
    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    try:
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            return data
    except:
        print("Error: File  not found.")
        return None
    

def unpackSelectedAssetPacks():
    """placeholder pseudo code"""
    pass

def loadAssetPack(filepath):
    myDict = jsonFileToDict(filepath)
    print(myDict)
    createCustomPointNodeFromDict(dict=myDict)
import glob
fp = 'D:/Tools/maya/maya_lgmfx/examples/json/assetPack_example.json'    
a=glob.glob(fp)
print(a)
loadAssetPack(filepath=fp)
#need to fix rename bug