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
        self.render("textbook_view.html")

class EditContent(BaseHandler):
    def get(self):
	self.render("edit_view.html")

