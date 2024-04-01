import os
import yaml

import pymel.core as pm
import maya.cmds as cmds
from bams_client import BamsClient

from maya_crowd import util


class CacheProxyNode(object):
    def __init__(self, node):
        self.__node = pm.PyNode(node)

    @property
    def fields(self):
        field_objs = []
        fields = str(self.__node.crowdFields.get())

        if fields != "":
            split_fields = fields.split(";")

            for field in split_fields:
                field_objs.append(CrowdField(field, self))

        return field_objs

    @property
    def cache_name(self):
        return self.__node.inputCacheName.get()

    @property
    def cache_directory(self):
        return self.__node.inputCacheDir.get()

    @property
    def layout_file(self):
        return self.__node.layoutFiles[0].path.get()

    @property
    def node(self):
        return self.__node

    @property
    def character_files(self):
        return str(self.__node.characterFiles.get()).split(";")

    def dump_description(self, output_name):
        data = []
        for field in self.fields:
            kill_dict = util.get_crowd_field_kill_dict(field.name, self.__node)
            for entity in field.entities:
                if not kill_dict[entity.entity_id]:
                    entity_info = {}
                    entity_info["position"] = entity.get_position()
                    entity_info["orientation"] = entity.get_orientation()
                    entity_info["asset_name"] = entity.asset_name
                    entity_info["entity_variant"] = entity.variant
                    entity_info["entity_id"] = entity.entity_id

                    data.append(entity_info)

        with open(output_name, "w") as fh:
            yaml.dump(data, fh)

        return data

    def entities_in_frustum(
        self, frame=1001, camera="persp", camera_margin=300, frustum_margin=30
    ):
        in_frustum = pm.glmSimulationCacheTool(
            cf=self.__crowd_field.name,
            cn=self.__node.cache_name,
            cd=self.__node.cache_directory,
            layoutFiles=self.__node.layout_file,
            getAttr="inCameraFrustum",
            characterFiles=";".join(self.__node.character_files),
            cameraName="{0};{1};{2}".format(camera, camera_margin, frustum_margin),
            frame=frame,
        )
        return in_frustum

    @property
    def layout_files(self):
        paths = []
        for layout_file in self.__node.layoutFiles:
            paths.append(layout_file.path.get())
        return paths

    def set_visibility_to_connected_nodes(self, state=True):
        nodes_to_change = []

        for field in self.fields:
            crowd_field = field.name
            nodes_to_change.append(crowd_field)
            connections = set(cmds.listConnections(crowd_field))
            nodes_to_change.extend(connections)

        nodes_to_change.append(self.node.name())

        if state:
            cmds.showHidden(nodes_to_change, above=True, below=True)
        else:
            cmds.hide(nodes_to_change)


class CrowdField(object):
    def __init__(self, field_name, node):
        self.__field_name = field_name
        self.__crowd_sim_node = node

    @property
    def entity_count(self):
        entity_count = pm.glmSimulationCacheTool(
            cf=self.name,
            cn=self.__crowd_sim_node.cache_name,
            cd=self.__crowd_sim_node.cache_directory,
            getAttr="entityCount",
        )

        return entity_count

    @property
    def name(self):
        return self.__field_name

    @property
    def entities(self):
        agent_objs = []
        for entity_id in range(self.entity_count):
            agent = CrowdAgent(entity_id, self, self.__crowd_sim_node)
            agent_objs.append(agent)

        return agent_objs

    def entities_in_frustum(
        self, frame=1001, camera="persp", camera_margin=300, frustum_margin=30
    ):
        camera = "{0};{1};{2}".format(camera, camera_margin, frustum_margin)

        in_frustum = pm.glmSimulationCacheTool(
            cf=self.name,
            cn=self.__crowd_sim_node.cache_name,
            cd=self.__crowd_sim_node.cache_directory,
            getAttr="inCameraFrustum",
            characterFiles=";".join(self.__crowd_sim_node.character_files),
            cameraName=camera,
            frame=frame,
            layoutFiles=";".join(self.__crowd_sim_node.layout_files),
        )

        return in_frustum


class CrowdAgent(object):
    def __init__(self, id, field, node):
        self.__id = id
        self.__crowd_field = field
        self.__node = node

    def get_position(self, frame=1001):
        bone_position = pm.glmSimulationCacheTool(
            cf=self.__crowd_field.name,
            cn=self.__node.cache_name,
            cd=self.__node.cache_directory,
            layoutFiles=self.__node.layout_file,
            getAttr="bonePosition",
            atIdx=0,
            entityIdx=self.__id,
            frame=frame,
        )

        return bone_position

    def get_orientation(self, frame=1001):
        bone_orientation = pm.glmSimulationCacheTool(
            cf=self.__crowd_field.name,
            cn=self.__node.cache_name,
            cd=self.__node.cache_directory,
            layoutFiles=self.__node.layout_file,
            getAttr="boneOrientation",
            atIdx=0,
            entityIdx=self.__id,
            frame=frame,
        )

        return bone_orientation

    @property
    def id(self):
        return self.__id

    @property
    def character_file_id(self):
        character_file_id = pm.glmSimulationCacheTool(
            cf=self.__crowd_field.name,
            cn=self.__node.cache_name,
            cd=self.__node.cache_directory,
            layoutFiles=self.__node.layout_file,
            getAttr="characterFileId",
            entityIdx=self.__id,
            characterFiles=";".join(self.__node.character_files),
            cameraName="persp",
        )
        return character_file_id

    @property
    def character_file(self):
        return self.__node.character_files[self.character_file_id]

    @property
    def asset_name(self):
        client = BamsClient()
        crowd_agent_output = client.Output.get_one(filepath=self.character_file)
        if crowd_agent_output:
            asset_name = crowd_agent_output.shot
            # this is going away and being replaced with an angry error once character files
            # are being published in earnest.

        else:
            asset_name = os.path.basename(char_file_path).split("_")[0]

        return str(asset_name)

    @property
    def variant(self):
        client = BamsClient()
        crowd_agent_output = client.Output.get_one(filepath=self.character_file)
        if crowd_agent_output:
            asset_variant = crowd_agent_output.variant

        return str(asset_variant)

    @property
    def entity_id(self):
        entity_id = pm.glmSimulationCacheTool(
            cf=self.__crowd_field.name,
            cn=self.__node.cache_name,
            cd=self.__node.cache_directory,
            layoutFiles=self.__node.layout_file,
            entityIdx=self.id,
            getAttr="entityId",
        )
        return entity_id

    def in_camera_frustum(
        self, frame=1001, camera="persp", camera_margin=300, frustum_margin=30
    ):
        in_frustum = pm.glmSimulationCacheTool(
            cf=self.__crowd_field.name,
            cn=self.__node.cache_name,
            cd=self.__node.cache_directory,
            layoutFiles=";".join(self.__node.layout_files),
            getAttr="inCameraFrustum",
            entityIdx=self.__id,
            characterFiles=";".join(self.__node.character_files),
            cameraName="{0};{1};{2}".format(camera, camera_margin, frustum_margin),
            frame=frame,
        )
        return in_frustum
