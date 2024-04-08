import os

def secure_path(path: str) -> str:
    return path.replace('../', '').replace('//', '/').replace('..\\', '').replace('\\', '/')

def create_output_directory(output_path: str):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

def list_files_in_folder(folder):
    files = []
    for root, _, filenames in os.walk(folder):
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(root, filename), folder))
    return files


