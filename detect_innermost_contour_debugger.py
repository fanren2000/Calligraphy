

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

class ScrollBorderDebugger:
    """交互式卷轴边界调试器"""
    
    def __init__(self, image_path):
        self.image_path = image_path
        self.img = cv2.imread(image_path)
        if self.img is None:
            raise ValueError(f"无法读取图像: {image_path}")
        
        self.height, self.width = self.img.shape[:2]
        self.rgba = cv2.cvtColor(self.img, cv2.COLOR_BGR2BGRA)
        
        # 初始化边界参数
        self.top_margin = 0.10
        self.bottom_margin = 0.10
        self.left_margin = 0.10
        self.right_margin = 0.10
        
        self.setup_ui()
    
    def create_mask(self):
        """根据当前边界参数创建掩码"""
        mask = np.zeros((self.height, self.width), dtype=np.uint8)
        
        top = int(self.height * self.top_margin)
        bottom = int(self.height * (1 - self.bottom_margin))
        left = int(self.width * self.left_margin)
        right = int(self.width * (1 - self.right_margin))
        
        # 确保边界有效
        top = max(0, top)
        bottom = min(self.height, bottom)
        left = max(0, left)
        right = min(self.width, right)
        
        mask[top:bottom, left:right] = 255
        
        return mask, (top, bottom, left, right)
    
    def update_image(self, val=None):
        """更新显示的图像"""
        mask, (top, bottom, left, right) = self.create_mask()
        
        # 创建带标记的图像
        marked_img = self.img.copy()
        cv2.rectangle(marked_img, (left, top), (right, bottom), (0, 255, 0), 3)
        
        # 应用透明度
        result = self.rgba.copy()
        result[:, :, 3] = mask
        
        # 更新子图
        self.ax1.clear()
        self.ax1.imshow(cv2.cvtColor(marked_img, cv2.COLOR_BGR2RGB))
        self.ax1.set_title(f'边界标记\n上:{top}, 下:{bottom}, 左:{left}, 右:{right}')
        self.ax1.axis('off')
        
        self.ax2.clear()
        self.ax2.imshow(mask, cmap='gray')
        self.ax2.set_title(f'透明度掩码\n不透明区域: {((bottom-top)*(right-left))/(self.height*self.width):.1%}')
        self.ax2.axis('off')
        
        self.ax3.clear()
        self.ax3.imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
        self.ax3.set_title('透明模板效果')
        self.ax3.axis('off')
        
        plt.draw()
    
    def setup_ui(self):
        """设置用户界面"""
        fig = plt.figure(figsize=(15, 10))
        
        # 创建子图
        self.ax1 = plt.subplot(2, 3, (1, 2))
        self.ax2 = plt.subplot(2, 3, 3)
        self.ax3 = plt.subplot(2, 3, (4, 6))
        
        # 创建滑块区域
        slider_ax = plt.axes([0.1, 0.05, 0.8, 0.03])
        self.top_slider = Slider(slider_ax, '上边界', 0.0, 0.5, valinit=self.top_margin)
        
        slider_ax2 = plt.axes([0.1, 0.01, 0.8, 0.03])
        self.bottom_slider = Slider(slider_ax2, '下边界', 0.0, 0.5, valinit=self.bottom_margin)
        
        slider_ax3 = plt.axes([0.1, 0.09, 0.8, 0.03])
        self.left_slider = Slider(slider_ax3, '左边界', 0.0, 0.5, valinit=self.left_margin)
        
        slider_ax4 = plt.axes([0.1, 0.13, 0.8, 0.03])
        self.right_slider = Slider(slider_ax4, '右边界', 0.0, 0.5, valinit=self.right_margin)
        
        # 添加按钮
        button_ax = plt.axes([0.8, 0.15, 0.1, 0.04])
        self.save_button = Button(button_ax, '保存模板')
        
        button_ax2 = plt.axes([0.8, 0.20, 0.1, 0.04])
        self.auto_button = Button(button_ax2, '自动检测')
        
        # 连接事件
        self.top_slider.on_changed(self.on_slider_change)
        self.bottom_slider.on_changed(self.on_slider_change)
        self.left_slider.on_changed(self.on_slider_change)
        self.right_slider.on_changed(self.on_slider_change)
        self.save_button.on_clicked(self.save_template)
        self.auto_button.on_clicked(self.auto_detect)
        
        # 初始显示
        self.update_image()
        
        plt.suptitle('卷轴边界调试器 - 拖动滑块调整边界', fontsize=14, y=0.95)
        plt.tight_layout()
        plt.show()
    
    def on_slider_change(self, val):
        """滑块变化时的回调"""
        self.top_margin = self.top_slider.val
        self.bottom_margin = self.bottom_slider.val
        self.left_margin = self.left_slider.val
        self.right_margin = self.right_slider.val
        self.update_image()
    
    def save_template(self, event):
        """保存模板"""
        mask, _ = self.create_mask()
        result = self.rgba.copy()
        result[:, :, 3] = mask
        
        output_path = "scroll_template_adjusted.png"
        cv2.imwrite(output_path, result)
        print(f"✅ 模板已保存: {output_path}")
        
        # 显示保存的边界参数
        _, (top, bottom, left, right) = self.create_mask()
        print(f"📐 边界参数:")
        print(f"   上边界: {top} ({self.top_margin:.1%})")
        print(f"   下边界: {self.height-bottom} ({self.bottom_margin:.1%})")
        print(f"   左边界: {left} ({self.left_margin:.1%})")
        print(f"   右边界: {self.width-right} ({self.right_margin:.1%})")
    
    def auto_detect(self, event):
        """尝试自动检测边界"""
        print("🔍 尝试自动检测边界...")
        
        # 使用边缘检测
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # 寻找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # 找到最大轮廓
            largest = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest)
            
            # 转换为百分比
            self.top_margin = y / self.height
            self.bottom_margin = (self.height - (y + h)) / self.height
            self.left_margin = x / self.width
            self.right_margin = (self.width - (x + w)) / self.width
            
            # 更新滑块
            self.top_slider.set_val(self.top_margin)
            self.bottom_slider.set_val(self.bottom_margin)
            self.left_slider.set_val(self.left_margin)
            self.right_slider.set_val(self.right_margin)
            
            print(f"✅ 自动检测完成:")
            print(f"   检测到矩形: x={x}, y={y}, w={w}, h={h}")
        else:
            print("❌ 未检测到明显边界")

# 运行调试器
debugger = ScrollBorderDebugger("Source/scroll_horizontal_green_black.png")