import bpy
import csv
import os
import re

from . import common

########################################################
# Constants And Setting            
########################################################
convert_file_table = ""

_NAME_CONVERT_ORIGINAL = common.NAME_CONVERT_ORIGINAL
_NAME_CONVERT_REPLACED = common.NAME_CONVERT_REPLACED

########################################################
# Constants And Setting            
########################################################
drc = 1 # 0:use colB 1: use colC 
COL_A = 0 if drc == 0 else 0 
COL_B = 1 if drc == 0 else 2
scriptDir = os.path.dirname(os.path.dirname(__file__)) #CSV file Directory
csvFileNm = 'boneVisibleTbl.csv'

########################################################
# functions                                            
########################################################
# get convert dict obj
def getDictionaryFromCsv(COL_A, COL_B):

    ret = {}
    with open(convert_file_table, newline='', encoding='cp932') as f:
        reader = csv.reader(f)
        for row in reader:
            ret[row[COL_A]] = row[COL_B]
                
        f.close()

    return ret

#Set bones visible
def setBonesVisible(armt, dict):

    currMode = 'EDIT' if bpy.context.mode == 'EDIT_ARMATURE' else bpy.context.mode
    ptn = '[Tt][Rr][Uu][Ee]'
    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    for bns in armt.data.bones:
        bnNm = bns.name
        if bnNm in dict :
            bns.hide = True if re.match(ptn, str(dict[bnNm])) else False
        else:
            continue

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    for ebns in armt.data.edit_bones:
        bnNm = ebns.name
        if bnNm in dict :
            ebns.hide = True if re.match(ptn, str(dict[bnNm])) else False
        else:
            continue

    bpy.ops.object.mode_set(mode=currMode, toggle=False)    

def _getColumn(type):
    
    if type == _NAME_CONVERT_ORIGINAL:
        return (0, 2)

    elif type == _NAME_CONVERT_REPLACED:
        return (1, 2)
    
    else:
        return (1, 2)


def set_values_main(context):

    scene = context.scene
    propgrp = scene.uil_edit_bones_by_spreadsheet_propgrp

    #Get Armature
    armt = context.active_object
    
    #get convert table
    col = _getColumn(propgrp.name_convert_type)
    dict = getDictionaryFromCsv(col[0],col[1]);        
    
    setBonesVisible(armt, dict)

    
########################################################
# main program 
########################################################
class SetBoneValuesByCSV(bpy.types.Operator):
    bl_idname = "uiler.setbonevaluesbycsv"
    bl_label = "Convert"
    bl_options = {'REGISTER', 'UNDO'}

    def validate(self, context):
        
        scene = context.scene
        propgrp = scene.uil_edit_bones_by_spreadsheet_propgrp

        obj = context.active_object

        err = "select Armature object."        
        if not obj:
            self.report({'ERROR'}, err)
            return err

        err = "select Armature object."        
        if obj.type != "ARMATURE":
            self.report({'ERROR'}, err)
            return err

        convert_tbl = propgrp.convert_table
        abspath = bpy.path.abspath(convert_tbl)
        if os.path.exists(abspath):
            global convert_file_table
            convert_file_table = abspath
        else:
            err = "file is not exist."
            self.report({'ERROR'}, err)
            return err
        
        return "VALID"
    
    def execute(self, context):

        # validate section
        validation = self.validate(context)
        
        if validation != "VALID":
            return {'FINISHED'}

        set_values_main(context)


        return {'FINISHED'}


