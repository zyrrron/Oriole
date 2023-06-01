import os
import shutil


def print_subfolder_names():
    current_directory = os.getcwd()
    dictD = {}

    for root, directories, files in os.walk(current_directory):
        if root != current_directory and os.path.dirname(root) == current_directory:
            directories = sorted(directories, key=lambda x: (len(x), x))
            rootName = root.split('/')[-1]
            dictD[rootName] = list()
            if rootName == '8':
                for folder_name in directories:
                    dictD[rootName].append(f"{rootName}input_{folder_name}-5c\t./benchmark/{rootName}-input-boolean-circuits/{folder_name}\t./lib\tTRUE\t1,7\t\t3\t2,2\t5\tTRUE\tC\t5\t./results/{rootName}-input-boolean-circuits/{folder_name}-5c")

    dictD = dict(sorted(dictD.items()))
    for d in dictD:
        for val in dictD[d]:
            print(val)


def delete_matching_subfolders(input_folder_name):
    current_directory = os.getcwd()

    for root, directories, files in os.walk(current_directory):
        if root != current_directory:
            for directory in directories:
                if directory == input_folder_name:
                    folder_path = os.path.join(root, directory)
                    shutil.rmtree(folder_path)
                    print(f"Deleted folder: {folder_path}")


# Example usage:
# delete_matching_subfolders("nparts")
print_subfolder_names()
