# Get direct script access (just for testing)
from procrustes import *

import matplotlib.pyplot as p; p.rcParams['toolbar'] = 'None';
import trimesh
import os


def load_obj(filepath):
    """Loads vertices and faces from an OBJ file."""
    vertices = []
    faces = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('f '):
                faces.append(line.strip())
    return np.array(vertices), faces


def save_obj(filepath, vertices, faces):
    """Saves vertices and faces to an OBJ file."""
    with open(filepath, 'w') as file:
        for vertex in vertices:
            file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            file.write(face + "\n")

def apply_gpa_to_folder(input_folder, output_folder):
    """
    Applies Generalized Procrustes Analysis to all OBJ files in a folder
    and saves the transformed files in another folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load all OBJ files from the input folder
    objs = []
    faces_list = []
    filenames = []
    for file in os.listdir(input_folder):
        if file.endswith('.obj'):
            filepath = os.path.join(input_folder, file)
            vertices, faces = load_obj(filepath)
            objs.append(vertices)  # Ensure numeric array
            faces_list.append(faces)
            filenames.append(file)

    # Perform GPA on the vertices
    objs = [np.array(obj, dtype=np.float64) for obj in objs]
    g = gpa(objs, -1)  # Perform GPA
    transformed_shapes = []
    for i in range(len(objs)):
        transformed_vertices = objs[i].dot(g[0][i]) * g[1][i] + g[2][i]
        transformed_shapes.append(transformed_vertices)

    # Save the transformed OBJ files
    for i, transformed_vertices in enumerate(transformed_shapes):
        output_path = os.path.join(output_folder, filenames[i])
        save_obj(output_path, transformed_vertices, faces_list[i])

# Example usage
input_folder ='/Users/navairarehman/Desktop/rsme2'  
output_folder = '/Users/navairarehman/Documents/FYP/3d preprocess/Procrustes/aligned_3d'  
apply_gpa_to_folder(input_folder, output_folder)
print("GPA done")

# input_file = '/Users/navairarehman/Documents/FYP/3d preprocess/Procrustes/rmse2/1010140217_cleaned.obj'
# vertices, faces = load_obj(input_file)
# print(vertices.dtype)