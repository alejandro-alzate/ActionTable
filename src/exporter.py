import bpy

def export_to_lua(filepath='/tmp/anim.lua', use_seconds=True, actions=None):
    print(f"[LuaExport] Exporting to {filepath}...")
    if actions is None:
        actions = bpy.data.actions

    scene = bpy.context.scene
    fps = scene.render.fps / scene.render.fps_base if scene.render.fps_base else scene.render.fps
    sec_per_frame = 1.0 / fps if use_seconds else 1.0

    def to_time(frames):
        return frames * sec_per_frame

    def lua_escape(s: str) -> str:
        return s.replace('\\', '\\\\').replace('"', '\\"')

    lines = []
    lines.append('local Animations = {')

    for action in actions:
        print(f"[LuaExport] Processing action: {action.name}")
        lines.append(f"\t[\"{lua_escape(action.name)}\"] = {{")
        for fcurve in sorted(action.fcurves, key=lambda fc: (fc.data_path, fc.array_index)):
            channel_name = f"{fcurve.data_path}[{fcurve.array_index}]"
            lines.append(f"\t\t[\"{lua_escape(channel_name)}\"] = {{")
            kps = sorted(fcurve.keyframe_points, key=lambda k: k.co.x)
            for kp in kps:
                t = to_time(kp.co.x)
                v = kp.co.y
                ipo = kp.interpolation
                if ipo == 'BEZIER':
                    lhx, lhy = kp.handle_left.x, kp.handle_left.y
                    rhx, rhy = kp.handle_right.x, kp.handle_right.y
                    tL = to_time(lhx)
                    tK = t
                    tR = to_time(rhx)
                    EPS = 1e-8
                    in_dt = max(EPS, (tK - tL))
                    out_dt = max(EPS, (tR - tK))
                    in_tan = (v - lhy) / in_dt
                    out_tan = (rhy - v) / out_dt
                    lines.append(
                        f"\t\t\t{{ {t:.6f}, \"{ipo}\", {v:.6f}, {in_tan:.6f}, {out_tan:.6f} }},"
                    )
                else:
                    lines.append(f"\t\t\t{{ {t:.6f}, \"{ipo}\", {v:.6f} }},")
            lines.append('\t\t},')
        lines.append('\t},')

    lines.append('}\n\nreturn Animations')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"[LuaExport] Export finished: {filepath}")

def register():
    pass

def unregister():
    pass
