"""
TCD Origin API Package
跨文明古文字拓扑破译引擎 - API服务
"""

__version__ = "3.0.1"
__author__ = "TCD Origin Team"

from api.main import app
from api.config import settings

__all__ = ["app", "settings"]
