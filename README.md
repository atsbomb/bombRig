# bombRig

Functions to create a temporary rig for hierarchical skeleton (or similar sorts), while retaining the existing animation on the source object.

# Installation

Clone this repository and add the path to  `MAYA_MODULE_PATH` in your `Maya.env`. Create a shelf button for one off use or write some snippets of codes with predetermined selection if you are dealing with same structured skeleton multiple times i.e. UE mannequin.

# Functions

- FK

Select multiple objects in order and run.
```
import importlib
import bombRig.fk
importlib.reload(bombRig.fk)
bombRig.fk.run()
```

- IK

Select exactly 4 objects and run. First selection should be parent of the following IK chain, the last 3 objects will be the actual IK chain (start, mid, end).
```
import importlib
import bombRig.ik
importlib.reload(bombRig.ik)
bombRig.ik.run()
```

- Spine

Select more than 3 objects in order. First is considered hip, the last is considered chest, while the rest is spine. Creates 2 points pseudo spline IK set up. Tweak the blend value of orientConstraint for the middle joints to achieve the preferred bend ratio for the spine.

Note: this function is destructive. Original animatio won't be kept exactly the same.
```
import importlib
import bombRig.spine
importlib.reload(bombRig.spine)
bombRig.spine.run()
```




