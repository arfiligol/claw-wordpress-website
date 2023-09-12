import datetime
import json
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def format(self, record):
        json_log_object = {
            "time": datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S,%f'),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(json_log_object, ensure_ascii=False)