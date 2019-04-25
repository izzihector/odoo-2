# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo.addons.account.tests.account_test_classes import AccountingTestCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestPart(AccountingTestCase):

    def setUp(self):
        super(TestPart, self).setUp()

        self.part = self.env['part.order']
        self.ResUsers = self.env['res.users']
        self.partMakeInvoice = self.env['part.order.make_invoice']
        self.res_group_user = self.env.ref('stock.group_stock_user')
        self.res_group_manager = self.env.ref('stock.group_stock_manager')
        self.part_r0 = self.env.ref('part.part_r0')
        self.part_r1 = self.env.ref('part.part_r1')
        self.part_r2 = self.env.ref('part.part_r2')

        self.res_part_user = self.ResUsers.create({
            'name': 'Part User',
            'login': 'maru',
            'email': 'part_user@yourcompany.com',
            'groups_id': [(6, 0, [self.res_group_user.id])]})

        self.res_part_manager = self.ResUsers.create({
            'name': 'Part Manager',
            'login': 'marm',
            'email': 'part_manager@yourcompany.com',
            'groups_id': [(6, 0, [self.res_group_manager.id])]})

    def _create_simple_part_order(self, invoice_method):
        product_to_part = self.env.ref('product.product_product_5')
        partner = self.env.ref('base.res_partner_address_1')
        return self.env['part.order'].create({
            'product_id': product_to_part.id,
            'product_uom': product_to_part.uom_id.id,
            'address_id': partner.id,
            'guarantee_limit': datetime.today().strftime('%Y-%m-%d'),
            'invoice_method': invoice_method,
            'partner_invoice_id': partner.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'partner_id': self.env.ref('base.res_partner_12').id
        })

    def _create_simple_operation(self, part_id=False, qty=0.0, price_unit=0.0):
        product_to_add = self.env.ref('product.product_product_5')
        return self.env['part.line'].create({
            'name': 'Add The product',
            'type': 'add',
            'product_id': product_to_add.id,
            'product_uom_qty': qty,
            'product_uom': product_to_add.uom_id.id,
            'price_unit': price_unit,
            'part_id': part_id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.location_production').id,
        })

    def _create_simple_fee(self, part_id=False, qty=0.0, price_unit=0.0):
        product_service = self.env.ref('product.product_product_2')
        return self.env['part.fee'].create({
            'name': 'PC Assemble + Custom (PC on Demand)',
            'product_id': product_service.id,
            'product_uom_qty': qty,
            'product_uom': product_service.uom_id.id,
            'price_unit': price_unit,
            'part_id': part_id,
        })

    def test_00_part_afterinv(self):
        part = self._create_simple_part_order('after_part')
        self._create_simple_operation(part_id=part.id, qty=1.0, price_unit=50.0)
        # I confirm part order taking Invoice Method 'After part'.
        part.sudo(self.res_part_user.id).action_part_confirm()

        # I check the state is in "Confirmed".
        self.assertEqual(part.state, "confirmed", 'Part order should be in "Confirmed" state.')
        part.action_part_start()

        # I check the state is in "Under part".
        self.assertEqual(part.state, "under_part", 'Part order should be in "Under_part" state.')

        # Repairing process for product is in Done state and I end part process by clicking on "End part" button.
        part.action_part_end()

        # I define Invoice Method 'After part' option in this part order.so I create invoice by clicking on "Make Invoice" wizard.
        make_invoice = self.partMakeInvoice.create({
            'group': True})
        # I click on "Create Invoice" button of this wizard to make invoice.
        context = {
            "active_model": 'part_order',
            "active_ids": [part.id],
            "active_id": part.id
        }
        make_invoice.with_context(context).make_invoices()

        # I check that invoice is created for this part order.
        self.assertEqual(len(part.invoice_id), 1, "No invoice exists for this part order")
        self.assertEqual(len(part.move_id.move_line_ids[0].consume_line_ids), 1, "Consume lines should be set")

    def test_01_part_b4inv(self):
        part = self._create_simple_part_order('b4part')
        # I confirm part order for Invoice Method 'Before part'.
        part.sudo(self.res_part_user.id).action_part_confirm()

        # I click on "Create Invoice" button of this wizard to make invoice.
        part.action_part_invoice_create()

        # I check that invoice is created for this part order.
        self.assertEqual(len(part.invoice_id), 1, "No invoice exists for this part order")

    def test_02_part_noneinv(self):
        part = self._create_simple_part_order('none')

        # Add a new fee line
        self._create_simple_fee(part_id=part.id, qty=1.0, price_unit=12.0)

        self.assertEqual(part.amount_total, 12, "Amount_total should be 12")
        # Add new operation line
        self._create_simple_operation(part_id=part.id, qty=1.0, price_unit=14.0)

        self.assertEqual(part.amount_total, 26, "Amount_total should be 26")

        # I confirm part order for Invoice Method 'No Invoice'.
        part.sudo(self.res_part_user.id).action_part_confirm()

        # I start the repairing process by clicking on "Start part" button for Invoice Method 'No Invoice'.
        part.action_part_start()

        # I check its state which is in "Under part".
        self.assertEqual(part.state, "under_part", 'Part order should be in "Under_part" state.')

        # Repairing process for product is in Done state and I end this process by clicking on "End part" button.
        part.action_part_end()

        self.assertEqual(part.move_id.location_id.id, self.env.ref('stock.stock_location_stock').id,
                         'Repaired product was taken in the wrong location')
        self.assertEqual(part.move_id.location_dest_id.id, self.env.ref('stock.stock_location_stock').id,
                         'Repaired product went to the wrong location')
        self.assertEqual(part.operations.move_id.location_id.id, self.env.ref('stock.stock_location_stock').id,
                         'Consumed product was taken in the wrong location')
        self.assertEqual(part.operations.move_id.location_dest_id.id, self.env.ref('stock.location_production').id,
                         'Consumed product went to the wrong location')

        # I define Invoice Method 'No Invoice' option in this part order.
        # So, I check that Invoice has not been created for this part order.
        self.assertNotEqual(len(part.invoice_id), 1, "Invoice should not exist for this part order")
