import re
import os
from datetime import datetime

#########################################################
# Constants
LETTERS_CASE_TYPE_UPPER = "ABC"
LETTERS_CASE_TYPE_LOWER = "abc"

NAME_CONVERT_ORIGINAL = "Original"
NAME_CONVERT_REPLACED = "Replaced"

WRITE_CSV_CLEAN = "Clean"
WRITE_CSV_ADD = "Add"
WRITE_CSV_UPDATE = "Update"

#########################################################
# Class
#########################################################


class BoneNameElements:

    bonename = ""
    basename = ""
    numid = ""
    basename_nonLR = ""
    lr_id = ""
    isPrefix = False
    isSuffix = False
    isLeft = False
    isRight = False
    isMirror = False
    lr_id_inv = ""
    mirror_bonename = ""


#########################################################
# Functions
#########################################################
# return BoneNameElements
def getNameElements(bone):

    nonNumberNm = bone.basename
    num = bone.name.replace(nonNumberNm, "")
    baseNm = ""
    mirrBoneNm = None
    chr = ""
    mirrChr = ""
    isPrefix = False
    isSuffix = False
    isLeft = False
    isRight = False
    isMirror = False

    res = re.match("^(L[._\- ]|Left)(.+)", nonNumberNm, re.IGNORECASE)
    if res:
        chr = res.group(1)
        baseNm = res.group(2)
        isPrefix = True
        isLeft = True

    res = re.match("(.+)(?=([._\- ]L|[._\- ]?Left)$)", nonNumberNm, re.IGNORECASE)
    if res:
        chr = res.group(2)
        baseNm = res.group(1)
        isSuffix = True
        isLeft = True

    res = re.match("^(R[._\- ]|Right)(.+)", nonNumberNm, re.IGNORECASE)
    if res:
        chr = res.group(1)
        baseNm = res.group(2)
        isPrefix = True
        isRight = True

    res = re.match("(.+)(?=([._\- ]R|[._\- ]?Right)$)", nonNumberNm, re.IGNORECASE)
    if res:
        chr = res.group(2)
        baseNm = res.group(1)
        isSuffix = True
        isRight = True

    if isPrefix or isSuffix:
        isMirror = True

    if isPrefix:

        if isLeft:
            # Left to Right
            if chr == "Left":
                mirrChr = "Right"
            elif chr == "LEFT":
                mirrChr = "RIGHT"
            elif chr == "left":
                mirrChr = "right"
            else:
                res = re.match("(L)([._\- ])", chr, re.IGNORECASE)
                if res.group(1) == "l":
                    mirrChr = "r" + res.group(2)
                elif res.group(1) == "L":
                    mirrChr = "R" + res.group(2)

        if isRight:
            # Right to Left
            if chr == "Right":
                mirrChr = "Left"
            elif chr == "RIGHT":
                mirrChr = "LEFT"
            elif chr == "right":
                mirrChr = "left"
            else:
                res = re.match("(R)([._\- ])", chr, re.IGNORECASE)
                if res.group(1) == "r":
                    mirrChr = "l" + res.group(2)
                elif res.group(1) == "R":
                    mirrChr = "L" + res.group(2)

        mirrBoneNm = mirrChr + baseNm + num

    if isSuffix:

        if isLeft:
            # Left to Right
            if chr == "Left":
                mirrChr = "Right"
            elif chr == "LEFT":
                mirrChr = "RIGHT"
            elif chr == "left":
                mirrChr = "right"
            else:
                res = re.match("([._\- ])(L)", chr, re.IGNORECASE)
                if res.group(2) == "l":
                    mirrChr = res.group(1) + "r"
                elif res.group(2) == "L":
                    mirrChr = res.group(1) + "R"

        if isRight:

            # Right to Left
            if chr == "Right":
                mirrChr = "Left"
            elif chr == "RIGHT":
                mirrChr = "LEFT"
            elif chr == "right":
                mirrChr = "left"
            else:
                res = re.match("([._\- ])(R)", chr, re.IGNORECASE)
                if res.group(2) == "r":
                    mirrChr = res.group(1) + "l"
                elif res.group(2) == "R":
                    mirrChr = res.group(1) + "L"

        mirrBoneNm = baseNm + mirrChr + num

    ret = BoneNameElements()
    ret.bonename = bone.name
    ret.basename = nonNumberNm
    ret.numid = num
    ret.basename_nonLR = baseNm
    ret.lr_id = chr
    ret.isPrefix = isPrefix
    ret.isSuffix = isSuffix
    ret.isLeft = isLeft
    ret.isRight = isRight
    ret.isMirror = isMirror
    ret.lr_id_inv = mirrChr
    ret.mirror_bonename = mirrBoneNm

    return ret

#     return (bone.name, nonNumberNm, num, baseNm, chr, isPrefix, isSuffix, isLeft, isRight, isMirror, mirrChr, mirrBoneNm)


def constructBoneName(baseNm, chr, num, isPrefix, isSuffix):

    if isPrefix:

        return chr + baseNm + num

    elif isSuffix:

        return baseNm + chr + num

    else:

        return baseNm + num


def getPaddingStringByDigit(num, padding):

    fPtn = "{0:0" + str(padding) + "d}"

    return fPtn.format(num)


# idx is 0-origin
def getAlphabetByNumber(idx, type):

    stChr = _alphaBetStartChrNum(type)
    ret = []

    mod = idx % 26
    i = mod + stChr
    ret.append(chr(i))
    next = (idx - mod) / 26

    while next != 0:
        mod = (next - 1) % 26
        i = mod + stChr
        ret.append(chr(int(i)))
        next = (next - 1 - mod) / 26

    ret.reverse()
    return "".join(ret)


def _alphaBetStartChrNum(type):

    if type == LETTERS_CASE_TYPE_UPPER:
        return 65
    else:
        return 97


def isEmptyStr(str):

    if str == "" or str is None:
        return True
    else:
        return False


def isVisiblePoseBone(bone):

    if not bone:
        return False

    data = bone.id_data.data

    bLayers = []
    bIdx = 0
    for isLayer in bone.bone.layers:

        if isLayer:
            bLayers.append(bIdx)

        bIdx = bIdx + 1

    for bLayer in bLayers:

        return data.layers[bLayer] and not bone.bone.hide

    return False


def isVisibleBone(bone):

    if not bone:
        return False

    data = bone.id_data

    bLayers = []
    bIdx = 0
    for isLayer in bone.layers:

        if isLayer:
            bLayers.append(bIdx)

        bIdx = bIdx + 1

    for bLayer in bLayers:

        return data.layers[bLayer] and not bone.hide

    return False


def getBackupFileNameByDate(orgNm, dt):

    base, ext = os.path.splitext(orgNm)

    return base + "_bkup" + dt.strftime("%Y%m%d%H%M%S") + ext


def getBackupFileName(orgNm):

    return getBackupFileNameByDate(orgNm, datetime.today())
