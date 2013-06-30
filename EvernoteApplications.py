from evernote.api.client import EvernoteClient
from evernote.api.client import NoteStore


class Library(object):

	def __init__(self, auth_token):
		"""
		Initialize access to the Evernote library.

		Arguments:
			auth_token (string) Evernote authentication token

		Implements the following Evernote client components:
			client (EvernoteClient)
			noteStore (NoteStore)
			userStore (UserStore)
			notebooks (list of Notebook)
			tags (list of Tag)
		"""

		self.auth_token = auth_token
		self.client = EvernoteClient(token = self.auth_token, sandbox = False)
		self.noteStore = self.client.get_note_store()
		self.userStore = self.client.get_user_store()
		self.notebooks = self.noteStore.listNotebooks(self.auth_token)
		self.tags = self.noteStore.listTags(self.auth_token)


class Application(object):

	def __init__(self, appName):
		"""
		Template class for generic application features.

		Arguments:
			appName (string) Provides the application name
		"""

		self.name = appName


class NotebookArchiveApplication(Application):

	def __init__(self, appName, library):
		"""
		Initializes the application Notebook Archive

		Arguments:
			appName (string) Provides the application name
			library (Library) Provides access to the Evernote library
		"""

		self.name = appName
		self.library = library
