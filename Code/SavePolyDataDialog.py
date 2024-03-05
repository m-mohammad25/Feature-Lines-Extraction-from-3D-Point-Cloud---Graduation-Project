from wx import *
#from ivtk import *
from vtk import vtkPolyDataWriter
from vtkWriters import WriterFactory

class SavePolyDataDialog(wx.Dialog):
  def __init__(self,parent,title="WriteImageData"):
      wx.Dialog.__init__(self,parent,-1,title,size=wx.DefaultSize,style=wx.DEFAULT_DIALOG_STYLE)

      sampleList = ['vtk']
      self.PolyDataType = wx.RadioBox(self, -1, "Poly Data Type",
                        wx.DefaultPosition,wx.Size(350,-1),
                        sampleList,7, wx.RA_SPECIFY_COLS)
      #EVT_RADIOBOX(self.PolyDataType,-1, self.OnPolyDataType)

      self.line0=wx.StaticLine(self, -1,wx.DefaultPosition,wx.Size(-1,-1),wx.LI_HORIZONTAL)
      
      self.PrefixBtn=wx.Button(self, -1, "FileName", wx.DefaultPosition, wx.DefaultSize, 0)
      self.CloseBtn=wx.Button(self, -1, "Close", wx.DefaultPosition, wx.DefaultSize, 0)
      self.WriteBtn=wx.Button(self, -1, "Write", wx.DefaultPosition, wx.DefaultSize, 0)

      EVT_BUTTON(self.PrefixBtn,-1,self.OnPrefix)
      EVT_BUTTON(self.CloseBtn,-1,self.OnClose)
      EVT_BUTTON(self.WriteBtn,-1,self.OnWrite)

      self.line1=wx.StaticLine(self, -1,wx.DefaultPosition,wx.Size(-1,-1),wx.LI_HORIZONTAL)

      self.line2=wx.StaticLine(self, -1,wx.DefaultPosition,wx.Size(-1,-1),wx.LI_HORIZONTAL)

      self.filePrefix=wx.TextCtrl(self,-1,"",size=wx.Size(325,-1),style=wx.TE_READONLY)


      H=wx.BoxSizer(wx.HORIZONTAL)
      #H.Add(5,5,1)
      H.Add(self.PolyDataType,0,wx.CENTER)
      #H.Add(5,5,1)

      sizer=wx.FlexGridSizer(5,2,0,0)
      sizer.AddWindow(self.PrefixBtn,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
      sizer.AddWindow(self.filePrefix,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)


      H1=wx.BoxSizer(wx.HORIZONTAL)
      #H1.Add(10,10,1)
      H1.Add(self.WriteBtn,0,wx.CENTER)
      #H1.Add(10,10,1)
      H1.Add(self.CloseBtn,0,wx.CENTER)
      #H1.Add(10,10,1)

      MainV=wx.BoxSizer(wx.VERTICAL)
      #MainV.Add(10,10,1)
      MainV.Add(H,0,wx.CENTER)
      #MainV.Add(10,10,1)
      MainV.Add(sizer,0,wx.GROW | wx.ALIGN_CENTRE | wx.ALL)
      #MainV.Add(10,10,1)
      MainV.Add(H1,0,wx.CENTER)
      #MainV.Add(10,10,1)


      MainV.Fit(self)
      MainV.SetSizeHints(self)

      self.SetAutoLayout(True)
      self.SetSizer(MainV)
      MainV.Fit(self)
      MainV.SetSizeHints(self)


      self.WriteBtn.Enable(False)
      #self.writer=vtkPolyDataWriter()
      #self.suffix=".vtk"
      self.ModeSelect="vtk"

  def SetInput(self,pts):
      self.pts = pts
      #print(pd)

  def OnPrefix(self,event):
        self.wildcard = "All files (*.*)|*.*"

        self.Filedlg = wx.FileDialog(self, "Choose a file Prefix", "", "", self.wildcard, wx.OPEN)#|wx.MULTIPLE)
        if self.Filedlg.ShowModal() == wx.ID_OK:
          path = self.Filedlg.GetPaths()[0]
          if(path):
                self.filePrefix.SetValue(self.Filedlg.GetPath())
                self.WriteBtn.Enable(True)
        self.Filedlg.Destroy()
        
  # def OnPolyDataType(self,event):
        # self.ModeSelect= self.PolyDataType.GetStringSelection()
	# if (self.ModeSelect=="vtk"):
           # self.writer=vtkPolyDataWriter()
           # self.suffix=".vtk"


           



  def OnClose(self,event):

        self.Close()

  def OnWrite(self,event):
        try:
            self.writer = WriterFactory().createWriter(self.ModeSelect,self.pts)
            self.writer.writePoints(self.filePrefix.GetValue())
            MessageBox('The file was saved successfully in:\n{path}.{ext}'.format(path=self.filePrefix.GetValue(),ext=self.ModeSelect.lower())
                   , 'Info'
                   ,wx.OK | wx.ICON_INFORMATION | wx.CENTRE)
        except:
            MessageBox('Could not write the file!','Error',wx.OK | wx.ICON_ERROR | wx.CENTRE)
        finally:
            self.Close()
        


#----------------------------------------------------------------------



