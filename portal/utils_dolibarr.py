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

    def get_listview_filter(self, parameters):
        filters = parameters.copy()
        # List of keys to remove
        keys_to_remove = ['limit', 'offset', 'order_by', 'order', 'csrfmiddlewaretoken']
        for key in keys_to_remove:
            if key in filters:
                del filters[key]
        # Iterate over a copy of the keys to avoid modifying the dictionary during iteration
        for key in list(filters.keys()):
            if not filters[key]:
                del filters[key]
        return filters
