from wx import *
#from vtk import*
from vtkReaders import ReaderFactory

class LoadPolyDataDialog(wx.Dialog):
  def __init__(self,parent,title="Load Poly Data"):
      wx.Dialog.__init__(self,parent,-1,title,size=wx.DefaultSize,style=wx.DEFAULT_DIALOG_STYLE)

      sampleList = ['vtk','OBJ','PLY']
      self.PolyDataType = wx.RadioBox(self, -1, "Poly Data Type",
                        wx.DefaultPosition,wx.Size(350,-1),
                        sampleList,7, wx.RA_SPECIFY_COLS)
      EVT_RADIOBOX(self.PolyDataType,-1, self.OnPolyDataType)

      self.line0=wx.StaticLine(self, -1,wx.DefaultPosition,wx.Size(-1,-1),wx.LI_HORIZONTAL)

      self.PrefixBtn=wx.Button(self, -1, "FileName", wx.DefaultPosition, wx.DefaultSize, 0)
      self.CloseBtn=wx.Button(self, wx.ID_CANCEL, "Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
      self.LoadBtn=wx.Button(self, wx.ID_OK, "OK", wx.DefaultPosition, wx.DefaultSize, 0)

      EVT_BUTTON(self.PrefixBtn,-1,self.OnPrefix)
      self.line1=wx.StaticLine(self, -1,wx.DefaultPosition,wx.Size(-1,-1),wx.LI_HORIZONTAL)
      self.line2=wx.StaticLine(self, -1,wx.DefaultPosition,wx.Size(-1,-1),wx.LI_HORIZONTAL)
      self.filePrefix=wx.TextCtrl(self,-1,"",size=wx.Size(325,-1),style=wx.TE_READONLY)


      H=wx.BoxSizer(wx.HORIZONTAL)
      #H.Add(5,5,1)
      H.Add(self.PolyDataType,0,wx.CENTER)
      #H.Add(5,5,1)

      sizer=wx.FlexGridSizer(1,2,0,0)
      sizer.AddWindow(self.PrefixBtn,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
      sizer.AddWindow(self.filePrefix,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)


      H1=wx.BoxSizer(wx.HORIZONTAL)
      #H1.Add(10,10,1)
      H1.Add(self.LoadBtn,0,wx.CENTER)
      #H1.Add(10,10,1)
      H1.Add(self.CloseBtn,0,wx.CENTER)
      #H1.Add(10,10,1)

      MainV=wx.BoxSizer(wx.VERTICAL)
      #MainV.Add(10,10,1)
      MainV.Add(sizer,0,wx.CENTER)
      #MainV.Add(10,10,1)
      MainV.Add(H,0,wx.GROW | wx.ALIGN_CENTRE | wx.ALL)
      #MainV.Add(10,10,1)
      MainV.Add(H1,0,wx.CENTER)
      #MainV.Add(10,10,1)


      MainV.Fit(self)
      MainV.SetSizeHints(self)

      self.SetAutoLayout(True)
      self.SetSizer(MainV)
      MainV.Fit(self)
      MainV.SetSizeHints(self)


      self.LoadBtn.Enable(False)
      self.wldCrds={
                    'vtk':"vtkPolyData (*.vtk)|*.vtk",
                    'ply':"plyPolyData (*.ply)|*.ply",
                    'obj':"objPolyData (*.obj)|*.obj"
                    }
      self.wildcard= "vtkPolyData (*.vtk)|*.vtk"
      #self.Reader=vtkPolyDataReader()
      #self.ModeSelect="vtk"
       
  def GetPolyData(self):
       if(self.ShowModal()==wx.ID_OK):
           rf=ReaderFactory()
           self.Reader=rf.createReader(self.PolyDataType.GetStringSelection()
                                                  ,self.filePrefix.GetValue()).getReader()#.SetFileName(self.filePrefix.GetValue())
           #self.Reader.Update()
           return self.Reader.GetOutput()

  def OnPrefix(self,event):

        self.Filedlg = wx.FileDialog(self, "Load Poly Data", "", "", self.wildcard, wx.OPEN)#|wx.MULTIPLE)
        if self.Filedlg.ShowModal() == wx.ID_OK:
           path = self.Filedlg.GetPaths()[0]
           if(path):
                self.filePrefix.SetValue(self.Filedlg.GetPath())
                self.LoadBtn.Enable(True)
        self.Filedlg.Destroy()
        

  def OnPolyDataType(self,event):
        self.LoadBtn.Enable(False)
        self.filePrefix.SetValue("")
        self.wildcard=self.wldCrds[self.PolyDataType.GetStringSelection().lower()]








#----------------------------------------------------------------------



