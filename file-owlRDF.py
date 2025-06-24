from owlready2 import *
import os
import sys
from pathlib import Path

# 配置文件路径
OWL_FILE_PATH = r"G:\TUNNEL\Tunnel_RDF.owl"

def create_clean_world():
    """创建一个干净的世界环境"""
    try:
        # 创建新的世界
        world = World()
        
        # 设置推理器选项
        world.set_backend(filename=":memory:")
        
        print("✅ 创建干净的世界环境成功")
        return world
    except Exception as e:
        print(f"❌ 创建世界环境失败: {e}")
        return None

def load_ontology_for_reasoning(world, file_path):
    """专门为推理加载本体"""
    try:
        # 尝试不同的加载方式
        loading_methods = [
            ("直接路径", file_path),
            ("file URI", f"file:///{file_path.replace(chr(92), '/')}"),
            ("pathlib转换", str(Path(file_path).resolve()))
        ]
        
        for method_name, path_to_try in loading_methods:
            try:
                print(f"🔄 尝试{method_name}: {path_to_try}")
                onto = world.get_ontology(path_to_try).load()
                print(f"✅ 成功加载本体: {onto.base_iri}")
                return onto
            except Exception as e:
                print(f"❌ {method_name}失败: {e}")
                continue
        
        return None
    except Exception as e:
        print(f"❌ 加载本体失败: {e}")
        return None

def extract_swrl_rules_advanced(world, onto):
    """高级SWRL规则提取方法"""
    print("\n🔍 深度搜索SWRL规则...")
    
    rules_found = []
    
    # 方法1: 直接从owl文件读取规则文本
    try:
        print("📖 方法1: 直接读取OWL文件内容...")
        with open(OWL_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 查找SWRL规则相关的XML标签
        swrl_patterns = [
            '<ruleml:imp>',
            '<swrl:Imp>',
            '<swrlb:',
            'swrl:body',
            'swrl:head',
            'DLSafeRule'
        ]
        
        found_patterns = []
        for pattern in swrl_patterns:
            if pattern in content:
                found_patterns.append(pattern)
        
        if found_patterns:
            print(f"✅ 在OWL文件中找到SWRL相关标签: {found_patterns}")
            
            # 尝试提取规则文本
            import re
            
            # 查找swrl:Imp标签内容
            imp_pattern = r'<swrl:Imp[^>]*>(.*?)</swrl:Imp>'
            imp_matches = re.findall(imp_pattern, content, re.DOTALL)
            
            if imp_matches:
                print(f"🎯 找到 {len(imp_matches)} 个SWRL规则定义")
                for i, match in enumerate(imp_matches, 1):
                    print(f"  规则 {i}: {match[:200]}...")
                    rules_found.append(f"Rule_{i}: {match}")
            
            # 查找DLSafeRule
            dlsafe_pattern = r'<DLSafeRule[^>]*>(.*?)</DLSafeRule>'
            dlsafe_matches = re.findall(dlsafe_pattern, content, re.DOTALL)
            
            if dlsafe_matches:
                print(f"🎯 找到 {len(dlsafe_matches)} 个DLSafeRule规则")
                for i, match in enumerate(dlsafe_matches, 1):
                    print(f"  DLSafe规则 {i}: {match[:200]}...")
                    rules_found.append(f"DLSafeRule_{i}: {match}")
        else:
            print("❌ 在OWL文件中未找到SWRL相关标签")
            
    except Exception as e:
        print(f"❌ 读取OWL文件失败: {e}")
    
    # 方法2: 使用owlready2的内部结构
    try:
        print("\n📊 方法2: 检查owlready2内部结构...")
        
        # 检查世界中的所有实体
        all_entities = list(world.individuals()) + list(world.classes()) + list(world.properties())
        print(f"📈 世界中总实体数: {len(all_entities)}")
        
        # 查找规则相关的实体
        rule_entities = []
        for entity in all_entities:
            try:
                entity_str = str(entity)
                if any(keyword in entity_str.lower() for keyword in ['rule', 'imp', 'swrl']):
                    rule_entities.append(entity)
            except:
                continue
        
        if rule_entities:
            print(f"✅ 找到 {len(rule_entities)} 个规则相关实体:")
            for entity in rule_entities:
                print(f"  🔗 {entity}")
                rules_found.append(str(entity))
        
    except Exception as e:
        print(f"❌ 检查内部结构失败: {e}")
    
    # 方法3: 通过RDF三元组查找
    try:
        print("\n🔍 方法3: 通过RDF三元组查找规则...")
        
        # 获取所有三元组
        triples = list(world.as_rdflib_graph().triples((None, None, None)))
        print(f"📊 总三元组数: {len(triples)}")
        
        # 查找包含SWRL命名空间的三元组
        swrl_triples = []
        for triple in triples:
            triple_str = str(triple)
            if 'swrl' in triple_str.lower() or 'rule' in triple_str.lower():
                swrl_triples.append(triple)
        
        if swrl_triples:
            print(f"✅ 找到 {len(swrl_triples)} 个SWRL相关三元组:")
            for i, triple in enumerate(swrl_triples[:10], 1):  # 只显示前10个
                print(f"  {i}. {triple}")
                rules_found.append(str(triple))
        
    except Exception as e:
        print(f"❌ RDF三元组查找失败: {e}")
    
    return rules_found

def create_test_individual(onto, world):
    """创建测试个体用于推理"""
    try:
        print("\n🧪 创建测试个体...")
        
        # 查看可用的类
        print("📋 查看可用的数据属性:")
        data_props = list(onto.data_properties())
        for i, prop in enumerate(data_props[:10], 1):
            try:
                prop_name = getattr(prop, 'name', str(prop))
                print(f"  {i}. {prop_name}")
            except:
                print(f"  {i}. {prop}")
        
        print("\n📋 查看可用的对象属性:")
        obj_props = list(onto.object_properties())
        for i, prop in enumerate(obj_props[:10], 1):
            try:
                prop_name = getattr(prop, 'name', str(prop))
                print(f"  {i}. {prop_name}")
            except:
                print(f"  {i}. {prop}")
        
        # 尝试创建一个简单的个体
        with onto:
            # 创建一个通用的个体
            test_individual = Thing(f"TestIndividual_{len(list(onto.individuals()))}")
            
            # 尝试设置一些属性
            for prop in data_props[:3]:
                try:
                    # 为数据属性设置测试值
                    if 'depth' in str(prop).lower():
                        setattr(test_individual, prop.name, 100.0)
                    elif 'length' in str(prop).lower():
                        setattr(test_individual, prop.name, 1000.0)
                    elif 'diameter' in str(prop).lower():
                        setattr(test_individual, prop.name, 5.0)
                except Exception as e:
                    print(f"⚠️ 设置属性 {prop} 失败: {e}")
            
            print(f"✅ 创建测试个体: {test_individual}")
            return test_individual
            
    except Exception as e:
        print(f"❌ 创建测试个体失败: {e}")
        return None

def perform_reasoning_test(world, onto):
    """执行推理测试"""
    print("\n🧠 执行推理测试...")
    
    try:
        # 记录推理前的状态
        before_individuals = len(list(onto.individuals()))
        print(f"📊 推理前个体数量: {before_individuals}")
        
        # 执行推理
        print("🔄 开始推理...")
        with onto:
            sync_reasoner_pellet(infer_property_values=True, 
                               infer_data_property_values=True,
                               debug=1)
        
        # 记录推理后的状态
        after_individuals = len(list(onto.individuals()))
        print(f"📊 推理后个体数量: {after_individuals}")
        
        if after_individuals > before_individuals:
            print(f"🎉 推理生成了 {after_individuals - before_individuals} 个新个体!")
        else:
            print("📈 推理完成，可能推导出了新的属性值")
        
        return True
        
    except Exception as e:
        print(f"❌ 推理失败: {e}")
        if "java" in str(e).lower():
            print("💡 提示: 确保Java环境正确安装")
        elif "pellet" in str(e).lower():
            print("💡 提示: Pellet推理器可能需要网络连接")
        return False

def main():
    print("🎯 SWRL规则推理分析器")
    print("=" * 60)
    
    # 检查文件
    if not os.path.exists(OWL_FILE_PATH):
        print(f"❌ 文件不存在: {OWL_FILE_PATH}")
        return
    
    print(f"✅ 文件存在: {OWL_FILE_PATH}")
    print(f"📁 文件大小: {os.path.getsize(OWL_FILE_PATH)} bytes")
    
    # 创建世界环境
    world = create_clean_world()
    if not world:
        return
    
    # 加载本体
    onto = load_ontology_for_reasoning(world, OWL_FILE_PATH)
    if not onto:
        print("❌ 无法加载本体文件")
        return
    
    # 提取SWRL规则
    rules = extract_swrl_rules_advanced(world, onto)
    
    if rules:
        print(f"\n🎉 总共找到 {len(rules)} 个规则相关项")
        print("\n📋 规则详情:")
        for i, rule in enumerate(rules, 1):
            print(f"  {i}. {rule[:100]}...")
    else:
        print("\n❌ 未找到任何SWRL规则")
    
    # 创建测试个体
    test_individual = create_test_individual(onto, world)
    
    # 执行推理测试
    reasoning_success = perform_reasoning_test(world, onto)
    
    print(f"\n📊 分析总结:")
    print(f"  - 本体加载: ✅")
    print(f"  - 规则查找: {'✅' if rules else '❌'}")
    print(f"  - 推理测试: {'✅' if reasoning_success else '❌'}")
    
    if not rules:
        print(f"\n💡 建议:")
        print(f"  1. 检查OWL文件是否真的包含SWRL规则")
        print(f"  2. 使用Protégé打开文件确认规则存在")
        print(f"  3. 确保规则的命名空间正确")
        print(f"  4. 考虑重新导出OWL文件")

if __name__ == "__main__":
    main()