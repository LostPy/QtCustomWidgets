import sys, os
from PyQt5 import QtCore, QtGui
 
# lance de la bibliothèque Qt4
app = QtCore.QCoreApplication(sys.argv)

base_directory = os.path.abspath(os.path.dirname(__file__))

envdico = os.environ.copy()  # lit les variables d'environnement dans un dictionnaire

envdico['PYTHONPATH'] = os.path.join(base_directory, 'widgets')  # enregistre dans PYTHONPATH le répertoire des fichiers des widgets
envdico['PYQTDESIGNERPATH'] = os.path.join(base_directory, 'plugins')  # enregistre dans PYQTDESIGNERPATH le répertoire des fichiers des plugins
 
# crée le process d'environnement des variables d'environnement
process_environment = QtCore.QProcessEnvironment()
for name, value in envdico.items():
	process_environment.insert(name, value)

designer = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.BinariesPath)  # trouve l'adresse du Designer à lancer selon l'OS (corriger selon la configuration)

if sys.platform == 'win32':
    designer += r'\designer.exe'  # Windows
elif sys.platform == 'linux':
    designer += '/designer'  # Linux
elif sys.platform == 'darwin':
    designer += '/Designer.app/Contents/MacOS/Designer'  # Mac OS X
else:
    pass  # autre cas à définir si nécessaire
    
print(designer)
 
# lance Designer dans un nouveau processus avec les variables d'environnement
proc = QtCore.QProcess()
proc.setProcessEnvironment(process_environment)
proc.waitForFinished(-1)
sys.exit(proc.exitCode())
