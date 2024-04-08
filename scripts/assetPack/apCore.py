import maya.cmds as cmds
import maya.OpenMaya as om
import json
import os
import glob

def validateFilepath(filepath):
    """This will validate if there is a backslash in the filepath"""
    #brainstorm for more features here when free
    if '\\' in filepath:
        raise ValueError("Filepath contains a backslash!",filepath)
    print("filepath>>>",filepath)
    if os.path.exists(filepath) is False:
        raise Exception("File does not exist:",filepath)
    else:
        pass


def createCustomPointNode(referenceFile="",transform=[0,0,0],rotation=[0,0,0],scale=[1,1,1]):
    cpn = cmds.createNode('customPointNode')
    print(cpn)
    cmds.setAttr(cpn+'.referenceFile',referenceFile,type="string")
    cmds.setAttr(cpn+'.transform',transform[0],transform[1],transform[2])
    cmds.setAttr(cpn+'.scale',scale[0],scale[1],scale[2])
    cmds.setAttr(cpn+'.rotation',rotation[0],rotation[1],rotation[2])
    if referenceFile is not "":
        name = referenceFile.split('/')[-1].split('_V')[0]
        print(name)
        cmds.rename(cpn,name)
    return cpn


def createCustomPointNodeFromDict(dict={}):
    """
    creates an assetPack node
    """
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
    validateFilepath(rFile)#this will make rFile an compulsary requirement in every dict that you input
    cpn = createCustomPointNode(referenceFile=rFile,transform=transform,rotation=rotation,scale=scale)
    return cpn


def jsonFileToDict(filepath):
    """
    Converts a JSON file to a Python dictionary.
    """
    try:
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            return data
    except:
        print("Error: File  not found.")
        return None
    

def unpackSelectedAssetPacks():
    """placeholder pseudo code"""#brainstorm topic in next iteration
    pass


def loadAssetPack(filepath):
    myDict = jsonFileToDict(filepath)
    print(myDict)
    createCustomPointNodeFromDict(dict=myDict)


if __name__ == "__main__":
    #test
    fp = 'D:/Tools/maya/maya_lgmfx/examples/json/assetPack_example.json'
    validateFilepath(fp)
    a=glob.glob(fp)
    print(a)
    loadAssetPack(filepath=fp)
