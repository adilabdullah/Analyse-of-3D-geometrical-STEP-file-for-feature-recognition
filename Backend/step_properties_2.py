import OCC.Core.TopoDS as topods
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.StepRepr import StepRepr_RepresentationItem


reader = STEPControl_Reader()
tr = reader.WS().TransferReader()
reader.ReadFile('D:\Thesis\Project\Backend\Example02.STEP')
reader.TransferRoots()
model = reader.StepModel()
shape = reader.OneShape()


exp = TopExp_Explorer(shape, TopAbs_FACE)
while exp.More():
    s = exp.Current()
     # Check entity type and extract properties
    if s.ShapeType() == TopAbs_FACE:
        face = topods.Face(s)
        # Calculate face area, etc.
    elif s.ShapeType() == TopAbs_EDGE:
        edge = topods.Edge(s)
        # Calculate edge length, etc.
    elif s.ShapeType() == TopAbs_VERTEX:
        vertex = topods.Vertex(s)
        # Get vertex coordinates
    #explorer.Next()
    s.Next()
    