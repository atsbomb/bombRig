# 2 point spine IK
# first be hip, last be chest

import maya.cmds as cmds

def run():
    sels = cmds.ls(sl=1)
    hipJoint = sels.pop(0)
    chestJoint = sels.pop(-1)

    hipLoc = cmds.spaceLocator(n=f'{hipJoint}_spine_loc')[0]
    chestLoc = cmds.spaceLocator(n=f'{chestJoint}_spine_loc')[0]

    for p in zip([hipJoint, chestJoint], [hipLoc, chestLoc]):
        for t in range(int(cmds.playbackOptions(q=1, min=1)), int(cmds.playbackOptions(q=1, max=1)) + 1):
            cmds.currentTime(t)
            cmds.xform(p[1], ws=1, t=cmds.xform(p[0], q=1, ws=1, t=1), ro=cmds.xform(p[0], q=1, ws=1, ro=1))
            cmds.setKeyframe(p[1])

    cmds.cutKey(f'{chestLoc}.t')
    cmds.pointConstraint(chestJoint, chestLoc, mo=0)

    midLocs = []
    for j in sels:
        loc = cmds.spaceLocator(n=f'{j}_spine_loc')[0]
        midLocs.append(loc)
        cmds.pointConstraint(j, loc, mo=0)
        cmds.hide(loc)

    for l in midLocs:
        cmds.orientConstraint(hipLoc, chestLoc, l, mo=0)

    # attach loc xform to source
    cmds.pointConstraint(hipLoc, hipJoint)
    cmds.orientConstraint(hipLoc, hipJoint)

    for p in zip(midLocs, sels):
        cmds.orientConstraint(p[0], p[1], mo=0)

    cmds.orientConstraint(chestLoc, chestJoint)

    # grouping
    cmds.group([hipLoc, chestLoc, *midLocs], n=f'{hipJoint}_spine_loc_grp')
    cmds.select(hipLoc, chestLoc)