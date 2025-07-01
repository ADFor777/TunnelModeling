import json
import os

def create_tunnel_case_base():
    """创建隧道案例库"""
    case_base = [
        {
            "features": [1200, 3, 2, 2, 1, 10.5],
            "label": "MountainTunnelProject_A",
            "outputs": {
                "hasConstructionMethod": "DrillBlast",
                "hasBoltLength": 4.5,
                "hasBoltRowCount": 2,
                "hasBoltColumnCount": 3,
                "hasLiningThickness": 30,
                "hasSteelArchSpacing": 0.8,
                "hasSteelArchCount": 5,
                "hasSteelArchThickness": 12,
                "hasWaterproofLayerThickness": 5
            }
        },
        {
            "features": [800, 2, 1, 1, 2, 9.0],
            "label": "UnderwaterTunnelProject_B",
            "outputs": {
                "hasConstructionMethod": "TBM",
                "hasBoltLength": 3.5,
                "hasBoltRowCount": 1,
                "hasBoltColumnCount": 2,
                "hasLiningThickness": 25,
                "hasSteelArchSpacing": 1.2,
                "hasSteelArchCount": 3,
                "hasSteelArchThickness": 10,
                "hasWaterproofLayerThickness": 8
            }
        },
        {
            "features": [2500, 4, 3, 3, 1, 12.0],
            "label": "MountainTunnelProject_C",
            "outputs": {
                "hasConstructionMethod": "NATM",
                "hasBoltLength": 5.0,
                "hasBoltRowCount": 3,
                "hasBoltColumnCount": 4,
                "hasLiningThickness": 35,
                "hasSteelArchSpacing": 0.6,
                "hasSteelArchCount": 6,
                "hasSteelArchThickness": 15,
                "hasWaterproofLayerThickness": 6
            }
        },
        {
            "features": [600, 1, 1, 1, 3, 8.5],
            "label": "ShallowTunnelProject_D",
            "outputs": {
                "hasConstructionMethod": "CutCover",
                "hasBoltLength": 3.0,
                "hasBoltRowCount": 1,
                "hasBoltColumnCount": 2,
                "hasLiningThickness": 20,
                "hasSteelArchSpacing": 1.5,
                "hasSteelArchCount": 2,
                "hasSteelArchThickness": 8,
                "hasWaterproofLayerThickness": 4
            }
        },
        {
            "features": [3500, 2, 2, 4, 4, 15.0],
            "label": "DeepTunnelProject_E",
            "outputs": {
                "hasConstructionMethod": "TBM",
                "hasBoltLength": 6.0,
                "hasBoltRowCount": 4,
                "hasBoltColumnCount": 5,
                "hasLiningThickness": 40,
                "hasSteelArchSpacing": 0.5,
                "hasSteelArchCount": 8,
                "hasSteelArchThickness": 18,
                "hasWaterproofLayerThickness": 10
            }
        },
        {
            "features": [1500, 5, 4, 5, 1, 11.0],
            "label": "MountainTunnelProject_F",
            "outputs": {
                "hasConstructionMethod": "StepMethod",
                "hasBoltLength": 5.5,
                "hasBoltRowCount": 3,
                "hasBoltColumnCount": 4,
                "hasLiningThickness": 38,
                "hasSteelArchSpacing": 0.7,
                "hasSteelArchCount": 7,
                "hasSteelArchThickness": 16,
                "hasWaterproofLayerThickness": 8
            }
        }
    ]
    
    return case_base

def main():
    """创建隧道案例库JSON文件"""
    print("🚇 隧道案例库生成器")
    print("=" * 40)
    
    # 创建案例库
    case_base = create_tunnel_case_base()
    
    # 保存到JSON文件
    json_file = "tunnel_case_base.json"
    
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(case_base, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 成功创建案例库文件: {json_file}")
        print(f"📊 包含 {len(case_base)} 个隧道工程案例")
        
        # 显示特征编码说明
        print(f"\n📋 特征编码说明:")
        print(f"1. 隧道长度 (m): 实际数值")
        print(f"2. 地质条件: 1=优, 2=良, 3=中, 4=差, 5=极差")
        print(f"3. 水文条件: 1=干燥, 2=微湿, 3=潮湿, 4=滴水, 5=涌水")
        print(f"4. 土壤类型: 1=岩石, 2=砂土, 3=粘土, 4=软土, 5=特殊土")
        print(f"5. 隧道类型: 1=山岭, 2=水下, 3=浅埋, 4=深埋")
        print(f"6. 隧道直径 (m): 实际数值")
        
        # 显示案例预览
        print(f"\n📄 案例预览:")
        for i, case in enumerate(case_base):
            print(f"  {i+1}. {case['label']}: {case['features']}")
            
    except Exception as e:
        print(f"❌ 创建案例库文件失败: {e}")

if __name__ == "__main__":
    main()