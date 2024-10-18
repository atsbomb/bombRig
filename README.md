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
