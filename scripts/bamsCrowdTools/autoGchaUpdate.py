from context_manager import Context
import os.path
from os import path

ctx = Context.from_environment()

maya_folder=ctx.path+"/maya/"
sfile=cmds.file(sn=True,shn=True,query=True).split(".")[0]

gcha=maya_folder+sfile+".gcha"
checkGcha="Gcha Exists:{}".format(path.exists(gcha))

gcgpath=maya_folder+sfile+".gcg"
"""fbxpath=maya_folder+sfile+".fbx"

def exportFbx(charFile="",fbxFile=""):
    if(checkGcha=="Gcha Exists:True"):
        print checkGcha
        if(charFile=="")and(fbxFile==""):
            cmds.glmExportCharacterGeometry(cf=gcha, fbx=fbxpath)
        else:
            cmds.glmExportCharacterGeometry(cf=charFile, fbx=fbxFile)
            
        return fbxpath
    else:
        print ("Please save scene and gcha in maya folder with same naming.\nFor example {}.mb will be {}.gcha".format(sfile,sfile))
#exportFbx(charFile="",fbxFile="")

fbxpath=maya_folder+sfile+".fbx"

def openFbx(fbxpath=""):    
    cmds.file(fbxpath,open=True,f=True)
    cfFbx=sfile
    #cmds.glmExportCharacter(cf="c:/temp/example.gcha", rjn="cwd_root_C")
#openFbx(fbxpath=fbxpath)
"""
mesh=cmds.ls("msh*",v=True)
#print mesh
gchaBlendFix2=str(maya_folder+sfile+"blendFix.gcha")
#print type(str(gcha))
#print type(gchaBlendFix)
def deleteGeo(inputFile="",outputFile=""):
    cmds.glmCharacterMaker(script=True,file=str(gcha),usk=["cwd_root_C",2,0],outputFile=gchaBlendFix)
    geoNodes=cmds.glmCharacterMaker(script=True,file=gchaBlendFix,listGeoNodes=True)
    deleteNodes=geoNodes[2:]
    if(inputFile==""):
        pass
    else:
        gcha=inputFile
    if(outputFile==""):
        pass
    else:
        gchaBlendFix2=outputFile
    print deleteNodes
    for each in deleteNodes:
        if(each.split("_")[0]=="msh"):
            delNode=cmds.glmCharacterMaker(script=True,file=gcha,removeGeoNode=["MeshAssetNode",str(each)],outputFile=gcha)
            #print delNode
        if(each.split("_")[0]=="animShaderGroup"):
            delNode=cmds.glmCharacterMaker(script=True,file=gcha,removeGeoNode=["ShadingGroupNode",str(each)],outputFile=gcha)
            #print delNode
        if(each.split("_")[0]=="animShader"):
            delNode=cmds.glmCharacterMaker(script=True,file=gcha,removeGeoNode=["ShadingGroupNode",str(each)],outputFile=gcha)
            #print delNode
        
        
    geoNodes=cmds.glmCharacterMaker(script=True,file=gcha,listGeoNodes=True)
    deleteNodes=geoNodes[2:]
    print "nodesLeftToDel>",deleteNodes
deleteGeo(inputFile=gcha,outputFile=gcha)


def updateGeoFromMeshes(inputFile="",outputFile=""): 
    if(inputFile==""):
        pass
    else:
        gchaBlendFix=inputFile
    if(outputFile==""):
        pass
    else:
        gchaBlendFix2=outputFile       
    gchaBlendFix2=str(maya_folder+sfile+"_blendFix2.gcha")    
    geoList=cmds.ls("msh*",v=True,et='transform')
    print sfile
    geoNodes=cmds.glmCharacterMaker(script=True,file=gchaBlendFix,listGeoNodes=True)
    print geoNodes[1]
    i=0
    for each in geoList:
        if(i==0):
            a=cmds.glmCharacterMaker(script=True,file=gchaBlendFix,addGeometry=["AssetGroupNode",geoNodes[1],each],outputFile=gchaBlendFix2)
        if(i>0):
            a=cmds.glmCharacterMaker(script=True,file=gchaBlendFix2,addGeometry=["AssetGroupNode",geoNodes[1],each],outputFile=gchaBlendFix2)
        i+=1
    #xx=cmds.glmCharacterMaker(script=True,file=gchaBlendFix,addGeometry=["AssetGroupNode","var_b","msh_body_C"],outputFile=gchaBlendFix2)
    #print ">>",xx
    geoNodes=cmds.glmCharacterMaker(script=True,file=gchaBlendFix2,listGeoNodes=True)
    print ">>>>",geoNodes
updateGeoFromMeshes(inputFile=gcha,outputFile=gcha)