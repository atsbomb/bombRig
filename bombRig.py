#     __                    __    ____  _          _   __            
#    / /_  ____  ____ ___  / /_  / __ \(_)___ _   / | / /__ _      __
#   / __ \/ __ \/ __ `__ \/ __ \/ /_/ / / __ `/  /  |/ / _ \ | /| / /
#  / /_/ / /_/ / / / / / / /_/ / _, _/ / /_/ /  / /|  /  __/ |/ |/ / 
# /_.___/\____/_/ /_/ /_/_.___/_/ |_/_/\__, /  /_/ |_/\___/|__/|__/  
#                                     /____/                         

import maya.cmds as cmds

def createFkChain(targets=[], parent=''):
    # takes targets list for FK generation
    # parent generated FK controls under given parent node

    startTime = cmds.playbackOptions(q=1, minTime=1)
    endTime = cmds.playbackOptions(q=1, maxTime=1)

    fkLocs = []
    fkLocGroups = []
    constraints = []

    # reverse list order, so that we can make controllers from bottom of hierarchy
    targets.reverse()

    for target in targets:
        fkLoc = cmds.spaceLocator(name=f'{target}_fk_loc')[0]
        fkLocs.append(fkLoc)
        fkLocGroup = cmds.group(fkLoc, name=f'{target}_fk_loc_group')
        fkLocGroups.append(fkLocGroup)
        cmds.matchTransform(fkLocGroup, target, pos=1, rot=1)
        # parent previously created locator group to newly created locator
        if len(fkLocGroups) > 1:
            cmds.parent(fkLocGroups[-2], fkLoc)
        constraint = cmds.parentConstraint(target, fkLoc, mo=0)[0]
        constraints.append(constraint)

    cmds.parentConstraint(parent, fkLocGroups[-1], mo=1)

    # bake locators
    cmds.bakeResults(fkLocs, time=(startTime, endTime), simulation=0)
    cmds.delete(fkLocs, staticChannels=1)
    cmds.delete(constraints)

    # constrain target joint back
    for jointAndLoc in zip(fkLocs, targets):
        cmds.parentConstraint(jointAndLoc[0], jointAndLoc[1])

    # add to set
    if not cmds.objExists('animLocs'):
        cmds.sets(n='animLocs', empty=1)
    #cmds.sets(fkLocs)
    for fkLoc in fkLocs:
        cmds.sets(fkLoc, e=1, include='animLocs')

def createIkChain(targets=[], parent='', ikOffset=50):
    # provide exactly 3 target objects for RP IK chain

    startTime = cmds.playbackOptions(q=1, minTime=1)
    endTime = cmds.playbackOptions(q=1, maxTime=1)
    curTime = cmds.currentTime(q=1)
    
    ikLocs = []
    ikLocGroups = []
    constraints = []
    
    cmds.currentTime(startTime)
    
    tempIkGroup = cmds.group(n=targets[0]+'_tempIk_grp', empty=1)
    
    # create joint chain
    cmds.select(clear=1)
    ikJointTop = cmds.joint(n=targets[0]+'_ik_jnt')
    cmds.matchTransform(ikJointTop, targets[0], pos=1, rot=1)
    cmds.makeIdentity(ikJointTop, apply=1, t=1, r=1, s=1)
    ikJointMid = cmds.joint(n=targets[1]+'_ik_jnt')
    cmds.matchTransform(ikJointMid, targets[1], pos=1, rot=1)
    cmds.makeIdentity(ikJointMid, apply=1, t=1, r=1, s=1)
    ikJointEnd = cmds.joint(n=targets[2]+'_ik_jnt')
    cmds.matchTransform(ikJointEnd, targets[2], pos=1, rot=1)
    cmds.makeIdentity(ikJointEnd, apply=1, t=1, r=1, s=1)
    
    # create IK handle
    ikHandle, ikEffector = cmds.ikHandle(n=f'{targets[0]}_ik_temp', startJoint=ikJointTop, endEffector=ikJointEnd)
    
    #create temp controls
    locTop = cmds.spaceLocator(name=targets[0]+'_top_loc')
    locTopGroup = cmds.group(locTop, name=targets[0]+'_loc_top_grp')
    cmds.parentConstraint(parent, locTopGroup)
    poleVectorLoc = cmds.spaceLocator(name=targets[1]+'_poleVector_loc')
    ikLoc = cmds.spaceLocator(n=targets[2]+'_ik_loc')
    cmds.poleVectorConstraint(poleVectorLoc, ikHandle)
    cmds.hide(locTop)
    cmds.parent(ikJointTop, tempIkGroup)
    cmds.parent(ikHandle, tempIkGroup)
    cmds.parent(locTopGroup, tempIkGroup)
    cmds.parent(poleVectorLoc, tempIkGroup)
    cmds.parent(ikLoc, tempIkGroup)
    
    #match temp controls to main controls
    constraint = cmds.parentConstraint(targets[0], locTop, mo=0)
    constraints.append(constraint)
    constraint = cmds.parentConstraint(targets[2], ikLoc, mo=0)
    constraints.append(constraint)
    
    # bake IK
    cmds.bakeResults(ikLoc, locTop, time=(startTime,endTime), simulation=0, preserveOutsideKeys=1)
    
    # pole vector fix
    midPoint = [
                (cmds.xform(targets[0], q=1, ws=1, t=1)[0] + cmds.xform(targets[2], q=1, ws=1, t=1)[0]) / 2,
                (cmds.xform(targets[0], q=1, ws=1, t=1)[1] + cmds.xform(targets[2], q=1, ws=1, t=1)[1]) / 2,
                (cmds.xform(targets[0], q=1, ws=1, t=1)[2] + cmds.xform(targets[2], q=1, ws=1, t=1)[2]) / 2
                ]
    
    aimLoc = cmds.spaceLocator(n="tempAimLoc")
    cmds.move(midPoint[0], midPoint[1], midPoint[2], aimLoc, a=1, ws=1)
    cmds.aimConstraint(targets[2], aimLoc, mo=0, aimVector=[0,1,0], upVector=[1,0,0], worldUpType="object", worldUpObject=targets[1])
    cmds.delete(aimLoc, constraints=1)
    cmds.move(ikOffset,0,0, aimLoc, r=1, objectSpace=1, worldSpaceDistance=1)
    cmds.parentConstraint(targets[1], aimLoc, mo=1)
    
    for t in range(int(startTime), int(endTime) + 1):
        cmds.currentTime(t, e=1)

        midPoint = [
                    (cmds.xform(targets[0], q=1, ws=1, t=1)[0] + cmds.xform(targets[2], q=1, ws=1, t=1)[0]) / 2,
                    (cmds.xform(targets[0], q=1, ws=1, t=1)[1] + cmds.xform(targets[2], q=1, ws=1, t=1)[1]) / 2,
                    (cmds.xform(targets[0], q=1, ws=1, t=1)[2] + cmds.xform(targets[2], q=1, ws=1, t=1)[2]) / 2
                    ]

        loc = cmds.spaceLocator()
        cmds.move(midPoint[0], midPoint[1], midPoint[2], loc, a=1, ws=1)
        cmds.aimConstraint(targets[2], loc, mo=0, aimVector=[0,1,0], upVector=[1,0,0], worldUpType="object", worldUpObject=aimLoc[0])
        cmds.delete(loc, constraints=1)
        cmds.move(ikOffset,0,0, loc, r=1, objectSpace=1, worldSpaceDistance=1)
        
        cmds.matchTransform(poleVectorLoc, loc, position=1)
        cmds.setKeyframe(poleVectorLoc)
        
        cmds.delete(loc)
    
    cmds.delete(aimLoc)
    
    cmds.cutKey(poleVectorLoc, attribute = ['rx', 'ry', 'rz'], clear=1)
    cmds.matchTransform(poleVectorLoc, targets[1], rotation=1)
    for attr in ['.rx', '.ry', '.rz', '.sx', '.sy', '.sz']:
        cmds.setAttr(poleVectorLoc[0] + attr, lock=1)
    
    for c in constraints:
        cmds.delete(c)
    
    cmds.pointConstraint(locTop, ikJointTop)
    cmds.hide(locTop)
    cmds.pointConstraint(ikLoc, ikHandle)
    cmds.orientConstraint(ikLoc, ikJointEnd)

    #constrain controls, skipping locked channels
    lockedAttr = []
    lockedPos = []
    lockedRot = []
    lockedAttr = cmds.listAttr(targets[0], locked=1, scalar=1)
    if lockedAttr:
        for attribute in lockedAttr:
            if attribute.startswith('translate'):
                attrName = str(attribute[9:])
                lockedPos.append(attrName.lower())
            elif attribute.startswith('rotate'):
                attrName = str(attribute[6:])
                lockedRot.append(attrName.lower())
    cmds.parentConstraint(ikJointTop, targets[0], skipTranslate=lockedPos, skipRotate=lockedRot, mo=1)
    
    lockedAttr = []
    lockedPos = []
    lockedRot = []
    lockedAttr = cmds.listAttr(targets[1], locked=1, scalar=1)
    if lockedAttr:
        for attribute in lockedAttr:
            if attribute.startswith('translate'):
                attrName = str(attribute[9:])
                lockedPos.append(attrName.lower())
            elif attribute.startswith('rotate'):
                attrName = str(attribute[6:])
                lockedRot.append(attrName.lower())
    cmds.parentConstraint(ikJointMid, targets[1], skipTranslate=lockedPos, skipRotate=lockedRot, mo=1)
    
    lockedAttr = []
    lockedPos = []
    lockedRot = []
    lockedAttr = cmds.listAttr(targets[2], locked=1, scalar=1)
    if lockedAttr:
        for attribute in lockedAttr:
            if attribute.startswith('translate'):
                attrName = str(attribute[9:])
                lockedPos.append(attrName.lower())
            elif attribute.startswith('rotate'):
                attrName = str(attribute[6:])
                lockedRot.append(attrName.lower())       
    cmds.orientConstraint(ikLoc, targets[2], skip=lockedRot, mo=1)
    
    cmds.select(ikLoc, poleVectorLoc)
    cmds.delete(staticChannels=1)
    cmds.filterCurve()
    
    # add to set
    if not cmds.objExists('animLocs'):
        cmds.sets(n='animLocs', empty=1)
    for ikLoc in [ikLoc, poleVectorLoc]:
        cmds.sets(ikLoc, e=1, include='animLocs')

    cmds.currentTime(curTime)
