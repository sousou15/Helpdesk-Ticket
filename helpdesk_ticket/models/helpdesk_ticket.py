from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HelpdeskTicket(models.Model):
    """
    Model to manage helpdesk tickets.
    """
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _rec_name = 'ticket_number'
    _order = 'ticket_number desc'

    customer_id = fields.Many2one('res.partner', string='Customer', required=True, help="Customer reporting the issue.")
    technician_id = fields.Many2one('res.users', string='Technician', help="Technician assigned to resolve the issue.")
    problem_description = fields.Text(string='Problem Description', help="Detailed description of the reported issue.")
    solution_description = fields.Text(string='Solution Description', help="Detailed description of the solution applied.")
    state = fields.Selection([
        ('new', 'New'),
        ('review', 'Review'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], string='Status', default='new', tracking=True, help="Current status of the ticket.")
    ticket_number = fields.Char(
        string='Ticket No.',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: self._get_ticket_number(),
        help="Unique ticket number."
    )

    customer_phone = fields.Char(related='customer_id.phone', string='Customer Phone', store=True)

    @api.model
    def _get_ticket_number(self):
        """
        Generates the ticket number using the sequence.
        """
        sequence = self.env['ir.sequence'].next_by_code('helpdesk.ticket')
        if sequence:
            return sequence
        else:
            # Generates a default value if the sequence is not available
            return 'TK-0000'

    @api.onchange('technician_id')
    def _onchange_technician(self):
        """
        Changes the ticket status to 'Review' when a technician is assigned.
        """
        if self.technician_id:
            self.state = 'review'
    
    @api.onchange('solution_description')
    def _onchange_solution_description(self):
        """
        Changes the ticket status to 'Resolved' when a solution description is added.
        """
        if self.solution_description and self.state == 'in_progress':
            self.state = 'resolved'

    def action_start_work(self):
        """
        Changes the ticket status to 'In Progress' when the technician starts working on it.
        """
        if self.state == 'review':
            self.state = 'in_progress'
        elif self.state != 'review':
            raise ValidationError("The ticket must be in 'Review' status to start work.")

    def action_resolve(self):
        """
        Changes the ticket status to 'Resolved' when a solution description is added.
        """
        if self.solution_description and self.state == 'in_progress':
            self.state = 'resolved'
        elif self.state != 'in_progress':
            raise ValidationError("The ticket must be in 'In Progress' status to mark it as resolved.")

    def action_print_report(self):
        return self.env.ref('helpdesk_ticket.action_report_helpdesk_ticket').report_action(self)
