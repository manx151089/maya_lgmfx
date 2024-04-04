#
import context_manager
import shot_api
from bams_client import resolver    
gchaDesc='"noDesc"'
gchaTextField=None

def setRenFilt():
    myEt=cmds.ls(selection=True)
    for each in myEt:
        atr=each+".renderFilter"
        print atr
        cmds.setAttr(atr,3)
def getStatus():
    status=cmds.confirmDialog(bgc=[0.7,0.3,0.1],title="Select the status",m="Select the status of your version",button=["latestApproved","latest"])
    return status
def connectContainer():
    #select entities
    sel= map(str, cmds.listRelatives(s=True))
    beShape=sel[-1]
    check=cmds.ls(beShape,type="CrowdBeContainer")
    if(check==[]):
        raise Exception("please select entity type followed by a be shape container")
    else:    
        selList=sel[:-1]
        for i in selList:
            print("{} node connected to {}".format(beShape,i))
            #enter name of container and entity
            cmds.connectAttr(str(beShape)+".message",  i+".inBeContainer", force=True) 


def unlock():
    mySel = map(str, cmds.ls(sl=1))
    for each in mySel:
        cmds.setAttr(each+".characterFile", l=0)
        cmds.setAttr(each+".motionMappingFile", l=0)    
def publishGchaFromCurrentScene():
    import context_manager
    import shot_api
    import subprocess
    import os
    pth=cmds.file(q=True, sn=True)
    context = context_manager.Context.from_path(pth)
    #mycmd='resolve maya_crowd  -- crowd_agent_publish --filepath '+pth+' --description "with eyelash fixed" --context '+str(context)
    print gchaDesc
    mycmd='resolve -vl maya_crowd --patch golaem-7.3.6.m1 -- crowd_agent_publish '+str(context)+' '+pth+' --description '+gchaDesc
    #mycmd='resolve maya_crowd  -- crowd_agent_publish '+str(context)+' '+pth+' --description '+gchaDesc
    cmd='bms '+str(context)+"\n"+mycmd
    print cmd
    pubRes=cmds.confirmDialog(backgroundColor=[0.05,0.15,0.175],title="Want to publish???",message=("Check your description!!! \n Desc:"+gchaDesc),button=["Yes","No"])
    print pubRes
    if (pubRes=="Yes"):
        os.system(cmd)
        cmds.confirmDialog(backgroundColor=[0.5,0.5,0.0],title="Publish Done",message=("Publish done \n desc:"+gchaDesc))

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
        print "gmmFile present here>>",t
        if(len(t)==0):
            print ("{}:no gmm found in folder!!!".format(family))
        else:
            if(t[-0]!=""):
                myMmf=etn[0]+".mmf"
                mmfPath=taskPath+t[-0]
                print mmfPath
                cmds.setAttr(myMmf,mmfPath,type="string",lock=True)
            
def getEntityFromGchaPath():
    result=cmds.promptDialog(t="importEntity",m="Paste entity type path here",button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK':
        gchaPath=cmds.promptDialog(query=True,text=True)
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

def getShaderFromSelected():
    import context_manager
    import shot_api
    myEt=cmds.ls(selection=True)
    myGch=str(myEt[0])+'.gch'
    pth=cmds.getAttr(myGch)
    context = context_manager.Context.from_path(pth)
    gchDiv=pth.split("/")
    gchDiv[6]=u"tasks"
    gchDiv[8]=u"maya"
    makeStr='/'.join(map(str,gchDiv[0:9]))
    makeStr+="/"
    print gchDiv[0:9]
    print makeStr
    t=cmds.getFileList( folder=makeStr,filespec='shader*')
    print t[0]
    for each in t:
        myFile=makeStr+each
        cmds.file(myFile,i=True)
        print myFile+" has been imported"
    
def updateEntityGchaToLatest():
    import os
    
    nodes=cmds.ls(sl=True)
    for each in nodes:
        myAtr=each+".gch"
        val=cmds.getAttr(myAtr,asString=True)
        arr=val.split("/")
        path="/".join(arr[:-3])
        ver=os.listdir(path)
        verDir=path+"/"+sorted(ver)[-1]
        for root, _, files in os.walk(verDir):
            for f in files:
                if os.path.splitext(f)[1]=='.gcha':
                    fpath=os.path.join(root,f)
                    cmds.setAttr(myAtr,fpath,type="string")
                    print myAtr + " is is set to " + f

def getEntityFamily():
    from bams_client import BamsClient
    bc = BamsClient()

    import os
    result=cmds.promptDialog(t="importEntity",m="type asset name here",button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK':
        assetName=cmds.promptDialog(query=True,text=True)
        #gchaPath=cmds.promptDialog(query=True,text=True)
    print assetName    
    workarea_objects = bc.Workarea.get(project='pony', sequence='char', shot=assetName, task='cwd')
    output_objects = bc.Output.get_one(sequence='char', shot=assetName,representation='gcha')
    outStr=(str(output_objects))
    gchaPath=outStr.strip("OutputEntity()")
    print workarea_objects,gchaPath
    gchaName=gchaPath.split("/")[-1]
    elem=gchaName.split("_")
    etName=elem[1]+"_"+elem[3]
    val=gchaPath
    arr=val.split("/")
    
    pathVariant="/".join(arr[:-5])
    var=os.listdir(pathVariant)
    print var
    varDirs=var
    ct=0
    for each in var:
        varDirs[ct]=pathVariant+"/"+each+"/mid"
        ct+=1
    print varDirs
    #path+"/"+sorted(ver)[-1]
    for dir in varDirs:
        path=dir
        print path
        ver=os.listdir(path)
        verDir=path+"/"+sorted(ver)[-1]
        for root, _, files in os.walk(verDir):
            for f in files:
                if os.path.splitext(f)[1]=='.gcha':
                    fpath=os.path.join(root,f)
                    getEntity(fpath)
                    print f +" has been imported"
                    
                    
def importShaderFamilyFromPath():
    import context_manager
    import shot_api
    result=cmds.promptDialog(t="importShaderFromPublishedGcha",m="Paste published gcha path here",button=['OK','Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK':
        pth=cmds.promptDialog(query=True,text=True)
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
                            
#update to the latest gcha make sure you unlock the attribute before
def updateEntityLatestApproved():    
    import os
    status=getStatus()
    
    nodes=cmds.ls(sl=True)
    for each in nodes:
        myAtr=each+".gch"
        val=cmds.getAttr(myAtr,asString=True)
        from bams_client import resolver
        source_path = val
        
        latest_source = resolver.resolve_filepath(source_path, resolve_by="latest_approved")
        if(status=='latestApproved'):
            cmds.setAttr(myAtr,latest_source,type="string")
            print ("Entity GCHA set to latest approved:{}".format(latest_source.split("/")[-1]))
        if(status=='latest'):
            arr=val.split("/")
            path="/".join(arr[:-3])
            ver=os.listdir(path)
            verDir=path+"/"+sorted(ver)[-1]
            for root, _, files in os.walk(verDir):
                for f in files:
                    if os.path.splitext(f)[1]=='.gcha':
                        fpath=os.path.join(root,f)
                    cmds.setAttr(myAtr,fpath,type="string")
                    print myAtr + " is is set to " + f

def getLatestGchaString():
    from maya_crowd import entities
    cpsl=cmds.ls(sl=True)
    cp=entities.CacheProxyNode(cpsl[0])
    myChars=cp.character_files
    #myChar="/projects/pony/prod/char/epGenericMale/products/crowdAgent/j/mid/v008/gcha/char_epGenericMale_crowdAgent_j_mid_v008.gcha;/projects/pony/prod/char/epGenericMale/products/crowdAgent/k/mid/v003/gcha/char_epGenericMale_crowdAgent_k_mid_v003.gcha;/projects/pony/prod/char/epGenericMale/products/crowdAgent/a/mid/v004/gcha/char_epGenericMale_crowdAgent_a_mid_v004.gcha;/projects/pony/prod/char/epGenericMale/products/crowdAgent/d/mid/v005/gcha/char_epGenericMale_crowdAgent_d_mid_v005.gcha;/projects/pony/prod/char/epGenericMale/products/crowdAgent/f/mid/v003/gcha/char_epGenericMale_crowdAgent_f_mid_v003.gcha;/projects/pony/prod/char/epGenericMale/products/crowdAgent/i/mid/v003/gcha/char_epGenericMale_crowdAgent_i_mid_v003.gcha;/projects/pony/prod/char/epGenericFemale/products/crowdAgent/b/mid/v005/gcha/char_epGenericFemale_crowdAgent_b_mid_v005.gcha;/projects/pony/prod/char/epGenericFemale/products/crowdAgent/n/mid/v004/gcha/char_epGenericFemale_crowdAgent_n_mid_v004.gcha;/projects/pony/prod/char/epGenericFemale/products/crowdAgent/e/mid/v010/gcha/char_epGenericFemale_crowdAgent_e_mid_v010.gcha;/projects/pony/prod/char/epGenericFemale/products/crowdAgent/f/mid/v004/gcha/char_epGenericFemale_crowdAgent_f_mid_v004.gcha;/projects/pony/prod/char/epGenericFemale/products/crowdAgent/g/mid/v004/gcha/char_epGenericFemale_crowdAgent_g_mid_v004.gcha;/projects/pony/prod/char/epGenericFemale/products/crowdAgent/j/mid/v004/gcha/char_epGenericFemale_crowdAgent_j_mid_v004.gcha;/projects/pony/prod/char/epGenericFemale/products/crowdAgent/k/mid/v004/gcha/char_epGenericFemale_crowdAgent_k_mid_v004.gcha;/projects/pony/prod/char/epGenericFemale/products/crowdAgent/p/mid/v004/gcha/char_epGenericFemale_crowdAgent_p_mid_v004.gcha;/projects/pony/prod/char/epGenericOld/products/crowdAgent/fA/mid/v005/gcha/char_epGenericOld_crowdAgent_fA_mid_v005.gcha;/projects/pony/prod/char/epGenericOld/products/crowdAgent/fB/mid/v008/gcha/char_epGenericOld_crowdAgent_fB_mid_v008.gcha;/projects/pony/prod/char/epGenericOld/products/crowdAgent/fC/mid/v006/gcha/char_epGenericOld_crowdAgent_fC_mid_v006.gcha;/projects/pony/prod/char/epGenericOld/products/crowdAgent/fF/mid/v006/gcha/char_epGenericOld_crowdAgent_fF_mid_v006.gcha;/projects/pony/prod/char/epGenericOld/products/crowdAgent/mA/mid/v006/gcha/char_epGenericOld_crowdAgent_mA_mid_v006.gcha;/projects/pony/prod/char/epGenericOld/products/crowdAgent/mB/mid/v005/gcha/char_epGenericOld_crowdAgent_mB_mid_v005.gcha;/projects/pony/prod/char/epGenericOld/products/crowdAgent/mC/mid/v006/gcha/char_epGenericOld_crowdAgent_mC_mid_v006.gcha;/projects/pony/prod/char/epGenericMale/products/crowdAgent/a/mid/v002/gcha/char_epGenericMale_crowdAgent_a_mid_v002.gcha"
    #myChars=myChar.split(";")
    status=getStatus()
    i=0
    x=cmds.listRelatives(str(cpsl[0]),s=True)[0]
    print x
    for each in myChars:
        #print each
        source_path=each
        if(status=='latest'):
            latest_source = resolver.resolve_filepath(source_path, resolve_by="latest")
        if(status=='latestApproved'):
            latest_source = resolver.resolve_filepath(source_path, resolve_by="latest_approved")
        #print i,latest_source
        myChars[i]=latest_source
        i+=1
    outputChars=";".join(myChars)
    cmds.setAttr((x+'.characterFiles'),outputChars,type="string")
    print outputChars
    


def updateEntityToLatest():
    import os

    nodes=cmds.ls(sl=True)
    for each in nodes:
        myAtr=each+".gch"
        val=cmds.getAttr(myAtr,asString=True)
        arr=val.split("/")
        path="/".join(arr[:-3])
        ver=os.listdir(path)
        verDir=path+"/"+sorted(ver)[-1]
        for root, _, files in os.walk(verDir):
            for f in files:
                if os.path.splitext(f)[1]=='.gcha':
                    fpath=os.path.join(root,f)
                    cmds.setAttr(myAtr,fpath,type="string")
                    print myAtr + " is is set to " + f
def gmoLister():
    execfile("/projects/pony/prod/ldCrowd/ldCrowd_s0010/tasks/crowd/maya/scripts/gmoLister.py")
def atomsProcessor():
    execfile("/projects/pony/prod/ldCrowd/ldCrowd_s0010/tasks/crowd/maya/scripts/crowdAtomsProcessor_v6.py")
def proceduralLookat():
    execfile("/projects/pony/prod/ldCrowd/ldCrowd_s0010/tasks/crowd/maya/scripts/proceduralLookAt.py")

def entityToolsUi():
    x=cmds.window("winETUI", exists=True)
    #print x
    if(x==1):
        print "showingCurrentUI"
        cmds.showWindow("winETUI")
        
    if(x==0):    
        winETUI=cmds.window("winETUI",title="Entity Tools",w=400,h=400)
        layout = cmds.frameLayout(label="EntityTools")
        col=cmds.columnLayout(adjustableColumn=True)
        
        cmds.separator(height=12,style='in')
        cmds.text(label='Entity Import')
        btnGEF=cmds.button(label="getEntityFamily",command='getEntityFamily()')
        btnGEFGP=cmds.button(label="getEntityFromGchaPath",command='getEntityFromGchaPath()')        

        
        cmds.separator(height=12,style='in')
        cmds.text(label='Entity Attributes')
        btnGSFS=cmds.button(label="setRenFilt",command='setRenFilt()')
        #btnGSFS=cmds.button(label="updateEntityToLatest",command='updateEntityToLatest()')
        btnUELA=cmds.button(label="updateEntityToLatestApproved",command='updateEntityLatestApproved()')
        btnULK=cmds.button(label="unlock",command='unlock()')
        btnCC=cmds.button(label="connectContainer",command='connectContainer()')
        btnCC=cmds.button(label="getLatestGchaString",command='getLatestGchaString()')
        btnPGFCS=cmds.button(label="gmoLister",command='gmoLister()')
        cmds.separator(height=12,style='in')
        cmds.text(label='Shader Import')
        btnGSFS=cmds.button(label="getShaderFamilyFromSelected",command='getShaderFromSelected()')
        btnISFFP=cmds.button(label="importShaderFamilyFromPath",command='importShaderFamilyFromPath()')

        cmds.separator(height=12,style='in')
        cmds.text(label='Asset Tools')
        global gchaTextField
        gchaTextField=cmds.textFieldGrp("descriptionPublish",label="Description",text="Add a description here",cc="updateGchaField()")
        cmds.text(bgc=[0.2,0.0,0.0],label="Press Enter To Update Description",parent="descriptionPublish",font="boldLabelFont")

        btnPGFCS=cmds.button(label="publishGchaFromCurrentScene",command='publishGchaFromCurrentScene()')
        btnAtom=cmds.button(label="atomsProcessor",command='atomsProcessor()')
        
        btnLookAt=cmds.button(label="proceduralLookat",command='proceduralLookat()')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.showWindow()
entityToolsUi()
def updateGchaField():
    global gchaDesc
    print gchaTextField
    txt=cmds.textFieldGrp(gchaTextField, q=1, text=1)
    gchaDesc='\"'+txt+'\"'
    print "in def",gchaDesc,txt