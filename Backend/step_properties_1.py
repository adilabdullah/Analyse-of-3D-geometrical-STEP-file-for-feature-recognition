from OCP.STEPControl import STEPControl_Reader
#from OCP.BRepTools import breptools_Read
#from OCP.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh

from OCC.Core.TopoDS import topods_Face, topods_Edge, topods_Vertex
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere
from OCC.Core.GProp import GProp_GProps

def read_step_file(file_path):
    # Create a STEP reader
    step_reader = STEPControl_Reader()
    
    # Read the STEP file
    status = step_reader.ReadFile(file_path)
    
    if status != 1:  # Check if the file was read successfully
        raise Exception("Error reading STEP file")
    
    # Transfer contents of STEP file to TopoDS_Shape
    step_reader.TransferRoots()
    shape = step_reader.OneShape()
    
    return shape

def get_shape_properties(shape):
    properties = {}
    
    # Topological properties
    explorer = TopExp_Explorer()
    # Explorer to iterate through the shape
    #explorer = TopExp_Explorer(shape, TopAbs_FACE)
    
    face_count = 0
    bounding_box = Bnd_Box()
    
    while explorer.More():
        face = topods_Face(explorer.Current())
        surf = BRepAdaptor_Surface(face, True)
        surf_type = surf.GetType()
        
        if surf_type == GeomAbs_Plane:
            properties['surface_types']['plane'] += 1
        elif surf_type == GeomAbs_Cylinder:
            properties['surface_types']['cylinder'] += 1
        elif surf_type == GeomAbs_Cone:
            properties['surface_types']['cone'] += 1
        elif surf_type == GeomAbs_Sphere:
            properties['surface_types']['sphere'] += 1
        else:
            properties['surface_types']['other'] += 1
        
        explorer.Next()
  
   
    return {
        "number_of_faces": face_count,
        "bounding_box": bounding_box
    }

#def print_bounding_box(bounding_box):
    #x_min, y_min, z_min, x_max, y_max, z_max = bounding_box.Get()
    #print(f"Bounding Box:\n  X: {x_min} to {x_max}\n  Y: {y_min} to {y_max}\n  Z: {z_min} to {z_max}")
    
# Replace 'your_step_file.step' with the path to your STEP file
step_file_path = 'D:\Thesis\Project\Backend\Example02.STEP'

shape = read_step_file(step_file_path)
properties = get_shape_properties(shape)

print(f"Number of Faces: {properties['number_of_faces']}")
print(f"Properties:{properties}");
#print_bounding_box(properties['bounding_box'])

#bb1 = get_boundingbox(shape)
#print(bb1)

"""import OCC.Core.STEPControl as stpctl
import OCC.Core.TopoDS as topods
import OCC.Core.BRepBuilderAPI as brepapi
import OCC.Core.TopExp as topExp
import OCC.Core.Geom as geom
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods_Face, topods_Edge, topods_Vertex
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve

def extract_face_properties(shape):
    properties = []
    face_count=0;
   # explorer = topExp.TopExp_Explorer(shape, topExp.TopAbs_FACE)
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face = explorer.Current()
        face_geometry = brepapi.BRepBuilderAPI_MakeFace(face).Face()
        
        face = topods_Face(explorer.Current())
        surf = BRepAdaptor_Surface(face, True)
        face_count += 1
    #    area = face_geometry.Area()
        # ... other properties
    #    properties.append({'area': area})
        explorer.Next()
    print("Face Count:"+str(face_count));    
    return properties

# Example usage:
# Create a STEP reader
#step_reader = STEPControl_Reader()
#step_reader.ReadFile("D:\Thesis\Project\Backend\Example02.STEP").TransferRoots()
#shape = step_reader.Shape()


step_reader = STEPControl_Reader()

status = step_reader.ReadFile("D:\Thesis\Project\Backend\Example02.STEP")
    
if status != 1:  # Check if the file was read successfully
    raise Exception("Error reading STEP file")
    
    # Transfer contents of STEP file to TopoDS_Shape
step_reader.TransferRoots()
shape = step_reader.OneShape()
face_properties = extract_face_properties(shape)
print(face_properties)"""
