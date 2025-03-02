import os
import re
import unicodedata

def is_chinese_char(char):
    """判断一个字符是否是中文字符"""
    # 使用 Unicode 范围来检测中文字符
    # 基本汉字范围：\u4e00-\u9fff
    return '\u4e00' <= char <= '\u9fff'

def rename_photos_with_chinese(folder_path, replacement='', file_extensions=('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
    """
    批量重命名文件夹中包含中文的照片文件名
    
    参数:
    folder_path: 照片所在的文件夹路径
    replacement: 用来替换中文字符的字符串，默认为空（直接删除中文字符）
    file_extensions: 要处理的文件扩展名元组
    """
    # 确保文件夹路径存在
    if not os.path.isdir(folder_path):
        print(f"错误: '{folder_path}' 不是一个有效的文件夹路径")
        return
    
    # 计数器
    renamed_count = 0
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否是照片（根据扩展名）
        if filename.lower().endswith(file_extensions):
            old_path = os.path.join(folder_path, filename)
            
            # 分离文件名和扩展名
            name, ext = os.path.splitext(filename)
            
            # 检查文件名中是否包含中文字符
            has_chinese = any(is_chinese_char(char) for char in name)
            
            if has_chinese:
                # 替换所有中文字符
                new_name = ''.join(replacement if is_chinese_char(char) else char for char in name)
                
                # 如果替换后文件名为空，使用默认名称
                if not new_name.strip():
                    new_name = f"image_{renamed_count + 1}"
                
                # 处理新文件名可能存在的特殊字符
                new_name = re.sub(r'[\\/:*?"<>|]', '_', new_name)
                
                # 组合新的完整路径
                new_path = os.path.join(folder_path, new_name + ext)
                
                # 处理文件名冲突
                counter = 1
                while os.path.exists(new_path):
                    new_path = os.path.join(folder_path, f"{new_name}_{counter}{ext}")
                    counter += 1
                
                # 重命名文件
                try:
                    os.rename(old_path, new_path)
                    print(f"已重命名: '{filename}' -> '{os.path.basename(new_path)}'")
                    renamed_count += 1
                except Exception as e:
                    print(f"重命名 '{filename}' 时出错: {e}")
    
    print(f"\n完成! 共重命名 {renamed_count} 个文件。")

def get_user_input():
    """交互式获取用户输入"""
    print("=" * 50)
    print("照片文件中文字符重命名工具")
    print("=" * 50)
    
    # 获取文件夹路径
    while True:
        folder_path = input("\n请输入照片所在的文件夹路径: ").strip()
        
        # 处理用户输入的路径
        # 去掉可能存在的引号（用户可能从文件资源管理器复制路径）
        if (folder_path.startswith('"') and folder_path.endswith('"')) or \
           (folder_path.startswith("'") and folder_path.endswith("'")):
            folder_path = folder_path[1:-1]
            
        # 检查路径是否存在
        if not os.path.exists(folder_path):
            print(f"错误: 路径 '{folder_path}' 不存在，请重新输入")
            continue
        
        # 检查是否是文件夹
        if not os.path.isdir(folder_path):
            print(f"错误: '{folder_path}' 不是一个文件夹，请重新输入")
            continue
        
        # 路径有效，跳出循环
        break
    
    # 获取替换字符
    replacement = input("\n请输入用于替换中文字符的字符串(直接回车表示删除中文字符): ").strip()
    
    # 确认操作
    print("\n您将要执行以下操作:")
    print(f"- 文件夹: {folder_path}")
    print(f"- 替换字符: {repr(replacement) if replacement else '删除中文字符'}")
    
    confirm = input("\n确认执行? (y/n): ").strip().lower()
    if confirm != 'y':
        print("操作已取消")
        return None, None
    
    return folder_path, replacement

if __name__ == "__main__":
    try:
        # 获取用户输入
        folder_path, replacement = get_user_input()
        
        if folder_path:
            # 执行重命名操作
            rename_photos_with_chinese(folder_path, replacement)
        
        # 程序结束提示
        input("\n按回车键退出...")
    except KeyboardInterrupt:
        print("\n\n操作已被用户中断")
    except Exception as e:
        print(f"\n发生错误: {e}")
        input("\n按回车键退出...")