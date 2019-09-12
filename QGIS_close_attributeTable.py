"""
Adapted to QGIS 3 using this base code: https://gis.stackexchange.com/a/231576/91497
"""

from PyQt5.QtWidgets import QApplication


def DeleteAllAttributeTables():
	attrTables = [d for d in QApplication.instance().allWidgets() if d.objectName().split("/")[0] == u'QgsAttributeTableDialog' or d.objectName().split("/")[0] == u'AttributeTable']
	TableName = attrTables[0].objectName().split("/")[-1]
	print("These attribute tables will be closed: '%s'"%','.join(TableName))
	for x in attrTables:
    	x.close()


def DeleteAttributeTableByName(name):
	attrTables = [d for d in QApplication.instance().allWidgets() if d.objectName().split("/")[0] == u'QgsAttributeTableDialog' or d.objectName().split("/")[0] == u'AttributeTable']
	TableName = attrTables[0].objectName().split("/")[-1]
	for x in attrTables:
		TableName = x.windowTitle().split(" :: ")[0]
		if TableName == name:
			print("Attribute table '%s' will be closed"%TableName)
			x.close()