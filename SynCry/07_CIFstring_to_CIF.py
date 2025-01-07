# we use this function to convert CIF string to CIF file.
from pymatgen.core import Lattice, Structure, Element
from pymatgen.io.cif import CifWriter
import json
import pandas as pd

def save_structure_to_cif(structure_str, filename):
    try:
        parts = structure_str.split(':')
        lattice_params = [float(x) for x in parts[0].split(',')]
        lattice = Lattice.from_parameters(*lattice_params)
        atoms = parts[1].split('), ')
        species = []
        coords = []
        for atom in atoms:
            if '(' in atom:
                element, position = atom.split('(')
                element_symbol = ''.join([char for char in element if char.isalpha()])
                species.append(Element(element_symbol.strip()))
                coords.append([float(x) for x in position.strip(')').split(',')])
        
        if not species or not coords:
            # print warnings
            return
        
        structure = Structure(lattice, species, coords)
        cif_writer = CifWriter(structure)
        cif_writer.write_file(filename)
    except Exception as e:
        print(e)