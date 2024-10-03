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

    def get_dol_account_id(self, dolibarr_module, related_module, related_id):
        suitecrmcached_instance = SuiteCRMManager.get_suitecrmcached_instance()
        account_bean = suitecrmcached_instance.get_bean(
            related_module,
            related_id,
        )

        num_cliente_erp = account_bean['numerp_c']

        filter_dolibarr = {
            'sqlfilters': '(ef.nmeroclienteerp:=:'+ "'" + num_cliente_erp + "'" + ')'
        }

        dolibarr_account = self.dolibarr_cached.get_all_records(dolibarr_module, filter_dolibarr)
        account_id = dolibarr_account['entry_list'][0]['id']

        return account_id


    def get_filter_layout(self, module, module_def):
        try:

            ordered_module_fields = OrderedDict()
            view = Layout.objects.get(module=module, view='filter')
            fields_list = json.loads(view.fields)
            if module_def.dolibarr_extrafield:
                module_fields = self.dolibarr_cached.get_module_fields(module_def.dolibarr_name, module_def.dolibarr_extrafield, module_def.dolibarr_extrafields_module)
            else:
                module_fields = self.dolibarr_cached.get_module_fields(module_def.dolibarr_name)
            for field in fields_list:
                if field in module_fields:
                    ordered_module_fields[field] = module_fields[field]
            return ordered_module_fields
        except Exception:
            return OrderedDict()

    def get_ordered_fields(self, module, module_def):
        ordered_module_fields = OrderedDict()
        module_fields = {}

        view = Layout.objects.get(module=module, view='list')

        fields_list = json.loads(view.fields)

        if module_def.dolibarr_extrafield:
            module_fields = self.dolibarr_cached.get_module_fields(module_def.dolibarr_name, module_def.dolibarr_extrafield, module_def.dolibarr_extrafields_module)
        else:
            module_fields = self.dolibarr_cached.get_module_fields(module_def.dolibarr_name)

        for field in fields_list:
            if field in module_fields:
                ordered_module_fields[field] = module_fields[field]
        self.set_sortable_atribute_on_module_fields(module_fields)

        return ordered_module_fields

    def set_sortable_atribute_on_module_fields(self, module_fields):
        for _, field_def in module_fields.items():
            field_def['sortable'] = True
