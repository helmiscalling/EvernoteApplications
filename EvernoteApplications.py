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
		self.notebooks = {}
		for notebook in self.noteStore.listNotebooks(self.auth_token):
			self.notebooks[notebook.name] = notebook.guid
		self.tags = {}
		for tag in self.noteStore.listTags(self.auth_token):
			self.tags[tag.name] = tag.guid


class Application(object):

	def __init__(self):
		"""
		Template class for generic application features.

		Arguments:
			appName (string) Provides the application name
		"""

		self.name = "Application"


class NotebookArchiveApplication(Application):

	def __init__(self, library, indexTagGuid, pageTagGuid, notebookGuid):
		"""
		Initializes the application Notebook Archive

		Arguments:
			library (Library) Provides access to the Evernote library
			notebookGuid (Guid) GUID of the notebook with the indexes and pages
			indexTagGuid (Guid) GUID of the Index tag
			pageTagGuid (Guid) GUID of the Page tag
		"""

		self.name = "Notebook Archive"
		self.library = library
		self.notebookGuid = notebookGuid
		self.indexTagGuid = indexTagGuid
		self.pageTagGuid = pageTagGuid

	def findNotes(self, words):
		"""
		Find indexes that match a search, and return a dictionary
		of the index titles and pages

		Arguments:
			words (String) Search terms based on Evernote's search grammar

		Results:
			(Dictionary) Dictionary of note titles with pages
		"""

		searchFilter = NoteStore.NoteFilter()
		searchFilter.words = words
		searchFilter.notebookGuid = self.notebookGuid
		searchFilter.tagGuids = [self.indexTagGuid]

		searchSpec = NoteStore.NotesMetadataResultSpec()
		searchSpec.includeTitle = True

		foundNotes = self.library.noteStore.findNotesMetadata(self.library.auth_token, searchFilter, 0, 100, searchSpec)

		results = {}
		for note in foundNotes.notes:
			firstPosition = 12
			lastPosition = note.title.find(')')
			pages = []
			pageReference = note.title[firstPosition:lastPosition]
			for reference in pageReference.split(','):
				if len(reference) == 4:
					pages.append(self.getPage(reference))
				else:
					for i in range(int(reference[:4]), int(reference[-4:]) + 1):
						pages.append(self.getPage(str(i).zfill(4)))

			results[note.title] = pages

		return results

	def getPage(self, pageNumber):
		"""
		Get specific page resources.

		Arguments:
			pageNumber (String) The four digit page number

		Results:
			(String) Binary representation of the image
		"""

		searchFilter = NoteStore.NoteFilter()
		searchFilter.words = pageNumber
		searchFilter.notebookGuid = self.notebookGuid
		searchFilter.tagGuids = [self.pageTagGuid]

		searchSpec = NoteStore.NotesMetadataResultSpec()
		searchSpec.includeTitle = True

		for note in self.library.noteStore.findNotesMetadata(self.library.auth_token, searchFilter, 0, 100, searchSpec).notes:
			if note.title[:5] == pageNumber + ' ':
				resources = self.library.noteStore.getNote(self.library.auth_token, note.guid, False, False, False, False).resources
				return self.library.noteStore.getResourceData(self.library.auth_token, resources[0].guid)

