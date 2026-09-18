#!/usr/bin/env python3

import sys
import subprocess
import tempfile
import redis
import pyaltiumlib
import os


def get_files_in_repo(repo_path, revision, extension):
    try:
        output = subprocess.check_output(
            ['/usr/bin/svnlook', 'tree', repo_path, '--full-paths', '-r', revision], 
            text=True
        )
        paths = []
        for line in output.splitlines():
            clean_path = line.strip()
            if clean_path.lower().endswith(extension):
                paths.append(clean_path)
        return paths
    except Exception as e:
        return []

def extract_file_and_get_parts(repo_path, revision, file_path):
    try:
        file_data = subprocess.check_output(
            ['/usr/bin/svnlook', 'cat', repo_path, file_path, '-r', revision]
        )
    except Exception as e:
        return []

    _, ext = os.path.splitext(file_path)
    
    with tempfile.NamedTemporaryFile(suffix=ext, delete=True) as tmp:
        tmp.write(file_data)
        tmp.flush()
        
        try:
            lib_file = pyaltiumlib.read(tmp.name)
            parts = lib_file.list_parts()
            return parts
        except Exception as e:
            return []

def get_all_symbols(repo_path, revision):
    schlib_files = get_files_in_repo(repo_path, revision, '.schlib')
    all_elements = []
    
    for file_path in schlib_files:
        parts = extract_file_and_get_parts(repo_path, revision, file_path)
        all_elements.extend([{"name": i, "type": "symbol"} for i in parts])
        
    return all_elements, len(schlib_files)

def get_all_footprints(repo_path, revision):
    pcblib_files = get_files_in_repo(repo_path, revision, '.pcblib')
    all_elements = []
    
    for file_path in pcblib_files:
        parts = extract_file_and_get_parts(repo_path, revision, file_path)
        all_elements.extend([{"name": i, "type": "footprint"} for i in parts])
        
    return all_elements, len(pcblib_files)

def main():
    if len(sys.argv) < 3:
        sys.exit(1)
    
    repo_path = sys.argv[1]
    revision = sys.argv[2]


    symbols, schlib_count = get_all_symbols(repo_path, revision)
    footprints, pcblib_count = get_all_footprints(repo_path, revision)

    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        
        r.set('schlib_count', schlib_count)
        r.set('pcblib_count', pcblib_count)
        r.set('symbols_count', len(symbols))
        r.set('footprints_count', len(footprints))
        
    except:
        print("Error setting Redis keys")

if __name__ == '__main__':
    main()