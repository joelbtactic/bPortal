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

    def get_module_fields_dolibarr(self, module):
        try:
            module_def = ModuleDefinitionFactory.get_module_definition(module)
        except ModuleDefinitionNotFoundException:
            return {
                'module_key': module,
                'unsupported_module': True
            }

        if module_def.dolibarr_extrafield:
            module_fields = self.dolibarr_cached.get_module_fields(module_def.dolibarr_name, module_def.dolibarr_extrafield, module_def.dolibarr_extrafields_module)
        else:
            module_fields = self.dolibarr_cached.get_module_fields(module_def.dolibarr_name)

        filterable_fields = OrderedDict()
        for field_name, field_def in module_fields.items():
            filterable_fields[field_name] = field_def
        return filterable_fields
