# -*- coding: utf-8 -*-
from odoo import http


class BookLibrary(http.Controller):

    @http.route('/book_library/book_library/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/book_library/book_library/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('book_library.listing', {
            'root': '/book_library/book_library',
            'objects': http.request.env['melon.book'].search([]),
        })

    @http.route('/book_library/book_library/objects/<model("melon.book"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('book_library.object', {
            'object': obj
        })
