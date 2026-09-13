from typing import Optional, Dict, Any

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
