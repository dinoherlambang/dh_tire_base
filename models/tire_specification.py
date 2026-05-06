from odoo import models, fields

class TireBrand(models.Model):
    _name = 'dh.tire.brand'
    _description = 'Tire Brand'
    _order = 'name'
    
    name = fields.Char(string='Brand Name', required=True)
    active = fields.Boolean(default=True)

class TireSize(models.Model):
    _name = 'dh.tire.size'
    _description = 'Tire Size'
    _order = 'name'
    
    name = fields.Char(string='Tire Size', required=True)
    active = fields.Boolean(default=True)

class TirePattern(models.Model):
    _name = 'dh.tire.pattern'
    _description = 'Tread Pattern'
    _order = 'name'
    
    name = fields.Char(string='Pattern Name', required=True)
    brand_id = fields.Many2one('dh.tire.brand', string='Brand')
    active = fields.Boolean(default=True)
