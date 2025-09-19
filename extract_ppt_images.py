#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT图片提取工具
从PPTX文件中提取所有图片并分析内容
"""
import zipfile
import os
import shutil
from xml.etree import ElementTree as ET
import re

def extract_images_from_pptx(pptx_path, output_dir="."):
    """从PPTX文件中提取所有图片"""

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 创建图片输出目录
    images_dir = os.path.join(output_dir, "extracted_images")
    os.makedirs(images_dir, exist_ok=True)

    extracted_images = []
    slide_info = []

    try:
        with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
            # 列出所有文件
            file_list = zip_ref.namelist()
            print(f"PPT文件结构分析:")
            print(f"总共包含 {len(file_list)} 个文件")

            # 查找媒体文件夹中的图片
            media_files = [f for f in file_list if f.startswith('ppt/media/')]
            print(f"媒体文件夹中包含 {len(media_files)} 个文件")

            # 提取所有图片文件
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.emf', '.wmf']

            for file_path in media_files:
                file_name = os.path.basename(file_path)
                file_ext = os.path.splitext(file_name)[1].lower()

                if file_ext in image_extensions:
                    # 提取图片
                    output_path = os.path.join(images_dir, file_name)
                    with zip_ref.open(file_path) as source, open(output_path, 'wb') as target:
                        shutil.copyfileobj(source, target)

                    # 获取文件大小
                    file_size = os.path.getsize(output_path)

                    extracted_images.append({
                        'filename': file_name,
                        'path': output_path,
                        'size': file_size,
                        'extension': file_ext,
                        'original_path': file_path
                    })

                    print(f"提取图片: {file_name} ({file_size} bytes)")

            # 分析幻灯片内容
            slide_files = [f for f in file_list if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            slide_files.sort()

            print(f"\n幻灯片分析:")
            print(f"共找到 {len(slide_files)} 张幻灯片")

            for i, slide_file in enumerate(slide_files, 1):
                try:
                    with zip_ref.open(slide_file) as f:
                        content = f.read().decode('utf-8')

                    # 解析XML内容
                    root = ET.fromstring(content)

                    # 查找文本内容
                    texts = []
                    for text_elem in root.iter():
                        if text_elem.text and text_elem.text.strip():
                            texts.append(text_elem.text.strip())

                    # 查找图片引用
                    image_refs = re.findall(r'r:id="([^"]*)"', content)

                    slide_info.append({
                        'slide_number': i,
                        'file': slide_file,
                        'texts': texts,
                        'image_references': len(image_refs),
                        'has_images': len(image_refs) > 0
                    })

                except Exception as e:
                    print(f"分析幻灯片 {slide_file} 时出错: {e}")

            # 分析主题和样式
            theme_files = [f for f in file_list if 'theme' in f and f.endswith('.xml')]
            print(f"\n主题文件: {len(theme_files)} 个")

            return extracted_images, slide_info

    except Exception as e:
        print(f"处理PPT文件时出错: {e}")
        return [], []

def analyze_image_content(image_path):
    """分析图片内容（基础分析）"""
    try:
        file_size = os.path.getsize(image_path)
        file_name = os.path.basename(image_path)

        # 根据文件名和大小推测图片类型
        analysis = {
            'filename': file_name,
            'size': file_size,
            'potential_type': 'unknown'
        }

        # 基于文件名模式分析
        if 'logo' in file_name.lower() or 'icon' in file_name.lower():
            analysis['potential_type'] = 'logo/图标'
        elif 'chart' in file_name.lower() or 'graph' in file_name.lower():
            analysis['potential_type'] = '图表/数据展示'
        elif 'product' in file_name.lower() or 'screenshot' in file_name.lower():
            analysis['potential_type'] = '产品截图'
        elif 'background' in file_name.lower() or 'bg' in file_name.lower():
            analysis['potential_type'] = '背景图片'
        elif file_size > 100000:  # 大于100KB的图片
            analysis['potential_type'] = '高质量图片/照片'
        elif file_size < 10000:   # 小于10KB的图片
            analysis['potential_type'] = '小图标/装饰元素'

        return analysis

    except Exception as e:
        return {'filename': os.path.basename(image_path), 'error': str(e)}

def main():
    ppt_path = "/mnt/c/Users/Simbelmyne/desktop/company/光忆科技(1).pptx"

    print("=" * 60)
    print("PPT图片提取工具")
    print("=" * 60)

    # 提取图片
    extracted_images, slide_info = extract_images_from_pptx(ppt_path)

    if not extracted_images:
        print("未找到任何图片文件")
        return

    print(f"\n" + "=" * 60)
    print(f"图片提取结果汇总")
    print("=" * 60)

    print(f"总共提取了 {len(extracted_images)} 张图片:")

    for i, img in enumerate(extracted_images, 1):
        print(f"\n{i}. {img['filename']}")
        print(f"   文件大小: {img['size']:,} bytes")
        print(f"   文件类型: {img['extension']}")
        print(f"   保存路径: {img['path']}")

        # 分析图片内容
        analysis = analyze_image_content(img['path'])
        print(f"   推测类型: {analysis['potential_type']}")

    print(f"\n" + "=" * 60)
    print(f"幻灯片内容分析")
    print("=" * 60)

    for slide in slide_info:
        print(f"\n幻灯片 {slide['slide_number']}:")
        print(f"  包含图片: {'是' if slide['has_images'] else '否'}")
        print(f"  图片引用数: {slide['image_references']}")
        if slide['texts']:
            print(f"  主要文本内容:")
            for text in slide['texts'][:3]:  # 只显示前3个文本
                if len(text) > 50:
                    print(f"    - {text[:50]}...")
                else:
                    print(f"    - {text}")

    print(f"\n" + "=" * 60)
    print("视觉设计风格分析")
    print("=" * 60)

    # 基于提取的图片进行设计风格分析
    total_images = len(extracted_images)
    large_images = len([img for img in extracted_images if img['size'] > 100000])
    small_images = len([img for img in extracted_images if img['size'] < 10000])

    print(f"图片使用特征:")
    print(f"  - 总图片数量: {total_images}")
    print(f"  - 高质量图片: {large_images} 张 ({large_images/total_images*100:.1f}%)")
    print(f"  - 小图标/装饰: {small_images} 张 ({small_images/total_images*100:.1f}%)")

    # 文件类型分布
    ext_count = {}
    for img in extracted_images:
        ext = img['extension']
        ext_count[ext] = ext_count.get(ext, 0) + 1

    print(f"\n文件格式分布:")
    for ext, count in ext_count.items():
        print(f"  - {ext}: {count} 张")

    print(f"\n所有图片已保存到: /mnt/c/Users/Simbelmyne/desktop/company/extracted_images/")

if __name__ == "__main__":
    main()