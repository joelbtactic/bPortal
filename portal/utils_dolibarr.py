from portal.suitecrm_api_service import SuiteCRMManager
from .models import Layout
from dolibarrpy.dolibarrpy_service import DolibarrApiService
from dolibarrpy.dolibarrpy_service_cached import DolibarrApiServiceCached

from collections import OrderedDict
import json
from .module_definitions import *
from .utils_datetime import *

class DolibarrUtils:

    def __init__(self) -> None:
        self.dolibarr_service = DolibarrApiService()
        self.dolibarr_cached = DolibarrApiServiceCached()
