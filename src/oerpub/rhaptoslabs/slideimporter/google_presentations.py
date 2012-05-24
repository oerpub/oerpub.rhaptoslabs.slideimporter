import gdata.docs.data
import gdata.docs.client
import gdata.docs.service
import sys
import gdata.client
import gdata.docs.client
import os
import stat
import mimetools, mimetypes
import time
import atom
class GooglePresentationUploader:
	def __init__(self,username,password):
		self.client = gdata.docs.client.DocsClient(source='connexions')
		self.client.api_version = "3"
		self.client.ssl = True
		self.client.ClientLogin(username, password, self.client.source)
	
	def upload(self,filepath):
		self.fd = open(filepath,"r")
		self.file_size = os.fstat(self.fd.fileno())[stat.ST_SIZE]
		self.filename = self.fd.name.split('/')[-1]
		self.file_type = mimetypes.guess_type(self.filename)[0] or 'application/octet-stream'
		self.media = gdata.data.MediaSource()
		self.media.SetFileHandle(filepath, self.file_type)
		self.new_presentation_resource = gdata.docs.data.Resource(filepath, self.filename)
		self.new_presentation = self.client.CreateResource(self.new_presentation_resource, create_uri=gdata.docs.client.RESOURCE_UPLOAD_URI, media=self.media)

# Is there a better way to get the reource id ?, This originaly returnds  'presentaion : id'
	def get_resource_id(self):
		self.resource_id = self.new_presentation.resource_id.text.split(':')[1] 
		return self.resource_id

	def get_revision_feeds(self):
		self.resource = self.client.GetResourceById(self.get_resource_id())
		self.revision_feeds = self.client.GetRevisions(self.resource)

# We havn't edited the PPT so just fetching the first revision
	def get_first_revision_feed(self):
		self.get_revision_feeds()
		self.entry = self.revision_feeds.entry[0]
		return self.entry
	def publish_presentation_on_web(self):
		self.entry.publish = gdata.docs.data.Publish(value='true')
		self.entry.publish_auto = gdata.docs.data.PublishAuto(value='true')
		self.update_entry = self.client.update(self.entry,force=True)
	def get_embed_url(self):
		s = """<iframe src="https://docs.google.com/presentation/embed?id="""+self.resource_id+"""&start=false&loop=false&delayms=3000" frameborder="0" width="1058" height="823" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>"""
		print s

if __name__ == "__main__":
	a = GooglePresentationUploader("saketkc","howdoyoudothis1314.")
	a.upload("/home/saket/Downloads/presentation.ppt")
	a.get_resource_id()
	a.get_first_revision_feed()
	a.publish_presentation_on_web()
	a.get_embed_url()