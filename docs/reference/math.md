# gta.math

```python
from gta import math as gmath
```

Small helpers for positions. They take `Vector3` values or plain `(x, y, z)` tuples.

```{tip}
Import it under another name (`gmath`) so it does not hide Python's own `math` module.
```

```{py:module} gta.math
```

```{py:function} distance(a, b)

Distance between two points, in metres.
```

```{py:function} distance_2d(a, b)

Distance ignoring height (as seen on the map).
```

```{py:function} length(v)

Length of a vector.
```

```{py:function} add(a, b)

`a + b`, as a tuple `(x, y, z)`.
```

```{py:function} sub(a, b)

`a - b`, as a tuple `(x, y, z)`. `sub(target, me)` is the direction from you to the target.
```

```{py:function} scale(v, s)

`v` multiplied by the number `s`.
```

```{py:function} offset_around(origin, radius, angle_rad)

A point at `radius` metres around `origin`, at the angle `angle_rad` (in radians, on the
ground plane; height unchanged). Handy to place things in a circle.
```

## Example: a ring of cones

```python
import math

from gta import math as gmath, player, world
from gta.natives import object as object_natives


def on_start():
    center = player.current().ped.position
    model = world.load_model("prop_roadcone02a")
    if not model:
        return
    for i in range(12):
        x, y, z = gmath.offset_around(center, 6.0, i * 2 * math.pi / 12)
        object_natives.CREATE_OBJECT(model, x, y, z - 1.0, False, False, False)
    world.release_model(model)
```

The game also has its own maths natives (`misc.GET_DISTANCE_BETWEEN_COORDS`, `builtin.VDIST`...),
but these Python helpers are faster: no call into the game.
