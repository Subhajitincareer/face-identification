import json
import uuid
from typing import Dict, Any, Optional
from utils.errors import format_success, format_error
from utils.helpers import get_paint_app, get_main_window
from planner.models import DrawingPlan, CanvasConfig, CompositionConfig, StyleConfig
from planner.generators import generate_stem, generate_leaf, generate_flower_ring
from planner.validator import validate_plan
from planner.preview import generate_svg_preview
from planner.executor import execute_plan, ExecutionState
import pyautogui

# In-memory storage for the current plan session
CURRENT_PLAN: Optional[DrawingPlan] = None

def _create_rose_plan(width: int, height: int, style: str) -> DrawingPlan:
    """Procedurally generates a complete scene graph for a rose."""
    plan_id = f"rose_{uuid.uuid4().hex[:8]}"
    
    plan = DrawingPlan(
        plan_id=plan_id,
        description="A beautiful procedural rose.",
        canvas=CanvasConfig(width=width, height=height, background="#FFFFFF"),
        composition=CompositionConfig(center=[0.5, 0.4], scale=1.0),
        style=StyleConfig(name=style, outline="#111111", outline_width=2)
    )
    
    # 1. Stem
    stem = generate_stem(start=(0.5, 0.5), end=(0.5, 0.9), curvature=0.05, color="#2E7D32", z_index=1)
    plan.elements.append(stem)
    
    # 2. Leaves
    leaf1 = generate_leaf(base=(0.5, 0.7), length=0.2, rotation_deg=-45, color="#3F9142", z_index=2)
    leaf2 = generate_leaf(base=(0.52, 0.8), length=0.15, rotation_deg=60, color="#3F9142", z_index=2)
    plan.elements.extend([leaf1, leaf2])
    
    # 3. Outer Petals
    outer = generate_flower_ring(center=(0.5, 0.5), radius=0.15, num_petals=5, length=0.2, width=0.15, 
                                 layer_name="outer", color="#C00020", z_index=10, rotation_offset=0)
    plan.elements.extend(outer)
    
    # 4. Middle Petals
    middle = generate_flower_ring(center=(0.5, 0.5), radius=0.08, num_petals=6, length=0.15, width=0.12, 
                                 layer_name="middle", color="#D32F2F", z_index=20, rotation_offset=15)
    plan.elements.extend(middle)
    
    # 5. Inner Petals
    inner = generate_flower_ring(center=(0.5, 0.5), radius=0.03, num_petals=4, length=0.1, width=0.08, 
                                 layer_name="inner", color="#E53935", z_index=30, rotation_offset=45)
    plan.elements.extend(inner)
    
    return plan

def plan_drawing(description: str, width: int = 1000, height: int = 1000, style: str = "realistic") -> Dict[str, Any]:
    global CURRENT_PLAN
    
    description_lower = description.lower()
    
    try:
        # We can expand this with LLM integration later.
        # For now, we procedurally map known complex objects.
        if "rose" in description_lower:
            plan = _create_rose_plan(width, height, style)
        else:
            # Generic fallback (could generate a basic shape or invoke an external planner)
            return format_error("plan_drawing", f"No procedural generator available for: {description}", "NotImplementedError")
            
        CURRENT_PLAN = plan
        return format_success("plan_drawing", f"Plan generated with {len(plan.elements)} elements.", {"plan_id": plan.plan_id})
        
    except Exception as e:
        return format_error("plan_drawing", "Failed to generate plan.", type(e).__name__, str(e))

def validate_drawing_plan(plan_id: str = "") -> Dict[str, Any]:
    global CURRENT_PLAN
    if not CURRENT_PLAN:
        return format_error("validate_drawing_plan", "No active plan.", "ValueError")
        
    is_valid, msg, dump = validate_plan(CURRENT_PLAN)
    if is_valid:
        return format_success("validate_drawing_plan", msg)
    else:
        return format_error("validate_drawing_plan", msg, "ValidationError")

def preview_drawing_plan(output_path: str = "preview.svg") -> Dict[str, Any]:
    global CURRENT_PLAN
    if not CURRENT_PLAN:
        return format_error("preview_drawing_plan", "No active plan.", "ValueError")
        
    try:
        path = generate_svg_preview(CURRENT_PLAN, output_path)
        return format_success("preview_drawing_plan", f"SVG preview saved to {path}.")
    except Exception as e:
        return format_error("preview_drawing_plan", "Failed to generate preview.", type(e).__name__, str(e))

def execute_drawing_plan(plan_id: str = "") -> Dict[str, Any]:
    global CURRENT_PLAN
    if not CURRENT_PLAN:
        return format_error("execute_drawing_plan", "No active plan.", "ValueError")
        
    try:
        result = execute_plan(CURRENT_PLAN)
        return format_success("execute_drawing_plan", f"Execution finished with status: {result['status']}.", result)
    except Exception as e:
        pyautogui.mouseUp(button='left')
        return format_error("execute_drawing_plan", "Failed to execute plan.", type(e).__name__, str(e))

def cancel_drawing_plan() -> Dict[str, Any]:
    ExecutionState.is_cancelled = True
    pyautogui.mouseUp(button='left')
    return format_success("cancel_drawing_plan", "Cancellation signal sent.")
