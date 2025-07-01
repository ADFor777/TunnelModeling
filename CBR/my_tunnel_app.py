import json
import os
from cbr_system import CBRSystem

def main():
    print("🚇 隧道工程CBR系统启动")
    print("=" * 50)
    
    # 检查案例库文件是否存在
    json_file = "tunnel_case_base.json"
    if not os.path.exists(json_file):
        print(f"❌ 案例库文件 {json_file} 不存在！")
        print(f"💡 请先运行 create_tunnel_cases.py 生成案例库文件")
        return
    
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
        
        # 询问是否保存更新后的案例库
        save_choice = input("\n💾 是否保存新案例到案例库？(y/n): ").lower().strip()
        if save_choice in ['y', 'yes', '是']:
            try:
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(cbr.case_base, f, indent=2, ensure_ascii=False)
                print(f"✅ 案例库已更新并保存到 {json_file}")
            except Exception as e:
                print(f"❌ 保存案例库失败: {e}")
        else:
            print("ℹ️ 新案例未保存到文件")
        
    else:
        print(f"\n⚠️ 由于相似度过低，建议:")
        print(f"  1. 调整特征权重")
        print(f"  2. 降低相似度阈值")
        print(f"  3. 增加更多相似案例")
        print(f"  4. 使用基于规则的推理(RBR)")
    
    print(f"\n🎉 CBR流程完成!")

if __name__ == "__main__":
    main()