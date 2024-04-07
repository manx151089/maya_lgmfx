import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

class CustomPointNode(OpenMayaMPx.MPxNode):
    kNodeName = "customPointNode"
    kNodeId = OpenMaya.MTypeId(0x00ff8919)
    
    # Attributes
    aTransform = None
    aReferenceFile = None
    aRotation = None
    aScale = [1,1,1]

    def __init__(self):
        super(CustomPointNode, self).__init__()

    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr(CustomPointNode())

    @staticmethod
    def initialize():
        nAttr = OpenMaya.MFnNumericAttribute()
        tAttr = OpenMaya.MFnTypedAttribute()

        # Reference file attribute (string)
        CustomPointNode.aReferenceFile = tAttr.create("referenceFile", "ref", OpenMaya.MFnData.kString)
        tAttr.setWritable(True)
        tAttr.setStorable(True)
        tAttr.setKeyable(True)
        
        CustomPointNode.addAttribute(CustomPointNode.aReferenceFile)
        
        # Transform attribute (double3)
        CustomPointNode.aTransform = nAttr.createPoint("transform", "trf")
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        CustomPointNode.addAttribute(CustomPointNode.aTransform)

        # Rotation attribute (double3)
        CustomPointNode.aRotation = nAttr.createPoint("rotation", "rot")
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        CustomPointNode.addAttribute(CustomPointNode.aRotation)

        # Scale attribute (double3)
        CustomPointNode.aScale = nAttr.createPoint("scale", "scl")
        nAttr.setWritable(True)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        CustomPointNode.addAttribute(CustomPointNode.aScale)
        
        

    def compute(self, plug, dataBlock):
        return OpenMaya.kUnknownParameter

def initializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        pluginFn.registerNode(CustomPointNode.kNodeName, CustomPointNode.kNodeId, CustomPointNode.creator, CustomPointNode.initialize)
    except:
        raise Exception("Failed to register node: " + CustomPointNode.kNodeName)

def uninitializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(CustomPointNode.kNodeId)
    except:
        raise Exception("Failed to deregister node: " + CustomPointNode.kNodeName)

# Load the plugin
if __name__ == "__main__":
    import sys
    pluginName = "customPointNodePlugin"
    sys.argv.append(pluginName)
    OpenMayaMPx.MPxCommand.execute(pluginName)
