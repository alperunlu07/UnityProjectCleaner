import os
import time
import shutil
from datetime import datetime, timedelta

# Specify the path to your Unity projects and the cleanup threshold (in days)
UNITY_PROJECTS_PATH = "C:/Path/To/Your/UnityProjects"
DAYS_THRESHOLD = 15  # Number of days after which files will be deleted

# Define folders to delete in each Unity project
FOLDERS_TO_DELETE = ["Library", "Logs", "obj", "Temp","MemoryCaptures"]

# Calculate the cutoff time
cutoff_time = time.time() - DAYS_THRESHOLD * 86400  # 86400 seconds in a day

def find_old_unity_folders(project_path):
    """Identify specified folders in a Unity project for potential deletion if not modified recently."""
    folders_to_remove = []
    for folder_name in FOLDERS_TO_DELETE:
        folder_path = os.path.join(project_path, folder_name)
        if os.path.exists(folder_path):
            folder_mod_time = os.path.getmtime(folder_path)
            if folder_mod_time < cutoff_time:
                folders_to_remove.append(folder_path)
            else:
                print(f"Skipping {folder_path} as it was modified")
                return
    return folders_to_remove

def main():
    all_folders_to_delete = []
    
    # Traverse each project in the Unity projects directory
    for root, dirs, _ in os.walk(UNITY_PROJECTS_PATH):
        for project_dir in dirs:
            project_path = os.path.join(root, project_dir)
            if os.path.isdir(project_path):
                print(f"\nChecking project: {project_path}")
                folders = find_old_unity_folders(project_path)
                if folders:
                    all_folders_to_delete.extend(folders)
                    print(f"Marked for deletion: {folders}")
        # No need to traverse deeper levels
        break

    # If there are folders marked for deletion, prompt the user for confirmation
    if all_folders_to_delete:
        print("\nThe following folders are marked for deletion:")
        for folder in all_folders_to_delete:
            print(f"- {folder}")
        
        confirm = input("\nDo you want to delete these folders? (yes/no): ").strip().lower()
        if confirm == 'yes':
            for folder in all_folders_to_delete:
                print(f"Deleting: {folder}")
                shutil.rmtree(folder)
            print("Deletion completed.")
        else:
            print("Deletion canceled.")
    else:
        print("No folders found for deletion.")

if __name__ == "__main__":
    main()