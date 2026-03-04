# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # ── Risk score fields (read from the related record) ──────────────────────
    risk_score_id = fields.One2many(
        'payment.risk.score', 'partner_id', string='Risk Scores')
    payment_risk_score = fields.Float(
        string='Payment Risk Score', compute='_compute_payment_risk_fields',
        store=False, digits=(5, 2))
    payment_risk_level = fields.Selection(
        [('low', 'Low Risk'), ('medium', 'Medium Risk'),
         ('high', 'High Risk'), ('critical', 'Critical Risk')],
        string='Payment Risk Level', compute='_compute_payment_risk_fields',
        store=False)
    payment_risk_color = fields.Char(
        string='Risk Color', compute='_compute_payment_risk_fields', store=False)
    payment_avg_delay = fields.Float(
        string='Avg Payment Delay (days)', compute='_compute_payment_risk_fields',
        store=False, digits=(6, 1))
    payment_overdue_amount = fields.Monetary(
        string='Total Overdue Amount', compute='_compute_payment_risk_fields',
        store=False, currency_field='currency_id')
    payment_last_computed = fields.Datetime(
        string='Score Last Computed', compute='_compute_payment_risk_fields',
        store=False)
    payment_followup_suggestion = fields.Text(
        string='Follow-up Suggestion', compute='_compute_payment_risk_fields',
        store=False)
    currency_id = fields.Many2one(
        'res.currency', compute='_compute_currency', string='Currency')

    def _compute_currency(self):
        for rec in self:
            rec.currency_id = self.env.company.currency_id

    @api.depends('risk_score_id', 'risk_score_id.score',
                 'risk_score_id.risk_level', 'risk_score_id.risk_color')
    def _compute_payment_risk_fields(self):
        for partner in self:
            score_rec = partner.risk_score_id.filtered(
                lambda r: r.company_id == self.env.company
            )[:1]
            if score_rec:
                partner.payment_risk_score = score_rec.score
                partner.payment_risk_level = score_rec.risk_level
                partner.payment_risk_color = score_rec.risk_color
                partner.payment_avg_delay = score_rec.avg_delay_days
                partner.payment_overdue_amount = score_rec.total_overdue_amount
                partner.payment_last_computed = score_rec.last_computed
                partner.payment_followup_suggestion = score_rec.followup_suggestion
            else:
                partner.payment_risk_score = 0.0
                partner.payment_risk_level = False
                partner.payment_risk_color = '#6c757d'
                partner.payment_avg_delay = 0.0
                partner.payment_overdue_amount = 0.0
                partner.payment_last_computed = False
                partner.payment_followup_suggestion = False

    def action_compute_risk_score(self):
        """Button: recompute risk score from the partner form."""
        for partner in self:
            self.env['payment.risk.score'].compute_for_partner(partner.id)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Score Updated'),
                'message': _('Payment risk score has been recalculated.'),
                'sticky': False,
                'type': 'success',
            },
        }

    def action_view_risk_score(self):
        """Open the risk score detail for this partner."""
        self.ensure_one()
        score = self.env['payment.risk.score'].search([
            ('partner_id', '=', self.id),
            ('company_id', '=', self.env.company.id),
        ], limit=1)
        if not score:
            score = self.env['payment.risk.score'].compute_for_partner(self.id)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payment Risk Score'),
            'res_model': 'payment.risk.score',
            'res_id': score.id,
            'view_mode': 'form',
            'target': 'current',
        }
