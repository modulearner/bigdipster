#!/usr/bin/env python3.4

from lib.basehandler import BaseHandler

class CardView(BaseHandler):
    def get(self):
        self.render("card_view.html")

