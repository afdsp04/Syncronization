import os
import shutil
from filecmp import dircmp
import time

def sync_folders(source, replica):
    if not os.path.exists(replica):
        os.makedirs(replica)
    
    # Compare directories
    comparison = dircmp(source, replica)

    print (comparison)
    
    # Copy files and directories from source to replica
    for item in comparison.left_only:
        src_path = os.path.join(source, item)
        dest_path = os.path.join(replica, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)