from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.STEPControl import STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopoDS import topods_Vertex,topods_Face
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder



def calculate_face_area(face):
    """
    Calculate the area of a given face.
    """
    props = GProp_GProps()
    brepgprop_SurfaceProperties(face, props)
    return props.Mass()

# Function to read the STEP file and return the shape
def read_step_file(file_path):
    step_reader = STEPControl_Reader()
    Interface_Static_SetCVal("read.step.product.mode", "1")
    status = step_reader.ReadFile(file_path)
    if status != 1:
        raise Exception("Error: can't read file.")
    step_reader.TransferRoot(1)
    shape = step_reader.Shape(1)
    return shape

# Function to extract properties
def extract_properties(shape):
    properties = {}

    # Volume properties
    props = GProp_GProps()
    brepgprop_VolumeProperties(shape, props)
    properties['Volume'] = props.Mass()
    properties['Center of Mass'] = props.CentreOfMass().Coord()
   # properties['Inertia Matrix'] = props.MatrixOfInertia();#.Data()
    inertia_matrix = props.MatrixOfInertia()
    properties['Inertia Matrix'] = [[inertia_matrix.Value(i, j) for j in range(1, 4)] for i in range(1, 4)]


    # Surface area
    brepgprop_SurfaceProperties(shape, props)
    properties['Surface Area'] = props.Mass()

    # Exploring Faces to get more details
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    face_count = 0
    
    
    for _ in range(exp.More()):
        face_count += 1
        exp.Next()
        
        
    properties['Number of Faces'] = face_count

    # Exploring Solids
    exp = TopExp_Explorer(shape, TopAbs_SOLID)
    solid_count = 0
    for _ in range(exp.More()):
        solid_count += 1
        exp.Next()
        
    properties['Number of Solids'] = solid_count

    return properties

def calculate_area(shape):
    topology = TopologyExplorer(shape)
    faces = list(topology.faces())
    areaList=[];
    # Calculate the area of each face and print it
    for i, face in enumerate(faces, start=1):
        area = calculate_face_area(face)
#        print(f"Face {i}: Area = {area:.2f} square units")
        areaList.append(f"Face {i}: Area = {area:.2f} square units")
    return areaList;
    
def calculate_edge(shape):
    edge_explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    # Count the number of edges
    edge_count = 0
    while edge_explorer.More():
        edge_count += 1
        edge_explorer.Next()
#    print("Edge count::"+str(edge_count));    
    return str(edge_count);  
      
def calculate_vertex(shape):
    vertices = []
    vertex_explorer = TopExp_Explorer(shape, TopAbs_VERTEX)
    while vertex_explorer.More():
        vertex = topods_Vertex(vertex_explorer.Current())
        pnt = BRep_Tool.Pnt(vertex)
        vertices.append((pnt.X(), pnt.Y(), pnt.Z()))
        vertex_explorer.Next();
#    for vertex in vertices:
#        print(vertex)
    return vertices;    

# Main function
def main_step(file_path):
    shape = read_step_file(file_path)
    properties = extract_properties(shape)
##    for prop, value in properties.items():
##        print(f"{prop}: {value}")
##    print(calculate_area(shape))   
##    print(calculate_edge(shape))
##    print(calculate_vertex(shape))
    print(analyze_shape(shape))
#    get_vert_edge_shape(shape)
##    print(explore_faces(shape))
##    print(get_faces(shape))
    
def analyze_shape(shape):
    prop = GProp_GProps()
    tolerance = 1e-5  # Adjust as needed
    analyzeList=[];

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

#    print(f"Total faces: {face_count}")
#    print(f"Planar faces: {plane_count}")
#    print(f"Cylindrical faces: {cylinder_count}")
#    print(f"Volume = {volume}")
#    print(f"Surface Area:{surface_area}");
#    print(f"center_of_mass:{center_of_mass}");
    analyzeList.append(f"Total faces: {face_count}")
    analyzeList.append(f"Planar faces: {plane_count}")
    analyzeList.append(f"Cylindrical faces: {cylinder_count}")
    analyzeList.append(f"Volume = {volume}")
    analyzeList.append(f"Surface Area:{surface_area}")
    analyzeList.append(f"center_of_mass:{center_of_mass}")
    return analyzeList;

"""def get_vert_edge_shape(shape):
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
    print("Vertex::"+str(vertex));"""


def explore_faces(shape):
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = topods_Face(exp.Current())
        # You can use BRep_Tool.Surface(face) to get the surface geometry
        print("Face found.")
        exp.Next()
def get_faces(shape):
    prop = GProp_GProps()
    tolerance = 1e-5  # Adjust as needed
    volume = brepgprop_VolumeProperties(shape, prop, tolerance)
#    print(f"Volume = {volume}")
    return "Volume = {volume}";
if __name__ == "__main__":
    # Replace 'your_step_file.step' with the path to your STEP file
    step_file_path = 'D:\Thesis\Project\Backend\Example02.STEP'
    main_step(step_file_path)
