# -*- coding: utf-8 -*-
# @Time    : 08/03/2023 13:10
# @Author  : Marshall
# @FileName: zip_util.py
import os
import os.path
from zipfile import ZipFile


def zip_file(file_i: str, file_o: str) -> None:
    with ZipFile(file_o, 'w') as z:
        z.write(file_i, arcname=(n := os.path.basename(file_i)))
        print('zip_file:', n)


def zip_files(*files_i: str, file_o: str) -> None:
    with ZipFile(file_o, 'w') as z:
        for f in files_i:
            z.write(f, arcname=(n := os.path.basename(f)))
            print('zip_files:', n)


def zip_dir(dir_i: str, file_o: str) -> None:
    dir_i_parent = os.path.dirname(dir_i)
    with ZipFile(file_o, 'w') as z:
        z.write(dir_i, arcname=(n := os.path.basename(dir_i)))
        print('zip_dir:', n)
        for root, dirs, files in os.walk(dir_i):
            for fn in files:
                z.write(
                    fp := os.path.join(root, fn),
                    arcname=(n := os.path.relpath(fp, dir_i_parent)),
                )
        print('zip_dir:', n)


def zip_dirs(*dirs_i: str, file_o: str) -> None:
    prefix = os.path.commonprefix(dirs_i)
    with ZipFile(file_o, 'w') as z:
        for d in dirs_i:
            z.write(d, arcname=(n := os.path.relpath(d, prefix)))
            print('zip_dirs:', n)
            for root, dirs, files in os.walk(d):
                for fn in files:
                    z.write(
                        fp := os.path.join(root, fn),
                        arcname=(n := os.path.relpath(fp, prefix)),
                    )
            print('zip_dirs:', n)


if __name__ == '__main__':
    zip_dir(r'F:\4_temp', r'F:\4_temp' + '.zip')
