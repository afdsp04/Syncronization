import os
import shutil
from filecmp import dircmp
import time
import logging
  

def sync_folders(source, replica,logfile):
    
    logging.basicConfig(filename=logfile,level=logging.INFO,
                    format="%(asctime)s %(message)s")
    
    if not os.path.exists(replica):
        os.makedirs(replica)
        print(f"Created new directory : {replica}")

    # Compare directories
    comparison = dircmp(source, replica)
    
    # Copy files and directories from source to replica
    for item in comparison.left_only:
        src_path = os.path.join(source, item)
        dest_path = os.path.join(replica, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
            print(f"Copying new directory : {item} to {replica}")
        else:
            shutil.copy2(src_path, dest_path)
            print(f"Copying {item} file from {source} to {replica}")
            logging.info(f"Copying {item} file from {source} to {replica}")

    # Remove files and directories from replica that are not in source
    for item in comparison.right_only:
        print(item)
        dest_path = os.path.join(replica, item)
        if os.path.isdir(dest_path):
            shutil.rmtree(dest_path)
            print(f"Removing directories from {replica}")
            logging.info(f"Removing directories from {replica}")
        else:
            os.remove(dest_path)
            print(f"Removing {item} from {replica}")
            logging.info(f"Removing {item} file from {replica}")
    
    # Update files that are different
    for item in comparison.diff_files:
        src_path = os.path.join(source, item)
        dest_path = os.path.join(replica, item)
        shutil.copy2(src_path, dest_path)
        logging.info(f"Updating {item} file in {replica}")
        print(f"Updating {item} file in {replica}")

    # Recursively synchronize subdirectories
    for common_dir in comparison.common_dirs:
        sync_folders(os.path.join(source, common_dir), os.path.join(replica, common_dir), logfile)

# Define periodicity to execute job
def run_periodically(src_dir, dest_dir, interval, logfile):

    try:
        while True:
            print(f"Syncing {src_dir} with {dest_dir}...")
            sync_folders(src_dir, dest_dir, logfile)
            print(f"Next sync on {interval} seconds...")
            time.sleep(interval)  # Wait for the interval before performing the next synchronization

    except KeyboardInterrupt:
        print("\nSync was interrupted by the user.") # Sync was interrupted by the user

if __name__ == "__main__":
    source_folder = input ("Source dir:")
    replica_folder = input("Replica dir: ")
    interval = int (input("Interval (in seconds): "))
    logfile= input ("Logfile dir: ")
    run_periodically(source_folder, replica_folder, interval, logfile)