# Functions

- Simple FK

Select multiple objects in order and run. First selection will be the parent of the following FK constrols.
```
import importlib
import bombRig.fk
importlib.reload(bombRig.fk)
bombRig.fk.run()
```

- Simple IK

Select exactly 5 objects and run. First selection should be the all character control, second selection should be parent of the following IK chain, the last 3 objects will be the actual IK chain (start, mid, end).
```
import importlib
import bombRig.ik
importlib.reload(bombRig.ik)
bombRig.ik.run()
```
