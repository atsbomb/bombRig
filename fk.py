# bombRig simpler
# FK chain

sels = cmds.ls(sl=1)
parent = sels.pop(0)
locs = []

for sel in sels:
    loc = cmds.spaceLocator(n=f'{sel}_fk_loc')[0]
    cmds.xform(loc, ws=1, t=cmds.xform(sel, q=1, ws=1, t=1), ro=cmds.xform(sel, q=1, ws=1, ro=1))
    locs.append(loc)

for i in range(1, len(locs)):
    cmds.parent(locs[i], locs[i-1])

cmds.group(locs[0], n=f'{sels[0]}_fk_loc_grp')
cmds.parentConstraint(parent, group)

for loc in locs:
    currentMatrix = cmds.xform(loc, q=1, matrix=1)
    cmds.setAttr(f'{loc}.offsetParentMatrix', *currentMatrix, type='matrix')
    cmds.setAttr(f'{loc}.t', 0, 0, 0)
    cmds.setAttr(f'{loc}.r', 0, 0, 0)
    cmds.setAttr(f'{loc}.s', 1, 1, 1)

for p in zip(sels, locs):
    for t in range(int(cmds.playbackOptions(q=1, min=1)), int(cmds.playbackOptions(q=1, max=1)) + 1):
        cmds.currentTime(t)
        cmds.xform(p[1], ws=1, t=cmds.xform(p[0], q=1, ws=1, t=1), ro=cmds.xform(p[0], q=1, ws=1, ro=1))
        cmds.setKeyframe(p[1])

for p in zip(locs, sels):
    cmds.parentConstraint(p[0], p[1], mo=0)

cmds.select(locs)