import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import Lib.pytorch3dunet.predict as predict
import Lib.pytorch3dunet.datasets.hdf5
from Lib.pytorch3dunet.nii2h5 import *
import SimpleITK as sitk
import sitkUtils
import slicer
#
# TMSPrediction
#

class TMSPrediction(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "TMS Prediction"
        self.parent.categories = ["TMS"]
        self.parent.dependencies = []
        self.parent.contributors = ["John Doe (AnyWare Corp.)"]
        self.parent.helpText = """"""
        self.parent.acknowledgementText = """"""


#
# TMSPredictionWidget
#

class TMSPredictionWidget(ScriptedLoadableModuleWidget):
    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        self.logic = None
        self._parameterNode = None
        self._updatingGUIFromParameterNode = False

    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # GUI
        collapsibleGB = ctk.ctkCollapsibleGroupBox()
        self.layout.addWidget(collapsibleGB)

        # new layout for collapsible button
        self.formLayout = qt.QFormLayout(collapsibleGB)


        ############
        # Input volume 1 selector
        #
        """
        self.inputSelector1 = slicer.qMRMLNodeComboBox()
        self.inputSelector1.nodeTypes = (("vtkMRMLScalarVolumeNode"), "")
        self.inputSelector1.addAttribute("vtkMRMLScalarVolumeNode", "LabelMap", 0)
        self.inputSelector1.selectNodeUponCreation = True
        self.inputSelector1.addEnabled = False
        self.inputSelector1.removeEnabled = False
        self.inputSelector1.noneEnabled = False
        self.inputSelector1.showHidden = False
        self.inputSelector1.showChildNodeTypes = False
        self.inputSelector1.setMRMLScene(slicer.mrmlScene)
        self.inputSelector1.setToolTip("Select Max-Eig Nifty")
        self.formLayout.addRow("Max-Eig Nifty: ", self.inputSelector1)

        ############
        # Input volume 2 selector
        #
        self.inputSelector2 = slicer.qMRMLNodeComboBox()
        self.inputSelector2.nodeTypes = (("vtkMRMLScalarVolumeNode"), "")
        self.inputSelector2.addAttribute("vtkMRMLScalarVolumeNode", "LabelMap", 0)
        self.inputSelector2.selectNodeUponCreation = True
        self.inputSelector2.addEnabled = False
        self.inputSelector2.removeEnabled = False
        self.inputSelector2.noneEnabled = False
        self.inputSelector2.showHidden = False
        self.inputSelector2.showChildNodeTypes = False
        self.inputSelector2.setMRMLScene(slicer.mrmlScene)
        self.inputSelector2.setToolTip("Select D Nifty")
        self.formLayout.addRow("D Nifty: ", self.inputSelector2)
        """

        # Select Eig
        self.EigInName = qt.QLineEdit("C:\Slicer\Slicer 4.13.0-2021-08-24\Mod\SampleDat\Coil1_137027_C2_ydir1_max_eig.nii.gz")
        self.formLayout.addRow("Enter Eig-Max Nifty:", self.EigInName)

        # Select D
        self.DInName = qt.QLineEdit("C:\Slicer\Slicer 4.13.0-2021-08-24\Mod\SampleDat\Coil1_137027_C2_ydir1_D.nii.gz")
        self.formLayout.addRow("Enter D Nifty:", self.DInName)

        # Select Output Node Name
        self.NOutName = qt.QLineEdit("TMS")
        self.formLayout.addRow("Enter Output Name:", self.NOutName)

        # Apply Button
        self.applyButton = qt.QPushButton("Apply")
        self.applyButton.toolTip = "Run TMS Prediction"
        self.applyButton.enabled = True
        self.formLayout.addRow(self.applyButton)

        # connections
        self.applyButton.clicked.connect(self.onApplyButton)
        # self.inputSelector1.currentNodeChanged.connect(self.onNewNode)

    def cleanup(self):
        """
        Called when the application closes and the module widget is destroyed.
        """
        # self.removeObservers()

    def onNewNode(self):
        self.NOutName.clear()
        self.NOutName.insert(self.inputSelector1.currentNode().GetName()+"_TMS")


    def onApplyButton(self):
        try:
            wdir = os.path.dirname(os.path.realpath(__file__))+"\\wdir\\"


            # eig_nifty = self.inputSelector1.currentNode().GetName()
            # D_nifty   = self.inputSelector2.currentNode().GetName()

            
            eig_nifty = self.EigInName.text
            D_nifty = self.DInName.text
            output = self.NOutName.text

            if output.strip() is "":
                output = self.inputSelector1.currentNode().GetName()+"_TMS"

            h5input = nifty2h5(eig_nifty, D_nifty, wdir,output)

            result = predict.main()
            print(result)



        except Exception as e:
            slicer.util.errorDisplay("Failed to compute results: " + str(e))
            import traceback
            traceback.print_exc()


#
# TMSPredictionLogic
#

class TMSPredictionLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

    def __init__(self):
        """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
        ScriptedLoadableModuleLogic.__init__(self)
