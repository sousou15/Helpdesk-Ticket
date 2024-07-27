from odoo.tests import common

class TestHelpdeskTicket(common.TransactionCase):

    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
            'phone': '1234567890',
        })
        self.user = self.env['res.users'].create({
            'name': 'Test Technician',
            'login': 'test_technician',
        })

    def test_ticket_creation(self):
        ticket = self.env['helpdesk.ticket'].create({
            'ticket_number': 'TK-0001',
            'customer_id': self.partner.id,
            'technician_id': self.user.id,
            'problem_description': 'Test problem',
        })
        self.assertEqual(ticket.ticket_number, 'TK-0001')
        self.assertEqual(ticket.customer_id, self.partner)
        self.assertEqual(ticket.technician_id, self.user)

    def test_ticket_state_change(self):
        ticket = self.env['helpdesk.ticket'].create({
            'ticket_number': 'TK-0002',
            'customer_id': self.partner.id,
            'technician_id': self.user.id,
            'problem_description': 'Test problem',
        })
        ticket.action_start_work()
        self.assertEqual(ticket.state, 'in_progress')

        ticket.solution_description = 'Test solution'
        ticket.action_resolve()
        self.assertEqual(ticket.state, 'resolved')
