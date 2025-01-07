import os
import json
from tqdm import tqdm

# you have to convert cif to json first(figure out at our StructLLM repo)

def extract_important_info(json_data):
    lattice = json_data["lattice"]
    a = round(lattice["a"], 3)
    b = round(lattice["b"], 3)
    c = round(lattice["c"], 3)
    alpha = round(lattice["alpha"], 5)
    beta = round(lattice["beta"], 5)
    gamma = round(lattice["gamma"], 5)
    #1. lattice
    lattice_info = f"{a}, {b}, {c}, {alpha}, {beta}, {gamma}"
    #2. sites
    site_info = []
    for site in json_data["sites"]:
        element_label = site["label"]
        abc_coords = site["abc"]
        abc_coords_rounded = [round(coord, 4) for coord in abc_coords]
        abc_str = f"{element_label}({abc_coords_rounded[0]}, {abc_coords_rounded[1]}, {abc_coords_rounded[2]})"
        site_info.append(abc_str)
    site_info_str = ", ".join(site_info)
    
    #3. creating CIF string
    result_string = f"{lattice_info} : {site_info_str}"
    
    return result_string

# saving the result to a file
def process_files(input_folder, output_folder):
    files = [f for f in os.listdir(input_folder) if f.endswith(".json")]

    for filename in tqdm(files):
        input_file_path = os.path.join(input_folder, filename)
        
        with open(input_file_path, 'r') as f:
            json_data = json.load(f)
        
        result_string = extract_important_info(json_data)
        
        output_file_name = f"{os.path.splitext(filename)[0]}_processed.json"
        output_file_path = os.path.join(output_folder, output_file_name)
        
        with open(output_file_path, 'w') as f:
            json.dump({"result": result_string}, f)

# folder paths
input_folder = ""  # your json-files folder path (CIF original)
output_folder = ""  # your output folder path (CIF string)

process_files(input_folder, output_folder)