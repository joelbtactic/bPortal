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

    def retrieve_list_view_records(self, module, arguments, user):
        try:
            module_def = ModuleDefinitionFactory.get_module_definition(module)
        except ModuleDefinitionNotFoundException:
            return {
                'module_key': module,
                'unsupported_module': True
            }
        try:
            user_type = user.userattr.user_type
            if (user_type == 'account'
                    and module_def.accounts_link_type != LinkType.CONTACT) \
                    or module_def.contacts_link_type == LinkType.ACCOUNT:
                related_module = 'Accounts'
                related_id = user.userattr.account_id
            else:
                related_module = None
        except Exception:
            return {
                'module_key': module,
                'error_retrieving_records': True
            }
        ordered_module_fields = OrderedDict()
        filterable_fields = OrderedDict()
        if (related_module == 'Accounts'):
            records = []
            order_by = arguments.get('order_by')
            order = arguments.get('order')
            try:
                ordered_module_fields = self.get_ordered_fields(module, module_def)
                filterable_fields = self.get_filter_layout(module, module_def)
                records = self._retrieve_records(module_def, related_module, related_id, arguments, filterable_fields, ordered_module_fields)

            except Exception as e:
                print(e)
        else:
            return {
                'module_key': module,
                'invoice_permissons': True
            }

        return {
            'module_key': module,
            'records': records,
            'module_fields': ordered_module_fields,
            'filterable_fields': filterable_fields,
            'current_filters': self.get_listview_filter(arguments),
            'order_by': order_by,
            'order': order
        }

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

    def get_view_layout(self, module, view_type):
        try:
            module_def = ModuleDefinitionFactory.get_module_definition(module)
        except ModuleDefinitionNotFoundException:
            return {
                'module_key': module,
                'unsupported_module': True
            }
        try:

            ordered_module_fields = []
            view = Layout.objects.get(module=module, view=view_type)
            fields_list = json.loads(view.fields)
            if module_def.dolibarr_extrafield:
                module_fields = self.dolibarr_cached.get_module_fields(module_def.dolibarr_name, module_def.dolibarr_extrafield, module_def.dolibarr_extrafields_module)
            else:
                module_fields = self.dolibarr_cached.get_module_fields(module_def.dolibarr_name)
            for row in fields_list:
                row_fields = []
                for field in row:
                    if field in module_fields:
                        row_fields.append(module_fields[field])
                    elif not field:
                        row_fields.append(None)
                ordered_module_fields.append(row_fields)
        except Exception:
            pass
        return ordered_module_fields

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

    def _retrieve_records(self, module_def, related_module, related_id, arguments, filterable_fields, fields_list):
        account_id = self.get_dol_account_id(module_def.dolibarr_account_link_name, related_module, related_id)
        filter_dolibarr = self.get_filter_query(module_def, filterable_fields, arguments, account_id, fields_list)
        records = self.dolibarr_service.get_all_records(module_def.dolibarr_name, filter_dolibarr)
        return records

    def set_sortable_atribute_on_module_fields(self, module_fields):
        for _, field_def in module_fields.items():
            field_def['sortable'] = True

    def get_filter_query(self, module_def, fields:dict, arguments, account_id, fields_list):
        order_by = arguments.get('order_by')
        order = arguments.get('order')
        limit = arguments.get('limit')
        offset = arguments.get('offset')

        prefix_filter, order_name = self._get_prefix_filter_field(fields_list, order_by)
        filter_dolibarr = {
            module_def.dolibarr_account_filter: account_id
        }
        if order_name != None:
            filter_dolibarr['sortfield'] = prefix_filter + order_name
        if order != None:
            filter_dolibarr['sortorder'] = order
        if limit:
            filter_dolibarr['limit']  = int(limit)
        if offset:
            filter_dolibarr['page']  = int(offset)

        sqlfilters = ''
        for field_name, field_def in fields.items():
            if field_name in arguments and arguments[field_name]:
                parameter = self.remove_special_char(arguments[field_name])
                if field_def['type'] in ['date', 'datetime', 'datetimecombo']:
                    date_filter_params = []
                    if field_name + '_1' in arguments:
                        date_filter_params.append(arguments[field_name + '_1'])
                        if field_name + '_2' in arguments:
                            date_filter_params.append(
                                arguments[field_name + '_2']
                            )
                    if 'sqlname' in field_def and field_def['sqlname']:
                        field_sqlname = field_def['sqlname']
                    else:
                        field_sqlname = field_name
                    sqlfilters += doli_get_datetime_option_in_mysql_format(
                        arguments[field_name],
                        field_sqlname,
                        date_filter_params
                    )

                else:
                    if 'sqlname' in field_def and field_def['sqlname']:
                        field_name = field_def['sqlname']

                    if 'extrafield' in field_def and field_def['extrafield']:
                        sqlfilters += f"(ef.{field_name}:like:'{parameter}') and "

                    else:
                        sqlfilters += f"(t.{field_name}:like:'{parameter}') and "

        if sqlfilters != '':
            filter_dolibarr['sqlfilters'] = sqlfilters[0:-4]
        return filter_dolibarr

    def _get_prefix_filter_field(self, fields, order_name):
        prefix_filter = 't.'
        if order_name in fields:
            field_def = fields[order_name]
            if 'sqlname' in field_def and field_def['sqlname']:
                order_name = field_def['sqlname']

            if 'extrafield' in field_def and field_def['extrafield']:
                prefix_filter = 'ef.'

        return prefix_filter, order_name

    def remove_special_char(self, filter_value):
        if "(" in filter_value:
            filter_value = filter_value.replace("(", "_")
            filter_value = filter_value.replace(")", "_")

        return filter_value
