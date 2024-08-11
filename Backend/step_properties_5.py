from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.STEPControl import STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Core.GProp import GProp_GProps

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
    
    # Inertia Matrix
    inertia_matrix = props.MatrixOfInertia()
    properties['Inertia Matrix'] = [[inertia_matrix.Value(i, j) for j in range(1, 4)] for i in range(1, 4)]
    
    return properties

# Main function
def main(file_path):
    shape = read_step_file(file_path)
    properties = extract_properties(shape)
    for prop, value in properties.items():
        if prop == 'Inertia Matrix':
            print(f"{prop}:")
            for row in value:
                print(f"  {row}")
        else:
            print(f"{prop}: {value}")

if __name__ == "__main__":
    # Replace 'your_step_file.step' with the path to your STEP file
    step_file_path = 'D:\Thesis\Project\Backend\Example02.STEP'
    main(step_file_path)
