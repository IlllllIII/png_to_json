import json
import os
from PIL import Image
import base64

def read_metadata(image_path):
    with Image.open(image_path) as img:
        # 获取所有PNG文本块数据
        metadata = img.text
        for key in metadata:
            try:
                # 尝试base64解码
                decoded_data = base64.b64decode(metadata[key])
                # 尝试解析JSON
                json_data = json.loads(decoded_data)
                return json_data
            except:
                continue
    return None

# 指定文件夹路径
input_folder = "png_file"
output_folder = "output_file"

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 处理所有PNG文件
for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        png_path = os.path.join(input_folder, filename)
        try:
            # 读取并解析角色卡数据
            card_data = read_metadata(png_path)

            if card_data:
                # 创建JSON文件名
                json_filename = os.path.splitext(filename)[0] + ".json"
                json_path = os.path.join(output_folder, json_filename)

                # 保存JSON文件
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(card_data, f, indent=4, ensure_ascii=False)
                print(f"成功转换: {filename}")
            else:
                print(f"无法提取信息: {filename}")

        except Exception as e:
            print(f"处理 {filename} 时出错: {str(e)}")
