# -*- coding: utf-8 -*-

import ast
import base64
import csv
import functools
import glob
import itertools
import jinja2
import logging
import operator
import datetime
import hashlib
import os
import re
import simplejson
import sys
import time
import urllib2
import zlib
from xml.etree import ElementTree
from cStringIO import StringIO

import babel.messages.pofile
import werkzeug.utils
import werkzeug.wrappers
try:
    import xlwt
except ImportError:
    xlwt = None

import openerp
import openerp.modules.registry
from openerp.addons.base.ir.ir_qweb import AssetsBundle, QWebTemplateNotFound
from openerp.modules import get_module_resource
from openerp.tools import topological_sort
from openerp.tools.translate import _
from openerp import http

from openerp.http import request, serialize_exception as _serialize_exception

_logger = logging.getLogger(__name__)

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('openerp.addons.web', "views")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = simplejson.dumps

# 1 week cache for asset bundles as advised by Google Page Speed
BUNDLE_MAXAGE = 60 * 60 * 24 * 7

#----------------------------------------------------------
# OpenERP Web helpers
#----------------------------------------------------------

db_list = http.db_list

db_monodb = http.db_monodb
class Session(openerp.addons.web.controllers.main.Session):
    @http.route('/web/session/change_password', type='json', auth="user")
    def change_password(self, fields):
        level = request.session.model('res.users').browse(request.session.uid).company_id.level
        old_password, new_password,confirm_password,varpassword_strength = operator.itemgetter('old_pwd', 'new_password','confirm_pwd','varpassword_strength')(
                dict(map(operator.itemgetter('name', 'value'), fields)))
        if (int(varpassword_strength) - int(level))<0 :
            return {'error': _('Your password level is too low.'),'title': _('Change Password')}
        if not (old_password.strip() and new_password.strip() and confirm_password.strip()):
            return {'error':_('You cannot leave any password empty.'),'title': _('Change Password')}
        if new_password != confirm_password:
            return {'error': _('The new password and its confirmation must be identical.'),'title': _('Change Password')}
        try:
            if request.session.model('res.users').change_password(
                old_password, new_password):
                return {'new_password':new_password}
        except Exception:
            return {'error': _('The old password you provided is incorrect, your password was not changed.'), 'title': _('Change Password')}
        return {'error': _('Error, password not changed !'), 'title': _('Change Password')}

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
