import maya.cmds as cmds

def setup():
    # set up rotation driver
    
    sels = cmds.ls(sl=1)

    driver = sels[0]
    driven = sels[1]

    md = cmds.createNode('multiplyDivide', n=f'{driver}_to_{driven}_rotationBlend_md')
    cmds.setAttr(f'{md}.operation', 1)
    cmds.connectAttr(f'{driver}.r', f'{md}.input1')
    cmds.setAttr(f'{md}.input2', 0.5, 0.5, 0.5)
    cmds.connectAttr(f'{md}.output', f'{driven}.r')

def remove():
    # remove rotation driver

    sels = cmds.ls(sl=1)

    for sel in sels:
        md = cmds.listConnections(f'{sel}.r', scn=1, type='multiplyDivide')
        cmds.delete(md)
