from vtk import vtkPLYReader,vtkPolyDataReader
#these readers are named according to the file extension wich they read
class IReader:
    def getReader(self): #add this to class diagram
       pass
    def getPoints(self): #add this to class diagram
        pass
class PlyReader(IReader):
      def __init__(self,path):
        self.reader=vtkPLYReader()
        self.reader.SetFileName(path)
        self.reader.Update()
      def getReader(self):
        return self.reader
      def getPoints(self):
        return self.reader.GetOutput().GetPoints() 
       
class VtkReader(IReader):
      def __init__(self,path):
        self.reader=vtkPolyDataReader()
        self.reader.SetFileName(path)
        self.reader.Update()
      def getReader(self):
        return self.reader
      def getPoints(self):
        return self.reader.GetOutput().GetPoints()
class ObjReader(IReader):
      def __init__(self,path):
        self.reader=vtkOBJReader()
        self.reader.SetFileName(path)
        self.reader.Update()
      def getReader(self):
        return self.reader
      def getPoints(self):
        return self.reader.GetOutput().GetPoints()    
class ReaderFactory:
      def createReader(self,rdrType,path):
        #dotIndex=path.find(".")
        #extension=path[dotIndex+1:]
        rdrType=rdrType.lower()
        try:
            reader=globals()[rdrType.capitalize()+'Reader'](path)
            return reader
        except:
            print("Something went wrong!")
        