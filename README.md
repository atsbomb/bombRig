# bombRig

Functions to create a temporary rig for hierarchical skeleton (or similar sorts), while retaining the existing animation on the source object.

# Installation

Clone this repository and add `MAYA_MODULE_PATH` to your `Maya.env`. Best if you create a shelf button for each functions.

# Functions

- Simple FK

Select multiple objects in order and run.
```
import importlib
import bombRig.fk
importlib.reload(bombRig.fk)
bombRig.fk.run()
```

- Simple IK

Select exactly 4 objects and run. First selection should be parent of the following IK chain, the last 3 objects will be the actual IK chain (start, mid, end).
```
import importlib
import bombRig.ik
importlib.reload(bombRig.ik)
bombRig.ik.run()
```
