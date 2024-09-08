# bombRig simpler
# IK chain 3 joints
# select exactly 5 objects: all, parent of IK, IK start joint, IK mid joint and IK end joint

import maya.cmds as cmds

sels = cmds.ls(sl=1)
all = sels.pop(0)
parent = sels.pop(0)

cmds.select(cl=1)
sj = cmds.joint(p=cmds.xform(sels[0], q=1, ws=1, t=1), n=f'{sels[0]}_ik_jnt')
mj = cmds.joint(p=cmds.xform(sels[1], q=1, ws=1, t=1), n=f'{sels[1]}_ik_jnt')
ej = cmds.joint(p=cmds.xform(sels[2], q=1, ws=1, t=1), n=f'{sels[2]}_ik_jnt')

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

mainGroup = cmds.group(group, sj, ikh, ikhl, polel, n=f'{sels[2]}_ik_loc_main_grp')
cmds.parentConstraint(all, mainGroup, mo=1)

for p in zip([sels[2], sels[1]], [ikhl, polel]):
    cmds.currentTime(cmds.playbackOptions(q=1, min=1))
    cmds.xform(p[1], ws=1, t=cmds.xform(p[0], q=1, ws=1, t=1), ro=cmds.xform(p[0], q=1, ws=1, ro=1))
    currentMatrix = cmds.xform(p[1], q=1, matrix=1)
    cmds.setAttr(f'{p[1]}.offsetParentMatrix', *currentMatrix, type='matrix')
    cmds.setAttr(f'{p[1]}.t', 0, 0, 0)
    cmds.setAttr(f'{p[1]}.r', 0, 0, 0)
    cmds.setAttr(f'{p[1]}.s', 1, 1, 1)

for p in zip([sels[2], sels[1]], [ikhl, polel]):
    for t in range(int(cmds.playbackOptions(q=1, min=1)), int(cmds.playbackOptions(q=1, max=1)) + 1):
        cmds.currentTime(t)
        cmds.xform(p[1], ws=1, t=cmds.xform(p[0], q=1, ws=1, t=1), ro=cmds.xform(p[0], q=1, ws=1, ro=1))
        cmds.setKeyframe(p[1])

for p in zip([sj, mj], [sels[0], sels[1]]):
    cmds.parentConstraint(p[0], p[1], st=['x', 'y', 'z'], mo=1)

cmds.orientConstraint(ikhl, sels[2], mo=0)
