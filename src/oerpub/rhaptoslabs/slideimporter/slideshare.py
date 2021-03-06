import urllib, urllib2
import  time
import sha
import sys
import mimetools, mimetypes
from cStringIO import StringIO
from BeautifulSoup import BeautifulSoup

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable
class SlideShowDoesNotExistError(Exception):
    def __init__(self,message):
        self.message = message
class MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10 
    
    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                     if type(value) == file:
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)
            request.add_data(data)
        return request

    def multipart_encode(vars, files, boundary = None, buf = None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buf is None:
            buf = StringIO()
        for(key, value) in vars:
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"' % key)
            buf.write('\r\n\r\n' + str(value) + '\r\n')
        for(key, fd) in files:
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename))
            buf.write('Content-Type: %s\r\n' % contenttype)            
            fd.seek(0)
            buf.write('\r\n' + fd.read() + '\r\n')
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        return boundary, buf
    multipart_encode = Callable(multipart_encode)
    https_request = http_request


class SlideShareApi:
    def __init__(self,params_as_dict,proxy=None):
        if ('api_key' not in params_as_dict) or ('api_secret' not in params_as_dict):
            print >> sys.stderr, "API Key and Secret Missing"
            return 0
        if proxy:
            self.use_proxy = True
            if not isinstance(proxy,dict):
                print >> sys.stderr," Proxy Config should be a dictionary"
                return 0
            self.proxy = proxy
        else:
            self.use_proxy = False

        self.params = params_as_dict
        if self.use_proxy:
            self.setup_proxy()

    def set_api_parameters(self,encode = True, **args):
        timestamp = int(time.time())
        all_params = {'api_key' : self.params['api_key'],'ts' :
                timestamp,'hash' : sha.new(self.params['api_secret'] + str(timestamp)).hexdigest()}
        for argument in args:
            if argument != 'slideshare_src':
                all_params[argument] = args[argument]
        if encode:
            return urllib.urlencode(all_params)
        else:
            return all_params

    def setup_proxy(self):
        proxy_support = urllib2.ProxyHandler({'http':'http://%(username)s:%(password)s@%(host)s:%(port)s'%self.proxy})
        proxy_opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(proxy_opener)

    def get_slideshow_by_user(self,username_for):
        params = self.set_api_parameters()
        url = "https://www.slideshare.net/api/2/get_slideshows_by_user?username_for=" + str(username_for)
        data = urllib2.urlopen(url,params).read()
        soup = BeautifulSoup(data)
        return soup
        
    def upload_slideshow(self,username,password,title,src_file):
        params =  self.set_api_parameters(encode = False,username=username,password=password,slideshow_title=title,slideshow_srcfile=src_file)
        params['slideshow_srcfile'] = open(src_file, 'rb')
        opener = urllib2.build_opener(MultipartPostHandler)
        data = opener.open("https://www.slideshare.net/api/2/upload_slideshow", params).read()
        return data    
    
    def get_slideshow_info(self,slideshow_id):
        params = self.set_api_parameters(encode=True,slideshow_id=str(slideshow_id))
        data = urllib2.urlopen("https://www.slideshare.net/api/2/get_slideshow", params).read()
        soup = BeautifulSoup(data)
        status = soup.find('status').string
        return status
        
    def get_detailed_info(self,slideshow_id):
        params = self.set_api_parameters(encode=True,slideshow_id=str(slideshow_id),detailed=1,get_transcript=1)
        data = urllib2.urlopen("https://www.slideshare.net/api/2/get_slideshow", params).read()
        soup = BeautifulSoup(data)
        return soup      

def get_number_of_slides(soup):
    return soup.find('numslides').string
    
def get_download_link(soup):
    try:
        return soup.find('downloadurl').string
    except:
        SlideShowDoesNotExistError("No Download link generated yet")        

def get_slideshow_status(soup):
    return soup.find('status').string

def get_transcript(soup):
    try:
        return soup.find('transcript').string
    except:
        return ""

def show_slideshow(slideshow_id):
    ss_api = SlideShareApi({"api_key":"oQO2stCt", "api_secret":"CnaNZzxx"})
    return ss_api.get_slideshow_info(slideshow_id)

def get_details(slideshow_id):
    ss_api = SlideShareApi({"api_key":"oQO2stCt", "api_secret":"CnaNZzxx"})
    return ss_api.get_detailed_info(slideshow_id)

def get_ppt_location(soup):
    return soup.find('pptlocation').string    

def get_stripped_title(soup):
    return soup.find('strippedtitle').string  
    
def get_slideshow_download_url(soup):
    return soup.find('url').string + "/download"
    
def get_embed_code(soup):
    return soup.find('embed').string



def upload_to_slideshare(username,filepath):
    ss_api = SlideShareApi({"api_key":"oQO2stCt", "api_secret":"CnaNZzxx"})
    filepath = filepath.replace("\\","/")
    filename = filepath.split('/')[-1]
    uploadname = filename.split('.')[0]
    soup = BeautifulSoup(ss_api.upload_slideshow('saketkc','fedora',uploadname,filepath))
    return soup.find('slideshowid').string
def fetch_slideshow_status(slideshow_id):
	ss_api = SlideShareApi({"api_key":"oQO2stCt", "api_secret":"CnaNZzxx"})
	return ss_api.get_slideshow_info(slideshow_id)
	
	
if __name__ == "__main__":
    ss = upload_to_slideshare("saketkc","/home/saket/Downloads/Training_Authoring.ppt")   
    x = get_details(ss)
    print x
    print get_slideshow_download_url(x)
    #print get_download_link(x)
    #print get_ppt_location(x)
