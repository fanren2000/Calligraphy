

import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

def get_dominant_color(image_path, k=3, background_threshold=0.3):
    """
    获取图像的主背景颜色
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("无法读取图像")
    
    # 转换为RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_shape = image_rgb.shape
    
    # 将图像展平为像素列表
    pixels = image.reshape(-1, 3)
    
    # 使用K-means聚类找到主要颜色
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # 获取聚类中心和标签
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    
    # 统计每个聚类的像素数量
    label_counts = Counter(labels)
    
    # 找到最大聚类（最可能是背景）
    dominant_label = label_counts.most_common(1)[0][0]
    dominant_color = colors[dominant_label]
    
    return dominant_color, colors, label_counts, image_shape

def visualize_colors(colors_bgr, label_counts, image_shape):
    """可视化检测到的颜色"""
    total_pixels = sum(label_counts.values())
    
    fig, axes = plt.subplots(1, len(colors_bgr) + 1, figsize=(15, 3))

    # 将BGR转换为RGB
    colors_rgb = [color_bgr[::-1] for color_bgr in colors_bgr]
    
    # 显示颜色块
    for i, (color, count) in enumerate(zip(colors_rgb, label_counts.values())):
        color_block = np.ones((100, 100, 3), dtype=np.uint8) * color
        axes[i].imshow(color_block)
        axes[i].axis('off')
        percentage = count / total_pixels * 100
        axes[i].set_title(f'Cluster {i}\n{color}\n{percentage:.1f}%')
    
    # 最后一个显示所有颜色
    all_colors = np.zeros((100, 300, 3), dtype=np.uint8)
    for i, color in enumerate(colors_rgb):
        all_colors[:, i*100:(i+1)*100] = color
    axes[-1].imshow(all_colors)
    axes[-1].axis('off')
    axes[-1].set_title('All Colors')
    
    plt.tight_layout()
    plt.show()

# 使用示例
image_path = "Frames/calligraphy_work_torn_edge.png"
dominant_color, all_colors, label_counts, image_shape = get_dominant_color(image_path, k=3)

print("主背景颜色 (RGB):", dominant_color)
print("所有主要颜色:", all_colors)
print("各颜色占比:", dict(label_counts))

print("\n📈 正在生成可视化结果...")
visualize_colors(all_colors, label_counts, image_shape)