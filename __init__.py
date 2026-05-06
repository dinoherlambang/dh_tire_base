from . import models

def _migrate_existing_tire_data(cr, registry):
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    _logger = __import__('logging').getLogger(__name__)
    _logger.info("Starting centralized tire data migration...")
    
    lots = env['stock.production.lot'].search([])
    for lot in lots:
        # Migrate Brand
        if hasattr(lot, 'casing_brand') and lot.casing_brand:
            brand_name = lot.casing_brand.strip()
            brand = env['dh.tire.brand'].search([('name', '=', brand_name)], limit=1)
            if not brand:
                brand = env['dh.tire.brand'].create({'name': brand_name})
            lot.tire_brand_id = brand.id

        # Migrate Size
        if hasattr(lot, 'casing_size') and lot.casing_size:
            size_name = lot.casing_size.strip()
            size = env['dh.tire.size'].search([('name', '=', size_name)], limit=1)
            if not size:
                size = env['dh.tire.size'].create({'name': size_name})
            lot.tire_size_id = size.id

        # Sync Status
        if hasattr(lot, 'casing_status'):
            mapping = {
                'in_warehouse': 'warehouse', 
                'in_production': 'production', 
                'scrapped': 'scrapped', 
                'delivered': 'warehouse'
            }
            if lot.casing_status in mapping:
                lot.tire_status = mapping[lot.casing_status]
    
    _logger.info("Centralized tire data migration completed.")
