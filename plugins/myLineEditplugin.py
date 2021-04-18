# -*- coding: utf-8 -*-
 
from PyQt5.QtGui import QIcon
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin
 
from QtCustomWidgets.testCustomWidgets.myLineEdit import MyLineEdit
 
 
class LineEditPlugin(QPyDesignerCustomWidgetPlugin):
    """classe pour renseigner Designer sur le widget
       nom de classe à renommer selon le widget
    """
 
    def __init__(self, parent=None):
        super(LineEditPlugin, self).__init__(parent)
        self.initialized = False
 
    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True
 
    def isInitialized(self):
        return self.initialized
 
    def createWidget(self, parent):
        """retourne une instance de la classe qui définit le nouveau widget
        """
        return MyLineEdit(parent)

    def name(self):
        """définit le nom du widget dans QtDesigner
        """
        return 'MyLineEdit'
 
    def group(self):
        """définit le nom du groupe de widgets dans QtDesigner
        """
        return 'testCustomWidgets'
 
    def icon(self):
        """retourne l'icone qui represente le widget dans Designer
           => un QIcon() ou un QIcon(imagepixmap)
        """
        return QIcon()
 
    def toolTip(self):
        """retourne une courte description du widget comme tooltip
        """
        return "Un QLineEdit avec un fond jaune"
 
    def whatsThis(self):
        """retourne une courte description du widget pour le "What's this?"
        """
        return "Un QLineEdit avec un fond jaune"
 
    def isContainer(self):
        """dit si le nouveau widget est un conteneur ou pas
        """
        return False
 
    def domXml(self):
        return (f"""
            <ui language="c++">
                <widget class="{self.name()}" name="{self.name()}">
                    <property name="toolTip">
                        <string>{self.toolTip()}</string>
                    </property>
                    <property name="whatsThis">
                        <string>{self.whatsThis()}</string>
                    </property>
                    <property name="styleSheet">
                        <string>background-color: yellow;</string>
                    </property>
                </widget>
                <customwidgets>
                    <customwidget>
                        <class>{self.name()}</class>
                        <extends>QWidget</extends>
                    </customwidget>
               </customwidgets>
            </ui>"""
        )
 
    def includeFile(self):
        """retourne le nom du fichier (str sans extension) du widget
        """
        return 'QtCustomWidgets.testCustomWidgets.myLineEdit'
 
