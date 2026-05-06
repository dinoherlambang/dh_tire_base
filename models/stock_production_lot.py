from odoo import models, fields, api

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    # 1. Centralized Identification
    is_tire = fields.Boolean(
        string='Is Tire', 
        compute='_compute_is_tire',
        inverse='_inverse_is_tire',
        store=True,
        readonly=False,
        help="Check this to enable tire-specific fields for this serial number."
    )
    
    def _inverse_is_tire(self):
        """Allow manual override of is_tire"""
        pass
    
    @api.depends('product_id', 'product_id.categ_id')
    def _compute_is_tire(self):
        """Identify tires based on product category"""
        for lot in self:
            is_tire = False
            if lot.product_id and lot.product_id.categ_id:
                categ_name = lot.product_id.categ_id.name.lower()
                if 'tire' in categ_name or 'ban' in categ_name:
                    is_tire = True
            lot.is_tire = is_tire

    # 2. Physical Specifications (Master Data)
    tire_brand_id = fields.Many2one('dh.tire.brand', string='Tire Brand', tracking=True)
    tire_size_id = fields.Many2one('dh.tire.size', string='Tire Size', tracking=True)
    tire_pattern_id = fields.Many2one('dh.tire.pattern', string='Tread Pattern', tracking=True)
    
    # 3. Universal Metrics
    retread_count = fields.Integer(
        string='Retread Count', 
        default=0, 
        tracking=True,
        help="Number of times this tire has been retreaded."
    )
    
    # 4. Global Lifecycle Status
    tire_status = fields.Selection([
        ('new', 'New'),
        ('mounted', 'Mounted on Vehicle'),
        ('unmounted', 'Unmounted / In Warehouse'),
        ('retread', 'In Retreading'),
        ('scrapped', 'Scrapped'),
    ], string='Tire Status', default='new', tracking=True)
