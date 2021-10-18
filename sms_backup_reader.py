from xml.dom import minidom


class BackupReader:

	# Holds information retrieved from file
	texts = dict()

	def __init__(self, filename):
		global texts

		# Open the passed filename and get all sms related elements
		xml_document = minidom.parse(filename)
		sms_tags = xml_document.getElementsByTagName("sms")

		# Search through all tags and assign them a spot in the dictionary
		for s in sms_tags:
			text = "Conversation found with " + s.attributes["contact_name"].value.strip() + ":" + s.attributes["body"].value
			text_date = s.attributes["readable_date"].value
			self.texts[text_date] = text

	# Returns a string of unformatted data
	def get_texts(self):
		global texts
		return self.texts

	# Returns a string of formatted data based on what the user specifies to add (list)
	def get_texts_formatted(self, to_add):
		global texts
		f_texts = ""

		# Loop through all data and return only the necessary parts
		for key in self.texts.keys():
			body = self.texts[key][self.texts[key].find(":") + 1:]
			date = key + " "
			contact = self.texts[key][:self.texts[key].find(":")] + " "

			f_texts += date if to_add[1] == 1 else ""
			f_texts += contact if to_add[2] == 1 else ""
			f_texts += body if to_add[0] == 1 and to_add[1] == 0 and to_add[2] == 0 else ": " + body if (to_add[1] == 1 or to_add[2] == 1) and to_add[0] == 1 else ""
			f_texts += "\n"

		return f_texts
