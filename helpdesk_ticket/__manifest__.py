{
    'name': 'Helpdesk Ticket Management',
    'version': '1.0',
    'summary': 'Module to manage technical support tickets',
    'description': 'A module to manage technical support tickets with automatic state changes and PDF report generation.',
    'author': 'Your Name',
    'category': 'Services',
    'depends': ['base'],
    'data': [
        'security/helpdesk_ticket_security.xml',
        'security/ir.model.access.csv',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_ticket_report.xml',
        'data/helpdesk_ticket_data.xml',
        'reports/helpdesk_ticket_report_template.xml',
    ],
    'installable': True,
    'application': True,
}
