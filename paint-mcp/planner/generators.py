import math
import uuid
from typing import List, Dict, Any, Tuple
from planner.geometry import sample_bezier_path, rotate_point
from planner.models import PathElement, ShapeElement, Element

def generate_petal(
    center: Tuple[float, float],
    length: float,
    width: float,
    rotation_deg: float,
    layer_id: str,
    color: str,
    z_index: int = 1
) -> PathElement:
    """
    Generate a petal as a closed bezier path element.
    center: base center of the petal (0..1)
    length: length of petal (0..1)
    width: width of petal (0..1)
    rotation_deg: rotation angle from straight up.
    """
    
    # Base petal pointing UP (from center)
    # Control points for a basic teardrop/petal shape
    p0 = (center[0], center[1])
    # left side control point
    p1 = (center[0] - width/2, center[1] - length * 0.3)
    p2 = (center[0] - width/2, center[1] - length * 0.8)
    # top tip
    p3 = (center[0], center[1] - length)
    # right side control point
    p4 = (center[0] + width/2, center[1] - length * 0.8)
    p5 = (center[0] + width/2, center[1] - length * 0.3)
    # back to base
    p6 = (center[0], center[1])
    
    control_points = [p0, p1, p2, p3, p4, p5, p6]
    
    # Rotate all points around the base center
    rotated_cps = [tuple(rotate_point(pt, center, rotation_deg)) for pt in control_points]
    
    # Sample path
    path_points = sample_bezier_path(rotated_cps, segments=10)
    
    return PathElement(
        id=f"petal_{layer_id}_{uuid.uuid4().hex[:6]}",
        semantic_role="petal",
        parent_id=layer_id,
        z_index=z_index,
        fill=color,
        stroke="#222222",
        points=path_points,
        is_closed=True
    )

def generate_flower_ring(
    center: Tuple[float, float],
    radius: float,
    num_petals: int,
    length: float,
    width: float,
    layer_name: str,
    color: str,
    z_index: int = 1,
    rotation_offset: float = 0.0
) -> List[Element]:
    """Generate a ring of petals arranged in a circle."""
    elements = []
    angle_step = 360.0 / num_petals
    
    for i in range(num_petals):
        angle = i * angle_step + rotation_offset
        # calculate base offset if radius > 0
        rad = math.radians(angle)
        base_x = center[0] + radius * math.sin(rad)
        base_y = center[1] - radius * math.cos(rad)
        
        petal = generate_petal(
            center=(base_x, base_y),
            length=length,
            width=width,
            rotation_deg=angle,
            layer_id=layer_name,
            color=color,
            z_index=z_index
        )
        elements.append(petal)
        
    return elements

def generate_stem(start: Tuple[float, float], end: Tuple[float, float], curvature: float, color: str, z_index: int = -5) -> PathElement:
    """Generate a curved stem."""
    # simple bezier from start to end with control points bent sideways
    mx = (start[0] + end[0]) / 2.0 + curvature
    my = (start[1] + end[1]) / 2.0
    
    cps = [start, (start[0], my), (mx, end[1]), end]
    path_points = sample_bezier_path(cps, segments=15)
    
    return PathElement(
        id=f"stem_{uuid.uuid4().hex[:6]}",
        semantic_role="stem",
        z_index=z_index,
        stroke=color,
        stroke_width=5, # we'd interpret this differently depending on tools, usually just brush size
        points=path_points,
        is_closed=False
    )

def generate_leaf(base: Tuple[float, float], length: float, rotation_deg: float, color: str, z_index: int = -3) -> PathElement:
    """Generate a leaf."""
    # Similar to a petal but pointier
    # ...
    width = length * 0.4
    p0 = (base[0], base[1])
    p1 = (base[0] - width, base[1] - length * 0.5)
    p2 = (base[0] - width/2, base[1] - length * 0.9)
    p3 = (base[0], base[1] - length)
    p4 = (base[0] + width/2, base[1] - length * 0.9)
    p5 = (base[0] + width, base[1] - length * 0.5)
    p6 = (base[0], base[1])
    
    cps = [p0, p1, p2, p3, p4, p5, p6]
    rotated_cps = [tuple(rotate_point(pt, base, rotation_deg)) for pt in cps]
    path_points = sample_bezier_path(rotated_cps, segments=8)
    
    return PathElement(
        id=f"leaf_{uuid.uuid4().hex[:6]}",
        semantic_role="leaf",
        z_index=z_index,
        fill=color,
        stroke="#111111",
        points=path_points,
        is_closed=True
    )
