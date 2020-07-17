"""
添加对文件进行解析的方法
"""
import re
import ase


def parse_struc_file(file_name):
    fe_au_atoms = []
    iron_idx = get_Fe_atoms(file_name)
    with open(file_name, 'r') as orig_fd:
        # very small file
        orig_str = orig_fd.readlines()

    for line_idx in range(len(orig_str)):
        if 'Fe' in orig_str[line_idx]:
            orig_str[line_idx] = orig_str[line_idx].replace('Fe', 'Au', 1)
            tmp_file_name = 'tmp.struct'
            with open(tmp_file_name, 'w') as tmp_fd:
                tmp_fd.writelines(orig_str)
            at = ase.io.read(tmp_file_name)
            fe_au_atoms.append(at)
            orig_str[line_idx] = orig_str[line_idx].replace('Au', 'Fe', 1)

    return iron_idx, fe_au_atoms


def parse_scf_file(file_name, iron_idx):
    mm = get_MM(file_name, iron_idx)
    hff = get_HFF(file_name, iron_idx)
    eta = get_ETA(file_name, iron_idx)
    efg = get_EFG(file_name, iron_idx)
    rto = get_RTO(file_name, iron_idx)
    ret = []
    for i in range(len(iron_idx)):
        ret.append((mm[i], hff[i], eta[i], efg[i], rto[i]))
    return ret


def get_lines(scffile_path):
    with open(scffile_path, 'r') as f:
        text = f.readlines()
        return text


def get_Fe_atoms(structfile_path):
    Fe_atoms = []
    for n,line in enumerate(get_lines(structfile_path)):
        line = [i for i in line.split(' ') if i != '']
        if line[0] == "ATOM":
            serial_number = ""
            for i in line[1]:
                if i in "0123456789":
                    serial_number = serial_number + i
            serial_number = int(serial_number)
        if "Fe" in line[0]:
            Fe_atoms.append(serial_number)
    return Fe_atoms


def get_MM(scffile_path, iron_idx):
    MM = []
    pat_MM = re.compile(r':MMI\d{3}:.+?=.*')
    for line in get_lines(scffile_path):
        match_MM = pat_MM.match(line)
        if match_MM:
            match_MM = match_MM.group().split()[-1]
            MM.append(match_MM)
    return MM[: len(iron_idx)]


def get_HFF(scffile_path, iron_idx):
    HFF = []
    pat_HFF = re.compile(r':HFF\d{3}:.*')
    for line in get_lines(scffile_path):
        match_HFF = pat_HFF.match(line)
        if match_HFF:
            match_HFF = match_HFF.group().split()[-2]
            HFF.append(match_HFF)
    return HFF[: len(iron_idx)]


def get_ETA(scffile_path, iron_idx):
    ETA = []
    pat_ETA = re.compile(r':ETA\d{3}:.*')
    for line in get_lines(scffile_path):
        match_ETA = pat_ETA.match(line)
        if match_ETA:
            match_ETA = match_ETA.group().split()[-1]
            ETA.append(match_ETA)
    return ETA[: len(iron_idx)]


def get_EFG(scffile_path, iron_idx):
    EFG = []
    pat_EFG = re.compile(r':EFG\d{3}:.+?=.*')
    for line in get_lines(scffile_path):
        match_EFG = pat_EFG.match(line)
        if match_EFG:
            match_EFG = match_EFG.group().split()[-5]
            EFG.append(match_EFG)
    return EFG[: len(iron_idx)]


def get_RTO(scffile_path, iron_idx):
    RTO = []
    pat_RTO = re.compile(r':RTO\d{3}:.*')
    for line in get_lines(scffile_path):
        match_RTO = pat_RTO.match(line)
        if match_RTO:
            match_RTO = match_RTO.group().split()[-1]
            RTO.append(match_RTO)
    return RTO[: len(iron_idx)]