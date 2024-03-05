from Main_GUI import MainFrame
from vtkActors import GlyphActor
from EdgeDetectors import HystAlgorithm
from vtkFilters import vertexFilter
from wx import App,EVT_MENU,EVT_BUTTON
from LoadPolyDataDialog import *
from SavePolyDataDialog import *
from vtk import vtkActor
class Controller:
    def __init__(self):
      self.frame=MainFrame(None)
      
      self.frame.LoadBtnL.Bind(EVT_BUTTON, self.OnLoad)
      self.frame.LoadFPBtnL.Bind(EVT_BUTTON, self.OnLoadFP)
      self.frame.ThBtnL.Bind(EVT_BUTTON, self.OnThr)
      self.frame.Bind(EVT_MENU, self.OnLoad,id=self.frame.ID_Menu_LoadMesh)
      self.frame.Bind(EVT_MENU, self.OnLoadFP,id=self.frame.ID_Menu_LoadFPMesh)
      self.frame.Bind(EVT_MENU, self.OnSave,id=self.frame.ID_Menu_SaveFPMesh)
      self.frame.Show()
      self.algo=HystAlgorithm()
      self.freatureLines=None
    def OnLoad(self,event):
          
          LoadDialog=LoadPolyDataDialog(None,"LoadPolyData")
          self.output=LoadDialog.GetPolyData()
          if not self.output : return
          self.points=self.output.GetPoints()
          
          self.frame.cleanScreen()
          self.frame.removeMnGlActor()
          self.frame.removeMxGlActor()
          
          self.frame.mx_gl_actor=vtkActor()
          self.frame.mn_gl_actor=vtkActor()
          
          self.frame.enableComponents()      
         
          self.algo.clearCurvLists()                
         
          self.mainActor = GlyphActor(polyData = self.output,opacity=1,rgbColor=[.85,.85,1],sphereSize=2).getActor()
         
          self.frame.setMainActor(self.mainActor)
          self.frame.addActor(self.mainActor)
         
          self.frame.refreshScene()
          #self.frame.ThBtnL.Enable(True)
          #self.frame.sld1.Enable(True)
          #self.frame.sld2.Enable(True)         
	     
          self.algo.findCurvatures(self.output)
    
    def OnThr(self,evt):
        self.frame.mn_checkbox_Curv_Actor.Enable(True)
        self.frame.mx_checkbox_Curv_Actor.Enable(True)
        self.frame.main_checkbox_Actor.Enable(True)
        #print self.frame.FileMenu.MenuItemCount
        self.frame.enableSaveMenuItem()
        mxThr=self.frame.getMaxThr()
        mnThr=self.frame.getMinThr()
        
        self.algo.setMaxCurvVal(mxThr)
        self.algo.setMinCurvVal(mnThr)
        
        outDict=self.algo.getEdgePoints(self.points)
        
        self.freatureLines=outDict["featueLines"]

        minVertFltr=vertexFilter(outDict["minPoints"])
        maxVertFltr=vertexFilter(outDict["maxPoints"])
        
        glSize=self.frame.getVSize()
        mn_gl_actor=GlyphActor(minVertFltr.getOutput(),opacity=1,rgbColor=list([1,0,0]),sphereSize=glSize).getActor()
        mx_gl_actor=GlyphActor(maxVertFltr.getOutput(),opacity=1,rgbColor=list([0,0,1]),sphereSize=glSize).getActor()
        
        self.frame.removeMnGlActor()
        self.frame.removeMxGlActor()
        
        self.frame.setMn_gl_actor(mn_gl_actor)
        self.frame.setMx_gl_actor(mx_gl_actor)
        
        self.frame.refreshGlPoints()
        self.frame.refreshScene()
            
    def OnLoadFP(self,evt):
      
      LoadDialog=LoadPolyDataDialog(None,"LoadPolyData")
      self.output=LoadDialog.GetPolyData()
      
      self.frame.cleanScreen()
      self.frame.disableComponents()
      
      self.mainActor = GlyphActor(polyData = self.output,opacity=1,rgbColor=[0,1,0],sphereSize=2).getActor()
         
      
      self.frame.setMainActor(self.mainActor)
      self.frame.refreshMainActor()
      self.frame.refreshScene()
      
    def OnSave(self,event):
        
      self.FinalSavePolyData=SavePolyDataDialog(None,"Write Final Registered Surface")


      self.FinalSavePolyData.SetInput(self.freatureLines)
      self.FinalSavePolyData.ShowModal()
      self.FinalSavePolyData.SetTitle("Save Feature Lines.")

      self.FinalSavePolyData.Destroy()
if __name__ == "__main__":
       app = App(False)
       controller = Controller()
       app.MainLoop()      