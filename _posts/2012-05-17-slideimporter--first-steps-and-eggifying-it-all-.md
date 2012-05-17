---
layout: post
title: "Slideimporter : First Steps and Eggifying it all ! "
description: ""
category: 
tags: []
---
{% include JB/setup %}
After struggling for quiet a time with getting used to Pyramid framework, I finally could get 
started with it. I could finally add a new page to the current oerpub.swordpush.buildout  
# What is buildout ?  
Buildout is used for **deploying applications** and the possibly needed dependecies in a repeatable way. It is possible that the 
dependecies  may not be just Python eggs. 
In short it acts like an importer for all the egg. Si once you do a buiild out (I will be explaining this steps shortly) the 
files that come up in the **bin** directory will have a path defined something like  this
  
	import sys  
	sys.path[0:0] = [  
		 '/some/thing1.egg',  
			  # and other things  
			]  

# What is  the need of Buildout ??
	It is in a very basic sense a package manager a-la virtual environment that gives isolates you 
	from os packaging. No matter what OS you develop on and what OS you deploy too.



Now I had to create a new repo for my GSoC 2012 project, which sits here : <https://github.com/oerpub/oerpub.rhaptoslabs.slideimporter>

This does not end here ! I have to eggify my repo, how do you do this ? But before that :


# What does eggifying your source code mean ?
	In lay man language Eggs are to Python as JARS are tp JAVA or .debs are to Debian and
	RPMs to Fedora. Its basically a package manager,a way of bundling additional information
	with a Python project that allows projects dependecies to be checked and satisfied at runtime
	The general packaged file format for distributing eggs is **.egg** zip file format.

More on Python eggs can be read at <http://peak.telecommunity.com/DevCenter/PythonEggs>

	
The next step was to include my code in the buildout, integrating it with rest of swordpushweb/  
1. I created a new branch on the swordpushweb-buildout repo : *git checkout -b gsoc2012*  
2. Added in the [eggs] section the name of my repo:  
	eggs =
    pyramid
    oerpub.rhaptoslabs.swordpushweb
    oerpub.rhaptoslabs.sword1cnx
    oerpub.rhaptoslabs.sword2cnx
    oerpub.rhaptoslabs.cnxml2htmlpreview
    oerpub.rhaptoslabs.html_gdocs2cnxml
    oerpub.rhaptoslabs.latex2cnxml
    oerpub.rhaptoslabs.slideimporter
    rhaptos.cnxmlutils
    sword2 
  
3. Added my repository to *buildout.cfg* this way : In the [sources] part Add this line :  

*oerpub.rhaptoslabs.slideimporter = git git://github.com/oerpub/oerpub.rhaptoslabs.slideimporter.git*  

4.You are almost there , now follow the README at :  <https://github.com/oerpub/oerpub.rhaptoslabs.swordpushweb-buildout/blob/master/README.rst>  


My next post would be on how I added a *Hello World* for my repo !  
Special Thanks to Marvin and Rijk for theri help !





