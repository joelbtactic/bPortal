# -*- coding: utf-8 -*-

#######################################################################
# bPortal is a SuiteCRM portal written using django project.

# Copyright (C) 2017 Marc Sanchez Fauste
# Copyright (C) 2017 BTACTIC, SCCL

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from suitepy.suitecrm import SuiteCRM
import json

# Create your views here.

def index(request):
    accounts = SuiteCRM().get_bean_list('Accounts', max_results = 10)
    template = loader.get_template('portal/index.html')
    context = {
        'accounts' : accounts
    }
    return HttpResponse(template.render(context, request))

def modules(request):
    modules = SuiteCRM().get_available_modules()
    template = loader.get_template('portal/modules.html')
    context = {
        'modules' : modules['modules']
    }
    return HttpResponse(template.render(context, request))

def module_list(request, module):
    records = SuiteCRM().get_bean_list(module, max_results = 10)
    fields_list = records[0].fields[:7]
    module_fields = SuiteCRM().get_module_fields(module, fields_list)
    template = loader.get_template('portal/module_list.html')
    context = {
        'module_key' : module,
        'records' : records,
        'module_fields' : module_fields['module_fields']
    }
    return HttpResponse(template.render(context, request))

def edit_list_layout(request, module):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            selected_fields = post_data['selected_fields']
        except KeyError:
            return JsonResponse({
                "status" : "Error",
                "error" : "Please specify 'selected_fields'."
            }, status = 400)
        print "Save", module, "list view. Fields:", json.dumps(selected_fields, indent=4)
        return JsonResponse({"status" : "Success"})
    elif request.method == 'GET':
        module_fields = SuiteCRM().get_module_fields(module)
        template = loader.get_template('portal/edit_list_layout.html')
        context = {
            'module_key' : module,
            'module_fields' : {},
            'available_fields' : module_fields['module_fields']
        }
        return HttpResponse(template.render(context, request))
