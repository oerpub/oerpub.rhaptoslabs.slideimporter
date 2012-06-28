import gdata.docs.data
import gdata.docs.client
import gdata.docs.service
import gdata.client
import gdata.docs.client
import os
import stat
import  mimetypes
from google_api_config import CONSUMER_KEY
from google_api_config import CONSUMER_SECRET

class GoogleOAuth:

    def __init__(self,request_token=''):		
        self.client = gdata.docs.client.DocsClient(source='connexions')
        self.client.api_version = "3"
        self.client.ssl = True
        self.scopes =  ['https://docs.google.com/feeds/ https://docs.googleusercontent.com/ https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile']

    def set_oauth_callback_url(self,url='http://localhost:6543/oauth2callback'):
        self.oauth_callback_url = url
    
    def get_oauth_token_from_google(self):
        self.saved_request_token = self.client.GetOAuthToken(self.scopes, self.oauth_callback_url, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
        return self.saved_request_token

    def get_authorization_url_from_google(self):
        return self.saved_request_token.generate_authorization_url()

    def authorize_request_token(self,saved_request_token,uri):
        self.request_token = gdata.gauth.AuthorizeRequestToken(saved_request_token, uri)

    def get_access_token(self):
        self.access_token = self.client.GetAccessToken(self.request_token)
        return self.access_token

    def get_token_key(self):
        return self.access_token.token

    def get_token_secret(self):
        return self.access_token.token_secret
        
        
    def test_oauth2(self):
        token = gdata.gauth.OAuth2Token(client_id='',
                                        client_secret='',
                                        scope=self.scopes,
                                        user_agent='cnx.testing')
        return token.generate_authorize_url()
        #code = raw_input('What is the verification code? ').strip()
        #token.get_access_token(code)
        #print token.refresh_token


class GooglePresentationUploader:
    def __init__(self):
        self.client = gdata.docs.client.DocsClient(source='connexions')
        self.client.api_version = "3"
        self.client.ssl = True

    def authentincate_client_with_oauth2(self,TOKEN_KEY,TOKEN_SECRET):		
        self.client.auth_token = gdata.gauth.OAuthHmacToken(CONSUMER_KEY, CONSUMER_SECRET, TOKEN_KEY, TOKEN_SECRET, gdata.gauth.ACCESS_TOKEN, next=None, verifier=None)

    def get_resource_id(self):
        self.resource_id = self.new_presentation.resource_id.text
        return self.resource_id

    def upload(self,filepath):
        self.fd = open(filepath,"r")
        self.file_size = os.fstat(self.fd.fileno())[stat.ST_SIZE]
        self.filename = self.fd.name.split('/')[-1]
        self.file_type = mimetypes.guess_type(self.filename)[0] or 'application/octet-stream'
        self.media = gdata.data.MediaSource(file_path=filepath,content_type=self.file_type)
        self.new_presentation =  self.client.Upload(self.media,self.filename)
        #self.media.SetFileHandle(filepath, self.file_type)   #gdata = 2.0.17
        #self.new_presentation_resource = gdata.docs.data.Resource(filepath, self.filename) #gdata = 2.0.17
        #self.new_presentation = self.client.CreateResource(self.new_presentation_resource, create_uri=gdata.docs.client.RESOURCE_UPLOAD_URI, media=self.media) #gdata = 2.0.17
# Is there a better way to get the reource id ?, This originaly returnds  'presentaion : id'

    def get_revision_feeds(self):
        #self.resource = self.client.GetDoc(self.get_resource_id()) #gdata = 2.0.17
        self.get_resource_id()
        self.revision_feeds = self.client.GetRevisions(self.resource_id)
        return self.revision_feeds

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
        return s



def upload_to_googledocs(oauth_token,oauth_token_secret,filepath):
    presentation = GooglePresentationUploader()
    presentation.get_access_token()
    presentation.upload("/home/saket/Downloads/presentation.ppt")
    presentation.get_resource_id()
    presentation.get_first_revision_feed()
    presentation.publish_presentation_on_web()
    return presentation.get_embed_url()


if __name__ == "__main__":
    upload_to_googledocs("","","")

