import os




def clear_directory_files(path):
    # 检查路径是否存在
    if not os.path.exists(path):
        print(f"路径 '{path}' 不存在。")
        return

    # 遍历目录中的所有文件和子目录
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        print(f"检查: {file_path}")  # 打印检查的文件路径
        try:
            # 如果是文件，删除它
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"已删除文件: {file_path}")
            else:
                print(f"跳过目录: {file_path}")  # 如果是目录，打印跳过信息
        except Exception as e:
            print(f"删除文件 {file_path} 时出错: {e}")


# 使用示例



clear_directory_files(r'C:\BrowserDownload\final')
clear_directory_files(r'C:\BrowserDownload\r_b')
clear_directory_files(r'C:\BrowserDownload\rb_ins')
clear_directory_files(r'C:\BrowserDownload\test')


