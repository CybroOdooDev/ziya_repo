# -*- coding: utf-8 -*-
from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # ── Gemini API key ────────────────────────────────────────────────────────
    gemini_api_key = fields.Char(
        string='Gemini API Key',
        config_parameter='predict_late_payment.gemini_api_key',
        password=True,
        placeholder='AIza...',
        help='Free API key from https://aistudio.google.com/apikey')

    gemini_model = fields.Selection([
        ('gemini-2.5-flash',      'Gemini 2.5 Flash'),
        ('gemini-2.5-flash-lite', 'Gemini 2.5 Flash-Lite'),
        ('gemini-2.5-pro',        'Gemini 2.5 Pro'),
        ('gemini-2.0-flash',      'Gemini 2.0 Flash'),
    ], string='Gemini Model',
       config_parameter='predict_late_payment.gemini_model',
       default='gemini-2.5-flash',
       help='Model to use for payment risk analysis.')

    def action_test_gemini_connection(self):
        """Test the Gemini API key and show result."""
        result = self.env['payment.risk.ai.service'].test_connection()
        ok = result.startswith('OK')
        return {
            'type': 'ir.actions.client',
            'tag':  'display_notification',
            'params': {
                'title':   _('Gemini Connected!') if ok else _('Gemini Connection Failed'),
                'message': result,
                'sticky':  True,
                'type':    'success' if ok else 'danger',
            },
        }

    def action_get_gemini_key(self):
        """Open Google AI Studio to get a free API key."""
        return {
            'type':   'ir.actions.act_url',
            'url':    'https://aistudio.google.com/apikey',
            'target': 'new',
        }
