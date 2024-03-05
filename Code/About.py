import wx

#---------------------------------------------------------------------------
class AboutDialog(wx.Dialog):
  def __init__(self,parent,title="About"):
                wx.Dialog.__init__(self,parent,-1,title,size=wx.DefaultSize,style=wx.DEFAULT_DIALOG_STYLE)
		self.__title="Feature Points Extraction"
		self.__author1="Dr. Eng. Yasser KHADRA"
		self.__author2="Eng. Omar and Mohammed "
		self.__comment="YPU 2020"
		self.CenterOnScreen()



		sizer=wx.BoxSizer(wx.VERTICAL)
		title=wx.StaticText(self,-1,self.__title,style=wx.ALIGN_CENTRE)
		title.SetFont(wx.Font(20,wx.ROMAN,wx.NORMAL,wx.BOLD))
		sizer.AddWindow(title,0,wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
		line=wx.StaticLine(self,-1,size=wx.Size(20,-1),style=wx.LI_HORIZONTAL)
		sizer.AddWindow(line,0,wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)

		sizer1=wx.BoxSizer(wx.HORIZONTAL)
		sizer11=wx.BoxSizer(wx.VERTICAL)
		sizer111=wx.BoxSizer(wx.HORIZONTAL)
		sizer1111=wx.BoxSizer(wx.VERTICAL)

		text=wx.StaticText(self,-1,"Author :")
		sizer1111.AddWindow(text,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)

		text=wx.StaticText(self,-1,"        ")
		sizer1111.AddWindow(text,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
		sizer111.AddSizer(sizer1111,0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,0)

		sizer1112=wx.BoxSizer(wx.VERTICAL)
		author1=wx.StaticText(self,-1,self.__author1)
		author2=wx.StaticText(self,-1,self.__author2)
		sizer1112.AddWindow(author1,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
		sizer1112.AddWindow(author2,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)

		sizer111.AddSizer(sizer1112,0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,0)
		sizer11.AddSizer(sizer111,0,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,0)

		sizer112=wx.BoxSizer(wx.HORIZONTAL)
		sizer112.AddSpacer(20,20,0,wx.ALIGN_CENTRE|wx.ALL,0)
		comment=wx.StaticText(self,-1,self.__comment)
		sizer112.AddWindow(comment,0,wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,0)
		sizer11.AddSizer(sizer112,0,wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL,0)
		sizer1.AddSizer(sizer11,0,wx.ALIGN_CENTRE|wx.ALL,5)
		sizer.AddSizer(sizer1,0,wx.ALIGN_CENTRE|wx.ALL,5)

		line=wx.StaticLine(self,-1,size=wx.Size(20,-1),style=wx.LI_HORIZONTAL)
		sizer.AddWindow(line,0,wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
		btn=wx.Button(self,wx.ID_OK,"OK")
		sizer.AddWindow(btn,0,wx.ALIGN_CENTRE|wx.ALL,5)

		self.SetAutoLayout(True)
		self.SetSizer(sizer)
		sizer.Fit(self)
		sizer.SetSizeHints(self)
  def SetTitle(self,t):
      self.__title=t;



#---------------------------------------------------------------------------


