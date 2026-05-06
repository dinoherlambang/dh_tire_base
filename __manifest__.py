{
    'name': 'Centralized Tire Base Management',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Unified master data and core logic for tire management across TMS, Production, and Field Reports.',
    'author': 'Antigravity',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/tire_specification_views.xml',
        'views/stock_production_lot_views.xml',
    ],
    'installable': True,
    'application': True,
    'post_init_hook': '_migrate_existing_tire_data',
}
