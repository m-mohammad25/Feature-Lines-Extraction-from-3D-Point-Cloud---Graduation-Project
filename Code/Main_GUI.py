#import math, os, sys
import wx
from vtk import vtkActor,vtkNamedColors,vtkRenderer
import wxVTKRWI
#import vtkPC

#from LoadPolyDataDialog import *
#from SavePolyDataDialog import *
from About import *



ID_Menu_Exit=1010

ID_MAIN=1020
ID_CURV=1021

#--------------------------------------------------------------------
class MainFrame(wx.Frame):
 def __init__(self,parent=None,id=1,title=" Feature Line Extraction ",size=(1000,1000)):
    wx.Frame.__init__(self,parent,id,title,size=(600,500),style=wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.MINIMIZE_BOX |wx.MAXIMIZE_BOX |wx.CAPTION |wx.FRAME_NO_WINDOW_MENU)
    
    self.Bind(wx.EVT_CLOSE,self.OnExit)
    self.FileMenu=wx.Menu()

    self.FileMenu.AppendSeparator()
    
    self.ID_Menu_LoadMesh=1011
    self.ID_Menu_LoadFPMesh=1012
    self.ID_Menu_SaveFPMesh=1013
    self.FileMenu.Append(self.ID_Menu_LoadMesh, "Load\tCTRL-L","Load")
    self.FileMenu.Append(self.ID_Menu_LoadFPMesh, "Load FP\tCTRL-A","Load FP")
    self.FileMenu.Append(self.ID_Menu_SaveFPMesh, "Save\tCTRL-S","Save").Enable(False)
    self.FileMenu.Append(ID_Menu_Exit, "Exit\tCTRL-Q","Exit")
    
    ico=wx.Icon('FD_Icon.jpg', wx.BITMAP_TYPE_JPEG)
    self.SetIcon(ico)
    
    HelpMenu=wx.Menu()
    HelpMenu.Append(wx.ID_ABOUT,"About","About")

    menuBar=wx.MenuBar()
    menuBar.Append(self.FileMenu,"File")
    menuBar.Append(HelpMenu,"Help")

    self.SetMenuBar(menuBar)
    

    
    
    #EVT_MENU(self,ID_Menu_LoadMesh,self.OnLoad)
    #EVT_MENU(self,ID_Menu_LoadFPMesh,self.OnLoadFP)
    #EVT_MENU(self,ID_Menu_SaveFPMesh,self.OnSave)
    wx.EVT_MENU(self,ID_Menu_Exit,self.OnExit)
    wx.EVT_MENU(self,wx.ID_ABOUT,self.OnAbout)



    self.PanelLeft = wx.Panel(self, -1,size=(-1, -1), style=wx.GROW|wx.SUNKEN_BORDER )

    self.LoadBtnL=wx.Button(self.PanelLeft, -1, "Load P.D.",size=wx.Size(60,15))
    self.LoadFPBtnL=wx.Button(self.PanelLeft, -1, "Load F.P.",size=wx.Size(60,15))

    self.ThBtnL=wx.Button(self.PanelLeft, -1, "Threshold",size=wx.Size(60,40))
    
    self.mn_checkbox_Curv_Actor = wx.CheckBox(self.PanelLeft,label="Min Feature Lines")
    self.mx_checkbox_Curv_Actor = wx.CheckBox(self.PanelLeft,label="Max Feature Lines")
    self.main_checkbox_Actor= wx.CheckBox(self.PanelLeft,label="Main Mesh")
    
    font= wx.Font(pointSize = 10,
                   family = wx.FONTFAMILY_DEFAULT,
                   style = wx.NORMAL,
                   weight = wx.FONTWEIGHT_NORMAL)

    self.maxThrSld = wx.SpinCtrl(self.PanelLeft, value="88", pos=wx.DefaultPosition,size=wx.Size(50,20), style=wx.SP_ARROW_KEYS | wx.ALIGN_CENTRE_HORIZONTAL, min=0, max=100, initial=0,name="max")
    self.maxThrSld.SetFont(font)
    self.val1 = wx.StaticText(self.PanelLeft,label="% Max Thr.", style=wx.ALIGN_CENTER)



    self.minThrSld = wx.SpinCtrl(self.PanelLeft, value="2", pos=wx.DefaultPosition,size=wx.Size(50,20), style=wx.SP_ARROW_KEYS | wx.ALIGN_CENTRE_HORIZONTAL, min=0, max=100, initial=0,name="max")
    self.minThrSld.SetFont(font)
    self.val2 = wx.StaticText(self.PanelLeft,label="% Min Thr.", style=wx.ALIGN_CENTER)

    self.vSizeSld = wx.SpinCtrl(self.PanelLeft, value="2", pos=wx.DefaultPosition,size=wx.Size(30,-1), style=wx.SP_ARROW_KEYS | wx.ALIGN_CENTRE_HORIZONTAL, min=1, max=10, initial=0,name="sz")
    self.vSizeSld.SetFont(font)
    self.val3 = wx.StaticText(self.PanelLeft,label="V. Size", style=wx.ALIGN_CENTER)


    self.widgetL = wxVTKRWI.wxVTKRenderWindowInteractor(self.PanelLeft, -1)


    #EVT_BUTTON(self.LoadBtnL,-1,self.OnLoad)
    #EVT_BUTTON(self.LoadFPBtnL,-1,self.OnLoadFP)
    


    #EVT_BUTTON(self.ThBtnL,-1,self.OnThr)
    
    wx.EVT_CHECKBOX(self.mn_checkbox_Curv_Actor,-1,self.OnMinCurvActor)
    wx.EVT_CHECKBOX(self.mx_checkbox_Curv_Actor,-1,self.OnMaxCurvActor)
    wx.EVT_CHECKBOX(self.main_checkbox_Actor,-1,self.OnMainPd)

    
    wx.EVT_SPINCTRL(self.maxThrSld,-1,self.OnMaxThrSld)
    wx.EVT_SPINCTRL(self.minThrSld,-1,self.OnMinThrSld)
    wx.EVT_SPINCTRL(self.vSizeSld,-1,self.OnVSizeSld)


    
    self.HBS4=wx.BoxSizer(wx.HORIZONTAL)
    self.HBS4.AddWindow(self.val1,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    self.HBS4.AddWindow(self.maxThrSld,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)



    self.HBS5=wx.BoxSizer(wx.HORIZONTAL)
    self.HBS5.AddWindow(self.val2,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    self.HBS5.AddWindow(self.minThrSld,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)


    self.HBS9=wx.BoxSizer(wx.HORIZONTAL)
    self.HBS9.AddWindow(self.val3,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    self.HBS9.AddWindow(self.vSizeSld,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    

    self.HBS2=wx.BoxSizer(wx.VERTICAL)
    self.HBS2.AddWindow(self.HBS4,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    self.HBS2.AddWindow(self.HBS5,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)




    self.HBS6=wx.BoxSizer(wx.VERTICAL)
    self.HBS6.AddWindow(self.mn_checkbox_Curv_Actor,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    self.HBS6.AddWindow(self.mx_checkbox_Curv_Actor,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    self.HBS6.AddWindow(self.main_checkbox_Actor,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)

    self.HBS10=wx.BoxSizer(wx.VERTICAL)
    self.HBS10.AddWindow(self.HBS9,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    self.HBS10.AddWindow(self.ThBtnL,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    
    self.HBS11=wx.BoxSizer(wx.VERTICAL)
    self.HBS11.AddWindow(self.LoadBtnL,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    self.HBS11.AddWindow(self.LoadFPBtnL,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    

    self.HBS1=wx.BoxSizer(wx.HORIZONTAL)
    self.HBS1.AddWindow(self.HBS11,1,wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND,0)
    self.HBS1.AddWindow(self.HBS2,1,wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND,2)
    self.HBS1.AddWindow(self.HBS10,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)
    self.HBS1.AddWindow(self.HBS6,1,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND,1)

    


    self.HBS7=wx.BoxSizer(wx.HORIZONTAL)
    self.HBS7.AddWindow(self.widgetL,1,wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND,2)


    self.VBS=wx.BoxSizer(wx.VERTICAL)
    self.VBS.AddWindow(self.HBS1,0,wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND,1)

    self.VBS.AddWindow(self.HBS7,1,wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND,1)



    MainVL=wx.BoxSizer(wx.VERTICAL)
    MainVL.Add( self.VBS,1,wx.GROW|wx.ALL|wx.EXPAND,10)





    self.PanelLeft.SetSizer(MainVL)
    MainVL.Fit(self.PanelLeft)
    MainVL.SetSizeHints(self.PanelLeft)


    self.widgetL.Enable(1)
    



    #self.widgetL.AddObserver("ExitEvent", lambda o,e,f=self: f.Close())
    #self.widgetL.AddObserver("ExitEvent", self.Close())

    


    #self.max_curvature=vtk.vtkCurvatures()
    #self.max_curvature.SetCurvatureTypeToMaximum()
    
    
    #self.min_curvature=vtk.vtkCurvatures()
    #self.min_curvature.SetCurvatureTypeToMinimum()


    self.mainActor= vtkActor()
    #self.max_curvActor=vtk.vtkActor()
    #self.min_curvActor=vtk.vtkActor()

    #self.procActor=vtk.vtkActor()
    self.mn_gl_actor= vtkActor()
    self.mx_gl_actor= vtkActor()
    #self.c_gl_actor=vtk.vtkActor()


    #self.mainMapper=vtk.vtkPolyDataMapper()
    #self.max_curvMapper=vtk.vtkPolyDataMapper()
    #self.min_curvMapper=vtk.vtkPolyDataMapper()

    #self.procMapper=vtk.vtkPolyDataMapper()


    #self.Feature_Lines_PD=vtk.vtkPolyData()
    

    colors = vtkNamedColors()

    self.renL = vtkRenderer()

    self.renL.SetBackground(colors.GetColor3d("White"))
    


    self.widgetL.GetRenderWindow().AddRenderer(self.renL)
    


    self.CenterOnScreen()
    
    
    #self.max_MinValue=9999999999.0
    #self.max_MaxValue= -9999999999.0

    #self.min_MinValue=9999999999.0
    #self.min_MaxValue= -9999999999.0

    #self.max_point_data=vtk.vtkPointData()
    #self.min_point_data=vtk.vtkPointData()

    #self.points=vtk.vtkPoints()
    #self.mn_points=vtk.vtkPoints()
    #self.mx_points=vtk.vtkPoints()
    
    #self.vertexFilter = vtk.vtkVertexGlyphFilter()

    
    #self.vol=0.0
    


    self.ThBtnL.Enable(False)
    self.maxThrSld.Enable(False)
    self.minThrSld.Enable(False)
    self.vSizeSld.Enable(False)
    
    self.mn_checkbox_Curv_Actor.Enable(False)
    self.mn_checkbox_Curv_Actor.SetValue(True)
    
    self.mx_checkbox_Curv_Actor.Enable(False)
    self.mx_checkbox_Curv_Actor.SetValue(True)
    
    self.main_checkbox_Actor.Enable(False)
    self.main_checkbox_Actor.SetValue(True)



    #self.max_curv_list=[]
    #self.min_curv_list=[]

    

 def OnSize(self, event):
        wx.LayoutAlgorithm().LayoutMDIFrame(self)


 def OnCurvSelect(self,event):
      pass
        
 def OnMainPd(self,event):
     
     if(self.main_checkbox_Actor.IsChecked()):
        self.addActor(self.mainActor)
     else:
        self.removeActor(self.mainActor)
     self.refreshScene()
     

 def OnMinCurvActor(self,event):
     
     if(self.mn_checkbox_Curv_Actor.IsChecked()):
        self.addActor(self.mn_gl_actor)
     else:
        self.removeActor(self.mn_gl_actor)
     self.refreshScene()

 def OnMaxCurvActor(self,event):
     
     if(self.mx_checkbox_Curv_Actor.IsChecked()):
        self.addActor(self.mx_gl_actor)
     else:
        self.removeActor(self.mx_gl_actor)
     self.refreshScene()

 def OnMaxThrSld(self,event):
     v=self.getMaxThr()
     #self.setMaxThrLbl(v)

 def OnMinThrSld(self,event):
     v=self.getMinThr()
     #self.setMinThrLbl(v)
     
     
 def OnVSizeSld(self,event):
             
             self.mn_gl_actor.GetProperty().SetPointSize(self.getVSize())
             self.mx_gl_actor.GetProperty().SetPointSize(self.getVSize()) 

             self.refreshGlPoints()
             self.refreshScene()

 def OnExit(self,event):
        self.renL.RemoveAllViewProps()
        del self.renL
        self.widgetL.GetRenderWindow().Finalize()
        self.widgetL.SetRenderWindow(None)
        del self.widgetL
        self.Destroy()

 def OnAbout(self,event):
     self.AD=AboutDialog(None,"About")
     self.AD.SetTitle("PC Processing")
     # self.AD.SetAuthor("Yasser KHADRA")
     #self.AD.SetComment("YPU 2020")
     if(self.AD.ShowModal()==wx.ID_OK):
	self.output=5;#self.LoadDialog.GetPolyData()

 def OnSize(self,event):
     pass
 def cleanScreen(self):
        self.renL.RemoveActor(self.mainActor)
        #self.renL.RemoveActor(self.max_curvActor)
        self.renL.RemoveActor(self.mn_gl_actor)
        self.renL.RemoveActor(self.mx_gl_actor)

 def enableComponents(self):
       self.ThBtnL.Enable(True)
       self.maxThrSld.Enable(True)
       self.minThrSld.Enable(True)
       self.vSizeSld.Enable(True)
       self.mn_checkbox_Curv_Actor.Enable(True)
       self.mx_checkbox_Curv_Actor.Enable(True)
       self.main_checkbox_Actor.Enable(True)
       self.mn_checkbox_Curv_Actor.Enable(True)

       self.mn_checkbox_Curv_Actor.SetValue(True)
       self.mx_checkbox_Curv_Actor.SetValue(True)
       self.main_checkbox_Actor.SetValue(True)

 def disableComponents(self):
    self.ThBtnL.Enable(False)
    self.maxThrSld.Enable(False)
    self.minThrSld.Enable(False)
    self.vSizeSld.Enable(False)
    self.mn_checkbox_Curv_Actor.Enable(False)
    self.mx_checkbox_Curv_Actor.Enable(False)
    self.main_checkbox_Actor.Enable(False)
    self.mn_checkbox_Curv_Actor.Enable(False)

    self.mn_checkbox_Curv_Actor.SetValue(True)
    self.mx_checkbox_Curv_Actor.SetValue(True)
    self.main_checkbox_Actor.SetValue(True)
 def addActor(self,act):
        self.renL.AddActor(act)
 def removeActor(self,act):
        self.renL.RemoveActor(act)
 def refreshScene(self):
        self.renL.ResetCamera()
        self.widgetL.Render()

 def getVSize(self):
         return self.vSizeSld.GetValue()
 def setMn_gl_actor(self,mnGlActor):
        self.mn_gl_actor=mnGlActor
 def setMx_gl_actor(self,mxGlActor):
        self.mx_gl_actor=mxGlActor
 def setMainActor(self,mnAct):
        self.mainActor=mnAct
 def refreshMainActor(self):
        self.removeActor(self.mainActor)
        self.addActor(self.mainActor)
 def refreshGlPoints(self):
         self.removeActor(self.mn_gl_actor)
         self.addActor(self.mn_gl_actor)
         self.removeActor(self.mx_gl_actor)
         self.addActor(self.mx_gl_actor)
 def getMaxThr(self):
         return self.maxThrSld.GetValue()
 def getMinThr(self):
         return self.minThrSld.GetValue()
 def setMaxThrLbl(self,txt):
         self.val1.SetLabel(str(txt)+"%")
 def setMinThrLbl(self,txt): 
         self.val2.SetLabel(str(txt)+"%")
 def removeMnGlActor(self):
        self.renL.RemoveActor(self.mn_gl_actor)
 def removeMxGlActor(self):
        self.renL.RemoveActor(self.mx_gl_actor) 
 def enableSaveMenuItem(self):
        self.FileMenu.FindItemById(self.ID_Menu_SaveFPMesh).Enable(True) 
#---------------------------------------------------------
class MyApp(wx.App):
   def OnInit(self):
      self.f=MainFrame()

      self.f.Show(True)

      return True

#----------------------------------------------------------

#app=MyApp(0)
#app.MainLoop()

