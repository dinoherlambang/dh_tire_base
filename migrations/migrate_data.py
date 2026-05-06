from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

def migrate_tire_data(env):
    # 1. Migrate Brands
    lots_with_brand = env['stock.production.lot'].search([('casing_brand', '!=', False)])
    for lot in lots_with_brand:
        brand_name = lot.casing_brand.strip()
        brand = env['dh.tire.brand'].search([('name', '=', brand_name)], limit=1)
        if not brand:
            brand = env['dh.tire.brand'].create({'name': brand_name})
        lot.tire_brand_id = brand.id
        _logger.info(f"Migrated brand {brand_name} for lot {lot.name}")

    # 2. Migrate Sizes
    lots_with_size = env['stock.production.lot'].search([('casing_size', '!=', False)])
    for lot in lots_with_size:
        size_name = lot.casing_size.strip()
        size = env['dh.tire.size'].search([('name', '=', size_name)], limit=1)
        if not size:
            size = env['dh.tire.size'].create({'name': size_name})
        lot.tire_size_id = size.id
        _logger.info(f"Migrated size {size_name} for lot {lot.name}")

    # 3. Synchronize Status
    # Move casing_status to universal tire_status
    # casing_status mapping: in_warehouse -> warehouse, in_production -> production, delivered -> warehouse (or keep), scrapped -> scrapped
    lots_with_status = env['stock.production.lot'].search([])
    for lot in lots_with_status:
        if hasattr(lot, 'casing_status'):
            mapping = {
                'in_warehouse': 'warehouse',
                'in_production': 'production',
                'scrapped': 'scrapped',
                'delivered': 'warehouse'
            }
            if lot.casing_status in mapping:
                lot.tire_status = mapping[lot.casing_status]
        
        # If it was marked as scrapped in field report, ensure status is scrapped
        if hasattr(lot, 'is_tire_scrapped') and lot.is_tire_scrapped:
            lot.tire_status = 'scrapped'

    return True
