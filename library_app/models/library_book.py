from odoo import fields, models
from odoo.exceptions import ValidationError


# class ProjectTaskDetails(models.Model):
#     _name = "product.details"
#     _description = "product_Detailsinfo"
#
#     # _auto = False
#     # project = fields.Many2one('product.product')
#     sales_order = fields.Many2one('sale_order')
#     partner = fields.Many2one('res.partner', string='Customer')
#     # date_deadline = fields.Char(string='Deadline Date')
#     sale_number = fields.Char(string="sales_name")
#     order_date = fields.Date(string="sales_date")
#     partner_name = fields.Char(string="PartenrName")
#     partner_phone = fields.Char(string="PartnerPhone")
#
#     def init(self):
#         self._cr.execute("""
#         select	so.name as sale_number,
# 	   			so.date_order as order_date,
# 				rp.name as partner_name,
# 				rp.phone as partner_phone
#  	   from sale_order so
# 	   join res_partner rp on so.partner_id=rp.id
#       """)

class Book(models.Model):
    _name = 'library.book'
    _description = "Book"
    name = fields.Char("Title", required=True)
    isbn = fields.Char('ISBN')
    active = fields.Boolean('Active?', default=True)
    date_published = fields.Date()
    image = fields.Binary('Cover')
    publisher_id = fields.Many2one('res.partner', string="Publisher")
    author_ids = fields.Many2many('res.partner', string='Authors')

    def _check_isbn(self):
        self.ensure_one()
        isbn = self.isbn.replace('-', '')
        digits = [int(x) for x in isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain !=0 else 0
            return digits[-1] == check


    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise ValidationError("Please provided an userful ISBN for %s" % book.name)
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s ISBN is an invalid " % book.isbn)
        return True
