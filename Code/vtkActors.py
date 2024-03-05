from vtk import vtkSphereSource,vtkGlyph3D,vtkPolyDataMapper,vtkActor,vtkTextProperty,vtkTextMapper,vtkActor2D,vtkPolyDataMapper
class IActor:
    def getActor(self):
          pass


class SphereActor(IActor):
    def __init__(self,polyData,sphereRadi):
        self.__polyData=polyData
        
        self.__sphereRadi=sphereRadi
        sphere=vtkSphereSource()
        sphere.SetRadius(self.__sphereRadi)
        sphere.Update()
        
        glyphPoints = vtkGlyph3D()
        glyphPoints.SetInputData(self.__polyData)
        glyphPoints.SetSourceData(sphere.GetOutput())
        
        gl_mapper = vtkPolyDataMapper()
        gl_mapper.SetInputConnection(glyphPoints.GetOutputPort())
        
        self.gl_actor= vtkActor()
        self.gl_actor.SetMapper(gl_mapper)
    
    def getActor(self):
        return self.gl_actor

        
class TextActor(IActor):
    def __init__(self,text,textSize,xPos,yPos):
        self.__text=text
        self.__xPos=xPos
        self.__yPos=yPos
        self.__textSize=textSize
        
        textProperty = vtkTextProperty()
        textProperty.SetFontSize(self.__textSize)
        textProperty.SetJustificationToCentered()
        
        textmapper= vtkTextMapper()
        textmapper.SetInput(self.__text)
        textmapper.SetTextProperty(textProperty)
        
        self.textactor= vtkActor2D()
        self.textactor.SetMapper(textmapper)
        self.textactor.SetPosition(self.__xPos, self.__yPos)
    
    def getActor(self):
        return self.textactor
    
class CurvatureActor(IActor):
    def __init__(self,curvPoints):
        self.__curvPoints=curvPoints
        
        #lut=vtk.vtkLookupTable()
        #lut.SetNumberOfColors(256)
        #lut.SetRange(0.25*minval, 0.25*maxval)
    
        curvMapper= vtkPolyDataMapper()
        curvMapper.SetInputConnection(self.__curvPoints.GetOutputPort())
        #curvMapper.SetLookupTable(lut)
        #curvMapper.SetUseLookupTableScalarRange(1)

        self.curvActor=vtkActor()
        self.curvActor.SetMapper(curvMapper)
    
    def getActor(self):
       return self.curvActor

class GlyphActor(IActor):
    def __init__(self,polyData,opacity,rgbColor,sphereSize=2):
         glMapper=vtkPolyDataMapper()
         glMapper.SetInputData(polyData)
         self.glActor=vtkActor()
         self.glActor.SetMapper(glMapper)
         self.glActor.GetProperty().SetOpacity(opacity)
         self.glActor.GetProperty().SetColor(rgbColor[0],rgbColor[1],rgbColor[2])
         self.glActor.GetProperty().SetPointSize(sphereSize)
    
    def getActor(self):
         return self.glActor
    
    def setSphereSize(self,size):
        self.glActor.GetProperty().SetPointSize(size)    