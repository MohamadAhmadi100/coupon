from source.modules import terminal_log
from config import config

from source.controllers.router_back_office import *
from source.controllers.router_coupon import *

response = {}
app_name = config.APP_NAME


def callback(message: dict) -> dict:
    terminal_log.action_log(message, app_name)
    terminal_log.request_log(message, app_name)
    data = message.get(app_name, {})
    if action := data.get("action"):
        body = data.get("body", {})
        try:
            exec(f"global response; response['{app_name}'] = {action}(**{body})")
            return response
        except Exception as e:
            return {f"{app_name}": {"success": False, "status_code": 503, "error": f"{app_name}: {e} {action}"}}
    else:
        return {f"{app_name}": {"success": False, "status_code": 501, "error": f"{app_name}: action not found"}}
