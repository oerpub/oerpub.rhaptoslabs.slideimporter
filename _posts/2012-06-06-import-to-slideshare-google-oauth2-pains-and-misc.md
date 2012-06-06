---
layout: post
title: "Import to Slideshare, Google OAuth2 Pains and Misc "
description: "Some quick snippets for consuming SlideShare and Google Docs API in python and OAUTH2"
category: 
tags: [slideshare,google docs api,gdata python, google docs upload oauth2,google oauth2]
---
{% include JB/setup %}

I completed the complete UI flow for importing to SlideShare <http://www.slideshare.net> . The UI flow is 
like this :(I will be referring to the user as *he* henceforth)
1. User logs in to Connexions <http://www.cnx.org>. To import a slide from his desktop he is directed to 
the http://www.cnx.org/slideshare_importer page. 

<img src ="assets/images/view1.png"/>

2. User can choose from PPT/PPTX/ODT presentation from his workstation and click 'Import' . The presenation
will get deposited in Connexions and will be queued for Conversion at SlideShare. 

<img src="assets/images/view2.png"/>

3. As SlideShare processes Slideshows in batches, there is generally a lag of 20 minutes before the SlideShow
get s converted at the SLideSHare End. The view looks like this :
<img src = "assets/images/view3.png" />

The user can click on *Refresh Status* to check if the slideshow has been converted


4. Once the Slideshow conversion is complete, it appears on the page as an oembed iframe
and a download link to download the original slides appear near it

<img src = "assets/images/view4.png"/>


The full code that got it working is here :

<script src="https://gist.github.com/2881036.js?file=python_slideshare_api.py"></script>


The other Challenge was to do similar stuff for Google Presentatios : 

I am just writing the code for it , will update this post later to talk about the logic(I have it on a different workstation and forgot to git add it :p)

<script src="https://gist.github.com/2881074.js?file=google_docs_upload_api_python.py"></script>





Saket 

