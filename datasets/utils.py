import ase
import os
from .parse import parse_scf_file,parse_struc_file
from ase.db import connect
import logging
"""
针对数据集的工具类
"""

logger = logging.getLogger(__name__)


def generate_ase_db(root_folder, target_path, db_name):
    """
    通过scf文件和struct文件生成ase db
    :param root_folder: 数据地址
    :param target_path: 生成db的路径
    :param db_name: 生成db名称
    :return:
    """
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    db_path = os.path.join(target_path, db_name)

    if os.path.exists(db_path):
        os.remove(db_path)
    db = connect(db_path)

    for root, dirs, files in os.walk(root_folder):
        if len(files) != 2:
            logger.info('file count != 2, pass')
            continue
        struct_name, scf_name = '', ''
        for f in files:
            file_name = os.path.join(root, f)
            if f.endswith('.struct') and struct_name == '':
                struct_name = file_name
            elif f.endswith('.scf') and scf_name == '':
                scf_name = file_name
            else:
                logger.error('file format error.')
                break
        else:
            iron_idx, at_lst = parse_struc_file(struct_name)
            props_lst = parse_scf_file(scf_name, iron_idx)

            if len(at_lst) != len(props_lst):
                logger.info('struct file and scf file is not a pair? diff length...')
                continue
            else:
                for i in range(len(at_lst)):
                    if '' not in props_lst[i]:
                        db.write(at_lst[i], data={'mm': float(props_lst[i][0]),
                            'hff': float(props_lst[i][1]),
                            'eta': float(props_lst[i][2]),
                            'efg': float(props_lst[i][3]),
                            'rto': float(props_lst[i][4])
                            })
