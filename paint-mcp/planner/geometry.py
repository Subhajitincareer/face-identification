import math
from typing import List, Tuple

def denormalize_points(points: List[List[float]], width: int, height: int, comp_center: List[float], comp_scale: float) -> List[List[int]]:
    """
    Convert normalized points [0..1] to pixel coordinates.
    Applies the global composition scale and center offset.
    """
    pixel_points = []
    
    # Calculate offset so that (0.5, 0.5) in normalized space aligns with comp_center in pixel space.
    # Base mapping: [0, 1] -> [0, width]
    base_center_x = width / 2.0
    base_center_y = height / 2.0
    
    target_center_x = comp_center[0] * width
    target_center_y = comp_center[1] * height
    
    offset_x = target_center_x - base_center_x
    offset_y = target_center_y - base_center_y

    for pt in points:
        # 1. Scale around center (0.5, 0.5)
        nx = 0.5 + (pt[0] - 0.5) * comp_scale
        ny = 0.5 + (pt[1] - 0.5) * comp_scale
        
        # 2. Convert to pixels
        px = int(nx * width + offset_x)
        py = int(ny * height + offset_y)
        
        # clamp to canvas
        px = max(0, min(width, px))
        py = max(0, min(height, py))
        
        pixel_points.append([px, py])
        
    return pixel_points

def evaluate_bezier(p0: Tuple[float, float], p1: Tuple[float, float], 
                    p2: Tuple[float, float], p3: Tuple[float, float], t: float) -> Tuple[float, float]:
    """Evaluate cubic bezier curve at parameter t (0 <= t <= 1)."""
    u = 1 - t
    u2 = u * u
    u3 = u2 * u
    t2 = t * t
    t3 = t2 * t
    
    x = (u3 * p0[0]) + (3 * u2 * t * p1[0]) + (3 * u * t2 * p2[0]) + (t3 * p3[0])
    y = (u3 * p0[1]) + (3 * u2 * t * p1[1]) + (3 * u * t2 * p2[1]) + (t3 * p3[1])
    return (x, y)

def sample_bezier_path(control_points: List[Tuple[float, float]], segments: int = 10) -> List[List[float]]:
    """
    Takes a list of control points representing a continuous cubic bezier path.
    Requires len(control_points) = 3n + 1
    Returns sampled points.
    """
    if len(control_points) < 4 or (len(control_points) - 1) % 3 != 0:
        raise ValueError("Invalid number of control points for cubic bezier path.")
        
    path = []
    
    for i in range(0, len(control_points) - 1, 3):
        p0 = control_points[i]
        p1 = control_points[i+1]
        p2 = control_points[i+2]
        p3 = control_points[i+3]
        
        # avoid duplicating the start point on subsequent segments
        start_j = 0 if i == 0 else 1 
        for j in range(start_j, segments + 1):
            t = j / segments
            x, y = evaluate_bezier(p0, p1, p2, p3, t)
            path.append([x, y])
            
    return path

def rotate_point(pt: Tuple[float, float], center: Tuple[float, float], angle_deg: float) -> List[float]:
    """Rotate a point around a center by angle in degrees."""
    angle_rad = math.radians(angle_deg)
    s = math.sin(angle_rad)
    c = math.cos(angle_rad)
    
    px, py = pt[0] - center[0], pt[1] - center[1]
    
    xnew = px * c - py * s
    ynew = px * s + py * c
    
    return [xnew + center[0], ynew + center[1]]
