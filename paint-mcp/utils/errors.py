from typing import Dict, Any, Optional

class PaintError(Exception):
    pass

class PaintNotRunningError(PaintError):
    pass

class PaintWindowNotFoundError(PaintError):
    pass

class CanvasNotFoundError(PaintError):
    pass

class ControlNotFoundError(PaintError):
    pass

class DialogDetectedError(PaintError):
    pass

class InvalidCoordinateError(PaintError):
    pass

class InvalidColorError(PaintError):
    pass

class FileOperationError(PaintError):
    pass

def format_success(action: str, message: str = "", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "success": True,
        "action": action,
        "message": message,
        "data": data or {},
        "error": None
    }

def format_error(
    action: str, 
    message: str, 
    error_type: str, 
    details: str = "", 
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {
        "success": False,
        "action": action,
        "message": message,
        "data": data or {},
        "error": {
            "type": error_type,
            "details": details
        }
    }
