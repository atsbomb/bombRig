# bombRig simpler
# IK chain 3 joints
# select exactly 4 objects: parent of IK, IK start joint, IK mid joint and IK end joint

import maya.cmds as cmds

def run():

    sels = cmds.ls(sl=1)
    #all = sels.pop(0)
    parent = sels.pop(0)

    cmds.select(cl=1)
    sj = cmds.joint(n=f'{sels[0]}_ik_jnt')
    cmds.matchTransform(sj, sels[0], position=1, rotation=1)
    cmds.makeIdentity(sj, apply=1, translate=1, rotate=1, scale=1)
    cmds.select(sj)
    mj = cmds.joint(n=f'{sels[1]}_ik_jnt')
    cmds.matchTransform(mj, sels[1], position=1, rotation=1)
    cmds.makeIdentity(mj, apply=1, translate=1, rotate=1, scale=1)
    cmds.select(mj)
    ej = cmds.joint(n=f'{sels[2]}_ik_jnt')
    cmds.matchTransform(ej, sels[2], position=1, rotation=1)
    cmds.makeIdentity(ej, apply=1, translate=1, rotate=1, scale=1)

    sjl = cmds.spaceLocator(n=f'{sels[0]}_ik_loc')[0]
    group = cmds.group(sjl, n=f'{sels[0]}_root_ik_grp')
    cmds.parentConstraint(parent, group, mo=0)
    cmds.delete(cmds.pointConstraint(sj, sjl, mo=0))
    cmds.pointConstraint(sjl, sj, mo=0)

    ikh, ee = cmds.ikHandle(sj=sj, ee=ej)

    ikhl = cmds.spaceLocator(n=f'{sels[2]}_ik_loc')[0]
    cmds.pointConstraint(ikhl, ikh)
    polel = cmds.spaceLocator(n=f'{sels[1]}_pole_loc')[0]
    cmds.poleVectorConstraint(polel, ikh)

    mainGroup = cmds.group(group, sj, ikh, ikhl, polel, n=f'{sels[2]}_ik_loc_grp')
    #cmds.parentConstraint(all, mainGroup, mo=1)

    for p in zip([sels[2], sels[1]], [ikhl, polel]):
        for t in range(int(cmds.playbackOptions(q=1, min=1)), int(cmds.playbackOptions(q=1, max=1)) + 1):
            cmds.currentTime(t)
            cmds.xform(p[1], ws=1, t=cmds.xform(p[0], q=1, ws=1, t=1), ro=cmds.xform(p[0], q=1, ws=1, ro=1))
            cmds.setKeyframe(p[1])

    cmds.currentTime(int(cmds.playbackOptions(q=1, min=1)))

    #for p in zip(locs, sels):
    for p in zip([sj, mj], [sels[0], sels[1]]):
        skipRot = []
        if cmds.getAttr(p[1] + '.rx', l=1):
            skipRot.append('x')
        if cmds.getAttr(p[1] + '.ry', l=1):
            skipRot.append('y')
        if cmds.getAttr(p[1] + '.rz', l=1):
            skipRot.append('z')

        #cmds.parentConstraint(p[0], p[1], st=skipTrans, sr=skipRot, mo=0)
        cmds.parentConstraint(p[0], p[1], st=['x', 'y', 'z'], sr=skipRot, mo=1)

    cmds.orientConstraint(ikhl, sels[2], mo=1)

    cmds.hide([sj, ikh, group])

    cmds.delete([ikhl, polel], staticChannels=1)
    cmds.filterCurve([ikhl, polel])

    cmds.select([ikhl, polel])

