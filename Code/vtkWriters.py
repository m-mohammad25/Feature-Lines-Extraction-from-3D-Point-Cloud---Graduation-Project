from vtk import vtkPolyDataWriter
class IWtirer:
    def __init__(self):
        pass
    def writePoints(self,path):
        pass

class VtkWriter(IWtirer):
    def __init__(self,pts):
        self.pts=pts
        self.writer=vtkPolyDataWriter()
        self.writer.SetInputData(pts)
    def writePoints(self,path):
        self.path=path
        self.writer.SetFileName(self.path+ ".vtk")
        self.writer.Write()
class WriterFactory:
    def __init__(self):
        pass
        
    def createWriter(self,wrType,pts):
        wrType=wrType.lower().capitalize()
        writer=globals()[wrType+'Writer'](pts)
        return writer
        