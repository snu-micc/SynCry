import os
import json
import warnings
from tqdm import tqdm
from pymatgen.core.structure import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher

SynCry_folder = "./Structures_SynCry"
exp_folder = "./Structures_ICSD"
OUTPUT_JSON = "./Matching_results.json"

def load_structure(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            cif_contents = f.read()
        structure = Structure.from_str(cif_contents, fmt="cif")
        return structure
    except Exception as e:
        print(f"Skipping invalid CIF file: {os.path.basename(filepath)} (Error: {e})")
    return None

def load_structures_from_folder(folder_path):
    structures = []
    filenames = []
    cif_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".cif")])
    for filename in tqdm(cif_files, desc=f"Loading structures from {os.path.basename(folder_path)}"):
        filepath = os.path.join(folder_path, filename)
        structure = load_structure(filepath)
        if structure:
            structures.append(structure)
            filenames.append(filename)
    return structures, filenames

A_structures, A_filenames = load_structures_from_folder(SynCry_folder)
B_structures, B_filenames = load_structures_from_folder(exp_folder)

matcher = StructureMatcher()

def match_structures():
    matching_results = {}
    for i, a_structure in enumerate(tqdm(A_structures, desc="Matching Structures", unit="file")):
        a_filename = A_filenames[i]
        matched = False
        for j, b_structure in enumerate(B_structures):
            if matcher.fit(a_structure, b_structure):
                matching_results[a_filename] = B_filenames[j]
                matched = True
                break
        if not matched:
            matching_results[a_filename] = "No Match"
    return matching_results

matching_results = match_structures()

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(matching_results, f, indent=4)
