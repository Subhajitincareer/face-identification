import keyboard
import time
from typing import Dict, Any
from planner.models import DrawingPlan
from planner.geometry import denormalize_points
from tools.drawing import draw_path, select_tool, set_primary_color
import logging
import pyautogui

logger = logging.getLogger("executor")

class ExecutionState:
    is_cancelled = False

def check_cancel():
    if keyboard.is_pressed('esc'):
        ExecutionState.is_cancelled = True
        logger.warning("ESC pressed! Cancelling execution.")

def execute_plan(plan: DrawingPlan) -> Dict[str, Any]:
    """
    Executes a complete drawing plan locally without continuous round-trips.
    Checks for ESC interruption.
    """
    ExecutionState.is_cancelled = False
    
    completed = []
    failed = []
    remaining = [el.id for el in plan.elements]
    
    # Sort elements by z-index
    elements = sorted(plan.elements, key=lambda e: e.z_index)
    
    w = plan.canvas.width
    h = plan.canvas.height
    comp_center = plan.composition.center
    comp_scale = plan.composition.scale
    
    logger.info(f"Executing Drawing Plan {plan.plan_id} with {len(elements)} elements.")
    
    # Pre-select brush tool for path execution
    try:
        select_tool("brush")
    except:
        select_tool("pencil")
        
    last_color = None
    
    for i, el in enumerate(elements):
        check_cancel()
        if ExecutionState.is_cancelled:
            logger.warning(f"Plan cancelled at element {i+1}/{len(elements)}.")
            break
            
        remaining.remove(el.id)
        
        try:
            # Color management
            stroke_color = el.stroke if el.stroke else plan.style.outline
            if stroke_color and stroke_color != last_color:
                set_primary_color(stroke_color)
                last_color = stroke_color
                time.sleep(0.1) # allow Paint UI to update
                
            if el.type == "path":
                # convert normalized points to absolute canvas pixels
                pts = denormalize_points(el.points, w, h, comp_center, comp_scale)
                if pts:
                    # Execute path on canvas
                    res = draw_path(pts, is_closed=el.is_closed)
                    if res.get("isError"):
                        raise Exception(res.get("result"))
                        
            completed.append(el.id)
            logger.info(f"[{i+1}/{len(elements)}] Executed: {el.id} ({el.semantic_role})")
            
            # Tiny sleep to allow interruption capture
            time.sleep(0.05)
            
        except Exception as e:
            logger.error(f"Failed to execute element {el.id}: {e}")
            failed.append(el.id)
            # If one fails, we might just continue or break based on strictness.
            # We'll continue for organic shapes (missing a petal is fine).

    # Clean up any lingering mouse downs
    pyautogui.mouseUp(button='left')
    
    status = "Completed" if not ExecutionState.is_cancelled else "Cancelled"
    
    return {
        "status": status,
        "completed": completed,
        "failed": failed,
        "remaining": remaining,
        "total": len(elements)
    }
