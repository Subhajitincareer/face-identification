from typing import Dict, Any, Tuple
import math
from planner.models import DrawingPlan

def validate_plan(plan: DrawingPlan) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validate a complete DrawingPlan.
    Returns (is_valid, error_message, plan_data)
    """
    try:
        # Basic checks
        if not plan.elements:
            return False, "Plan contains no elements.", {}
            
        if plan.canvas.width <= 0 or plan.canvas.height <= 0:
            return False, "Invalid canvas dimensions.", {}
            
        if plan.composition.scale <= 0:
            return False, "Invalid scale.", {}
            
        for el in plan.elements:
            if el.type == "path":
                if not el.points or len(el.points) < 2:
                    return False, f"Path element {el.id} has insufficient points.", {}
                # check for NaN
                for pt in el.points:
                    if math.isnan(pt[0]) or math.isnan(pt[1]):
                        return False, f"NaN detected in path {el.id}.", {}
                        
            elif el.type in ["ellipse", "rectangle"]:
                if math.isnan(el.x1) or math.isnan(el.y1):
                    return False, f"NaN detected in shape {el.id}.", {}
                    
        # Sort elements by z_index
        plan.elements.sort(key=lambda e: e.z_index)
        
        return True, "Plan validated successfully.", plan.model_dump()
    except Exception as e:
        return False, f"Validation exception: {str(e)}", {}
