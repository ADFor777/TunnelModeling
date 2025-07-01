# ==========================================
# tunnel_case_base_generator.py
# 生成隧道案例库JSON文件
# ==========================================

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

# ==========================================
# cbr_system.py (改进版)
# ==========================================

import numpy as np

class CBRSystem:
    def __init__(self, case_base, feature_weights, threshold=0.85):
        self.case_base = case_base
        self.feature_weights = np.array(feature_weights, dtype=float)
        self.threshold = threshold
        self.feature_mins, self.feature_maxs = self.compute_feature_ranges()
        
        # 特征名称映射
        self.feature_names = [
            "hasTunnelLength", "hasGeologicalCondition", "hasHydroCondition",
            "hasSoilType", "TunnelType", "hasTunnelDiameter"
        ]

    def compute_feature_ranges(self):
        """计算特征的最小值和最大值用于归一化"""
        if not self.case_base:
            return np.array([]), np.array([])
            
        all_features = np.array([case["features"] for case in self.case_base])
        feature_mins = all_features.min(axis=0)
        feature_maxs = all_features.max(axis=0)
        return feature_mins, feature_maxs

    def normalize(self, features):
        """归一化特征值到[0,1]范围"""
        features = np.array(features, dtype=float)
        denom = self.feature_maxs - self.feature_mins
        # 避免除零错误
        denom = np.where(denom == 0, 1, denom)
        return (features - self.feature_mins) / denom

    def calculate_similarity(self, target_features, case_features):
        """使用欧式距离计算相似度"""
        norm_target = self.normalize(target_features)
        norm_case = self.normalize(case_features)
        diff = norm_target - norm_case
        
        # 加权欧式距离
        weighted_squared = self.feature_weights * diff ** 2
        distance = np.sqrt(weighted_squared.sum())
        
        # 转换为相似度（距离越小，相似度越高）
        similarity = 1 / (1 + distance)
        return similarity

    def retrieve(self, target_case):
        """检索最相似的案例"""
        similarities = []
        target_features = target_case['features']
        
        print(f"\n🔍 开始检索，目标特征: {target_features}")
        print(f"📏 特征权重: {self.feature_weights}")
        
        for i, case in enumerate(self.case_base):
            sim = self.calculate_similarity(target_features, case['features'])
            similarities.append((case, sim))
            print(f"  案例{i+1} 【{case['label']}】: 相似度 {sim:.3f}")
        
        # 按相似度降序排列
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities

    def adapt_case(self, source_case, target_case):
        """案例适应"""
        print(f"\n✅ 采用案例【{source_case['label']}】的参数作为推荐方案")
        print(f"📋 原案例特征: {source_case['features']}")
        print(f"🎯 目标案例特征: {target_case['features']}")
        
        # 可以在这里添加更复杂的适应逻辑
        # 例如：根据特征差异调整输出参数
        adapted_case = source_case.copy()
        
        # 简单的适应策略示例
        target_length = target_case['features'][0]  # 隧道长度
        source_length = source_case['features'][0]
        length_ratio = target_length / source_length if source_length > 0 else 1.0
        
        # 根据长度比例调整某些参数
        if 'outputs' in adapted_case:
            outputs = adapted_case['outputs'].copy()
            # 例如：调整钢拱架数量
            if 'hasSteelArchCount' in outputs:
                original_count = outputs['hasSteelArchCount']
                outputs['hasSteelArchCount'] = max(1, int(original_count * length_ratio))
            adapted_case['outputs'] = outputs
            
        return adapted_case

    def reuse(self, retrieved_case, target_case):
        """案例重用"""
        case, similarity = retrieved_case
        
        if similarity >= self.threshold:
            print(f"✅ 相似度 {similarity:.3f} ≥ 阈值 {self.threshold}")
            return self.adapt_case(case, target_case)
        else:
            print(f"⚠️ 相似度 {similarity:.3f} < 阈值 {self.threshold}，需要调用RBR推理或组合多个案例。")
            return None

    def revise(self, adapted_case, target_case):
        """案例修正"""
        print("✅ 案例修正阶段：可以根据专家知识或反馈进行调整")
        return adapted_case

    def retain(self, new_case):
        """案例保留"""
        self.case_base.append(new_case)
        # 重新计算特征范围
        self.feature_mins, self.feature_maxs = self.compute_feature_ranges()
        print(f"✅ 新案例【{new_case['label']}】已加入案例库。")

    def print_outputs(self, case):
        """打印输出参数"""
        print("\n📌 推荐的后续设计参数：")
        if 'outputs' in case:
            for k, v in case["outputs"].items():
                print(f"  - {k}: {v}")
        else:
            print("  未找到输出参数")
    
    def print_feature_analysis(self, target_case, retrieved_cases):
        """打印特征分析"""
        print("\n📊 特征对比分析：")
        print("特征名称".ljust(25) + "目标值".ljust(10) + "最佳案例".ljust(12) + "差异".ljust(10))
        print("-" * 60)
        
        target_features = target_case['features']
        best_case_features = retrieved_cases[0][0]['features']
        
        for i, name in enumerate(self.feature_names):
            target_val = target_features[i] if i < len(target_features) else 'N/A'
            case_val = best_case_features[i] if i < len(best_case_features) else 'N/A'
            
            if isinstance(target_val, (int, float)) and isinstance(case_val, (int, float)):
                diff = abs(target_val - case_val)
                print(f"{name:<25}{target_val:<10}{case_val:<12}{diff:.2f}")
            else:
                print(f"{name:<25}{target_val:<10}{case_val:<12}N/A")

# ==========================================
# my_tunnel_app.py (完整版)
# ==========================================

def main():
    print("🚇 隧道工程CBR系统启动")
    print("=" * 50)
    
    # 创建案例库文件（如果不存在）
    json_file = "tunnel_case_base.json"
    if not os.path.exists(json_file):
        print(f"📁 创建案例库文件: {json_file}")
        case_base = create_tunnel_case_base()
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(case_base, f, indent=2, ensure_ascii=False)
    else:
        print(f"📁 加载已存在的案例库文件: {json_file}")
    
    # 加载案例库
    try:
        with open(json_file, encoding="utf-8") as f:
            case_base = json.load(f)
        print(f"✅ 成功加载 {len(case_base)} 个案例")
    except Exception as e:
        print(f"❌ 加载案例库失败: {e}")
        return
    
    # 特征权重设置
    # [长度, 地质, 水文, 土壤, 类型, 直径]
    feature_weights = [0.2, 0.15, 0.1, 0.1, 0.15, 0.3]
    
    # 创建CBR系统
    cbr = CBRSystem(case_base, feature_weights, threshold=0.85)
    
    # 显示特征说明
    print(f"\n📋 特征编码说明:")
    print(f"1. 隧道长度 (m): 实际数值")
    print(f"2. 地质条件: 1=优, 2=良, 3=中, 4=差, 5=极差")
    print(f"3. 水文条件: 1=干燥, 2=微湿, 3=潮湿, 4=滴水, 5=涌水")
    print(f"4. 土壤类型: 1=岩石, 2=砂土, 3=粘土, 4=软土, 5=特殊土")
    print(f"5. 隧道类型: 1=山岭, 2=水下, 3=浅埋, 4=深埋")
    print(f"6. 隧道直径 (m): 实际数值")
    
    # 模拟用户输入
    target_case = {
        "features": [1100, 3, 2, 2, 1, 10.2]
    }
    
    print(f"\n🌟 输入的目标案例特征: {target_case['features']}")
    print(f"📊 特征权重: {feature_weights}")
    
    # 运行CBR流程
    print(f"\n" + "="*50)
    print(f"🔄 开始CBR四步流程")
    print(f"="*50)
    
    # 1. Retrieve - 检索
    print(f"\n📖 第1步: Retrieve (检索)")
    retrieved_list = cbr.retrieve(target_case)
    best_case, best_similarity = retrieved_list[0]
    
    print(f"\n🏆 最相似案例: {best_case['label']}")
    print(f"🎯 最高相似度: {best_similarity:.3f}")
    
    # 显示特征分析
    cbr.print_feature_analysis(target_case, retrieved_list)
    
    # 2. Reuse - 重用
    print(f"\n🔄 第2步: Reuse (重用)")
    adapted_case = cbr.reuse(retrieved_list[0], target_case)
    
    # 3. Revise - 修正
    if adapted_case:
        print(f"\n📝 第3步: Revise (修正)")
        revised_case = cbr.revise(adapted_case, target_case)
        
        # 输出结果
        cbr.print_outputs(revised_case)
        
        # 4. Retain - 保留
        print(f"\n💾 第4步: Retain (保留)")
        new_case = {
            "features": target_case["features"],
            "label": "NewTunnelCase_001",
            "outputs": revised_case["outputs"]
        }
        cbr.retain(new_case)
        
        # 保存更新后的案例库
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(cbr.case_base, f, indent=2, ensure_ascii=False)
        print(f"💾 案例库已更新并保存到 {json_file}")
        
    else:
        print(f"\n⚠️ 由于相似度过低，建议:")
        print(f"  1. 调整特征权重")
        print(f"  2. 降低相似度阈值")
        print(f"  3. 增加更多相似案例")
        print(f"  4. 使用基于规则的推理(RBR)")
    
    print(f"\n🎉 CBR流程完成!")

if __name__ == "__main__":
    main()