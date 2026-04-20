#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级点击脚本 - Python版本
支持多种反检测技术
"""
import subprocess
import time
import random
import json
from datetime import datetime

ADB_PATH = "/Users/benson/Library/Android/sdk/platform-tools/adb"

class SmartClicker:
    def __init__(self):
        self.adb = ADB_PATH
        self.width = 0
        self.height = 0
        self.click_history = []
        
    def log(self, emoji, message, color=""):
        """彩色日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {emoji} {message}")
    
    def run_adb_command(self, command):
        """执行ADB命令"""
        full_command = f"{self.adb} {command}"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    
    def get_screen_size(self):
        """获取屏幕尺寸"""
        self.log("📱", "获取屏幕尺寸...")
        output = self.run_adb_command("shell wm size")
        
        for line in output.split('\n'):
            if "Physical size" in line:
                size_str = line.split(':')[1].strip()
                self.width, self.height = map(int, size_str.split('x'))
                self.log("✅", f"屏幕尺寸: {self.width}x{self.height}")
                return True
        
        self.log("❌", "无法获取屏幕尺寸")
        return False
    
    def simulate_human_delay(self, min_delay=0.5, max_delay=2.5):
        """模拟人类反应延迟（正态分布）"""
        # 使用正态分布，更接近人类行为
        mean = (min_delay + max_delay) / 2
        std_dev = (max_delay - min_delay) / 4
        delay = random.gauss(mean, std_dev)
        delay = max(min_delay, min(max_delay, delay))  # 限制范围
        
        self.log("⏳", f"模拟思考延迟: {delay:.2f}秒")
        time.sleep(delay)
        return delay
    
    def calculate_random_offset(self, base_x, base_y, max_offset=20):
        """计算随机偏移（避免固定位置）"""
        # 使用正态分布生成偏移
        offset_x = int(random.gauss(0, max_offset / 2))
        offset_y = int(random.gauss(0, max_offset / 2))
        
        # 限制偏移范围
        offset_x = max(-max_offset, min(max_offset, offset_x))
        offset_y = max(-max_offset, min(max_offset, offset_y))
        
        actual_x = base_x + offset_x
        actual_y = base_y + offset_y
        
        # 确保在屏幕范围内
        actual_x = max(10, min(self.width - 10, actual_x))
        actual_y = max(10, min(self.height - 10, actual_y))
        
        self.log("🎯", f"位置偏移: ({offset_x:+d}, {offset_y:+d})")
        return actual_x, actual_y
    
    def simulate_scroll_behavior(self, x, y, probability=0.6):
        """随机模拟滚动行为"""
        if random.random() < probability:
            # 随机选择滚动方向和距离
            scroll_distance = random.randint(100, 300)
            direction = random.choice(['up', 'down'])
            
            if direction == 'up':
                end_y = y - scroll_distance
                self.log("👆", f"模拟向上滚动 {scroll_distance}px")
            else:
                end_y = y + scroll_distance
                self.log("👇", f"模拟向下滚动 {scroll_distance}px")
            
            # 滚动速度也随机化
            duration = random.randint(200, 500)
            self.run_adb_command(f"shell input swipe {x} {y} {x} {end_y} {duration}")
            time.sleep(random.uniform(0.2, 0.5))
            return True
        else:
            self.log("⏭️", "跳过滚动行为")
            return False
    
    def simulate_micro_movements(self, x, y):
        """模拟手指微小移动（更真实）"""
        # 70%概率添加微小的手指移动
        if random.random() < 0.7:
            # 生成一个小的曲线移动
            start_x = x + random.randint(-5, 5)
            start_y = y + random.randint(-5, 5)
            
            self.log("🤏", "添加微小手指移动")
            self.run_adb_command(f"shell input swipe {start_x} {start_y} {x} {y} 50")
            time.sleep(0.05)
    
    def perform_click(self, x, y):
        """执行点击"""
        self.log("👆", f"点击位置: ({x}, {y})")
        result = self.run_adb_command(f"shell input tap {x} {y}")
        return result
    
    def click_center_smart(self, enable_scroll=True, enable_micro_move=True):
        """智能点击屏幕中心"""
        self.log("🚀", "开始智能点击流程")
        print("=" * 50)
        
        # 1. 获取屏幕尺寸
        if not self.get_screen_size():
            return False
        
        # 2. 计算中心点
        base_x = self.width // 2
        base_y = self.height // 2
        self.log("📍", f"屏幕中心: ({base_x}, {base_y})")
        
        # 3. 人类延迟
        delay = self.simulate_human_delay()
        
        # 4. 计算随机偏移
        actual_x, actual_y = self.calculate_random_offset(base_x, base_y)
        
        # 5. 可选：模拟滚动
        if enable_scroll:
            self.simulate_scroll_behavior(actual_x, actual_y)
        
        # 6. 可选：微小移动
        if enable_micro_move:
            self.simulate_micro_movements(actual_x, actual_y)
        
        # 7. 执行点击
        self.perform_click(actual_x, actual_y)
        
        # 8. 记录历史
        click_record = {
            'timestamp': datetime.now().isoformat(),
            'position': (actual_x, actual_y),
            'delay': delay,
            'had_scroll': enable_scroll,
            'had_micro_move': enable_micro_move
        }
        self.click_history.append(click_record)
        
        # 9. 输出总结
        print("=" * 50)
        self.log("✅", "点击完成")
        print(f"\n📊 操作统计:")
        print(f"  • 思考延迟: {delay:.2f}秒")
        print(f"  • 位置偏移: ({actual_x - base_x:+d}, {actual_y - base_y:+d})")
        print(f"  • 滚动行为: {'是' if enable_scroll else '否'}")
        print(f"  • 微小移动: {'是' if enable_micro_move else '否'}")
        print(f"  • 历史点击次数: {len(self.click_history)}")
        print("=" * 50)
        
        return True
    
    def analyze_click_pattern(self):
        """分析点击模式（检测是否过于规律）"""
        if len(self.click_history) < 2:
            return
        
        print("\n🔍 点击模式分析:")
        print("=" * 50)
        
        # 分析时间间隔
        delays = [record['delay'] for record in self.click_history]
        avg_delay = sum(delays) / len(delays)
        print(f"平均延迟: {avg_delay:.2f}秒")
        
        # 分析位置分布
        positions = [record['position'] for record in self.click_history]
        x_coords = [pos[0] for pos in positions]
        y_coords = [pos[1] for pos in positions]
        
        x_variance = sum((x - sum(x_coords)/len(x_coords))**2 for x in x_coords) / len(x_coords)
        y_variance = sum((y - sum(y_coords)/len(y_coords))**2 for y in y_coords) / len(y_coords)
        
        print(f"X轴方差: {x_variance:.2f} (越大越随机)")
        print(f"Y轴方差: {y_variance:.2f}")
        
        if x_variance < 10 or y_variance < 10:
            print("⚠️  警告: 点击位置过于集中，建议增加随机性")
        else:
            print("✅ 点击位置分布良好")
        
        print("=" * 50)

def main():
    clicker = SmartClicker()
    
    # 执行智能点击
    clicker.click_center_smart(
        enable_scroll=True,      # 启用滚动模拟
        enable_micro_move=True   # 启用微小移动
    )
    
    # 如果需要多次点击，可以循环
    # for i in range(3):
    #     print(f"\n第 {i+1} 次点击:")
    #     clicker.click_center_smart()
    #     time.sleep(random.uniform(2, 5))
    
    # 分析点击模式
    # clicker.analyze_click_pattern()

if __name__ == "__main__":
    main()
