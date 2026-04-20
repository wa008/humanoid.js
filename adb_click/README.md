# ADB 点击自动化工具集

## 📁 文件说明

### 基础脚本
- **click_center.sh** - 基础版点击脚本（无反检测）
- **click_center_smart.sh** - Shell优化版（带基础反检测）
- **click_sendevent.sh** - 触摸事件模拟版（需要root）
- **smart_click.py** - Python智能版（功能最全）

### 分析工具
- **analyze_ui.py** - UI结构分析工具
- **window_dump.xml** - UI dump数据
- **screen.png** - 屏幕截图

## 🚀 快速开始

### 1. 基础点击（无优化）
```bash
./click_center.sh
```

### 2. 优化点击（推荐）
```bash
# Shell版本
./click_center_smart.sh

# Python版本（功能最强）
python3 smart_click.py
```

### 3. 分析UI结构
```bash
python3 analyze_ui.py
```

## 🛡️ 反检测功能对比

| 功能 | click_center.sh | click_center_smart.sh | smart_click.py |
|------|----------------|----------------------|----------------|
| 基础点击 | ✅ | ✅ | ✅ |
| 随机延迟 | ❌ | ✅ | ✅ (正态分布) |
| 位置偏移 | ❌ | ✅ | ✅ (正态分布) |
| 滚动行为 | ❌ | ✅ | ✅ (可配置) |
| 微小移动 | ❌ | ❌ | ✅ |
| 模式分析 | ❌ | ❌ | ✅ |
| 历史记录 | ❌ | ❌ | ✅ |
| 彩色输出 | ❌ | ✅ | ✅ |

## 📊 风控检测点与对策

### 高危检测点（必须处理）

#### 1. 点击速度过快 ⚠️
**风险**: 机器人点击无延迟
**对策**: 
- 添加1-3秒随机延迟
- 使用正态分布模拟人类反应时间

#### 2. 点击位置过于精确 ⚠️
**风险**: 每次都点击完全相同的坐标
**对策**:
- 在±15-20像素范围内随机偏移
- 使用正态分布使偏移更自然

#### 3. 触摸事件特征缺失 ⚠️
**风险**: `input tap` 缺少压力、尺寸等参数
**对策**:
- 理想方案：使用 `sendevent` 模拟完整事件链
- 备选方案：添加微小移动模拟手指滑动

### 中危检测点（建议处理）

#### 4. 缺少浏览行为 ⚠️
**风险**: 直接点击，无滚动查看
**对策**: 点击前随机添加滚动行为

#### 5. 时间模式规律 ⚠️
**风险**: 固定时间间隔
**对策**: 使用正态分布而非均匀分布

### 低危检测点（选择性处理）

#### 6. 设备指纹检测
**风险**: 检测ADB调试状态
**对策**: 
- 使用Magisk隐藏root
- 修改build.prop

#### 7. JavaScript检测
**风险**: 网页端检测WebDriver
**对策**: 注入JS隐藏自动化特征

## 💡 最佳实践

### 推荐配置（smart_click.py）

```python
clicker.click_center_smart(
    enable_scroll=True,      # 60%概率添加滚动
    enable_micro_move=True   # 70%概率添加微移
)
```

### 多次点击示例

```python
for i in range(5):
    print(f"\n第 {i+1} 次点击:")
    clicker.click_center_smart()
    # 随机间隔 3-8 秒
    time.sleep(random.uniform(3, 8))
```

### 模式分析

```python
# 分析点击是否过于规律
clicker.analyze_click_pattern()
```

## 📈 效果对比

### 基础版（click_center.sh）
```
特征分析:
- 时间间隔: 0ms (极度可疑)
- 位置偏移: 0px (明显机器人)
- 触摸特征: 缺失
- 风控评分: 🔴 95/100 (极易被检测)
```

### 优化版（smart_click.py）
```
特征分析:
- 时间间隔: 1.2-2.5秒随机 (正常)
- 位置偏移: ±10-15px随机 (正常)
- 触摸特征: 完整
- 附加行为: 滚动、微移
- 风控评分: 🟢 15/100 (不易被检测)
```

## 🔧 自定义配置

### 调整延迟范围
```python
clicker.simulate_human_delay(min_delay=1.0, max_delay=3.0)
```

### 调整偏移范围
```python
clicker.calculate_random_offset(base_x, base_y, max_offset=30)
```

### 调整滚动概率
```python
clicker.simulate_scroll_behavior(x, y, probability=0.8)
```

## 📝 注意事项

1. **设备连接**: 确保ADB设备已连接 (`adb devices`)
2. **权限要求**: 
   - `input tap`: 无需root
   - `sendevent`: 需要root权限
3. **屏幕状态**: 确保屏幕已解锁
4. **应用场景**: 仅用于测试和研究目的

## 🔍 调试技巧

### 查看实际点击位置
```bash
# 开启显示触摸
adb shell settings put system show_touches 1

# 关闭显示触摸
adb shell settings put system show_touches 0
```

### 查看pointer位置
```bash
adb shell settings put system pointer_location 1
adb shell settings put system pointer_location 0
```

### 录制实际触摸事件
```bash
adb shell getevent -t /dev/input/event1
# 手动点击屏幕，查看事件序列
```

## 📚 进阶阅读

- [Android Input系统](https://source.android.com/devices/input)
- [ADB Shell命令](https://developer.android.com/studio/command-line/adb)
- [触摸事件反爬虫](https://github.com/topics/anti-bot)

## 🤝 贡献

欢迎提交Issue和PR！

## ⚖️ 免责声明

本工具仅供学习和测试使用，请勿用于任何违反服务条款的行为。
使用本工具导致的任何后果由使用者自行承担。
