"""
state_machine.py -- State machine (DFA/NFA/process state) diagram builder.

Supports:
  - States (regular, initial, accepting/final)
  - Transitions with labels (input symbol / condition)
  - Self-loop transitions
  - Initial state marker (filled circle with arrow)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Any

from pydantic import BaseModel, model_validator
from reportlab.graphics.shapes import Path

if TYPE_CHECKING:
    pass

from . import shapes as S
from .base import DiagramBase
from .layout import auto_layout_graph
from .theme import DiagramTheme

_STATE_R = 22.0  # default state circle radius
_STATE_LABEL_MAX_W = 82.0
_TRANSITION_LABEL_MAX_W = 96.0
_Point = tuple[float, float]
_Rect = tuple[float, float, float, float]


class _SMState(BaseModel):
    id: str
    label: str
    x: float | None = None
    y: float | None = None
    initial: bool = False
    accepting: bool = False

    @model_validator(mode="after")
    def validate_id(self) -> "_SMState":
        if not self.id.strip():
            raise ValueError("State id must not be empty")
        return self


class _SMTransition(BaseModel):
    from_id: str
    to_id: str
    label: str = ""
    pill: bool = False
    offset: float = 0.0


class StateMachine(DiagramBase):
    """
    State machine diagram builder. Suitable for DFA, NFA, and OS process states.

    Usage::

        sm = StateMachine(width=380, height=180, caption="Simple DFA")
        sm.state("q0", "q0", x=60, y=90, initial=True)
        sm.state("q1", "q1", x=190, y=90)
        sm.state("q2", "q2", x=320, y=90, accepting=True)
        sm.transition("q0", "q1", label="a")
        sm.transition("q1", "q2", label="b")
        sm.transition("q1", "q0", label="a")
        sm.transition("q2", "q2", label="a,b")
        story.extend(sm.as_flowable())
    """

    def __init__(
        self,
        width: float,
        height: float,
        theme: DiagramTheme | None = None,
        caption: str | None = None,
        state_r: float = _STATE_R,
        direction: str | None = None,
        state_label_max_width: float = _STATE_LABEL_MAX_W,
        transition_label_max_width: float = _TRANSITION_LABEL_MAX_W,
    ) -> None:
        super().__init__(width, height, theme, caption)
        self.state_r = state_r
        self.direction = direction
        self.state_label_max_width = state_label_max_width
        self.transition_label_max_width = transition_label_max_width
        self._states: list[_SMState] = []
        self._transitions: list[_SMTransition] = []
        self._state_index: dict[str, _SMState] = {}
        self._custom_drawers: dict[str, Callable[..., None]] = {}

    def state(
        self,
        id: str,
        label: str,
        x: float | None = None,
        y: float | None = None,
        initial: bool = False,
        accepting: bool = False,
        custom_draw: Callable[..., None] | None = None,
    ) -> "StateMachine":
        """Add a state circle. initial=True draws an entry arrow; accepting=True draws double circle."""
        if id in self._state_index:
            raise ValueError(f"Duplicate state id: '{id}'")
        s = _SMState(id=id, label=label, x=x, y=y, initial=initial, accepting=accepting)
        self._states.append(s)
        self._state_index[id] = s
        if custom_draw is not None:
            self._custom_drawers[id] = custom_draw
        return self

    def _state_label_lines(self, st: _SMState) -> list[str]:
        """Return measured label lines that fit inside a state circle."""
        t = self.theme
        return S.wrap_text(
            st.label,
            max_width=self.state_label_max_width,
            font=t.font_name_bold,
            size=9.0,
        )

    def _transition_label_lines(self, label: str) -> list[str]:
        """Return measured transition-label lines to reduce edge-label overlap."""
        t = self.theme
        return S.wrap_text(
            label,
            max_width=self.transition_label_max_width,
            font=t.font_name_italic,
            size=8.0,
        )

    def transition(
        self,
        from_id: str,
        to_id: str,
        label: str = "",
        pill: bool = False,
        offset: float = 0.0,
    ) -> "StateMachine":
        """
        Add a transition arrow from from_id to to_id.
        Use from_id == to_id for a self-loop.
        """
        for sid in (from_id, to_id):
            if sid not in self._state_index:
                raise ValueError(
                    f"State id '{sid}' not found. Add state before transitioning."
                )
        self._transitions.append(
            _SMTransition(
                from_id=from_id, to_id=to_id, label=label, pill=pill, offset=offset
            )
        )
        return self

    def _state_radius(self, st: _SMState) -> float:
        t = self.theme
        lines = self._state_label_lines(st)
        w = (
            max(S.text_width(line, t.font_name_bold, 9.0) for line in lines)
            if lines
            else 0.0
        )
        needed_r = (w + 16.0) / 2.0
        h_padding = len(lines) * 11.0 + 8.0
        return max(self.state_r, needed_r, h_padding / 2.0)

    def _draw_transition(self, tr: _SMTransition) -> None:
        t = self.theme
        fs = self._state_index[tr.from_id]
        ts = self._state_index[tr.to_id]
        assert fs.x is not None and fs.y is not None
        assert ts.x is not None and ts.y is not None
        rf = self._state_radius(fs)
        rt = self._state_radius(ts)

        if tr.from_id == tr.to_id:
            # Self-loop: symmetric arc above the state circle
            import math
            theta1 = 2.0 * math.pi / 3.0  # 120 deg
            theta2 = math.pi / 3.0        # 60 deg

            sx = fs.x + rf * math.cos(theta1)
            sy = fs.y + rf * math.sin(theta1)
            ex = fs.x + rf * math.cos(theta2)
            ey = fs.y + rf * math.sin(theta2)

            offset_val = 18.0
            c1x = sx - offset_val * 0.5
            c1y = sy + offset_val * 1.5
            c2x = ex + offset_val * 0.5
            c2y = ey + offset_val * 1.5

            p = Path()
            p.moveTo(sx, sy)
            p.curveTo(c1x, c1y, c2x, c2y, ex, ey)
            p.fillColor = None
            p.strokeColor = S._hex(t.transition_color)
            p.strokeWidth = 1.3
            self._add(p)

            # Draw arrowhead at the end (ex, ey) pointing tangent to the curve
            arrow_size = 6.0
            self._add(
                S._arrowhead_polygon(
                    ex,
                    ey,
                    -offset_val * 0.5,
                    -offset_val * 1.5,
                    arrow_size,
                    True,
                    t.transition_color,
                )
            )

            font_size = 8.0
            lines = self._transition_label_lines(tr.label) if tr.label else [""]
            tw = max(
                S.text_width(line, t.font_name_italic, font_size) for line in lines
            )
            lh = font_size * 1.2
            th = font_size + (len(lines) - 1) * lh

            # Center label directly above the self-loop
            lx = fs.x
            ly = fs.y + rf + offset_val * 1.5 + 4.0

            if tr.pill:
                pad_x = 3.5
                pad_y = 2.0
                pill_w = tw + 2 * pad_x
                pill_h = th + 2 * pad_y
                rx, ry = self.get_non_overlapping_position(lx - pill_w / 2.0, ly, pill_w, pill_h)
                pill_text_color = S.get_contrast_color(
                    t.surface, light_fg=t.transition_label_color, dark_fg="#0f172a"
                )
                self._add(
                    S.pill_label(
                        rx,
                        ry,
                        "\n".join(lines),
                        font=t.font_name_italic,
                        size=font_size,
                        text_color=pill_text_color,
                        bg_color=t.surface,
                        border_color=t.state_stroke,
                        pad_x=pad_x,
                        pad_y=pad_y,
                    )
                )
            else:
                rx, ry = self.get_non_overlapping_position(lx - tw / 2.0, ly, tw + 4.0, th + 2.0)
                loop_text_color = S.get_contrast_color(
                    t.bg, light_fg=t.transition_label_color, dark_fg="#0f172a"
                )
                if len(lines) > 1:
                    first_baseline = ry + (len(lines) - 1) * lh / 2.0
                    self._add(
                        S.multiline_label(
                            rx,
                            first_baseline,
                            lines,
                            font=t.font_name_italic,
                            size=font_size,
                            color=loop_text_color,
                            line_height=lh,
                            anchor="middle",
                        )
                    )
                else:
                    self._add(
                        S.label(
                            rx + tw / 2.0,
                            ry,
                            tr.label,
                            font=t.font_name_italic,
                            size=font_size,
                            color=loop_text_color,
                            anchor="middle",
                        )
                    )
            return

        # Setup base vectors
        dx, dy = ts.x - fs.x, ts.y - fs.y
        length = (dx**2 + dy**2) ** 0.5 or 1
        ux, uy = dx / length, dy / length
        px, py = -uy, ux  # perpendicular direction

        import math

        if tr.offset == 0.0:
            # Straight transition
            x1_shifted = fs.x + ux * rf
            y1_shifted = fs.y + uy * rf
            x2_shifted = ts.x - ux * rt
            y2_shifted = ts.y - uy * rt

            self._add(
                S.arrow_line(
                    x1_shifted,
                    y1_shifted,
                    x2_shifted,
                    y2_shifted,
                    color=t.transition_color,
                    width=1.3,
                    arrow_end=True,
                    arrow_size=7.0,
                )
            )
            lx = (x1_shifted + x2_shifted) / 2.0
            ly = (y1_shifted + y2_shifted) / 2.0
            shift_x = px * 10
            shift_y = py * 10
            lx += shift_x
            ly += shift_y
        else:
            # Curved transition: Quadratic Bezier curve
            mx = (fs.x + ts.x) / 2.0
            my = (fs.y + ts.y) / 2.0
            cx = mx + px * tr.offset
            cy = my + py * tr.offset

            # Vector from fs to control point C
            v1x, v1y = cx - fs.x, cy - fs.y
            v1_len = math.hypot(v1x, v1y)
            if v1_len > 1e-9:
                u1x, u1y = v1x / v1_len, v1y / v1_len
            else:
                u1x, u1y = ux, uy
            x1_shifted = fs.x + u1x * rf
            y1_shifted = fs.y + u1y * rf

            # Vector from ts to control point C
            v2x, v2y = cx - ts.x, cy - ts.y
            v2_len = math.hypot(v2x, v2y)
            if v2_len > 1e-9:
                u2x, u2y = v2x / v2_len, v2y / v2_len
            else:
                u2x, u2y = -ux, -uy
            x2_shifted = ts.x + u2x * rt
            y2_shifted = ts.y + u2y * rt

            # End direction vector (tangent at P2 pointing from C to P2)
            dx_end, dy_end = x2_shifted - cx, y2_shifted - cy
            dist_end = math.hypot(dx_end, dy_end)
            if dist_end > 1e-9:
                ux_end, uy_end = dx_end / dist_end, dy_end / dist_end
            else:
                ux_end, uy_end = ux, uy

            arrow_size = 7.0
            # Shorten the curve to end at the base of the arrowhead
            ex = x2_shifted - ux_end * arrow_size
            ey = y2_shifted - uy_end * arrow_size

            # Convert quadratic control point C to cubic control points C1, C2
            c1x = x1_shifted + (2.0 / 3.0) * (cx - x1_shifted)
            c1y = y1_shifted + (2.0 / 3.0) * (cy - y1_shifted)
            c2x = ex + (2.0 / 3.0) * (cx - ex)
            c2y = ey + (2.0 / 3.0) * (cy - ey)

            # Draw the curve
            path = Path()
            path.moveTo(x1_shifted, y1_shifted)
            path.curveTo(c1x, c1y, c2x, c2y, ex, ey)
            path.fillColor = None
            path.strokeColor = S._hex(t.transition_color)
            path.strokeWidth = 1.3
            self._add(path)

            # Draw arrowhead
            self._add(
                S._arrowhead_polygon(
                    x2_shifted,
                    y2_shifted,
                    dx_end,
                    dy_end,
                    arrow_size,
                    True,
                    t.transition_color,
                )
            )

            # Label position: midpoint of the curve (t=0.5)
            lx = (x1_shifted + 2.0 * cx + x2_shifted) / 4.0
            ly = (y1_shifted + 2.0 * cy + y2_shifted) / 4.0
            label_sign = 1.0 if tr.offset >= 0 else -1.0
            shift_x = px * 10 * label_sign
            shift_y = py * 10 * label_sign
            lx += shift_x
            ly += shift_y

        if tr.label:
            font_size = 8.0
            lines = self._transition_label_lines(tr.label)
            tw = max(
                S.text_width(line, t.font_name_italic, font_size) for line in lines
            )
            lh = font_size * 1.2
            th = font_size + (len(lines) - 1) * lh

            # Adjust label position to prevent overlaps using layout-aware shifting
            is_tb = getattr(self, "_active_direction", "LR") == "TB"
            if is_tb:
                # Vertical layout: shift label horizontally based on shift direction
                if shift_x > 0.0:
                    lx = lx + tw / 2.0 + 4.0
                elif shift_x < 0.0:
                    lx = lx - tw / 2.0 - 4.0
            else:
                # Horizontal layout: shift label vertically based on shift direction
                if shift_y > 0.0:
                    ly = ly + th - font_size * 0.2
                elif shift_y < 0.0:
                    ly = ly - font_size * 0.8

            if tr.pill:
                pad_x = 3.5
                pad_y = 2.0
                pill_w = tw + 2 * pad_x
                pill_h = th + 2 * pad_y
                rx, ry = self.get_non_overlapping_position(lx, ly, pill_w, pill_h)
                pill_text_color = S.get_contrast_color(
                    t.surface, light_fg=t.transition_label_color, dark_fg="#0f172a"
                )
                self._add(
                    S.pill_label(
                        rx,
                        ry,
                        "\n".join(lines),
                        font=t.font_name_italic,
                        size=font_size,
                        text_color=pill_text_color,
                        bg_color=t.surface,
                        border_color=t.state_stroke,
                        pad_x=pad_x,
                        pad_y=pad_y,
                    )
                )
            else:
                rx, ry = self.get_non_overlapping_position(lx, ly, tw + 4.0, th + 2.0)
                transition_text_color = S.get_contrast_color(
                    t.bg, light_fg=t.transition_label_color, dark_fg="#0f172a"
                )
                if len(lines) > 1:
                    first_baseline = ry + (len(lines) - 1) * lh / 2.0
                    self._add(
                        S.multiline_label(
                            rx,
                            first_baseline,
                            lines,
                            font=t.font_name_italic,
                            size=font_size,
                            color=transition_text_color,
                            line_height=lh,
                            anchor="middle",
                        )
                    )
                else:
                    self._add(
                        S.label(
                            rx,
                            ry,
                            tr.label,
                            font=t.font_name_italic,
                            size=font_size,
                            color=transition_text_color,
                            anchor="middle",
                        )
                    )

    def get_transition_geometry(
        self, tr: _SMTransition, offset: float
    ) -> dict[str, Any]:
        fs = self._state_index[tr.from_id]
        ts = self._state_index[tr.to_id]
        rf = self._state_radius(fs)
        rt = self._state_radius(ts)

        if fs.x is None or fs.y is None or ts.x is None or ts.y is None:
            return {"curve_pts": [], "label_box": None, "apex": (0.0, 0.0)}

        import math

        if tr.from_id == tr.to_id:
            # Self-loop
            cx, cy = fs.x, fs.y
            self_loop_pts: list[_Point] = []
            for angle in range(45, 136, 15):
                rad = math.radians(angle)
                self_loop_pts.append(
                    (cx + (rf + 25.0) * math.cos(rad), cy + (rf + 25.0) * math.sin(rad))
                )

            font_size = 8.0
            lines = self._transition_label_lines(tr.label) if tr.label else [""]
            t = self.theme
            tw = (
                max(S.text_width(line, t.font_name_italic, font_size) for line in lines)
                if tr.label
                else 0.0
            )
            lh = font_size * 1.2
            th = font_size + (len(lines) - 1) * lh
            lx = fs.x + rf + 18
            ly = fs.y + rf + 8
            return {
                "curve_pts": self_loop_pts,
                "label_box": (
                    (lx - tw / 2, ly - th / 2, lx + tw / 2, ly + th / 2)
                    if tr.label
                    else None
                ),
                "apex": (fs.x, fs.y + rf + 30.0),
            }

        dx, dy = ts.x - fs.x, ts.y - fs.y
        length = math.hypot(dx, dy) or 1.0
        ux, uy = dx / length, dy / length
        px, py = -uy, ux  # perpendicular direction

        mx = (fs.x + ts.x) / 2.0
        my = (fs.y + ts.y) / 2.0

        if offset == 0.0:
            x1 = fs.x + ux * rf
            y1 = fs.y + uy * rf
            x2 = ts.x - ux * rt
            y2 = ts.y - uy * rt
            cx, cy = mx, my
        else:
            cx = mx + px * offset
            cy = my + py * offset
            v1x, v1y = cx - fs.x, cy - fs.y
            v1_len = math.hypot(v1x, v1y) or 1.0
            x1 = fs.x + (v1x / v1_len) * rf
            y1 = fs.y + (v1y / v1_len) * rf

            v2x, v2y = cx - ts.x, cy - ts.y
            v2_len = math.hypot(v2x, v2y) or 1.0
            x2 = ts.x + (v2x / v2_len) * rt
            y2 = ts.y + (v2y / v2_len) * rt

        # Sample curve points
        curve_pts: list[_Point] = []
        num_samples = 10
        for i in range(num_samples + 1):
            ratio = i / num_samples
            if offset == 0.0:
                xt = x1 + ratio * (x2 - x1)
                yt = y1 + ratio * (y2 - y1)
            else:
                xt = (
                    (1 - ratio) ** 2 * x1 + 2 * (1 - ratio) * ratio * cx + ratio**2 * x2
                )
                yt = (
                    (1 - ratio) ** 2 * y1 + 2 * (1 - ratio) * ratio * cy + ratio**2 * y2
                )
            curve_pts.append((xt, yt))

        # Apex is midpoint of curve
        ax = (x1 + 2.0 * cx + x2) / 4.0
        ay = (y1 + 2.0 * cy + y2) / 4.0

        label_box = None
        if tr.label:
            font_size = 8.0
            lines = self._transition_label_lines(tr.label)
            t = self.theme
            tw = max(
                S.text_width(line, t.font_name_italic, font_size) for line in lines
            )
            lh = font_size * 1.2
            th = font_size + (len(lines) - 1) * lh

            lx = ax
            ly = ay
            label_sign = 1.0 if offset >= 0 else -1.0
            shift_x = px * 10 * label_sign
            shift_y = py * 10 * label_sign
            lx += shift_x
            ly += shift_y

            is_tb = getattr(self, "_active_direction", "LR") == "TB"
            if is_tb:
                if shift_x > 0.0:
                    lx = lx + tw / 2.0 + 4.0
                elif shift_x < 0.0:
                    lx = lx - tw / 2.0 - 4.0
            else:
                if shift_y > 0.0:
                    ly = ly + th - font_size * 0.2
                elif shift_y < 0.0:
                    ly = ly - font_size * 0.8

            label_box = (
                lx - tw / 2 - 2.0,
                ly - th / 2 - 2.0,
                lx + tw / 2 + 2.0,
                ly + th / 2 + 2.0,
            )

        return {"curve_pts": curve_pts, "label_box": label_box, "apex": (ax, ay)}

    def auto_layout(self) -> None:
        direction = getattr(self, "_active_direction", "LR")
        if direction == "TB":
            self.width = max(self.width, 350.0)
            self.height = max(self.height, 680.0)
        else:
            self.width = max(self.width, 650.0)
            self.height = max(self.height, 140.0)

        if hasattr(self, "drawing") and self.drawing:
            self.drawing.width = self.width
            self.drawing.height = self.height

        state_ids = [s.id for s in self._states]
        edges = [(t.from_id, t.to_id) for t in self._transitions if t.from_id != t.to_id]
        coords = auto_layout_graph(
            state_ids, edges, self.width, self.height, direction=direction
        )
        for s in self._states:
            if s.x is None or s.y is None:
                x, y = coords[s.id]
                if s.x is None:
                    s.x = x
                if s.y is None:
                    s.y = y

        # Compute ranks to detect linear layout
        adj: dict[str, list[str]] = {nid: [] for nid in state_ids}
        for u, v in edges:
            if u in adj and v in adj:
                adj[u].append(v)
        visited = {nid: 0 for nid in state_ids}
        back_edges = set()
        def dfs(u: str) -> None:
            visited[u] = 1
            for v in adj[u]:
                if visited[v] == 1:
                    back_edges.add((u, v))
                elif visited[v] == 0:
                    dfs(v)
            visited[u] = 2
        for nid in state_ids:
            if visited[nid] == 0:
                dfs(nid)
        dag_adj: dict[str, list[str]] = {nid: [] for nid in state_ids}
        for u in state_ids:
            for v in adj[u]:
                if (u, v) in back_edges:
                    dag_adj[v].append(u)
                else:
                    dag_adj[u].append(v)
        ranks = {nid: 0 for nid in state_ids}
        for _ in range(len(state_ids)):
            changed = False
            for u in state_ids:
                for v in dag_adj[u]:
                    if ranks[v] <= ranks[u]:
                        ranks[v] = ranks[u] + 1
                        changed = True
            if not changed:
                break

        # Check if every rank has at most one real state
        rank_counts: dict[int, int] = {}
        for nid, r in ranks.items():
            rank_counts[r] = rank_counts.get(r, 0) + 1
        is_linear = all(count <= 1 for count in rank_counts.values())

        if is_linear:
            if direction == "LR":
                center_y = self.height / 2.0
                for s in self._states:
                    s.y = center_y
            elif direction == "TB":
                center_x = self.width / 2.0
                for s in self._states:
                    s.x = center_x

        self._normalize_bounds()

    def _normalize_bounds(self) -> None:
        import math

        # Auto-calculate offsets for bidirectional or crossing transitions
        is_tb = getattr(self, "_active_direction", "LR") == "TB"
        for tr in self._transitions:
            if tr.from_id == tr.to_id:
                continue
            fs = self._state_index[tr.from_id]
            ts = self._state_index[tr.to_id]
            if fs.x is None or fs.y is None or ts.x is None or ts.y is None:
                continue

            # 1. Bidirectional check
            has_reverse = any(
                r.from_id == tr.to_id and r.to_id == tr.from_id
                for r in self._transitions
            )
            if has_reverse and tr.offset == 0.0:
                tr.offset = 22.0

            # 2. Crossing check
            if tr.offset == 0.0:
                crossed = False
                max_r = 0.0
                for s in self._states:
                    if s.id == tr.from_id or s.id == tr.to_id:
                        continue
                    if s.x is None or s.y is None:
                        continue
                    if is_tb:
                        if min(fs.y, ts.y) + 5.0 < s.y < max(fs.y, ts.y) - 5.0:
                            if abs(s.x - (fs.x + ts.x) / 2.0) < 30.0:
                                crossed = True
                                max_r = max(max_r, self._state_radius(s))
                    else:
                        if min(fs.x, ts.x) + 5.0 < s.x < max(fs.x, ts.x) - 5.0:
                            if abs(s.y - (fs.y + ts.y) / 2.0) < 30.0:
                                crossed = True
                                max_r = max(max_r, self._state_radius(s))
                if crossed:
                    desired_offset = max_r + 26.0
                    if is_tb:
                        dy = ts.y - fs.y
                        uy = dy / (math.hypot(ts.x - fs.x, dy) or 1.0)
                        px = -uy
                        if px > 0.0:
                            tr.offset = -desired_offset
                        else:
                            tr.offset = desired_offset
                    else:
                        dx = ts.x - fs.x
                        ux = dx / (math.hypot(dx, ts.y - fs.y) or 1.0)
                        py = ux
                        if py > 0.0:
                            tr.offset = -desired_offset
                        else:
                            tr.offset = desired_offset

        # Iterative repulsion collision solver
        def boxes_overlap(
            box1: _Rect | None, box2: _Rect | None, padding: float = 2.0
        ) -> bool:
            if box1 is None or box2 is None:
                return False
            x1_min, y1_min, x1_max, y1_max = box1
            x2_min, y2_min, x2_max, y2_max = box2
            return not (
                x1_max + padding < x2_min
                or x2_max + padding < x1_min
                or y1_max + padding < y2_min
                or y2_max + padding < y1_min
            )

        def point_in_box(pt: _Point, box: _Rect | None, padding: float = 2.0) -> bool:
            if box is None:
                return False
            x, y = pt
            xmin, ymin, xmax, ymax = box
            return (
                xmin - padding <= x <= xmax + padding
                and ymin - padding <= y <= ymax + padding
            )

        import math

        max_iters = 20
        for _ in range(max_iters):
            # Compute geometries with current offsets
            geoms: dict[int, dict[str, Any]] = {}
            for tr in self._transitions:
                geoms[id(tr)] = self.get_transition_geometry(tr, tr.offset)

            adjusted = False

            for i, tr1 in enumerate(self._transitions):
                g1 = geoms[id(tr1)]
                if not g1["curve_pts"]:
                    continue

                # 1. Check collision of tr1 curve with intermediate states
                for s in self._states:
                    if s.id == tr1.from_id or s.id == tr1.to_id:
                        continue
                    r = self._state_radius(s)
                    collides = any(
                        math.hypot(pt[0] - s.x, pt[1] - s.y) < r + 12.0
                        for pt in g1["curve_pts"]
                    )
                    if collides:
                        if tr1.offset == 0.0:
                            tr1.offset = -30.0
                        else:
                            sign = 1.0 if tr1.offset >= 0.0 else -1.0
                            tr1.offset += sign * 6.0
                        adjusted = True

                # 2. Check collision with other transitions
                for j, tr2 in enumerate(self._transitions):
                    if i >= j:
                        continue
                    g2 = geoms[id(tr2)]
                    if not g2["curve_pts"]:
                        continue

                    # Check label vs label overlap
                    if g1["label_box"] and g2["label_box"]:
                        if boxes_overlap(g1["label_box"], g2["label_box"], padding=4.0):
                            if abs(tr1.offset) >= abs(tr2.offset):
                                sign = 1.0 if tr1.offset >= 0.0 else -1.0
                                tr1.offset += sign * 6.0
                            else:
                                sign = 1.0 if tr2.offset >= 0.0 else -1.0
                                tr2.offset += sign * 6.0
                            adjusted = True

                    # Check curve1 vs label2
                    if g2["label_box"]:
                        if any(
                            point_in_box(pt, g2["label_box"], padding=4.0)
                            for pt in g1["curve_pts"]
                        ):
                            if abs(tr1.offset) >= abs(tr2.offset):
                                sign = 1.0 if tr1.offset >= 0.0 else -1.0
                                tr1.offset += sign * 6.0
                            else:
                                sign = 1.0 if tr2.offset >= 0.0 else -1.0
                                tr2.offset += sign * 6.0
                            adjusted = True

                    # Check curve2 vs label1
                    if g1["label_box"]:
                        if any(
                            point_in_box(pt, g1["label_box"], padding=4.0)
                            for pt in g2["curve_pts"]
                        ):
                            if abs(tr2.offset) >= abs(tr1.offset):
                                sign = 1.0 if tr2.offset >= 0.0 else -1.0
                                tr2.offset += sign * 6.0
                            else:
                                sign = 1.0 if tr1.offset >= 0.0 else -1.0
                                tr1.offset += sign * 6.0
                            adjusted = True

                    # Check curve1 vs curve2 collision (if not same endpoints)
                    if not (tr1.from_id == tr2.from_id and tr1.to_id == tr2.to_id):
                        close_count = 0
                        for pt1 in g1["curve_pts"]:
                            for pt2 in g2["curve_pts"]:
                                if math.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1]) < 10.0:
                                    close_count += 1
                        if close_count > 0:
                            if abs(tr1.offset) >= abs(tr2.offset):
                                sign = 1.0 if tr1.offset >= 0.0 else -1.0
                                tr1.offset += sign * 6.0
                            else:
                                sign = 1.0 if tr2.offset >= 0.0 else -1.0
                                tr2.offset += sign * 6.0
                            adjusted = True

            if not adjusted:
                break

        # Re-compute geometries with final resolved offsets
        final_geoms: dict[int, dict[str, Any]] = {}
        for tr in self._transitions:
            final_geoms[id(tr)] = self.get_transition_geometry(tr, tr.offset)

        # Normalization / Bounding Box adjustment with symmetric centering
        state_xs = [s.x for s in self._states if s.x is not None]
        state_ys = [s.y for s in self._states if s.y is not None]

        if not state_xs:
            return

        # Center of states before shifting
        states_cx = sum(state_xs) / len(state_xs)
        states_cy = sum(state_ys) / len(state_ys)

        # Collect all points (states, curve points, label boxes)
        all_pts = []
        for s in self._states:
            assert s.x is not None and s.y is not None
            r = self._state_radius(s)
            all_pts.append((s.x - r, s.y))
            all_pts.append((s.x + r, s.y))
            all_pts.append((s.x, s.y - r))
            all_pts.append((s.x, s.y + r))

        for tr in self._transitions:
            geom = final_geoms[id(tr)]
            for pt in geom["curve_pts"]:
                all_pts.append(pt)
            if geom["label_box"]:
                xmin, ymin, xmax, ymax = geom["label_box"]
                all_pts.append((xmin, ymin))
                all_pts.append((xmax, ymax))

        margin = 40.0
        if is_tb:
            # Center horizontally on states_cx
            left_dist = 0.0
            right_dist = 0.0
            for px, py in all_pts:
                left_dist = max(left_dist, states_cx - px)
                right_dist = max(right_dist, px - states_cx)
            max_dist_x = max(left_dist, right_dist)

            # Simple bounds for Y
            min_y = min(pt[1] for pt in all_pts)
            max_y = max(pt[1] for pt in all_pts)

            new_cx = max_dist_x + margin
            shift_x = new_cx - states_cx
            shift_y = margin - min_y

            self.width = max_dist_x * 2.0 + margin * 2.0
            self.height = max_y - min_y + margin * 2.0
        else:
            # Center vertically on states_cy
            down_dist = 0.0
            up_dist = 0.0
            for px, py in all_pts:
                down_dist = max(down_dist, states_cy - py)
                up_dist = max(up_dist, py - states_cy)
            max_dist_y = max(down_dist, up_dist)

            # Simple bounds for X
            min_x = min(pt[0] for pt in all_pts)
            max_x = max(pt[0] for pt in all_pts)

            new_cy = max_dist_y + margin
            shift_x = margin - min_x
            shift_y = new_cy - states_cy

            self.width = max_x - min_x + margin * 2.0
            self.height = max_dist_y * 2.0 + margin * 2.0

        for s in self._states:
            assert s.x is not None and s.y is not None
            s.x += shift_x
            s.y += shift_y

        if hasattr(self, "drawing") and self.drawing:
            self.drawing.width = self.width
            self.drawing.height = self.height

    def build(self) -> None:
        # 1. Compute ranks to determine layer assignments for auto-switching layout orientation
        state_ids = [s.id for s in self._states]
        edges = [(t.from_id, t.to_id) for t in self._transitions if t.from_id != t.to_id]
        adj: dict[str, list[str]] = {nid: [] for nid in state_ids}
        for u, v in edges:
            if u in adj and v in adj:
                adj[u].append(v)

        # Simple DFS to detect cycles (back-edges) and build DAG adjacency
        visited = {nid: 0 for nid in state_ids}
        back_edges = set()

        def dfs(u: str) -> None:
            visited[u] = 1
            for v in adj[u]:
                if visited[v] == 1:
                    back_edges.add((u, v))
                elif visited[v] == 0:
                    dfs(v)
            visited[u] = 2

        for nid in state_ids:
            if visited[nid] == 0:
                dfs(nid)

        dag_adj: dict[str, list[str]] = {nid: [] for nid in state_ids}
        for u in state_ids:
            for v in adj[u]:
                if (u, v) in back_edges:
                    dag_adj[v].append(u)
                else:
                    dag_adj[u].append(v)

        # Bellman-Ford ranking
        ranks = {nid: 0 for nid in state_ids}
        for _ in range(len(state_ids)):
            changed = False
            for u in state_ids:
                for v in dag_adj[u]:
                    if ranks[v] <= ranks[u]:
                        ranks[v] = ranks[u] + 1
                        changed = True
            if not changed:
                break

        # Calculate required width in horizontal layout ("LR")
        num_layers = max(ranks.values()) + 1 if ranks else 1
        max_label_w_between = {i: 0.0 for i in range(num_layers)}
        font_size = 8.0

        for tr in self._transitions:
            if tr.from_id == tr.to_id:
                continue
            r1 = ranks[tr.from_id]
            r2 = ranks[tr.to_id]
            span_start = min(r1, r2)
            span_end = max(r1, r2)

            lines = self._transition_label_lines(tr.label) if tr.label else [""]
            tw = (
                max(
                    S.text_width(line, self.theme.font_name_italic, font_size)
                    for line in lines
                )
                if tr.label
                else 0.0
            )

            for k in range(span_start, span_end):
                max_label_w_between[k] = max(max_label_w_between[k], tw)

        # Compute max radius per rank
        max_r_per_rank = {i: 0.0 for i in range(num_layers)}
        for st in self._states:
            r = self._state_radius(st)
            max_r_per_rank[ranks[st.id]] = max(max_r_per_rank[ranks[st.id]], r)

        # Sum up distances between adjacent ranks
        margin = 35.0
        width_lr = 100.0  # margin_x * 2.0
        for i in range(num_layers - 1):
            dist_i = (
                max_r_per_rank[i]
                + max_r_per_rank[i + 1]
                + max_label_w_between[i]
                + margin
            )
            width_lr += dist_i

        unspecified = any(s.x is None or s.y is None for s in self._states)

        # Auto-decide direction if not chosen explicitly
        direction = self.direction
        if direction is None:
            if not unspecified:
                xs = [s.x for s in self._states if s.x is not None]
                ys = [s.y for s in self._states if s.y is not None]
                if xs and ys:
                    dx = max(xs) - min(xs)
                    dy = max(ys) - min(ys)
                    direction = "LR" if dx >= dy else "TB"
                else:
                    direction = "LR"
            else:
                # If horizontal layout exceeds 480pt, auto-switch to vertical layout
                direction = "LR" if width_lr <= 480.0 else "TB"

        self._active_direction = direction

        # Set default width if in horizontal mode
        if direction == "LR":
            self.width = max(self.width, width_lr)

        if unspecified:
            self.auto_layout()
        else:
            self._normalize_bounds()

        # Register state circles in self._label_rects
        self._label_rects = []
        for st in self._states:
            assert st.x is not None and st.y is not None
            r = self._state_radius(st)
            self._label_rects.append((st.x, st.y, r * 2.0, r * 2.0))

        t = self.theme

        # Initial state markers
        for st in self._states:
            assert st.x is not None and st.y is not None
            if st.initial:
                r = self._state_radius(st)
                if getattr(self, "_active_direction", "LR") == "TB":
                    self._add(
                        S.initial_state_marker(
                            st.x,
                            st.y + r,
                            direction="down",
                            r=5.0,
                            color=t.initial_fill,
                            arrow_len=16.0,
                        )
                    )
                else:
                    self._add(
                        S.initial_state_marker(
                            st.x - r,
                            st.y,
                            direction="right",
                            r=5.0,
                            color=t.initial_fill,
                            arrow_len=16.0,
                        )
                    )

        # Transitions (drawn before states so arrows go under circles)
        for tr in self._transitions:
            self._draw_transition(tr)

        # States
        for st in self._states:
            assert st.x is not None and st.y is not None
            r = self._state_radius(st)
            drawer = self._custom_drawers.get(st.id)
            if drawer is not None:
                try:
                    drawer(self, st.x, st.y, r, t.state_fill, t.state_stroke)
                except TypeError:
                    drawer(self, st.x, st.y, t.state_fill, t.state_stroke)
            else:
                if st.accepting:
                    self._add(
                        S.double_circle(
                            st.x,
                            st.y,
                            r,
                            fill=t.state_fill,
                            stroke=t.accepting_stroke,
                        )
                    )
                else:
                    self._add(
                        S.circle(
                            st.x,
                            st.y,
                            r,
                            fill=t.state_fill,
                            stroke=t.state_stroke,
                        )
                    )
                state_text_color = S.get_contrast_color(
                    t.state_fill, light_fg=t.state_text, dark_fg="#0f172a"
                )
                self._add(
                    S.centered_wrapped_label(
                        st.x,
                        st.y,
                        st.label,
                        max_width=min(self.state_label_max_width, r * 2.0 - 4.0),
                        font=t.font_name_bold,
                        size=9.0,
                        color=state_text_color,
                        anchor="middle",
                    )
                )
