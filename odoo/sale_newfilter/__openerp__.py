{
    'name':'Sale filters Qarea',
    'description':'Adds new filters to customer, lead and opportunities viewes',
    'author':'Leonid Kolesnichenko',
    'depends':['sale','crm','marketing_crm','project_team'],
    'version': '8.2.0',
    'summary': "Changed positions of fields in leads",
    'data':[
            'sale_newfilter_lead_view.xml',
            'sale_newfilter_oppo_view.xml',
            'res_partner_view.xml',
            'lead_report_view.xml',
            'lead_convert_wizard.xml',
            'data/lead_type.xml',
            'security/ir.model.access.csv',
    ],
    'css': ['static/src/css/lead.css'],
    'application':True,
}