from owlready2 import *
import types

# 文件路径
file_path = r"G:\tunnel3dmodeling\Tunnel.owl"

print("🚀 SWRL推理系统启动...")
print(f"📁 加载本体: {file_path}")

try:
    # 加载本体
    onto = get_ontology(file_path).load()
    print("✅ 本体加载成功！")
    print(f"📋 本体IRI: {onto.base_iri}")
    
    # 设置推理器
    print("\n🔧 配置推理器...")
    
    # 尝试不同的推理器
    reasoners = ['Pellet', 'HermiT', 'FaCT++']
    reasoner_success = False
    
    for reasoner_name in reasoners:
        try:
            print(f"尝试使用 {reasoner_name} 推理器...")
            with onto:
                if reasoner_name == 'Pellet':
                    sync_reasoner_pellet()
                elif reasoner_name == 'HermiT':
                    sync_reasoner_hermit()
                else:
                    sync_reasoner()
            print(f"✅ {reasoner_name} 推理器配置成功！")
            reasoner_success = True
            break
        except Exception as e:
            print(f"❌ {reasoner_name} 推理器失败: {e}")
    
    if not reasoner_success:
        print("⚠️  使用默认推理器...")
        try:
            with onto:
                sync_reasoner()
            reasoner_success = True
        except Exception as e:
            print(f"❌ 默认推理器也失败: {e}")
    
    # 分析现有的SWRL规则
    print("\n🔍 分析现有SWRL规则...")
    try:
        # 查找SWRL规则
        swrl_rules = []
        for individual in onto.individuals():
            try:
                if hasattr(individual, 'rdf_type'):
                    for rdf_type in individual.rdf_type:
                        if 'swrl' in str(rdf_type).lower() or 'rule' in str(rdf_type).lower():
                            swrl_rules.append(individual)
            except:
                pass
        
        if swrl_rules:
            print(f"📜 发现 {len(swrl_rules)} 个SWRL规则")
            for i, rule in enumerate(swrl_rules, 1):
                print(f"  规则{i}: {rule.name}")
        else:
            print("📜 未发现现有SWRL规则，将创建示例规则")
    except Exception as e:
        print(f"❌ SWRL规则分析失败: {e}")
    
    # 创建SWRL推理函数
    def create_swrl_rule(rule_name, rule_body, rule_head):
        """创建SWRL规则"""
        try:
            # 这里需要根据您的本体结构来定义具体的规则
            print(f"📝 创建SWRL规则: {rule_name}")
            print(f"   规则体: {rule_body}")
            print(f"   规则头: {rule_head}")
            return True
        except Exception as e:
            print(f"❌ 创建规则失败: {e}")
            return False
    
    # SWRL推理主函数
    def swrl_inference(input_data):
        """
        SWRL推理主函数
        input_data: 输入的参数字典
        返回: 推理得到的参数字典
        """
        print(f"\n🧠 开始SWRL推理...")
        print(f"📥 输入参数: {input_data}")
        
        results = {}
        
        try:
            # 步骤1: 将输入数据添加到本体中
            print("📝 步骤1: 添加输入数据到本体...")
            
            # 创建或获取个体来存储输入数据
            input_individual = None
            
            # 查找合适的类来创建个体
            available_classes = []
            try:
                for cls in onto.classes():
                    try:
                        class_name = cls.name if hasattr(cls, 'name') else str(cls)
                        available_classes.append(class_name)
                        if len(available_classes) >= 5:  # 只显示前5个
                            break
                    except:
                        continue
                        
                if available_classes:
                    print(f"   可用的类: {available_classes}")
                    # 使用第一个可用的类
                    target_class = list(onto.classes())[0]
                    input_individual = target_class(f"input_instance_{hash(str(input_data)) % 10000}")
                    print(f"   ✅ 创建个体: {input_individual}")
                
            except Exception as e:
                print(f"   ❌ 创建个体失败: {e}")
            
            # 步骤2: 设置属性值
            print("📝 步骤2: 设置属性值...")
            if input_individual:
                # 获取可用属性
                available_properties = []
                try:
                    properties = list(onto.properties())
                    print(f"   发现 {len(properties)} 个属性")
                    
                    for prop in properties[:10]:  # 显示前10个属性
                        try:
                            prop_name = prop.name if hasattr(prop, 'name') else str(prop)
                            available_properties.append(prop_name)
                            print(f"     - {prop_name}")
                        except:
                            continue
                    
                    # 尝试设置输入数据中的属性
                    for key, value in input_data.items():
                        # 查找匹配的属性
                        matching_prop = None
                        for prop in properties:
                            try:
                                if hasattr(prop, 'name') and prop.name.lower() == key.lower():
                                    matching_prop = prop
                                    break
                            except:
                                continue
                        
                        if matching_prop:
                            try:
                                setattr(input_individual, matching_prop.name, value)
                                print(f"     ✅ 设置 {matching_prop.name} = {value}")
                            except Exception as e:
                                print(f"     ❌ 设置属性失败: {e}")
                        else:
                            print(f"     ⚠️  未找到匹配属性: {key}")
                
                except Exception as e:
                    print(f"   ❌ 属性处理失败: {e}")
            
            # 步骤3: 执行推理
            print("📝 步骤3: 执行推理...")
            if reasoner_success:
                try:
                    with onto:
                        sync_reasoner()
                    print("   ✅ 推理执行成功")
                    
                    # 获取推理结果
                    if input_individual:
                        print("📝 步骤4: 获取推理结果...")
                        for prop in onto.properties():
                            try:
                                prop_name = prop.name if hasattr(prop, 'name') else str(prop)
                                values = getattr(input_individual, prop_name, None)
                                if values and prop_name not in input_data:
                                    results[prop_name] = values
                                    print(f"     🎯 推理得到: {prop_name} = {values}")
                            except:
                                continue
                
                except Exception as e:
                    print(f"   ❌ 推理执行失败: {e}")
            else:
                print("   ⚠️  推理器未就绪，跳过推理步骤")
            
            # 步骤5: 应用自定义规则（如果没有SWRL规则）
            if not results:
                print("📝 步骤5: 应用自定义推理规则...")
                results = apply_custom_rules(input_data)
        
        except Exception as e:
            print(f"❌ 推理过程失败: {e}")
        
        print(f"📤 推理结果: {results}")
        return results
    
    def apply_custom_rules(input_data):
        """应用自定义推理规则"""
        results = {}
        
        # 示例规则1: 基于几何参数的推理
        if 'diameter' in input_data and 'length' in input_data:
            diameter = float(input_data['diameter'])
            length = float(input_data['length'])
            
            # 计算截面积
            import math
            area = math.pi * (diameter / 2) ** 2
            results['cross_sectional_area'] = area
            
            # 计算体积
            volume = area * length
            results['volume'] = volume
            
            # 判断隧道类型
            if diameter > 10:
                results['tunnel_type'] = 'large_tunnel'
            elif diameter > 5:
                results['tunnel_type'] = 'medium_tunnel'
            else:
                results['tunnel_type'] = 'small_tunnel'
            
            print(f"   🧮 几何计算: 直径={diameter}m, 长度={length}m")
            print(f"   📊 截面积={area:.2f}m², 体积={volume:.2f}m³")
        
        # 示例规则2: 基于材料属性的推理
        if 'material' in input_data and 'stress' in input_data:
            material = input_data['material']
            stress = float(input_data['stress'])
            
            # 材料安全系数推理
            safety_factors = {
                'concrete': 2.5,
                'steel': 3.0,
                'rock': 2.0
            }
            
            if material.lower() in safety_factors:
                max_stress = stress * safety_factors[material.lower()]
                results['max_allowable_stress'] = max_stress
                results['safety_factor'] = safety_factors[material.lower()]
                print(f"   🔧 材料分析: {material}, 最大允许应力={max_stress:.2f}MPa")
        
        # 示例规则3: 基于地质条件的推理
        if 'geology' in input_data and 'depth' in input_data:
            geology = input_data['geology']
            depth = float(input_data['depth'])
            
            # 支护方案推理
            if geology.lower() == 'rock' and depth > 50:
                results['support_method'] = 'rock_bolt_and_mesh'
                results['excavation_method'] = 'drill_and_blast'
            elif geology.lower() == 'soil' and depth > 20:
                results['support_method'] = 'steel_ribs_and_shotcrete'
                results['excavation_method'] = 'shield_tunneling'
            else:
                results['support_method'] = 'light_support'
                results['excavation_method'] = 'cut_and_cover'
            
            print(f"   🏔️  地质分析: {geology}, 深度={depth}m")
            print(f"   🔨 推荐: 支护={results['support_method']}, 开挖={results['excavation_method']}")
        
        return results
    
    # 交互式推理系统
    def interactive_inference():
        """交互式推理系统"""
        print("\n🎮 交互式SWRL推理系统")
        print("=" * 50)
        
        while True:
            print("\n📝 请输入参数 (输入 'quit' 退出):")
            print("支持的参数类型:")
            print("  - diameter: 隧道直径(m)")
            print("  - length: 隧道长度(m)")
            print("  - material: 材料类型(concrete/steel/rock)")
            print("  - stress: 应力值(MPa)")
            print("  - geology: 地质条件(rock/soil)")
            print("  - depth: 埋深(m)")
            
            # 获取用户输入
            input_data = {}
            
            try:
                while True:
                    param_input = input("\n参数名=值 (或按回车完成输入): ").strip()
                    
                    if param_input.lower() == 'quit':
                        return
                    
                    if not param_input:
                        break
                    
                    if '=' in param_input:
                        key, value = param_input.split('=', 1)
                        input_data[key.strip()] = value.strip()
                        print(f"✅ 添加参数: {key.strip()} = {value.strip()}")
                    else:
                        print("❌ 格式错误，请使用 '参数名=值' 格式")
                
                if input_data:
                    # 执行推理
                    results = swrl_inference(input_data)
                    
                    # 显示结果
                    print("\n" + "="*50)
                    print("🎯 推理结果:")
                    print("="*50)
                    for key, value in results.items():
                        print(f"📊 {key}: {value}")
                    print("="*50)
                else:
                    print("⚠️  未输入任何参数")
            
            except KeyboardInterrupt:
                print("\n👋 退出推理系统")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
    
    # 启动交互式系统
    if reasoner_success or True:  # 即使推理器失败也可以使用自定义规则
        interactive_inference()
    else:
        print("❌ 推理系统初始化失败")

except Exception as e:
    print(f"❌ 系统启动失败: {e}")
    print("\n💡 建议:")
    print("1. 检查本体文件是否正确")
    print("2. 确保安装了推理器(如Pellet)")
    print("3. 检查SWRL规则的语法")

print("\n👋 SWRL推理系统结束")