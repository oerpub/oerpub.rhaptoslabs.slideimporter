import urllib, urllib2
#from xml2dict import fromstring
import  time
import sha
import sys
from BeautifulSoup import BeautifulSoup
class SlideShareApi:
    def __init__(self,params_as_dict,proxy=None):
        if ('api_key' not in params_as_dict) or ('api_secret' not in params_as_dict):
            print >> sys.stderr, "API Key and Secret Missing"
            return 0
        if proxy:
            self.use_proxy = True
            if not istnstance(proxy,dict):
                print >> sys.stderr," Proxy Config should be a dictionary"
                return 0
            self.proxy = proxy
        else:
            self.use_proxy = False

        self.params = params_as_dict
        if self.use_proxy:
            self.setup_proxy()

    def set_api_parameters(self,**args):
        timestamp = int(time.time())
        all_params = {'api_key' : self.params['api_key'],'ts' :
                timestamp,'hash' : sha.new(self.params['api_secret'] + str(timestamp)).hexdigest()}
        for argument in args:
            all_params[argument] = args[argument]

        return urllib.urlencode(all_params)
    
    def setup_proxy(self):
       
        urllib2.ProxyHandler({'http':'http://%(username)s:%(password)s@%(host)s:%(port)s'%self.proxy})
        proxy_opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(proxy_opener)

 

    def get_slideshow_by_user(self,username_for):
        params = self.set_api_parameters()
        url = "http://www.slideshare.net/api/2/get_slideshows_by_user?username_for=" + str(username_for)
        data = urllib2.urlopen(url,params).read()
        soup = BeautifulSoup(data)
        return soup

def main(username="saketkc"):
    ss_api = SlideShareApi({"api_key":"oQO2stCt", "api_secret":"CnaNZzxx"})
    soup = ss_api.get_slideshow_by_user(username)
    output = ""
    for index,slideshow in enumerate(soup.findAll('slideshow')):
        title = slideshow.find('title').string
        url = slideshow.find('url').string
        downloadurl = slideshow.find('downloadurl').string
        output += str(index+1) + ". " + title + "\n URL: " + url + "\n Download Url : " + downloadurl
    print output

if __name__ == "__main__":
    main()
