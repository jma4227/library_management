# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
# Add Methods and Event handlers to models
# Ensure that if a Library Transactino is made, the Article in question must be in stock and teh
# member loaning the Article must have a valid membership.

class LibraryTransaction(Document):
	def validate(self):
		last_transaction = frappe.get_list("Library Transaction",
										   fields=["transaction_type", "transaction_date"],
										   filters = {
											   "articles": self.articles,
											   "transaction_date": ("<=", self.transaction_date),
											   "name": ("!=", self.name)
											   })
		if self.transaction_type=="Issue":
			msg = _("Articles {0} {1} has not been recorded as returned since {2}")
			if last_transaction and last_transaction[0].transaction_type=="Issue":
				frappe.throw(msg.format(self.articles, self.article_name,
										last_transaction[0].transaction_date))
		else:
			if not last_transaction or last_transaction[0].transaction_type!="Issue":
				frappe.throw(_("Cannot return article not issued"))
