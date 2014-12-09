# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
#   @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import simplejson

from flask_cors import cross_origin
from flask import request, make_response

from pywebdriver import app, config, drivers


@app.route('/pos/print_receipt', methods=['GET'])
@cross_origin()
def print_receipt_http():
    """ For Odoo 7.0"""
    params = dict(request.args)
    receipt = simplejson.loads(params['r'][0])['params']['receipt']
    # Add required information if not provided
    if not receipt.get('precision', False):
        receipt['precision'] = {
            'price': config.getint('odoo', 'precision_price'),
            'money': config.getint('odoo', 'precision_money'),
            'quantity': config.getint('odoo', 'precision_quantity')}
    else:
        if not receipt['precision'].get('price', False):
            receipt['precision']['price'] = config.getint(
                'odoo', 'precision_price')
        if not receipt['precision'].get('money', False):
            receipt['precision']['money'] = config.getint(
                'odoo', 'precision_money')
        if not receipt['precision'].get('quantity', False):
            receipt['precision']['quantity'] = config.getint(
                'odoo', 'precision_quantity')
    drivers['escpos'].push_task('receipt', receipt)
    return make_response('')
