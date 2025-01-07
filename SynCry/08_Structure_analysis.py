from tqdm import tqdm

# we use below function to find crystal systems
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

def get_crystal_systems(structures):
    crystal_systems = []
    for i, structure in enumerate(tqdm.tqdm(structures, desc="Processing structures")):
        if isinstance(structure, Structure):
            try:
                analyzer = SpacegroupAnalyzer(structure)
                space = analyzer.get_crystal_system()
                crystal_systems.append(space)
            except Exception as e:
                print("Error processing structure: ", e)
        else:
            print(f"Error processing structure {i}")
    return crystal_systems

# we use below function to find space groups
def get_space_groups(structures):
    space_groups = []
    for i, structure in enumerate(tqdm.tqdm(structures, desc="Processing structures")):
        if isinstance(structure, Structure):
            try:
                analyzer = SpacegroupAnalyzer(structure)
                space_group = analyzer.get_space_group_symbol()
                space_groups.append(space_group)
            except Exception as e:
                print("Error processing structure: ", e)
        else:
            print(f"Error processing structure {i}")
    return space_groups

# we use below function to calculate energy above hull and formation energy

from mp_api.client import MPRester
from pymatgen.core import Structure
from chgnet.model.model import CHGNet

mpr = MPRester("") # your api key
chgnet = CHGNet.load()

def calculate_energy_and_hull(structure_list, reference_structures):
    real_energy_list = []
    predicted_energy_list = []
    
    for structure, ref_structure in tqdm(zip(structure_list, reference_structures), total=len(structure_list), desc="Processing Structures"):
        try:

            composition_no_spaces = str(structure.composition).replace(' ', '')
            materials = mpr.materials.summary.search(formula=composition_no_spaces, fields=["energy_above_hull", "formation_energy_per_atom"])

            if not materials:
                continue
            min_hull_energy = min(item["energy_above_hull"] for item in materials)
            min_formation_energy = min(item["formation_energy_per_atom"] for item in materials)

            prediction_original = chgnet.predict_structure(ref_structure)
            prediction_fixed = chgnet.predict_structure(structure)
            energy_difference = prediction_fixed["e"] - prediction_original["e"]

            predicted_energy = min_hull_energy + energy_difference
            
            real_energy_list.append(min_hull_energy)
            predicted_energy_list.append(predicted_energy)

        except Exception as e:
            print(f"Error processing structure: {e}")
            continue
    
    return real_energy_list, predicted_energy_list