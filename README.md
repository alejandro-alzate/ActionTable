# _ActionTables_

Short for Blender actions to lua tables.

# Overview

Action tables is a simple addon made in the name of fixing a very
annoying pain point with blender animation:
Get it out of blender on a human readable format.

Currently is VERY bare bones as it only extracts the raw keyframes
found on the timeline, no modifiers, no drivers, **_Nothing_** outside keyframes.

(This is planned to be added on the future, but I gotta get the hang of the Blender UI API first)

# Getting started

Add the addon as you normally would on blender with any other addon.

Where in blender 4x there's the QoL Feature of just dropping the zip on the window.

Then a prompt will show up asking if you wanna add the addon, say yes of course.

Once enabled on your tool panel should appear a `ActionTable` tab.

You'll need to understand the basics of the addon, don't they're pretty easy to understand:

- Global: Export all actions inside the current blender file.
- Export List: When `Global` is turned off only the actions on the list will be exported.
    - It has to additional buttons:
        - `+`: Adds the actions of the currently selected object.
        - `-`: Removes the currently selected action from the list.
- Autofill: It fills the `Export List` with all actions, this is useful when you want to export all except a couple ones.
- Export path: Where the exported file will be written to, has a handy folder icon to use the blender ui itself to select the path.
- Export to lua: Exports the actions to the designated file.

# Schema

This addon closely follows the format of blender's action system.
It will create a `Animations` table and return it with the following format:

```
Animations
└───Actions
    └───Targets
        └───Keyframes
```

### Keyframe

The most important part of the schema is the keyframe, it holds the necessary info of a keyframe on the given target with this format:

```
{time, interpolation, value, handle1?, handle2?}
```

| Name            | Type     | Description                                                                          |
| --------------- | -------- | ------------------------------------------------------------------------------------ |
| `time`          | `number` | Where the keyframe is located in the timeline.                                       |
| `interpolation` | `string` | Has 3 possible values: `"LINEAR`, `"CONSTANT"`, `"BEZIER"`. It indicates the easing. |
| `handle1?`      | `number` | When `interpolation` is `"BEZIER"` this field has the first handle value             |
| `handle2?`      | `number` | When `interpolation` is `"BEZIER"` this field has the second handle value            |

### Target

This one is quite simple they're named after the property that is being animated.
You're supposed to access them like a driver by passing the string of the property you intend to read,
These are common examples:

```
"location[0]"
"location[1]"
"location[2]"
"rotation_euler[0]"
"rotation_euler[1]"
"rotation_euler[2]"
"scale[0]"
"scale[1]"
"scale[2]"
```

### Action

This contains arrays of animated objects. when you insert a keyframe let's say the `Z` position on the default cube blender silently creates a object called an `Action` which inherits the name of the object when is created, and then gets linked back to the object where you inserted the keyframe.

It's a bit confusing at first but it probably has some technical reason behind why blender does it like that.

My best guess it's that because pretty much every field on blender can be animated, The animation of the value itself is a generic object to make it easy to plug it wherever the hell you want.

```
(Mesh) Cube
└───(Animation) Animation
	└───(Action) CubeAction
```

`CubeAction` is what gets exported with the `ActionTables` addon hence the name.

### Animation

Once you made your first animation and then export it, the file should look like this:

```lua
local Animations = {
	["CubeAction"] = {
		["location[2]"] = {
			{ 0.041667, "BEZIER", 0.000000, 0.000000, 0.000000 },
		},
	},
}

return Animations
```

You then can access the values for example like this:

```lua
Animations["CubeAction"]["location[2]"]
```

You could technically access them like this, but it's rather sketchy and prone to fail if done incorrectly.

```lua
Animations.CubeAction["location[2]"]
```
