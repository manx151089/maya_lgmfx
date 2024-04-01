import os, time, re
import maya.cmds as cmds
from functools import partial
from datetime import datetime
from maya_util.loaders import import_atom_curves 
from operator import itemgetter
import context_manager
import shot_api
#Global Var Animation Dictionary
Displayfiles = {}

# Clear the listview and display the current lights in the scene.
from bams_client import resolver  
def getLatest(source_path=""):
    if (source_path==""):
        raise Exception("No source_path attribute in getLatest()")

    latest_source = resolver.resolve_filepath(source_path, resolve_by="latest")
    return latest_source

def getLatestApproved(source_path=""):
    if (source_path==""):
        raise Exception("No source_path attribute in getLatest()")

    latest_source = resolver.resolve_filepath(source_path, resolve_by="latest_approved")
    return latest_source


def refreshList(*args):
    root = cmds.textFieldGrp(filedirVar, q=1, text=1)
    ends = cmds.textFieldGrp(fileendVar, q=1, text=1)

    # Clear all items in list.
    cmds.textScrollList(listAnimations, e=True, removeAll=True)
    cmds.textScrollList(listVersions, e=True, removeAll=True)
    cmds.textScrollList(listDates, e=True, removeAll=True)

    allAnims = []
    legacyAnims = []
    sortAnims = []
    
    for subdir, dirs, files in os.walk(root): 
        for item in files:
            itempath = subdir + os.sep + item

            if itempath.endswith(ends):
                folderls = (subdir.split("/"))
                if(len(folderls)>10):
                    creationdate = str(time.ctime(os.path.getmtime(itempath)))
                    
                    folder = folderls[5]+"_"+folderls[8]
                    instanceName= folderls[8]
                    version = folderls[10]
                    keyv = folder+"_"+version
                    key = folder
                    fullfile = (key,version,creationdate)
                    alllegfile = (keyv,version,creationdate)
                    sortme = (key, version)
                    Displayfiles[key] = itempath
                    sortAnims.append(sortme)
                    allAnims.append(fullfile)
                    legacyAnims.append(alllegfile)
                    print(key)
                    print "itempath:"+itempath
    
    sortvers = {}
    for k, i, in sortAnims:
        sortvers.setdefault(k, []).append(i)

    for k, vers in sortvers.items():
        vers.sort(reverse=True)
    
    keyedDict = {}
    for k, vers, tim in allAnims:
        new = (k, vers, tim)
        keyedDict.setdefault(k, []).append(new)
    
    
    updatedAnims = []
    
    for key in sortvers:
        if key in keyedDict:
            for item in keyedDict[key]:
                if sortvers[key][0] == item [1]:
                    updatedAnims.append(item)
    
    legacyAnims = sorted(legacyAnims,key=itemgetter(0))  
    updatedAnims = sorted(updatedAnims,key=itemgetter(0))    
  
    if(cmds.checkBox(legacy, query=True, value=True)): 
        # Add anims to the listview.     
        for obj in legacyAnims:
            myFiltExp=cmds.textFieldGrp(fileFilterRegex, q=1, text=1)
            filter=re.search(myFiltExp,obj[0])
            if filter:
                print "\n run in "+obj[0]
                cmds.textScrollList(listAnimations, e=True, append=obj[0])
                cmds.textScrollList(listVersions, e=True, append=obj[1])    
                cmds.textScrollList(listDates, e=True, append=obj[2])   
            
    else:                    
        # Add anims to the listview.     
        for obj in updatedAnims:
            myFiltExp=cmds.textFieldGrp(fileFilterRegex, q=1, text=1)
            filter=re.search(myFiltExp,obj[0])
            if filter:
                print "\n run in "+obj[0]
                cmds.textScrollList(listAnimations, e=True, append=obj[0])
                cmds.textScrollList(listVersions, e=True, append=obj[1])    
                cmds.textScrollList(listDates, e=True, append=obj[2])   
        

def selectInTextList():
    # Collect a list of selected items.
    # 'or []' converts it to a list when nothing is selected to prevent errors.
    selectedItems = cmds.textScrollList(listAnimations, q=True, selectItem=True) or []
    fulllist = cmds.textScrollList(listAnimations, q=True, ai=True)
    
    """
    newSelection = [obj for obj in selectedItems if cmds.objExists(obj)]
    print (selectedItems)
    cmds.select(newSelection)
    """
    
    #select corrsesponding information of version and creationdate
    for obj in selectedItems:
        index = fulllist.index(obj)+1
        print (index)
        cmds.textScrollList(listVersions, e=True, sii=index) 
        cmds.textScrollList(listDates, e=True, sii=index) 
    
    lskeys = cmds.textScrollList(listAnimations, q=1, si=1)
    print lskeys
    for key in lskeys:
        print key,Displayfiles
        fullp = Displayfiles[key]
        filep = fullp.rsplit("/", 1)[0]
        filepath = filep.replace("atom", "gmo")
        filen = fullp.rsplit("/", 1)[1]
        filename = filen.replace("atom", "gmo")
        #filepath = fullp.replace("atom", "gmo")
        
        #added write path from context changed filename to filtname
        contextWrite = context_manager.Context.from_environment()
        pthToWrite=contextWrite.path+"/maya"
        
    cmds.textFieldGrp(exportpath, edit=1, text=pthToWrite)
    cmds.textFieldGrp(exportname, edit=1, text=filtname+".gmo")


def cleanupScene():
    cmds.file(new=True, force=True) 

def getRig(*args):
    
    cleanupScene()
    
    impRigFile = cmds.textFieldGrp( rigfile, query = True, text = True)

    cmds.file(impRigFile,i=True)
    
    #disconnect translate constraints except for root joint
    joints = cmds.ls('cwd_*', type='joint')

    cmds.select(joints)
    cmds.select( 'cwd_root_C', d=True )
    mil=cmds.ls (sl=True)
    
    import maya.mel
    maya.mel.eval("source channelBoxCommand;")
    
   
    if(cmds.checkBox(transformdel, query=True, value=True)):
        for each in mil:
            tx="%s.tx"%each
            ty="%s.ty"%each
            tz="%s.tz"%each
            
            attr = tx
            maya.mel.eval("CBdeleteConnection \"%s\";"%attr)
            attr = ty
            maya.mel.eval("CBdeleteConnection \"%s\";"%attr)
            attr = tz
            maya.mel.eval("CBdeleteConnection \"%s\";"%attr)
     
    
    #turn the crowd bone display on
    cmds.setAttr('rig.jointDisplay', 0)
    
    #select all controllers
    ctl=cmds.ls("ctl*")
    cmds.select(ctl)


def importSelected(*args):
    
    lskeys = cmds.textScrollList(listAnimations, q=1, si=1)
    for key in lskeys:
        pth = Displayfiles[key]

    print(pth)
    
    
    joints = cmds.ls('cwd_*', type='joint')
    print joints[0]
    cmds.select(joints)
    cmds.select( 'cwd_root_C', d=True )
    mil=cmds.ls (sl=True)
    import maya.mel
    maya.mel.eval("source channelBoxCommand;")
            
                
    #turn the crowd bone display on
    cmds.setAttr('rig.jointDisplay', 0)
    #select all controllers
    ctl=cmds.ls("ctl*")
    cmds.select(ctl)
            
    ctl=cmds.ls("ctl*")  
    flags = {
        "targetTime": 3,
        "option": "scaleReplace",
        "match": "string",
        "selected": "selectedOnly",
        "search": "*:",
        "replace": "",
        }
    import_atom_curves(pth, ctl, flags=flags)
    import context_manager
    import shot_api
    
    context = context_manager.Context.from_path(pth)
    print context
    shot = shot_api.Shot.from_context(context)
    start_frame, end_frame = shot.get_frame_range()
    scene_start = pm.currentTime(start_frame)
    scene_end = pm.currentTime(end_frame)
            
    cmds.playbackOptions(
        minTime=scene_start,
        maxTime=scene_end,
        animationStartTime=scene_start,
        animationEndTime=scene_end,
    )
    cmds.currentTime(scene_start)
    

def bakeAnim(*args):
    start = cmds.playbackOptions( q=True,min=True )
    end  = cmds.playbackOptions( q=True,max=True )
    cmds.bakeResults("cwd_*", sm=True, t = (start, end) )   
    cmds.filterCurve("cwd_*")
    print("filtered")
    return

def animdirect(*args):
    startdir = cmds.textFieldGrp(filedirVar, q=1, text=1)
    aPath = cmds.fileDialog2(fileMode=1, startingDirectory=startdir)
    if aPath is not None:
        aPath = aPath[0]
        cmds.textFieldGrp(filedirVar, q=1, text=fPath)
    return aPath 

def exportmotion(*args):
    loadedgcha = cmds.textFieldGrp( gchafile, query = True, text = True)
    rootcwd = cmds.textFieldGrp( rootbone, query = True, text = True)
    
    savetopath = cmds.textFieldGrp( exportpath, query = True, text = True)
    motionname = cmds.textFieldGrp( exportname, query = True, text = True)
    fullname = savetopath+"/"+motionname

    print ("exporting"+"\n"+"Motion:"+"\n"+motionname+"\n"+"to"+"\n"+"Path:"+"\n"+savetopath)
    
    cmds.glmExportMotion(outputFile=fullname, fromRoot=rootcwd, characterFile=loadedgcha , automaticFootprints=True)
    cmds.glmExportMotion(outputFile=fullname,fromInputMotionFile=fullname,footprintsOnChannel=["legFront_R","legFront_L","legHind_R","legHind_L"],automaticFootprints=True)
    print "full name of GMO File is :{}".format(fullname)
    cmds.glmCharacterMaker(file=fullname)

def rigtoload(*args):
    startdir = cmds.textFieldGrp( rigfile, query = True, text = True)
    filtertype = cmds.textFieldGrp( fileendRig, query = True, text = True)
    fPath = cmds.fileDialog2(fileMode=1,ff=filtertype, startingDirectory=startdir)
    if fPath is not None:
        fPath = fPath[0]
        cmds.textFieldGrp(rigfile, edit=1, text=fPath)
    return fPath 
    
def kidRig(*args):
    startdir = cmds.textFieldGrp( rigfile, query = True, text = True)
    fPath=getLatest("/projects/pony/prod/char/epGenericKid/products/rigCrowd/fC/mid/v013/mb/char_epGenericKid_rigCrowd_fC_mid_v013.mb")
    cmds.textFieldGrp(rigfile, edit=1, text=fPath)
    return fPath
    print fPath
    
def pegasusRig(*args):
    startdir = cmds.textFieldGrp( rigfile, query = True, text = True)
    fPath=getLatest("/projects/pony/prod/char/pgGenericMale/products/rigCrowd/a/mid/v002/mb/char_pgGenericMale_rigCrowd_a_mid_v002.mb")
    cmds.textFieldGrp(rigfile, edit=1, text=fPath)
    return fPath
    print fPath
    
def defaultRig(*args):
    startdir = cmds.textFieldGrp( rigfile, query = True, text = True)
    fPath=getLatest(source_path="/projects/pony/prod/char/epGenericMale/products/rigCrowd/factoryWorkerPipesAcA/mid/v006/mb/char_epGenericMale_rigCrowd_factoryWorkerPipesAcA_mid_v006.mb")
    cmds.textFieldGrp(rigfile, edit=1, text=fPath)
    return fPath
    print fPath
def tinHatRig(*args):
    startdir = cmds.textFieldGrp( rigfile, query = True, text = True)
    fPath=getLatest(source_path="/projects/pony/prod/char/epGenericMale/products/rigCrowd/dTinHat/mid/v010/mb/char_epGenericMale_rigCrowd_dTinHat_mid_v010.mb")
    cmds.textFieldGrp(rigfile, edit=1, text=fPath)
    return fPath
def tinHatAdultRig(*args):
    startdir = cmds.textFieldGrp( rigfile, query = True, text = True)
    fPath=getLatest(source_path="/projects/pony/prod/char/epGenericMaleAdult/products/rigCrowd/dTinHat/mid/v006/mb/char_epGenericMaleAdult_rigCrowd_dTinHat_mid_v006.mb")
    cmds.textFieldGrp(rigfile, edit=1, text=fPath)
    return fPath  

def kidGcha(*args):
    startdir = cmds.textFieldGrp( gchafile, query = True, text = True)
    fPath=getLatest(source_path="/projects/pony/prod/char/epGenericKid/products/crowdAgent/fC/mid/v004/gcha/char_epGenericKid_crowdAgent_fC_mid_v004.gcha")
    cmds.textFieldGrp(gchafile, edit=1, text=fPath)
    return fPath
    print fPath
  
def pegasusGcha(*args):
    startdir = cmds.textFieldGrp( gchafile, query = True, text = True)
    fPath=getLatest(source_path="/projects/pony/prod/char/pgGenericMale/products/crowdAgent/a/mid/v003/gcha/char_pgGenericMale_crowdAgent_a_mid_v003.gcha")
    cmds.textFieldGrp(gchafile, edit=1, text=fPath)
    return fPath
    print fPath
    
def defaultGcha(*args):
    startdir = cmds.textFieldGrp( gchafile, query = True, text = True)
    fPath=getLatest(source_path="/projects/pony/prod/char/epGenericMale/products/crowdAgent/factoryWorkerPipesAcA/mid/v009/gcha/char_epGenericMale_crowdAgent_factoryWorkerPipesAcA_mid_v009.gcha")
    cmds.textFieldGrp(gchafile, edit=1, text=fPath)
    return fPath
    print fPath
def tinHatAdultGcha(*args):
    startdir = cmds.textFieldGrp( gchafile, query = True, text = True)
    fPath=getLatest(source_path="/projects/pony/prod/char/epGenericMaleAdult/products/crowdAgent/dTinHat/mid/v001/gcha/char_epGenericMaleAdult_crowdAgent_dTinHat_mid_v001.gcha")
    
    cmds.textFieldGrp(gchafile, edit=1, text=fPath)
    return fPath
    print fPath
def tinHatGcha(*args):
    startdir = cmds.textFieldGrp( gchafile, query = True, text = True)
    fPath=getLatest(source_path="/projects/pony/prod/char/epGenericMale/products/crowdAgent/dTinHat/mid/v006/gcha/char_epGenericMale_crowdAgent_dTinHat_mid_v006.gcha")
    cmds.textFieldGrp(gchafile, edit=1, text=fPath)
    return fPath
    print fPath
       
def gchatoload(*args):
    startdir = cmds.textFieldGrp( gchafile, query = True, text = True)
    filtertype = cmds.textFieldGrp( gchaend, query = True, text = True)
    fPath = cmds.fileDialog2(fileMode=1,ff=filtertype, startingDirectory=startdir)
    if fPath is not None:
        fPath = fPath[0]
        cmds.textFieldGrp(gchafile, edit=1, text=fPath)
    return fPath 

def updateExportpath(*args):
    fileext = ".gmo"
    lskeys = cmds.textScrollList(listAnimations, q=1, si=1)
    for key in lskeys:
        fullp = Displayfiles[key]
        startdir = fullp.rsplit("/", 1)[0]

    fPath = cmds.fileDialog2(fileMode=2,ff=fileext, startingDirectory=startdir)
    if fPath is not None:
        fPath = fPath[0]
        cmds.textFieldGrp(exportpath, edit=1, text=fPath)
    return fPath 
def getEntity(result):
    if result == None:
        print "please type filename"
    #result=cmds.promptDialog(t="importEntity",m="Paste entity type path here",button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result != None:
        print "trying to import"+result
        gchaPath=result
        import maya.mel
        maya.mel.eval("addCrowdEntityTypeNode;")
        etn=cmds.ls(selection=True)
        #gchaPath="/projects/pony/prod/char/epGenericFemale/products/crowdAgent/b/mid/v004/gcha/char_epGenericFemale_crowdAgent_b_mid_v004.gcha"
        gchaName=gchaPath.split("/")[-1]
        elem=gchaName.split("_")
        etName=elem[1]+"_"+elem[3]
        #print etn[0]+" is "+etName
    
        setGch=str(etn[0])+'.gch'
    
        #print etn[0]
        
        pth=cmds.setAttr(setGch,gchaPath,type="string",lock=True)
        setDc=str(etn[0])+'.dc'
        cmds.setAttr(setDc,lock=True)
        setSmi=str(etn[0])+'.scaleMin'
        cmds.setAttr(setSmi,1,lock=True)
        setSma=str(etn[0])+'.scaleMax'
        cmds.setAttr(setSma,1,lock=True)
        
        
        setRad=str(etn[0])+'.radius'
        cmds.setAttr(setRad,1.5,lock=True)
        setPs=str(etn[0])+'.personalSpace'
        cmds.setAttr(setPs,0.5,lock=True)
        
        setOpa=str(etn[0])+'.overridePerceptionAttributes'
        cmds.setAttr(setOpa,1,lock=True)
        setPes0=str(etn[0])+'.perceptionEntitySize0'
        cmds.setAttr(setPes0,0.1,lock=True)
        setPes2=str(etn[0])+'.perceptionEntitySize2'
        cmds.setAttr(setPes2,0.1,lock=True)
        
        print etName+" is imported"
        cmds.rename(etn[0],etName)
        
        #Assign gmm path
        etn=cmds.ls(sl=True)
        family=etn[0].split("_")[0]
        #if(etn[0].split("_")[0]="epGenericFemale"):
        taskPath="/projects/pony/prod/char/"+family+"/tasks/crowdAgent/maya/"
        print taskPath
        t=cmds.getFileList( folder=taskPath,filespec='*gmm')
        print t
        print t[-0]
        
        if(t[-0]!=""):
            myMmf=etn[0]+".mmf"
            mmfPath=taskPath+t[-0]
            print mmfPath
            cmds.setAttr(myMmf,mmfPath,type="string",lock=True)
import os   
import context_manager         
def importShaderFamily(pth):
    context = context_manager.Context.from_path(pth)
    gchDiv=pth.split("/")
    gchDiv[6]=u"tasks"
    gchDiv[8]=u"maya"
    makeStr='/'.join(map(str,gchDiv[0:9]))
    makeStr+="/"
    print gchDiv[0:9]
    print makeStr
    t=cmds.getFileList( folder=makeStr,filespec='shader*')
    print t
    print t[0]
    
    mayaFiles=[]
    import os.path
    for root, dirs, files in os.walk(makeStr):
        for filename in files:
            if filename.endswith(('.ma', '.mb')):
                mayaFiles.append(filename)
    print mayaFiles
def importShaderFamilyFromPath(result):
    import context_manager
    import shot_api
    #result=cmds.promptDialog(t="importShaderFromPublishedGcha",m="Paste published gcha path here",button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result != None:
        pth=result
        context = context_manager.Context.from_path(pth)
        gchDiv=pth.split("/")
        gchDiv[6]=u"tasks"
        gchDiv[8]=u"maya"
        makeStr='/'.join(map(str,gchDiv[0:9]))
        makeStr+="/"
        print gchDiv[0:9]
        print makeStr
        t=cmds.getFileList( folder=makeStr,filespec='shader*')
        print t
        print t[0]
            
        mayaFiles=[]
        import os.path
        for root, dirs, files in os.walk(makeStr):
            for filename in files:
                if filename.endswith(('.ma', '.mb')):
                    mayaFiles.append(filename)
                        
        files=[] #to filter maya files with shader name
        for i in t: 
            if i in mayaFiles:
                files.append(i)            
                                    
        for each in files:
            myFile=makeStr+each
            print myFile
            cmds.file(myFile,i=True)
            print myFile+" has been imported"
                            
                
def createGmoPresentation(path):                
    importShaderFamilyFromPath(path)
    import glm.crowdUtils as crowdUtils
    x=cmds.workspace(q=True,rd=True)
    print x
    import os
    gmo="a"
    for file in os.listdir(x):
        #print file
        if file.endswith(".gmo"):
            gmo=(os.path.join(x,file))
            
    print(gmo)
    crowdUtils.createGolaemScene(4,path,gmo)  
    cmds.setAttr("beMotionShape1.startPercentMax",0)      
def createAutoPresentation():
    impRigFile = cmds.textFieldGrp( rigfile, query = True, text = True)
    impGchaFile = cmds.textFieldGrp( gchafile, query = True, text = True)
    print impGchaFile
    createGmoPresentation(impGchaFile)
    print "finished Presentation setup",impGchaFile

    
# Create window.
animLoader = 'Animation Loader'
if cmds.window(animLoader, q = True, exists =True):
    cmds.deleteUI(animLoader)
    
animLoader = cmds.window(title='Animation Loader', wh=(550,400), sizeable=False)

scrollLayout = cmds.scrollLayout(
	verticalScrollBarThickness=16)

clm1 = cmds.columnLayout(adjustableColumn=True)
   
# Create interface items.
cmds.separator(parent=clm1,  height=20, style='none' )
cmds.separator(parent=clm1,  height=20, style='out')
cmds.text(parent=clm1,  label='1. Import Rig' )
cmds.separator(parent=clm1,  height=20, style='none' )
rigfile = cmds.textFieldGrp(parent=clm1, label='RigFile', text='/projects/pony/prod/char/epGenericMale/products/rigCrowd/factoryWorkerPipesAcA/mid/v006/mb/char_epGenericMale_rigCrowd_factoryWorkerPipesAcA_mid_v006.mb')
cmds.radioButtonGrp( label='swapRig', labelArray4=['Default', 'Kid', 'Pegasus', 'TinHat'], numberOfRadioButtons=4,cc1='defaultRig()',cc2='kidRig()',cc3='pegasusRig()',cc4='tinHatRig()' )
cmds.radioButtonGrp( label='swapRig', labelArray4=['Default', 'TinHatAdult', 'None', 'None'], numberOfRadioButtons=4,cc1='defaultRig()',cc2='tinHatAdultRig()',cc3='',cc4='' )

fileendRig = cmds.textFieldGrp(parent=clm1, label='File_Ending', text="*.mb", editable=True)
transformdel = cmds.checkBox(parent=clm1,  label='Delete Bone Transformation Constraints', value=1, align='center' )
loadrig = cmds.button(parent=clm1, label='Change Rig', command = rigtoload, width=200, height=25, align='center')


importRig = cmds.button(parent=clm1, label='Import Clean Rig', command = getRig, width=200, height=25, align='center')


cmds.separator(parent=clm1,  height=20, style='out')
cmds.text(parent=clm1,  label='2.Animation Files' )
cmds.separator(parent=clm1,  height=20, style='none' )

#getting context from env



contextRoot = context_manager.Context.from_environment()
contextRoot.task=None
pthToAnim=contextRoot.path
print contextRoot.task
print pthToAnim
cmds.text(parent=clm1,  label='Specs' )
filedirVar = cmds.textFieldGrp(parent=clm1, label='Root_Directory', text=pthToAnim)
fileendVar = cmds.textFieldGrp(parent=clm1, label='File_Ending', text='atom', editable=True)

cmds.separator(parent=clm1,  height=20, style='none' )


cmds.text(parent=clm1,  label='Available Animation Files' )
import context_manager
#processing filter name
xCon=(context_manager.Context.from_environment())


contextE = "{}".format(context_manager.Context.from_environment())
cxE=contextE.split("/")
filtname=xCon.shot
print filtname
filtname=filtname[8:]
fileFilterRegex = cmds.textFieldGrp(parent=clm1, label='Filter', text=filtname,editable=True)
   
rwl1 = cmds.rowLayout(parent=clm1, numberOfColumns=3)   
listAnimations = cmds.textScrollList(parent=rwl1, numberOfRows=8, allowMultiSelection=True, showIndexedItem=4, selectCommand='selectInTextList()', w=250)
listVersions = cmds.textScrollList(parent=rwl1, numberOfRows=8, allowMultiSelection=False, showIndexedItem=4, w=50)
listDates = cmds.textScrollList(parent=rwl1, numberOfRows=8, allowMultiSelection=False, showIndexedItem=4, w=200)


cmds.separator(parent=clm1, height=20, style='none' )
legacy = cmds.checkBox(parent=clm1, label='List Legacy Animations', value=0, align='center' )
findanimdir = cmds.button(parent=clm1,label='Change Root Directory', command = animdirect, width=200, height=25, align='center')
refreshButton = cmds.button(parent=clm1,label='Refresh list', command = refreshList, width=200, height=25, align='center')
importAnim = cmds.button(parent=clm1,label='Import Selected Anim', command = importSelected, width=200, height=25, align='center')

cmds.separator(parent=clm1, height=20, style='out')
cmds.separator( parent=clm1,height=5, style='none' )
cmds.text(parent=clm1, label='3.Prepare for Export' )
cmds.separator(parent=clm1, height=20, style='none' )

bakebutton = cmds.button(parent=clm1,label='BakeAnim', command = bakeAnim, width=200, height=25, align='center')

cmds.separator(parent=clm1, height=20, style='out')
cmds.separator(parent=clm1, height=5, style='none' )
cmds.text(parent=clm1, label='4.Export with Golaem' )
cmds.separator(parent=clm1, height=20, style='none' )

gchafile = cmds.textFieldGrp(parent=clm1,label='GCHA_File', text='/projects/pony/prod/char/epGenericMale/products/crowdAgent/factoryWorkerPipesAcA/mid/v008/gcha/char_epGenericMale_crowdAgent_factoryWorkerPipesAcA_mid_v008.gcha')
cmds.radioButtonGrp(parent=clm1, label='swapGcha', labelArray4=['Default', 'Kid', 'Pegasus', 'TinHat'], numberOfRadioButtons=4,cc1='defaultGcha()',cc2='kidGcha()',cc3='pegasusGcha()',cc4='tinHatGcha()' )
cmds.radioButtonGrp(parent=clm1, label='swapGcha', labelArray4=['Default', 'tinHatAdult', 'None', 'None'], numberOfRadioButtons=4,cc1='defaultGcha()',cc2='tinHatAdultGcha()',cc3='',cc4='' )
gchaend = cmds.textFieldGrp(parent=clm1,label='File_Ending', text="*.gcha", editable=True)
rootbone = cmds.textFieldGrp(parent=clm1,label='Root_Bone', text="cwd_root_C", editable=True)
exportpath = cmds.textFieldGrp(parent=clm1,label='Export Motion Path', editable=True)
exportname = cmds.textFieldGrp(parent=clm1,label='Export Motion Name', editable=True)
loadrig = cmds.button(parent=clm1,label='Change Gcha', command = gchatoload, width=200, height=25, align='center')
PathGMO = cmds.button(parent=clm1,label='Change GMO ExportPath', command = updateExportpath, width=200, height=25, align='center')
createGMO = cmds.button(parent=clm1,label='Export GMO Motion', command = exportmotion, width=200, height=25, align='center')

cmds.separator(parent=clm1, height=20, style='out')
cmds.separator(parent=clm1, height=5, style='none' )

cmds.button(parent=clm1,label='Create Auto Presentation',command="createAutoPresentation()")
cmds.button(parent=clm1,label='Close Window',command="cmds.deleteUI('%s')" % animLoader)

cmds.showWindow(animLoader)
    

