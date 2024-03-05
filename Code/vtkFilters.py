from vtk import vtkVertexGlyphFilter
class Filter:
    def __init__(self,pts):
        pass
        
    def getOutput(self):
        pass

class vertexFilter(Filter):
    def __init__(self,pts):
        self.pts=pts
    def getOutput(self):
        myFilter=vtkVertexGlyphFilter()
        myFilter.SetInputData(self.pts)
        myFilter.Update()
        return myFilter.GetOutput()
    