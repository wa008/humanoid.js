#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风控检测对比测试
对比基础版和优化版的点击特征
"""
import subprocess
import time
import statistics

ADB_PATH = "/Users/benson/Library/Android/sdk/platform-tools/adb"

def analyze_click_characteristics(name, delays, positions):
    """分析点击特征"""
    print(f"\n{'='*60}")
    print(f"📊 {name} - 特征分析")
    print(f"{'='*60}")
    
    # 时间特征
    if len(delays) > 1:
        avg_delay = statistics.mean(delays)
        std_delay = statistics.stdev(delays) if len(delays) > 1 else 0
        print(f"\n⏱️  时间特征:")
        print(f"  • 平均间隔: {avg_delay:.3f}秒")
        print(f"  • 标准差: {std_delay:.3f}秒")
        if std_delay < 0.1:
            print(f"  ⚠️  警告: 时间间隔过于规律！")
            risk_time = 80
        else:
            print(f"  ✅ 时间随机性良好")
            risk_time = 20
    else:
        risk_time = 50
    
    # 位置特征
    if len(positions) > 1:
        x_coords = [p[0] for p in positions]
        y_coords = [p[1] for p in positions]
        
        x_std = statistics.stdev(x_coords) if len(x_coords) > 1 else 0
        y_std = statistics.stdev(y_coords) if len(y_coords) > 1 else 0
        
        print(f"\n📍 位置特征:")
        print(f"  • X轴标准差: {x_std:.2f}px")
        print(f"  • Y轴标准差: {y_std:.2f}px")
        
        if x_std < 5 and y_std < 5:
            print(f"  ⚠️  警告: 点击位置几乎完全相同！")
            risk_position = 90
        elif x_std < 10 and y_std < 10:
            print(f"  ⚠️  警告: 点击位置偏移过小")
            risk_position = 60
        else:
            print(f"  ✅ 位置随机性良好")
            risk_position = 15
    else:
        risk_position = 50
    
    # 总体风险评分
    risk_score = (risk_time + risk_position) / 2
    
    print(f"\n🎯 风控风险评分: {risk_score:.1f}/100")
    if risk_score > 70:
        print(f"  🔴 极高风险 - 几乎必然被检测")
    elif risk_score > 50:
        print(f"  🟠 高风险 - 很可能被检测")
    elif risk_score > 30:
        print(f"  🟡 中等风险 - 可能被检测")
    else:
        print(f"  🟢 低风险 - 不易被检测")
    
    return risk_score

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║           ADB点击 - 风控检测特征对比测试                    ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("\n本测试将演示基础版和优化版的特征差异")
    print("（不会实际执行点击，仅展示特征对比）\n")
    
    # 模拟基础版特征
    print("🔴 基础版 (click_center.sh) 特征模拟:")
    basic_delays = [0.001, 0.001, 0.001, 0.001, 0.001]  # 几乎无延迟
    basic_positions = [(540, 1200), (540, 1200), (540, 1200), (540, 1200), (540, 1200)]  # 完全相同
    
    basic_risk = analyze_click_characteristics("基础版", basic_delays, basic_positions)
    
    # 模拟优化版特征
    print("\n" + "="*60)
    time.sleep(1)
    
    print("\n🟢 优化版 (smart_click.py) 特征模拟:")
    smart_delays = [1.23, 1.87, 2.34, 1.56, 2.01]  # 随机延迟
    smart_positions = [
        (534, 1197),
        (547, 1205),
        (538, 1193),
        (543, 1208),
        (536, 1196)
    ]  # 随机偏移
    
    smart_risk = analyze_click_characteristics("优化版", smart_delays, smart_positions)
    
    # 对比总结
    print("\n" + "="*60)
    print("📈 对比总结")
    print("="*60)
    
    print(f"\n基础版风险: {basic_risk:.1f}/100 🔴")
    print(f"优化版风险: {smart_risk:.1f}/100 🟢")
    print(f"风险降低: {basic_risk - smart_risk:.1f}分")
    print(f"改善幅度: {((basic_risk - smart_risk) / basic_risk * 100):.1f}%")
    
    print("\n" + "="*60)
    print("💡 关键改进点:")
    print("="*60)
    print("""
1. ✅ 添加随机延迟（1-3秒）
   → 模拟人类思考时间
   
2. ✅ 位置随机偏移（±10-20px）
   → 避免固定坐标点击
   
3. ✅ 使用正态分布
   → 更接近真实人类行为
   
4. ✅ 添加辅助行为
   → 滚动、微小移动等
   
5. ✅ 避免时间规律
   → 不使用固定间隔
    """)
    
    print("\n推荐使用: python3 smart_click.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
