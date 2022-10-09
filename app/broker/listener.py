import sys
from app.config import settings
from app.modules import terminal_log

# Important imports don't remove
from app.controllers.coupon_router import *
from app.controllers.transfer_router import *
from app.controllers.supplier_router import *

response = {}
app_name = settings.APP_NAME


def callback(message: dict) -> dict:
    terminal_log.action_log(message, app_name)
    terminal_log.request_log(message, app_name)
    data = message.get(app_name, {})
    action = data.get("action")
    if action:
        body = data.get("body", {})
        try:
            exec(f"global response; response['{app_name}'] = {action}(**{body})")
            return response
        except Exception as e:
            return {f"{app_name}": {"success": False, "status_code": 503, "error": f"{app_name}: {e}"}}
    else:
        return {f"{app_name}": {"success": False, "status_code": 501, "error": f"{app_name}: action not found"}}
