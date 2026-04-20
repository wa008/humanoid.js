#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Dump分析工具 - 提取网页风控相关信息
"""
import xml.etree.ElementTree as ET
import re

def analyze_ui_dump(xml_file):
    """分析UI Dump文件"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        print("=" * 60)
        print("📱 UI结构分析")
        print("=" * 60)
        
        # 查找所有包含文本的节点
        all_texts = []
        all_content_desc = []
        
        for node in root.iter('node'):
            text = node.get('text', '')
            content_desc = node.get('content-desc', '')
            resource_id = node.get('resource-id', '')
            class_name = node.get('class', '')
            bounds = node.get('bounds', '')
            
            if text:
                all_texts.append({
                    'text': text,
                    'resource_id': resource_id,
                    'class': class_name,
                    'bounds': bounds
                })
            
            if content_desc:
                all_content_desc.append({
                    'desc': content_desc,
                    'resource_id': resource_id,
                    'class': class_name,
                    'bounds': bounds
                })
        
        # 显示找到的文本
        print("\n📝 页面文本内容:")
        if all_texts:
            for item in all_texts:
                print(f"  • {item['text']}")
                print(f"    位置: {item['bounds']}, 类型: {item['class']}")
        else:
            print("  ⚠️  未找到文本内容（可能在WebView中）")
        
        print("\n🔍 Content Description:")
        if all_content_desc:
            for item in all_content_desc[:10]:  # 只显示前10个
                print(f"  • {item['desc']}")
        
        # 风控关键词检测
        risk_keywords = [
            '风险', '检测', 'risk', 'detect', 'bot', 'captcha',
            '验证', 'verify', '人机', '异常', 'suspicious', 'blocked'
        ]
        
        print("\n🚨 风控关键词检测:")
        found_risks = []
        for item in all_texts + all_content_desc:
            content = item.get('text', '') or item.get('desc', '')
            for keyword in risk_keywords:
                if keyword.lower() in content.lower():
                    found_risks.append(f"{keyword}: {content}")
        
        if found_risks:
            for risk in found_risks:
                print(f"  ⚠️  {risk}")
        else:
            print("  ✅ 未发现明显风控关键词")
        
        # 分析WebView
        webviews = [node for node in root.iter('node') 
                   if 'WebView' in node.get('content-desc', '') or
                      'web' in node.get('class', '').lower()]
        
        print(f"\n🌐 WebView数量: {len(webviews)}")
        
        # URL信息
        url_nodes = [node for node in root.iter('node')
                    if 'url' in node.get('resource-id', '').lower()]
        if url_nodes:
            print("\n🔗 当前URL:")
            for node in url_nodes:
                url_text = node.get('text', '')
                if url_text:
                    print(f"  {url_text}")
        
        return all_texts, all_content_desc
        
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        return [], []

def print_anti_detection_tips():
    """打印反检测建议"""
    print("\n" + "=" * 60)
    print("🛡️  风控检测机制分析与对策")
    print("=" * 60)
    
    tips = [
        {
            "检测点": "1. 点击速度过快",
            "风险": "机器人点击通常是瞬时完成，没有人类的反应时间",
            "对策": "• 点击前添加随机延迟 (0.5-2秒)\n"
                   "         • 模拟人类思考时间"
        },
        {
            "检测点": "2. 点击位置过于精确",
            "风险": "正中心点击是典型机器人行为，人类点击会有偏移",
            "对策": "• 在目标区域内随机偏移 (±5-20像素)\n"
                   "         • 避免每次都点击完全相同的坐标"
        },
        {
            "检测点": "3. 触摸事件特征",
            "风险": "input tap生成的事件缺少压力、尺寸等真实触摸数据",
            "对策": "• 使用 sendevent 模拟完整触摸序列\n"
                   "         • 包含 DOWN -> MOVE -> UP 事件\n"
                   "         • 添加触摸压力和接触面积参数"
        },
        {
            "检测点": "4. 时间模式规律性",
            "风险": "固定时间间隔的操作容易被识别",
            "对策": "• 使用正态分布的随机间隔\n"
                   "         • 偶尔加入长时间停顿"
        },
        {
            "检测点": "5. 缺少滑动/滚动行为",
            "风险": "正常用户会有浏览、滚动等行为",
            "对策": "• 点击前先模拟滚动查看内容\n"
                   "         • 添加一些无意义的小幅移动"
        },
        {
            "检测点": "6. 设备指纹检测",
            "风险": "检测ADB调试状态、开发者选项、root状态",
            "对策": "• 使用 Magisk 隐藏 root\n"
                   "         • 修改 build.prop 隐藏模拟器特征\n"
                   "         • 使用真实设备而非模拟器"
        },
        {
            "检测点": "7. 传感器数据缺失",
            "风险": "真实用户设备会有陀螺仪、加速度计数据",
            "对策": "• 模拟设备晃动时的传感器数据变化"
        },
        {
            "检测点": "8. JavaScript检测",
            "风险": "网页端检测 WebDriver、自动化标识",
            "对策": "• 注入JS脚本隐藏自动化特征\n"
                   "         • 修改 navigator.webdriver 属性"
        }
    ]
    
    for tip in tips:
        print(f"\n{tip['检测点']}")
        print(f"  ⚠️  风险: {tip['风险']}")
        print(f"  ✅ 对策: {tip['对策']}")
    
    print("\n" + "=" * 60)
    print("💡 优先级建议:")
    print("=" * 60)
    print("  🔥 高优先级: 随机延迟、位置偏移、触摸事件模拟")
    print("  🔸 中优先级: 添加浏览行为、时间模式随机化")
    print("  🔹 低优先级: 设备指纹处理、传感器模拟")

if __name__ == "__main__":
    xml_file = "/Users/benson/code/automation-dev/adb_click/window_dump.xml"
    analyze_ui_dump(xml_file)
    print_anti_detection_tips()
