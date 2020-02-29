import bpy
import os

from . import common
from . import rename_bonenames
from . import set_bone_values
from . import export_csv

from asyncore import poll


bl_info = {
    "name" : "Edit bones by spreadsheet",
    "author" : "Uiler",
    "version" : (0,1), 
    "blender" : (2, 7, 8),
    "location" : "User",
    "description" : "Edit bones data by csv.Names,hide,...and so on.",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "User"
}

#########################################################
# Constants
#########################################################
_NAME_CONVERT_ORIGINAL = common.NAME_CONVERT_ORIGINAL
_NAME_CONVERT_REPLACED = common.NAME_CONVERT_REPLACED
_WRITE_CSV_CLEAN = common.WRITE_CSV_CLEAN
_WRITE_CSV_ADD = common.WRITE_CSV_ADD
_WRITE_CSV_UPDATE = common.WRITE_CSV_UPDATE

#########################################################
# Global Variables
#########################################################
#########################################################
# Class
#########################################################
#########################################################
# Properties
#########################################################
class EditBonesBySpreadSheetProperties(bpy.types.PropertyGroup):

    it = []
    it.append((_NAME_CONVERT_ORIGINAL, _NAME_CONVERT_ORIGINAL, "Execute snap on current frame.","", 0))
    it.append((_NAME_CONVERT_REPLACED, _NAME_CONVERT_REPLACED, "Execute snap on keyframe points between range.","", 1))
    name_convert_type = bpy.props.EnumProperty(items = it, default=_NAME_CONVERT_ORIGINAL)
    
    it2 = []
    it2.append((_WRITE_CSV_CLEAN, _WRITE_CSV_CLEAN, "Clean CSV file and write new data.","", 0))
#     it2.append((_WRITE_CSV_ADD, _WRITE_CSV_ADD, "Add new data to CSV file.Existing values is not updated.","", 1))
    it2.append((_WRITE_CSV_UPDATE, _WRITE_CSV_UPDATE, "Update data on CSV file except name.If bone name is not exist, add new row to CSV file.","", 2))
    csv_export_type = bpy.props.EnumProperty(items = it2, default=_WRITE_CSV_UPDATE)
    
    convert_table = bpy.props.StringProperty(name="convert_table", description="Table file of CSV for converting bones data.", default="//convert_table.csv", subtype='FILE_PATH')
    
def _defProperties():

    # Define Addon's Properties
    bpy.types.Scene.uil_edit_bones_by_spreadsheet_propgrp = bpy.props.PointerProperty(type=EditBonesBySpreadSheetProperties)
    
#########################################################
# Functions(Private)
#########################################################
#########################################################
# Actions
#########################################################
#########################################################
# UI
#########################################################
class EditBonesBySpreadSheet(bpy.types.Panel):
    bl_label = "Edit bones by spread sheet"
    bl_idname = "UILER_EDIT_BONES_BY_SPREAD_SHEET_UI_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
#     bl_category = ""
#     bl_context = ""

    @classmethod
    def poll(cls, context):
        return "OK"
    
    def draw(self, context):
        
        scene = context.scene
        propgrp = scene.uil_edit_bones_by_spreadsheet_propgrp

        layout = self.layout
        
        box = layout.box()
        row = box.row()
        row.label(text="Current name is")
        row = box.row()
        row.prop(propgrp, "name_convert_type", expand=True)
        row = box.row()
        row.prop(propgrp, "convert_table", text="")
        row = box.row()
        col = row.column(align=True)
        row = col.row(align=True)
        row.prop(propgrp, "csv_export_type", expand=True)
#         row = col.row()
        col.operator("uiler.writebonevaluesbycsv", text="Export CSV", icon="LOAD_FACTORY")
        
        
        box = layout.box()
        row = box.row()
        row.label(text="Convert name to")
        row = box.row()
        row.prop(propgrp, "name_convert_type", expand=True)
        row = box.row()
        row.operator("uiler.convertbonesnamebycsv", text="Convert Name", icon="PLAY")
        
        box = layout.box()
        row = box.row()
        row.label(text="Current name is")
        row = box.row()
        row.prop(propgrp, "name_convert_type", expand=True)
        row = box.row()
        row.operator("uiler.setbonevaluesbycsv", text="Set Hide", icon="PLAY")


def register():
    bpy.utils.register_class(EditBonesBySpreadSheetProperties)
    _defProperties()
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_class(EditBonesBySpreadSheetProperties)
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()


