#!/bin/bash
# 带压力和接触面积的点击脚本 - 使用 input motionevent 模拟真实触摸
# 无需root权限

# ADB路径
ADB="/Users/benson/Library/Android/sdk/platform-tools/adb"

# 获取屏幕尺寸
echo "正在获取屏幕尺寸..."
screen_size=$($ADB shell wm size | grep "Physical size" | awk '{print $3}')

if [ -z "$screen_size" ]; then
    echo "错误: 无法获取屏幕尺寸，请确保设备已连接"
    exit 1
fi

echo "屏幕尺寸: $screen_size"

# 解析宽度和高度
width=$(echo $screen_size | cut -d 'x' -f 1)
height=$(echo $screen_size | cut -d 'x' -f 2)

# 计算中心点坐标
center_x=$((width / 2))
center_y=$((height / 2))

echo "中心点坐标: ($center_x, $center_y)"

# 生成随机的压力和接触面积 (模拟真实触摸)
# 压力范围: 0.3-0.8 (归一化值，1.0为最大压力)
pressure=$(awk "BEGIN {printf \"%.2f\", 0.3 + ($RANDOM % 50) / 100}")
# 接触面积SIZE: 0.03-0.08 (归一化值)
size=$(awk "BEGIN {printf \"%.3f\", 0.03 + ($RANDOM % 50) / 1000}")
# 接触面积主轴 (像素值): 10-30
touch_major=$((10 + RANDOM % 21))
# 接触面积次轴: 略小于主轴
touch_minor=$((touch_major - 2 - RANDOM % 5))

# 确保 touch_minor 不小于0
if [ $touch_minor -lt 1 ]; then
    touch_minor=1
fi

echo "触摸参数:"
echo "  压力 (PRESSURE): $pressure"
echo "  接触面积 (SIZE): $size"
echo "  接触面积主轴 (TOUCH_MAJOR): $touch_major"
echo "  接触面积次轴 (TOUCH_MINOR): $touch_minor"
echo ""
echo "正在点击屏幕中央..."

# 使用 input motionevent 发送带压力和接触面积的触摸事件
# 按下事件 (DOWN)
$ADB shell input touchscreen motionevent DOWN $center_x $center_y \
    --axis PRESSURE,$pressure \
    --axis SIZE,$size \
    --axis TOUCH_MAJOR,$touch_major \
    --axis TOUCH_MINOR,$touch_minor

# 短暂延迟模拟真实按压时间 (50-150ms)
sleep_time=$(echo "scale=3; (50 + $RANDOM % 101) / 1000" | bc)
sleep $sleep_time

# 抬起事件 (UP)
$ADB shell input touchscreen motionevent UP $center_x $center_y

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 点击成功！"
    echo "📊 触摸事件已包含压力和接触面积信息"
else
    echo "❌ 点击失败！"
    exit 1
fi
