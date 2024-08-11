from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods_Face
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties,brepgprop_SurfaceProperties
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder


def read_step_file(filename):
    # Create a STEP reader
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)
    
    if status == IFSelect_RetDone:
        # Transfer the contents of the file to a shape
        step_reader.TransferRoots()
        shape = step_reader.Shape()
        print("STEP file loaded successfully.")
        return shape
    else:
        raise Exception("Error: Unable to read the STEP file.")

def get_vert_edge_shape(shape):
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    face=[];
    edge=[];
    vertex=[];
    while exp.More():
        s = exp.Current()
     # Check entity type and extract properties
        if s.ShapeType() == TopAbs_FACE:
            face = topods_Face(s)
            face.append(topods.face(s))
        # Calculate face area, etc.
        elif s.ShapeType() == TopAbs_EDGE:
            edge = topods_Edge(s)
            edge.append(topods.edge(s))
        # Calculate edge length, etc.
        elif s.ShapeType() == TopAbs_VERTEX:
            vertex = topods_Vertex(s)
            vertex.append(topods.vertex(s))
        # Get vertex coordinates
    #explorer.Next()
        exp.Next()
    print("Face::"+str(face));
    print("Edge::"+str(edge));
    print("Vertex::"+str(vertex));


def explore_faces(shape):
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = topods_Face(exp.Current())
        # You can use BRep_Tool.Surface(face) to get the surface geometry
        print("Face found.")
        exp.Next()
def get_faces():
    prop = GProp_GProps()
    tolerance = 1e-5  # Adjust as needed
    volume = brepgprop_VolumeProperties(my_shape, prop, tolerance)
    print(f"Volume = {volume}")
    
    
def analyze_shape(shape):
    prop = GProp_GProps()
    tolerance = 1e-5  # Adjust as needed
    from OCC.Core.TopAbs import TopAbs_FACE
    from OCC.Core.TopExp import TopExp_Explorer

    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    volume = brepgprop_VolumeProperties(shape, prop, tolerance)
    face_count = 0
    plane_count = 0
    cylinder_count = 0
    center_of_mass=prop.CentreOfMass().Coord()

# Compute surface area
    brepgprop_SurfaceProperties(shape, prop)
    surface_area = prop.Mass()
    
    
    while explorer.More():
        face = topods_Face(explorer.Current())
        surf = BRepAdaptor_Surface(face, True)
        face_count += 1

        if surf.GetType() == GeomAbs_Plane:
            plane_count += 1
        elif surf.GetType() == GeomAbs_Cylinder:
            cylinder_count += 1

        explorer.Next()

    print(f"Total faces: {face_count}")
    print(f"Planar faces: {plane_count}")
    print(f"Cylindrical faces: {cylinder_count}")
    print(f"Volume = {volume}")
    print(f"Surface Area:{surface_area}");
    print(f"center_of_mass:{center_of_mass}");
    #    properties['center_of_mass'] = mass_props.CentreOfMass().Coord()

# Main function
if __name__ == "__main__":
#    filename = "D:\Thesis\Project\Backend\Example02.STEP"  # Replace with the path to your STEP file
#    shape = read_step_file(filename)
#    explore_faces(shape)
    path_to_file = "D:\Thesis\Project\Backend\Example02.STEP";  # Replace with your actual file path
    my_shape = read_step_file(path_to_file)
    analyze_shape(my_shape);
    get_vert_edge_shape(my_shape);
    #get_faces();