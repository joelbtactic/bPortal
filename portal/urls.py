#######################################################################
# bPortal is a SuiteCRM portal written using django project.

# Copyright (C) 2017-2018 BTACTIC, SCCL
# Copyright (C) 2017-2018 Marc Sanchez Fauste

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

from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^modules/$', views.modules, name='modules'),
    re_path(r'^module/(?P<module>\w+)/list$', views.module_list, name='module_list'),
    re_path(r'^module/(?P<module>\w+)/detail/(?P<id>[\w-]+)/$',
        views.module_detail, name='module_detail'),
    re_path(r'^module/(?P<module>\w+)/edit/(?P<id>[\w-]+)/$',
        views.module_edit, name='module_edit'),
    re_path(r'^module/(?P<module>\w+)/create/$',
        views.module_create, name='module_create'),
    re_path(r'^module/(?P<module>\w+)/remove/$',
        views.module_remove_record, name='module_remove_record'),
    re_path(r'^layouts/$', views.edit_layouts, name='edit_layouts'),
    re_path(r'^user_records/(?P<module>\w+)/$',
        views.user_records, name='user_records'),
    re_path(r'^layout/list/(?P<module>\w+)/$',
        views.edit_list_layout, name='edit_list_layout'),
    re_path(r'^layout/filter/(?P<module>\w+)/$',
        views.edit_filter_layout, name='edit_filter_layout'),
    re_path(r'^layout/detail/(?P<module>\w+)/$',
        views.edit_detail_layout, name='edit_detail_layout'),
    re_path(r'^layout/edit/(?P<module>\w+)/$',
        views.edit_edit_layout, name='edit_edit_layout'),
    re_path(r'^layout/create/(?P<module>\w+)/$',
        views.edit_create_layout, name='edit_create_layout'),
    re_path(r'^roles/$', views.edit_roles, name='edit_roles'),
    re_path(r'^role/(?P<role>\w+)$', views.edit_role, name='edit_role'),
    re_path(r'^roles/delete$', views.delete_role, name='delete_role'),
    re_path(r'^roles/create$', views.create_role, name='create_role'),
    re_path(r'^note_attachment/(?P<id>[\w-]+)/$',
        views.note_attachment, name='note_attachment'),
    re_path(r'^add_case_update/$', views.add_case_update, name='add_case_update'),
    re_path(r'^close_case/$', views.close_case, name='close_case'),
    re_path(r'^reopen_case/$', views.reopen_case, name='reopen_case'),
    re_path(r'^users/$', views.edit_users, name='edit_users'),
    re_path(r'^user/(?P<user_id>\d+)$', views.edit_user, name='edit_user'),
    re_path(r'^user_profile/$', views.user_profile, name='user_profile'),
    re_path(r'^cache/$', views.cache, name='cache'),
    re_path(r'^pdf_templates/$', views.pdf_templates, name='pdf_templates'),
    re_path(r'^get_pdf/(?P<module>\w+)/(?P<id>[\w-]+)/$',
        views.get_pdf, name='get_pdf'),
    re_path(r'^index.php$', views.crm_entry_point, name='crm_entry_point'),
    re_path('^offline/$', views.offline, name='offline'),
]
