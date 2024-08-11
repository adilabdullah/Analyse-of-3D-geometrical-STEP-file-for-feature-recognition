import os
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopoDS import topods_Face, TopoDS_Shape
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopoDS import topods_Vertex
def calculate_face_area(face):
    """
    Calculate the area of a given face.
    """
    props = GProp_GProps()
    brepgprop_SurfaceProperties(face, props)
    return props.Mass()

def main(step_file_path):
    vertices = []
    # Read the STEP file
    shape = read_step_file(step_file_path)
    
    # Explore the shape to find faces
    topology = TopologyExplorer(shape)
    faces = list(topology.faces())
    
    # Calculate the area of each face and print it
    for i, face in enumerate(faces, start=1):
        area = calculate_face_area(face)
        print(f"Face {i}: Area = {area:.2f} square units")

    edge_explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    vertex_explorer = TopExp_Explorer(shape, TopAbs_VERTEX)
  
    # Count the number of edges
    edge_count = 0
    while edge_explorer.More():
        edge_count += 1
        edge_explorer.Next()
        
        
    while vertex_explorer.More():
        vertex = topods_Vertex(vertex_explorer.Current())
        pnt = BRep_Tool.Pnt(vertex)
        vertices.append((pnt.X(), pnt.Y(), pnt.Z()))
        vertex_explorer.Next();
    print("Edge count::"+str(edge_count));
    
    for vertex in vertices:
        print(vertex)
if __name__ == "__main__":
    # Path to the STEP file
    step_file_path = "D:\Thesis\Project\Backend\Example02.STEP"
    
    # Run the main function
    main(step_file_path)
