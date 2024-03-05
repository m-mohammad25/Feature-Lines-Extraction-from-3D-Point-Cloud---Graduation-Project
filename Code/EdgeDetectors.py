from vtk import vtkCurvatures,vtkPoints,vtkPolyData,vtkCellArray,vtkIdList
class IEdgeDetector:
    def getEdgePoints(self,points):
        pass
class HystAlgorithm(IEdgeDetector):
    def __init__(self):
       self.max_curvature=vtkCurvatures()
       self.max_curvature.SetCurvatureTypeToMaximum()
       self.min_curvature=vtkCurvatures()
       self.min_curvature.SetCurvatureTypeToMinimum()
    
    def setMaxCurvVal(self,max):
         self.maxCurvVal=max
    def setMinCurvVal(self,min):
         self.minCurvVal=min
    def findCurvatures(self,pointOutput):
        
        
         self.clearCurvLists()
         
         self.max_curvature.SetInputData(pointOutput)
         self.max_curvature.Update()
                
                
         self.min_curvature.SetInputData(pointOutput)
         self.min_curvature.Update()


         self.max_point_data = self.max_curvature.GetOutputDataObject(0).GetPointData()
         self.min_point_data = self.min_curvature.GetOutputDataObject(0).GetPointData()

         num_points = self.max_point_data.GetNumberOfTuples()

         min_MaxValue= self.max_curvature.GetOutputDataObject(0).GetPointData().GetScalars().GetRange()[0]
         max_MaxValue= self.max_curvature.GetOutputDataObject(0).GetPointData().GetScalars().GetRange()[1]
                
         min_MinValue= self.min_curvature.GetOutputDataObject(0).GetPointData().GetScalars().GetRange()[0]
         max_MinValue= self.min_curvature.GetOutputDataObject(0).GetPointData().GetScalars().GetRange()[1]



         for i in range(num_points):
            max_cur_val = self.max_point_data.GetScalars().GetValue(i)
            min_cur_val = self.min_point_data.GetScalars().GetValue(i)
            self.max_curv_list.append(max_cur_val)
            self.min_curv_list.append(min_cur_val)
                   


         self.max_curv_list.sort()
         self.min_curv_list.sort() 
                
    def getEdgePoints(self,points):
         self.points=points
         #pointCloud= vtkPC.VtkPointCloud()
         out_points = vtkPoints()
         out_vertices = vtkCellArray()


         out_points.Reset()
         out_vertices.Reset()
                
                
         mx_out_points = vtkPoints()
         mx_out_points.Reset()
                
         mn_out_points = vtkPoints()
         mn_out_points.Reset()

         #c_out_points = vtkPoints()
         #c_out_points.Reset()

         lngth=self.points.GetNumberOfPoints()
         mx_pos= int(round(0.01*self.maxCurvVal*lngth))
         mn_pos= int(round(0.01*self.minCurvVal*lngth))

                
         feature_pts= vtkIdList()
         for k in range(lngth):
           mx_cur_val = self.max_point_data.GetScalars().GetValue(k)
           mn_cur_val = self.min_point_data.GetScalars().GetValue(k)


           if mx_cur_val > self.max_curv_list[mx_pos]:
             mx_out_points.InsertNextPoint(self.points.GetPoint(k))
             pointId=out_points.InsertNextPoint(self.points.GetPoint(k))
             out_vertices.InsertNextCell(1)
             out_vertices.InsertCellPoint(pointId)
             feature_pts.InsertNextId(k)
   
           if mn_cur_val < self.min_curv_list[mn_pos]:
             mn_out_points.InsertNextPoint(self.points.GetPoint(k))
             pointId=out_points.InsertNextPoint(self.points.GetPoint(k))
             out_vertices.InsertNextCell(1)
             out_vertices.InsertCellPoint(pointId)
             feature_pts.InsertNextId(k)
             
         featureLines=vtkPolyData()
         featureLines.SetPoints(out_points) 
         featureLines.SetVerts(out_vertices)
         
         mn_polydata = vtkPolyData()
         mn_polydata.SetPoints(mn_out_points)

         mx_polydata = vtkPolyData()
         mx_polydata.SetPoints(mx_out_points)
        
         return {"featueLines":featureLines,"minPoints":mn_polydata,"maxPoints":mx_polydata}
    
    def clearCurvLists(self):
        self.max_curv_list =[] 
        self.min_curv_list =[]
        