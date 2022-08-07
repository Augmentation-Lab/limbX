"""
VISION SCRIPT
uses ml to process camera data
"""

from classes import TargetObj, TargetPos

def get_obj_label(targetObj):
    assert isinstance(targetObj, TargetObj), "targetObj must be of type TargetObj"
    objLabel = "unknown"
    # implement object labeling here
    return objLabel

def get_rel_pos(targetObj):
    assert isinstance(targetObj, TargetObj), "targetObj must be of type TargetObj"
    # map targetObj.imgData and targetObj.objLabel onto depth camera map to determine targetObj.relPos
    targetRelPos = TargetPos(x=0, y=0, z=0)
    return targetRelPos