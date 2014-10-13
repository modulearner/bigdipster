#!/usr/bin/env python3.4

from lib.basehandler import BaseHandler

class CardView(BaseHandler):
    def get(self):
        self.render("card_view.html")

class CirclePack(BaseHandler):
    def get(self):
        self.render("circlepack.html")

class TextbookView(BaseHandler):
    def get(self):
        node_id = self.get_argument("node_id")
        self.render("textbook_view.html", node_id = node_id)

class EditContent(BaseHandler):
    def get(self):
	self.render("edit_view.html")

