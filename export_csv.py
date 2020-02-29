import bpy
import csv
import os
import re
import shutil
from collections import OrderedDict

from . import common

########################################################
# Constants And Setting
########################################################
_NAME_CONVERT_ORIGINAL = common.NAME_CONVERT_ORIGINAL
_NAME_CONVERT_REPLACED = common.NAME_CONVERT_REPLACED

_WRITE_CSV_CLEAN = common.WRITE_CSV_CLEAN
_WRITE_CSV_ADD = common.WRITE_CSV_ADD
_WRITE_CSV_UPDATE = common.WRITE_CSV_UPDATE

COL_A_NAME_O = 0
COL_B_NAME_R = 1
COL_C_PBONE_HIDE = 2

COMMENT_ROW = ("#BoneName(Original)", "BoneName(Replace)", "Bone.hide(Pose)")

########################################################
# functions
########################################################


# type:_NAME_CONVERT_ORIGINAL / _NAME_CONVERT_REPLACED
def getConvertDictionaryFromCsv(type, bones):

    ret = OrderedDict()

    if not os.path.exists(convert_file_table):
        return ret

    with open(convert_file_table, newline='', encoding='cp932') as f:
        reader = csv.reader(f)
        for row in reader:
            if re.match("#.+", row[COL_A_NAME_O]):
                # Ignore comment row
                continue

            data = (row[COL_A_NAME_O], row[COL_B_NAME_R], row[COL_C_PBONE_HIDE])
            key = ""
            if type == _NAME_CONVERT_ORIGINAL:
                key = row[COL_A_NAME_O]
            else:
                key = row[COL_B_NAME_R]

            if common.isEmptyStr(key):
                key = str(row)

            ret[key] = data

        f.close()

    return ret


# write csv
def writeToCsv(rows):

    ret = OrderedDict()
    with open(convert_file_table, 'w', newline='', encoding='cp932') as f:
        writer = csv.writer(f)

        # write comment
        writer.writerow(COMMENT_ROW)

        for row in rows:
            # print(row)
            writer.writerow(row)

        f.close()

    return ret


def _convertBoolToCellString(atr):

    if atr:
        return "TRUE"
    else:
        return "FALSE"


def getWriteRowData(conv_type, write_type, dict, bones):

    ret = []
    newRows = []
    newDict = dict

    for bone in bones:

        if conv_type == _NAME_CONVERT_ORIGINAL:
            row = (bone.name, "", _convertBoolToCellString(bone.hide))
        else:
            row = ("", bone.name, _convertBoolToCellString(bone.hide))

        if write_type == _WRITE_CSV_UPDATE and bone.name in dict:

            if conv_type == _NAME_CONVERT_ORIGINAL:
                row = (bone.name, dict[bone.name][1], _convertBoolToCellString(bone.hide))
            else:
                row = (dict[bone.name][0], bone.name, _convertBoolToCellString(bone.hide))

            newDict[bone.name] = row

        else:

            newRows.append(row)

    if write_type != _WRITE_CSV_CLEAN:

        for key in newDict.keys():

            ret.append(newDict[key])

        ret.extend(newRows)

    else:

        ret = newRows

    return ret


def write_csv_main(context):

    scene = context.scene
    propgrp = scene.uil_edit_bones_by_spreadsheet_propgrp
    conv_type = propgrp.name_convert_type
    write_type = propgrp.csv_export_type

    # Get Armature
    armt = context.active_object
    bones = armt.data.bones

    # get convert table
    dict = getConvertDictionaryFromCsv(conv_type, bones)

    # Write to csv
    rows = getWriteRowData(conv_type, write_type, dict, bones)
    writeToCsv(rows)


class WriteBoneValuesByCSV(bpy.types.Operator):
    bl_idname = "uiler.writebonevaluesbycsv"
    bl_label = "Export CSV"
    bl_description = "Export csv file"    
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

            # backup file
            backup = common.getBackupFileName(abspath)
            shutil.copyfile(abspath, backup)
            print("backup file:" + backup)

        else:

            newfilepath = bpy.path.ensure_ext(convert_tbl, ".csv")
            abspath = bpy.path.abspath(newfilepath)
            print("newfile:" + newfilepath)

        global convert_file_table
        convert_file_table = abspath

        return "VALID"

    def execute(self, context):

        # validate section
        validation = self.validate(context)

        if validation != "VALID":
            return {'FINISHED'}

        write_csv_main(context)

        return {'FINISHED'}
