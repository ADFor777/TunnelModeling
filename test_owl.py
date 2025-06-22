from owlready2 import get_ontology, sync_reasoner, Thing, ObjectProperty, DataProperty
from pathlib import Path
import traceback

def safe_load_ontology(file_path):
    """
    安全加载OWL本体，处理常见错误
    """
    try:
        print("🔄 正在加载本体...")
        onto = get_ontology(file_path).load()
        print("✅ 本体加载成功！")
        return onto
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return None

def safe_get_classes(onto):
    """
    安全获取类列表，避免元类冲突
    """
    try:
        # 方法1: 直接获取
        classes = list(onto.classes())
        return classes
    except Exception as e:
        print(f"⚠️  直接获取类失败: {e}")
        
        # 方法2: 通过搜索获取
        try:
            print("🔄 尝试通过搜索获取类...")
            classes = []
            for entity in onto.search():
                if hasattr(entity, '__class__') and 'ThingClass' in str(type(entity)):
                    classes.append(entity)
            return classes
        except Exception as e2:
            print(f"⚠️  搜索方法也失败: {e2}")
            return []

def safe_get_individuals(onto):
    """
    安全获取个体列表
    """
    try:
        individuals = list(onto.individuals())
        return individuals
    except Exception as e:
        print(f"⚠️  获取个体失败: {e}")
        
        # 尝试通过搜索获取
        try:
            individuals = []
            for entity in onto.search():
                if hasattr(entity, 'is_a') and Thing in entity.is_a:
                    individuals.append(entity)
            return individuals
        except:
            return []

def safe_get_properties(onto):
    """
    安全获取属性列表
    """
    try:
        properties = list(onto.properties())
        return properties
    except Exception as e:
        print(f"⚠️  获取属性失败: {e}")
        
        # 分别获取对象属性和数据属性
        try:
            obj_props = list(onto.object_properties())
            data_props = list(onto.data_properties())
            return obj_props + data_props
        except:
            return []

def analyze_ontology(onto):
    """
    分析本体内容
    """
    print("\n📊 本体分析:")
    print("-" * 40)
    
    # 安全获取各种元素
    classes = safe_get_classes(onto)
    individuals = safe_get_individuals(onto)
    properties = safe_get_properties(onto)
    
    print(f"类的数量: {len(classes)}")
    print(f"个体数量: {len(individuals)}")
    print(f"属性数量: {len(properties)}")
    
    # 显示类信息
    if classes:
        print(f"\n📝 类列表 (前10个):")
        for i, cls in enumerate(classes[:10], 1):
            try:
                class_name = getattr(cls, 'name', str(cls))
                print(f"  {i}. {class_name}")
            except:
                print(f"  {i}. [获取类名失败]")
    
    # 显示个体信息
    if individuals:
        print(f"\n👥 个体列表 (前10个):")
        for i, indiv in enumerate(individuals[:10], 1):
            try:
                indiv_name = getattr(indiv, 'name', str(indiv))
                print(f"  {i}. {indiv_name}")
                
                # 尝试获取类型
                try:
                    types = [str(t) for t in indiv.is_a if t != Thing]
                    if types:
                        print(f"     类型: {', '.join(types[:3])}")
                except:
                    pass
                    
            except Exception as e:
                print(f"  {i}. [获取个体信息失败: {e}]")
    
    # 显示属性信息
    if properties:
        print(f"\n🔗 属性列表 (前10个):")
        for i, prop in enumerate(properties[:10], 1):
            try:
                prop_name = getattr(prop, 'name', str(prop))
                prop_type = "对象属性" if isinstance(prop, type) and issubclass(prop, ObjectProperty) else "数据属性"
                print(f"  {i}. {prop_name} ({prop_type})")
            except:
                print(f"  {i}. [获取属性信息失败]")

def safe_display_individual_properties(individuals):
    """
    安全显示个体属性
    """
    if not individuals:
        print("⚠️  没有个体可显示")
        return
    
    print(f"\n🔍 个体详细信息 (前5个):")
    print("-" * 50)
    
    for i, indiv in enumerate(individuals[:5], 1):
        try:
            indiv_name = getattr(indiv, 'name', f'个体{i}')
            print(f"\n【{i}. {indiv_name}】")
            
            # 获取属性
            try:
                props = indiv.get_properties()
                if not props:
                    print("  - 无属性")
                    continue
                
                prop_count = 0
                for prop in props:
                    if prop_count >= 5:  # 只显示前5个属性
                        break
                    try:
                        values = prop[indiv]
                        if values:
                            prop_name = getattr(prop, 'name', str(prop))
                            if isinstance(values, list):
                                for val in values[:3]:  # 每个属性最多显示3个值
                                    print(f"  - {prop_name}: {val}")
                            else:
                                print(f"  - {prop_name}: {values}")
                            prop_count += 1
                    except Exception as prop_error:
                        prop_name = getattr(prop, 'name', str(prop))
                        print(f"  - {prop_name}: [获取值失败]")
                        
            except Exception as e:
                print(f"  - [获取属性失败: {e}]")
                
        except Exception as e:
            print(f"【个体{i}】: [处理失败: {e}]")

def safe_reasoning(onto):
    """
    安全执行推理
    """
    print("\n🤖 开始推理...")
    try:
        with onto:
            sync_reasoner(infer_property_values=True, infer_data_property_values=True)
        print("✅ 推理完成！")
        return True
    except Exception as e:
        print(f"❌ 推理失败: {e}")
        print("💡 尝试基础推理...")
        try:
            with onto:
                sync_reasoner()
            print("✅ 基础推理完成！")
            return True
        except Exception as e2:
            print(f"❌ 基础推理也失败: {e2}")
            return False

def main():
    # 你的文件路径
    file_path = r"G:\02.研一\TUNNEL\Tunnel"
    
    print(f"🔍 处理文件: {file_path}")
    print(f"📏 文件大小: {Path(file_path).stat().st_size} 字节")
    
    # 加载本体
    onto = safe_load_ontology(file_path)
    if not onto:
        print("❌ 无法加载本体，程序终止")
        return
    
    # 分析本体
    analyze_ontology(onto)
    
    # 安全获取个体
    individuals = safe_get_individuals(onto)
    
    # 显示个体属性
    safe_display_individual_properties(individuals)
    
    # 执行推理
    reasoning_success = safe_reasoning(onto)
    
    if reasoning_success:
        print("\n🔄 推理后重新分析...")
        # 推理后重新获取个体（可能有新的推理结果）
        individuals_after = safe_get_individuals(onto)
        
        if len(individuals_after) > len(individuals):
            print(f"🎉 推理产生了新个体！({len(individuals)} -> {len(individuals_after)})")
        
        # 显示推理后的部分结果
        safe_display_individual_properties(individuals_after[:3])
    
    print("\n✅ 程序执行完成！")

if __name__ == "__main__":
    main()