import os

# 获取当前脚本所在目录
current_directory = os.path.dirname(__file__)

# 定义子文件夹的相对路径
subfolder_path = 'modules'

# 获取子文件夹的完整路径
folder_path = os.path.join(current_directory, subfolder_path)

# 获取子文件夹的名字
folder_name = os.path.basename(folder_path)

# 初始化一个列表，用于存储文件名
file_names = []

# 遍历子文件夹下的所有文件名
for filename in os.listdir(folder_path):

    if filename.endswith('.v'):
        # 拼接完整的文件路径
        file_path = os.path.join(folder_path, filename)
        # 在文件名前面加上子文件夹的名字
        new_filename = os.path.join(f"../modules", filename)
        # 将新的文件名加入到列表中
        file_names.append(new_filename)

# 将文件名列表转换为一个字符串，用空格分隔
result = ' '.join(file_names)

# 打印结果
print(result)
