# Copyright (c) 2013, Web Notes Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Language(Document):
	pass

def get_info(lang):
	def _get():
		return {
			"total": frappe.db.sql("""select count(*) from `tabTranslated Message`
				where language=%s""", lang)[0][0],
			"verified": frappe.db.sql("""select count(*) from `tabTranslated Message`
				where language=%s and verified > 0""", lang)[0][0]
		}

	return frappe.cache().get_value("lang-data:" + lang, _get)

def get_data():
	lang = frappe.get_doc("Language", frappe.form_dict.lang)
	data = {
		"language_name": lang.language_name,
		"messages": frappe.db.sql("""select name, source, translated, verified, modified
			from `tabTranslated Message`
			where language = %s order by source""", lang.name, as_dict=True)
	}
	return data

def clear_cache():
	for lang in frappe.db.sql_list("select name from tabLanguage"):
		frappe.cache().delete_value("lang-data:" + lang)
