import bpy
import csv
import os

from . import common

########################################################
# Constants And Setting            
########################################################
convert_file_table = ""

_NAME_CONVERT_ORIGINAL = common.NAME_CONVERT_ORIGINAL
_NAME_CONVERT_REPLACED = common.NAME_CONVERT_REPLACED

########################################################
# functions                                            
########################################################
# get convert dict obj
def getConvertDictionaryFromCsv(COL_A, COL_B):

    ret = {}
    with open(convert_file_table, newline='', encoding='cp932') as f:
        reader = csv.reader(f)
        for row in reader:
            ret[row[COL_A]] = row[COL_B]
                
        f.close()

    return ret

#Rename Bones
def renameBones(armt, dict):

   for bns in armt.data.bones:
        bnNm = bns.name
        if bnNm in dict :
            if common.isEmptyStr(dict[bnNm]):
                continue
            
            bns.name = dict[bnNm]
        else:
            continue

def _getColumn(type):
    
    if type == _NAME_CONVERT_REPLACED:
        return (0, 1)
    
    elif type == _NAME_CONVERT_ORIGINAL:
        return (1, 0)
    
    else:
        return (0, 1)

def renameBonesMain(context):
    
    scene = context.scene
    propgrp = scene.uil_edit_bones_by_spreadsheet_propgrp

    #Get Armature
    armt = context.active_object
    
    #get convert table
    col = _getColumn(propgrp.name_convert_type)
    dict = getConvertDictionaryFromCsv(col[0], col[1]);        
    
    #Rename bones
    renameBones(armt, dict);
    
########################################################
# main program 
########################################################
class ConvertBonesNameByCSV(bpy.types.Operator):
    bl_idname = "uiler.convertbonesnamebycsv"
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

        scene = context.scene
        propgrp = scene.uil_edit_bones_by_spreadsheet_propgrp

        renameBonesMain(context)


        return {'FINISHED'}

