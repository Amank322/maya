import maya.cmds as cmds

def create_controls_on_selected_joints(normal_axis='X', ctrl_size=1.5, parent_joint=True):
    axis_map = {
        'X': [1, 0, 0],
        'Y': [0, 1, 0],
        'Z': [0, 0, 1]
    }

    normal = axis_map.get(normal_axis, [1, 0, 0])
    selected_joints = cmds.ls(selection=True, type='joint')
    
    if not selected_joints:
        cmds.warning("Please select at least one joint.")
        return

    for joint in selected_joints:
        # Create control curve
        ctrl_name = joint.replace('_JNT', '_CTRL') if '_JNT' in joint else joint + '_CTRL'
        ctrl = cmds.circle(name=ctrl_name, normal=normal, radius=ctrl_size)[0]

        # Create an offset group
        offset_grp = cmds.group(empty=True, name=ctrl + '_GRP')

        # Parent control under group
        cmds.parent(ctrl, offset_grp)

        # Match group to joint
        cmds.delete(cmds.parentConstraint(joint, offset_grp, mo=False))

        # Freeze control transforms
        cmds.makeIdentity(ctrl, apply=True, t=1, r=1, s=1, n=0)

        # Optionally parent joint under control
        if parent_joint:
            cmds.parent(joint, ctrl)

        print(f"Created {ctrl} (size {ctrl_size}, normal {normal_axis}) for joint {joint}")

# ============================
# UI Function
# ============================

def show_control_ui():
    if cmds.window("ctrlMakerWin", exists=True):
        cmds.deleteUI("ctrlMakerWin")

    window = cmds.window("ctrlMakerWin", title="Control Creator", sizeable=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")

    cmds.text(label="Select Controller Normal Axis:")

    # Option menu for normal axis
    normal_option = cmds.optionMenu("ctrlNormalOption", width=150)
    cmds.menuItem(label='X')
    cmds.menuItem(label='Y')
    cmds.menuItem(label='Z')

    # Float field for controller size
    cmds.text(label="Enter Controller Size:")
    size_field = cmds.floatField("ctrlSizeField", value=1.5, minValue=0.01)

    # Checkbox for parenting
    parent_check = cmds.checkBox("parentJointCheck", label="Parent Joint under Controller", value=True)

    # Create control button
    cmds.button(label="Create Controls", height=40, bgc=(0.2, 0.6, 0.3), 
        command=lambda *_: create_controls_on_selected_joints(
            cmds.optionMenu(normal_option, query=True, value=True),
            cmds.floatField(size_field, query=True, value=True),
            cmds.checkBox(parent_check, query=True, value=True)
        ))

    cmds.setParent("..")
    cmds.showWindow(window)

# Run the UI
show_control_ui()
