
# coding=utf-8
import os
import os.path
import xml.dom.minidom
 
path = 'Annotations'
files = os.listdir(path)
s = []
for xmlFile in files:
	portion = os.path.splitext(xmlFile)
	if not os.path.isdir(xmlFile):
 
		dom = xml.dom.minidom.parse(os.path.join(path, xmlFile))

		root = dom.documentElement
		name = root.getElementsByTagName('name')

		for i in range(len(name)):
			if name[i].firstChild.data == 'pedestrain':
				name[i].firstChild.data = 'red pedestrian'
	with open(os.path.join(path, xmlFile), 'w', encoding='UTF-8') as fh:
		dom.writexml(fh)
		print('replace filename OK!')
