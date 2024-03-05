import os
import string
import six
import vtk
from Tkinter import *

from numpy import random

# Yasser
def close_window(iren):
    render_window = iren.GetRenderWindow()
    render_window.Finalize()
    iren.TerminateApp()
    del render_window, iren
    

class VtkPointCloud:

    def __init__(self, zMin=-10.0, zMax=10.0, maxNumPoints=1e6):
        self.maxNumPoints = maxNumPoints

        self.vtkPolyData = vtk.vtkPolyData()

        self.clearPoints()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)


    def addPoint(self, point):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextValue(point[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
            r = random.randint(0, self.maxNumPoints)
            self.vtkPoints.SetPoint(r, point[:])
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')



def main():

    filename1='../../data/mesh/fandisk.vtk'
    filename2='../../data/mesh/cube.vtk'
    filename3='../../data/mesh/octoflower.vtk'

    filename4='../../data/mesh/House2.vtk'

    # reader1 = vtk.vtkPLYReader()
#     reader1.SetFileName(filename4)
#     reader1.Update()


    #Read and display for verication
    reader1 = vtk.vtkPolyDataReader()
    reader1.SetFileName(filename1)
    reader1.Update()

    colors = vtk.vtkNamedColors()

    cleaner = vtk.vtkCleanPolyData()
    cleaner.SetInputConnection(reader1.GetOutputPort())
    cleaner.SetTolerance(0.005)



    curvature=vtk.vtkCurvatures()
    curvature.SetCurvatureTypeToMean()
    curvature.SetInputConnection(reader1.GetOutputPort())
    curvature.Update()
    #curvature.SetInputConnection(cleaner.GetOutputPort())



    point_data = curvature.GetOutputDataObject(0).GetPointData()
    num_points = point_data.GetNumberOfTuples()

    maxval = -999999.0
    minval =  999999.0
    for i in range(num_points):
       cur_val = point_data.GetScalars().GetValue(i)
       #print("cur_val= ",cur_val)
       if cur_val > maxval:
          maxval = cur_val
       if  cur_val< minval:
          minval = cur_val

     #self.curvatures.append(curvature)
    print("Max val= ",maxval)
    print("Min val= ",minval)

    pointCloud= VtkPointCloud()
    
    out_points = vtk.vtkPoints()

    
    points=reader1.GetOutput().GetPoints()
    for k in range(points.GetNumberOfPoints()):
       cur_val = point_data.GetScalars().GetValue(k)
       if cur_val > 0.07*maxval:
          #x, y, z = points.GetPoint(k)
          out_points.InsertNextPoint(points.GetPoint(k))
       if cur_val < 0.07*minval:
          #x, y, z = points.GetPoint(k)
          #pointCloud.addPoint([x, y, z])
          out_points.InsertNextPoint(points.GetPoint(k))
       #print("point = ",points.GetPoint(k))


    # Create a common text property.
    textProperty = vtk.vtkTextProperty()
    textProperty.SetFontSize(24)
    textProperty.SetJustificationToCentered()

    names = ['Gaussian Curvature', 'Mean Curvature']

    #sources[idx].Update()

    lut=vtk.vtkLookupTable()
    lut.SetNumberOfColors(256)
    lut.SetRange(0.25*minval, 0.25*maxval)


    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(1)
    #sphere.SetPhiResolution()
    #sphere.SetThetaResolution( Globals.renderProps["sphereThetaResolution"] )
    sphere.Update()

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(out_points)


    glyphPoints = vtk.vtkGlyph3D()
    glyphPoints.SetInputData(polydata)
    glyphPoints.SetSourceData(sphere.GetOutput() )

    gl_mapper = vtk.vtkPolyDataMapper()
    gl_mapper.SetInputConnection(glyphPoints.GetOutputPort() )
    
    gl_actor=vtk.vtkActor()
    gl_actor.SetMapper(gl_mapper)
        

    mapper=vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(curvature.GetOutputPort())
    mapper.SetLookupTable(lut)
    mapper.SetUseLookupTableScalarRange(1)

    actor=vtk.vtkActor()
    actor.SetMapper(mapper)

    textmapper=vtk.vtkTextMapper()
    textmapper.SetInput(names[1])
    textmapper.SetTextProperty(textProperty)

    textactor=vtk.vtkActor2D()
    textactor.SetMapper(textmapper)
    textactor.SetPosition(150, 16)

    renderer=vtk.vtkRenderer()


    rendererSize = 300

    # Create the RenderWindow
    #

    renderer.AddActor(actor)
    renderer.AddActor(textactor)
    renderer.AddActor(pointCloud.vtkActor)
    renderer.AddActor(gl_actor)
    renderer.SetBackground(colors.GetColor3d("Black"))
    
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(rendererSize , rendererSize )
    renderWindow.AddRenderer(renderer)


            
    #renderer.SetViewport(viewport)


    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    renderWindow.Render()

    interactor.Start()


if __name__ == "__main__":
    main()