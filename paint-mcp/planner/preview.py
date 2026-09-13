import os
from typing import Dict, Any
from planner.models import DrawingPlan
from planner.geometry import denormalize_points

def generate_svg_preview(plan: DrawingPlan, output_path: str = "preview.svg") -> str:
    """Generate an SVG file representing the current drawing plan."""
    
    # Sort elements by z-index
    elements = sorted(plan.elements, key=lambda e: e.z_index)
    
    w = plan.canvas.width
    h = plan.canvas.height
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">')
    svg_lines.append(f'<rect width="100%" height="100%" fill="{plan.canvas.background}"/>')
    
    comp_center = plan.composition.center
    comp_scale = plan.composition.scale
    
    for el in elements:
        fill = el.fill if el.fill else "none"
        stroke = el.stroke if el.stroke else plan.style.outline
        stroke_width = el.stroke_width if el.stroke_width else plan.style.outline_width
        
        if el.type == "path":
            # Denormalize points
            pts = denormalize_points(el.points, w, h, comp_center, comp_scale)
            if not pts:
                continue
                
            d = f"M {pts[0][0]} {pts[0][1]} "
            for pt in pts[1:]:
                d += f"L {pt[0]} {pt[1]} "
                
            if el.is_closed:
                d += "Z"
                
            svg_lines.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
            
        elif el.type == "ellipse":
            # Very basic representation of absolute shape in preview
            # Note: Assuming x1,y1 are normalized in a full impl, but handling simpler here.
            pass
            
        elif el.type == "rectangle":
            pass
            
    svg_lines.append("</svg>")
    svg_content = "\n".join(svg_lines)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    return os.path.abspath(output_path)
