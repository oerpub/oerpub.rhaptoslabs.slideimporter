import sys
import gdata.client
import gdata.docs.client
import os
import stat
import mimetools, mimetypes
import time
import atom
fd = open("/home/saket/Downloads/presentation.ppt","r")
file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
filename = fd.name.split('/')[-1]
file_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
#print contenttype
#print fd.name
docsclient = gdata.docs.client.DocsClient()
username = 'saketkc'
password = 'howdoyoudothis1314.'
docsclient.ClientLogin(username, password, docsclient.source)
uri = 'https://docs.google.com/feeds/upload/create-session/default/private/full'
collection = 'test'
resources = docsclient.GetAllResources(uri='https://docs.google.com/feeds/default/private/full/-/folder?title=' + collection + '&title-exact=true')
uri = resources[0].get_resumable_create_media_link().href
#uri += '?convert=false'
t1 = time.time()
uploader = gdata.client.ResumableUploader(docsclient, fd, file_type, file_size, chunk_size=1048576, desired_class=gdata.data.GDEntry)
new_entry = uploader.UploadFile(uri, entry=gdata.data.GDEntry(title=atom.data.Title(text=os.path.basename(fd.name))))

print new_entry

