from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union

class CanvasConfig(BaseModel):
    width: int
    height: int
    background: str = "#FFFFFF"

class CompositionConfig(BaseModel):
    center: List[float] = Field(default_factory=lambda: [0.5, 0.5])
    scale: float = 1.0

class StyleConfig(BaseModel):
    name: str = "simple"
    outline: str = "#000000"
    outline_width: int = 1

class DrawingElement(BaseModel):
    id: str
    semantic_role: str
    type: str  # e.g., "path", "ellipse", "rectangle", "polygon"
    parent_id: Optional[str] = None
    z_index: int = 0
    fill: Optional[str] = None
    stroke: Optional[str] = None
    stroke_width: int = 1
    
    # Internal usage for scaling and offsets
    center: Optional[List[float]] = None
    rotation: float = 0.0
    scale: float = 1.0

class PathElement(DrawingElement):
    type: str = "path"
    points: List[List[float]]  # Normalized points [0.0, 1.0]
    is_closed: bool = False

class ShapeElement(DrawingElement):
    type: str # "ellipse" or "rectangle"
    x1: float
    y1: float
    x2: float
    y2: float

# Element can be any valid drawing primitive
Element = Union[PathElement, ShapeElement]

class DrawingPlan(BaseModel):
    plan_id: str
    description: str
    canvas: CanvasConfig
    composition: CompositionConfig
    style: StyleConfig
    elements: List[Element] = Field(default_factory=list)
