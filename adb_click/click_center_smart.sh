#!/bin/bash
# 优化版点击脚本 - 加入反风控检测机制 + 压力和接触面积

ADB="/Users/benson/Library/Android/sdk/platform-tools/adb"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🤖 智能点击脚本 v3.0 (反检测版+触摸真实性)${NC}"
echo -e "${BLUE}========================================${NC}"

# 获取屏幕尺寸
echo -e "\n${YELLOW}[1/6]${NC} 正在获取屏幕尺寸..."
screen_size=$($ADB shell wm size | grep "Physical size" | awk '{print $3}')

if [ -z "$screen_size" ]; then
    echo -e "${RED}❌ 错误: 无法获取屏幕尺寸，请确保设备已连接${NC}"
    exit 1
fi

width=$(echo $screen_size | cut -d 'x' -f 1)
height=$(echo $screen_size | cut -d 'x' -f 2)
echo -e "${GREEN}✓${NC} 屏幕尺寸: ${width}x${height}"

# 计算中心点基准坐标
base_center_x=$((width / 2))
base_center_y=$((height / 2))

# 1. 添加随机延迟 (模拟人类思考时间)
echo -e "\n${YELLOW}[2/6]${NC} 模拟人类思考延迟..."
# 生成 1.0 到 2.5 秒之间的随机延迟
delay=$(awk "BEGIN {printf \"%.2f\", 1.0 + ($RANDOM % 150) / 100}")
echo -e "${GREEN}✓${NC} 等待 ${delay} 秒..."
sleep $delay

# 2. 添加随机位置偏移 (避免点击完全相同的位置)
echo -e "\n${YELLOW}[3/6]${NC} 计算随机偏移量..."
# 生成 -15 到 +15 像素的随机偏移
offset_x=$((RANDOM % 31 - 15))
offset_y=$((RANDOM % 31 - 15))

actual_x=$((base_center_x + offset_x))
actual_y=$((base_center_y + offset_y))

echo -e "${GREEN}✓${NC} 基准坐标: (${base_center_x}, ${base_center_y})"
echo -e "${GREEN}✓${NC} 偏移量: (${offset_x}, ${offset_y})"
echo -e "${GREEN}✓${NC} 实际点击: (${actual_x}, ${actual_y})"

# 3. 生成随机的压力和接触面积
echo -e "\n${YELLOW}[4/6]${NC} 生成触摸参数..."
# 压力范围: 0.3-0.8 (归一化值)
pressure=$(awk "BEGIN {printf \"%.2f\", 0.3 + ($RANDOM % 50) / 100}")
# 接触面积SIZE: 0.03-0.08 (归一化值)
size=$(awk "BEGIN {printf \"%.3f\", 0.03 + ($RANDOM % 50) / 1000}")
# 接触面积主轴: 10-30
touch_major=$((10 + RANDOM % 21))
# 接触面积次轴: 略小于主轴
touch_minor=$((touch_major - 2 - RANDOM % 5))
if [ $touch_minor -lt 1 ]; then touch_minor=1; fi

echo -e "${GREEN}✓${NC} 压力: ${pressure}"
echo -e "${GREEN}✓${NC} 接触面积: ${size} (主轴:${touch_major}, 次轴:${touch_minor})"

# 4. 可选：添加滚动行为 (模拟浏览)
echo -e "\n${YELLOW}[5/6]${NC} 模拟浏览行为..."
# 随机决定是否添加滚动 (50%概率)
if [ $((RANDOM % 2)) -eq 0 ]; then
    scroll_distance=$((50 + RANDOM % 100))
    echo -e "${GREEN}✓${NC} 轻微向上滚动 ${scroll_distance}px..."
    $ADB shell input swipe $actual_x $actual_y $actual_x $((actual_y - scroll_distance)) 300
    sleep 0.3
else
    echo -e "${GREEN}✓${NC} 跳过滚动（随机决策）"
fi

# 5. 执行点击操作 (使用 motionevent 发送完整触摸事件)
echo -e "\n${YELLOW}[6/6]${NC} 执行点击操作..."

# 按下事件
$ADB shell input touchscreen motionevent DOWN $actual_x $actual_y \
    --axis PRESSURE,$pressure \
    --axis SIZE,$size \
    --axis TOUCH_MAJOR,$touch_major \
    --axis TOUCH_MINOR,$touch_minor

# 随机按压时长 (50-150ms)
press_duration=$(awk "BEGIN {printf \"%.3f\", (50 + $RANDOM % 101) / 1000}")
sleep $press_duration

# 抬起事件
$ADB shell input touchscreen motionevent UP $actual_x $actual_y

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ 点击成功！${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "📊 操作总结:"
    echo -e "  • 思考延迟: ${delay}s"
    echo -e "  • 位置随机化: (${offset_x}, ${offset_y})"
    echo -e "  • 最终坐标: (${actual_x}, ${actual_y})"
    echo -e "  • 压力: ${pressure}"
    echo -e "  • 接触面积: SIZE=${size}, MAJOR=${touch_major}, MINOR=${touch_minor}"
    echo -e "  • 按压时长: ${press_duration}s"
    echo -e "${BLUE}========================================${NC}"
else
    echo -e "${RED}❌ 点击失败！${NC}"
    exit 1
fi
