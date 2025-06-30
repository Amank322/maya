import maya.cmds as cmds

def create_basic_locators(add_fingers=False, add_feet=False, add_face=False, locator_size=1.0, side_option='Both'):
    locator_data = {
        "C_Root_LOC": (0, 10, 0),
        "C_Spine_LOC": (0, 12, 0),
        "C_Spine01_LOC": (0, 13, 0),
        "C_Spine02_LOC": (0, 14, 0),
        "C_Spine03_LOC": (0, 15, 0),
        "C_Chest_LOC": (0, 16, 0),
        "C_Neck_LOC": (0, 17, 0),
        "C_Neck01_LOC": (0, 17.5, 0),
        "C_Head_LOC": (0, 18.5, 0),
    }

    if add_face:
        locator_data.update({
            "C_Face_LOC": (0, 19, 1),
            "C_FaceEnd_LOC": (0, 19.5, 1),
            "C_Mouth_LOC": (0, 18.8, 1.2),
            "C_MouthEnd_LOC": (0, 19, 1.2),
        })

    left_data = {
        "L_Shoulder_LOC": (-2, 16.5, 0),
        "L_Hand_LOC": (-3, 16.5, 0),
        "L_Elbow_LOC": (-4, 16.5, 0),
        "L_Wrist_LOC": (-6, 16.5, 0),
        "L_Hips_LOC": (-1, 10, 0),
        "L_Knee_LOC": (-1, 6, 0),
        "L_Ankle_LOC": (-1, 2, 0),
        "L_Tip_LOC": (-1, 2, 2),
    }

    right_data = {}
    if side_option in ['Right', 'Both']:
        right_data = {k.replace('L_', 'R_'): (-v[0], v[1], v[2]) for k, v in left_data.items() if 'L_Hand_LOC' not in k}
        right_data['R_Hand_LOC'] = (3, 16.5, 0)

    if add_fingers:
        left_fingers = {
            "L_Thumb_LOC": (-6.5, 16.3, 0.5),
            "L_Thumb01_LOC": (-7.2, 16.1, 0.7),
            "L_Thumb02_LOC": (-7.8, 15.9, 0.9),
            "L_Index_LOC": (-6.8, 16.4, 0.2),
            "L_Index01_LOC": (-7.5, 16.4, 0.2),
            "L_Index02_LOC": (-8.2, 16.4, 0.2),
            "L_Middle_LOC": (-6.9, 16.5, 0.0),
            "L_Middle01_LOC": (-7.6, 16.5, 0.0),
            "L_Middle02_LOC": (-8.3, 16.5, 0.0),
            "L_Pinky_LOC": (-6.5, 16.6, -0.5),
            "L_Pinky01_LOC": (-7.1, 16.6, -0.6),
            "L_Pinky02_LOC": (-7.7, 16.6, -0.7)
        }
        if side_option in ['Left', 'Both']:
            left_data.update(left_fingers)
        if side_option in ['Right', 'Both']:
            right_data.update({k.replace('L_', 'R_'): (-v[0], v[1], v[2]) for k, v in left_fingers.items()})

    if add_feet:
        if side_option in ['Left', 'Both']:
            left_data.update({"L_Toe_LOC": (-1, 2, 1)})
        if side_option in ['Right', 'Both']:
            right_data.update({"R_Toe_LOC": (1, 2, 1), "R_Tip_LOC": (1, 2, 2)})

    if side_option in ['Left', 'Both']:
        locator_data.update(left_data)
    if side_option in ['Right', 'Both']:
        locator_data.update(right_data)

    for name, pos in locator_data.items():
        if not cmds.objExists(name):
            loc = cmds.spaceLocator(name=name)[0]
            cmds.setAttr(loc + "Shape.localScaleX", locator_size)
            cmds.setAttr(loc + "Shape.localScaleY", locator_size)
            cmds.setAttr(loc + "Shape.localScaleZ", locator_size)
            cmds.xform(loc, ws=True, t=pos)

    hierarchy = [
        ("C_Spine_LOC", "C_Root_LOC"),
        ("C_Spine01_LOC", "C_Spine_LOC"),
        ("C_Spine02_LOC", "C_Spine01_LOC"),
        ("C_Spine03_LOC", "C_Spine02_LOC"),
        ("C_Chest_LOC", "C_Spine03_LOC"),
        ("C_Neck_LOC", "C_Chest_LOC"),
        ("C_Neck01_LOC", "C_Neck_LOC"),
        ("C_Head_LOC", "C_Neck01_LOC"),
    ]

    if add_face:
        hierarchy.extend([
            ("C_Face_LOC", "C_Head_LOC"),
            ("C_FaceEnd_LOC", "C_Face_LOC"),
            ("C_Mouth_LOC", "C_Head_LOC"),
            ("C_MouthEnd_LOC", "C_Mouth_LOC"),
        ])

    arm_leg = [
        ("L_Hand_LOC", "L_Shoulder_LOC"),
        ("L_Elbow_LOC", "L_Hand_LOC"),
        ("L_Wrist_LOC", "L_Elbow_LOC"),
        ("R_Hand_LOC", "R_Shoulder_LOC"),
        ("R_Elbow_LOC", "R_Hand_LOC"),
        ("R_Wrist_LOC", "R_Elbow_LOC"),
        ("L_Knee_LOC", "L_Hips_LOC"),
        ("L_Ankle_LOC", "L_Knee_LOC"),
        ("R_Knee_LOC", "R_Hips_LOC"),
        ("R_Ankle_LOC", "R_Knee_LOC"),
        ("L_Tip_LOC", "L_Ankle_LOC"),
        ("R_Tip_LOC", "R_Ankle_LOC")
    ]

    if add_feet:
        arm_leg.extend([
            ("L_Toe_LOC", "L_Ankle_LOC"),
            ("R_Toe_LOC", "R_Ankle_LOC"),
            ("L_Tip_LOC", "L_Toe_LOC"),
            ("R_Tip_LOC", "R_Toe_LOC")
        ])

    hierarchy.extend(arm_leg)

    if side_option in ['Left', 'Both']:
        hierarchy.extend([
            ("L_Hips_LOC", "C_Root_LOC"),
            ("L_Shoulder_LOC", "C_Chest_LOC")
        ])
    if side_option in ['Right', 'Both']:
        hierarchy.extend([
            ("R_Hips_LOC", "C_Root_LOC"),
            ("R_Shoulder_LOC", "C_Chest_LOC")
        ])

    if add_fingers:
        fingers = [
            ("L_Thumb_LOC", "L_Wrist_LOC"),
            ("L_Thumb01_LOC", "L_Thumb_LOC"),
            ("L_Thumb02_LOC", "L_Thumb01_LOC"),
            ("L_Index_LOC", "L_Wrist_LOC"),
            ("L_Index01_LOC", "L_Index_LOC"),
            ("L_Index02_LOC", "L_Index01_LOC"),
            ("L_Middle_LOC", "L_Wrist_LOC"),
            ("L_Middle01_LOC", "L_Middle_LOC"),
            ("L_Middle02_LOC", "L_Middle01_LOC"),
            ("L_Pinky_LOC", "L_Wrist_LOC"),
            ("L_Pinky01_LOC", "L_Pinky_LOC"),
            ("L_Pinky02_LOC", "L_Pinky01_LOC"),
        ]
        if side_option in ['Left', 'Both']:
            hierarchy.extend(fingers)
        if side_option in ['Right', 'Both']:
            r_fingers = [(a.replace("L_", "R_"), b.replace("L_", "R_")) for a, b in fingers]
            hierarchy.extend(r_fingers)

    for child, parent in hierarchy:
        if cmds.objExists(child) and cmds.objExists(parent):
            cmds.parent(child, parent)

    cmds.select(clear=True)
    print("✅ Basic human locators created.")

def mirror_selected_locators(side):
    if side not in ['Left', 'Right']:
        cmds.warning("❗ Please choose 'Left' or 'Right' for mirroring.")
        return

    prefix = 'L_' if side == 'Left' else 'R_'
    opp_prefix = 'R_' if side == 'Left' else 'L_'

    all_locs = cmds.ls(type='transform')
    side_locs = [loc for loc in all_locs if loc.startswith(prefix) and loc.endswith('_LOC')]

    if not side_locs:
        cmds.warning(f"No {side} side locators found.")
        return

    mirrored_map = {}

    for loc in side_locs:
        mirrored_name = loc.replace(prefix, opp_prefix)

        matrix = cmds.xform(loc, q=True, ws=True, m=True)
        matrix[12] *= -1
        matrix[0] *= -1
        matrix[1] *= -1
        matrix[2] *= -1

        if cmds.objExists(mirrored_name):
            mirror_loc = mirrored_name
        else:
            mirror_loc = cmds.spaceLocator(name=mirrored_name)[0]

        if cmds.listRelatives(mirror_loc, parent=True):
            cmds.parent(mirror_loc, w=True)

        cmds.xform(mirror_loc, ws=True, m=matrix)
        mirrored_map[loc] = mirror_loc

    for src, mirrored in mirrored_map.items():
        parent = cmds.listRelatives(src, parent=True)
        if parent:
            mirrored_parent = parent[0].replace(prefix, opp_prefix)
            if cmds.objExists(mirrored_parent):
                try:
                    cmds.parent(mirrored, mirrored_parent)
                except:
                    cmds.warning(f"⚠ Could not parent {mirrored} under {mirrored_parent}")

    cmds.select(list(mirrored_map.values()), r=True)
    print(f"✅ Mirrored {side} locators and selected them.")

def create_joints_from_locators_with_radius(radius=1.0, mirror=True):
    selection = cmds.ls(selection=True, type="transform")
    locators = [loc for loc in selection if loc.endswith("_LOC")]

    if not locators:
        locators = cmds.ls("*_LOC", type="transform")

    loc_to_joint = {}
    for loc in locators:
        cmds.select(clear=True)
        pos = cmds.xform(loc, q=True, ws=True, t=True)
        joint_name = loc.replace("_LOC", "_JNT")
        if not cmds.objExists(joint_name):
            jnt = cmds.joint(name=joint_name, p=pos, radius=radius)
            loc_to_joint[loc] = jnt

    for loc, joint in loc_to_joint.items():
        parent = cmds.listRelatives(loc, parent=True)
        if parent and parent[0] in loc_to_joint:
            cmds.parent(joint, loc_to_joint[parent[0]])

    all_joints = list(loc_to_joint.values())
    mirror_candidates = [j for l, j in loc_to_joint.items() if "L_" in l]

    if all_joints:
        top_joints = [j for j in all_joints if not cmds.listRelatives(j, parent=True)]
        for top in top_joints:
            cmds.select(top, hi=True)
            cmds.joint(e=True, oj='xyz', sao='yup', ch=True, zso=True)

    if mirror:
        top_joints = [j for j in mirror_candidates if not cmds.listRelatives(j, parent=True)]
        for jnt in top_joints:
            mirrored = cmds.mirrorJoint(jnt, mirrorYZ=True, mirrorBehavior=True, searchReplace=("L", "R"))
            if mirrored:
                print(f"✅ Mirrored {jnt} ➜ {mirrored[0]}")

    cmds.select(clear=True)
    print("✅ Joint creation complete.")

def open_joint_ui():
    if cmds.window("jointFromLocUI", exists=True):
        cmds.deleteUI("jointFromLocUI")

    cmds.window("jointFromLocUI", title="Create Joints", widthHeight=(320, 500))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    cmds.text(label="Enter Locator Size:")
    locator_size_field = cmds.floatField(value=1.0)

    cmds.text(label="Enter Joint Radius:")
    radius_field = cmds.floatField(value=1.0)

    mirror_check = cmds.checkBox(label="Mirror Side Joints (L ↔ R)", value=True)
    finger_check = cmds.checkBox(label="Include Finger Locators", value=True)
    foot_check = cmds.checkBox(label="Include Foot Locators", value=True)
    face_check = cmds.checkBox(label="Include Face Locators", value=True)

    cmds.separator(h=10, style='in')
    cmds.text(label="Select Side:")
    side_menu = cmds.optionMenu()
    cmds.menuItem(label="Both")
    cmds.menuItem(label="Left")
    cmds.menuItem(label="Right")

    cmds.button(label="Create Human Locators", height=30,
        command=lambda *args: create_basic_locators(
            side_option=cmds.optionMenu(side_menu, q=True, value=True),
            locator_size=cmds.floatField(locator_size_field, q=True, value=True),
            add_fingers=cmds.checkBox(finger_check, q=True, value=True),
            add_feet=cmds.checkBox(foot_check, q=True, value=True),
            add_face=cmds.checkBox(face_check, q=True, value=True)
        ))

    cmds.separator(h=10, style='in')

    cmds.button(label="Create Joints from Locators", height=40,
        command=lambda *args: create_joints_from_locators_with_radius(
            cmds.floatField(radius_field, q=True, value=True),
            cmds.checkBox(mirror_check, q=True, value=True)
        ))

    cmds.button(label="Mirror Selected Side Locators", height=30,
        command=lambda *args: mirror_selected_locators(cmds.optionMenu(side_menu, q=True, value=True)))

    cmds.showWindow("jointFromLocUI")

open_joint_ui()
