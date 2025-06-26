"""
json_to_owl_dynamic.py
支持动态规则加载的主程序
当pure_swrl_rules.txt文件更改时，程序会自动使用最新的规则
"""

import sys
import json
import os
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL
from datetime import datetime

# 导入动态SWRL规则加载器
try:
    from dynamic_swrl_loader import DynamicSWRLLoader, apply_dynamic_rules
    DYNAMIC_LOADER_AVAILABLE = True
except ImportError:
    DYNAMIC_LOADER_AVAILABLE = False
    print("[警告] 未找到dynamic_swrl_loader模块，将使用简化的内置规则")

# 定义命名空间
OWL = Namespace("http://www.w3.org/2002/07/owl#")
SWRL = Namespace("http://www.w3.org/2003/11/swrl#")
SWRLA = Namespace("http://swrl.stanford.edu/ontologies/3.3/swrla.owl#")
DLS = Namespace("http://example.com/dlsafe#")

class DynamicTunnelProcessor:
    """支持动态规则加载的隧道处理器"""
    
    def __init__(self, swrl_rules_path: str = "pure_swrl_rules.txt"):
        self.swrl_rules_path = swrl_rules_path
        self.graph = None
        self.tunnel_individual = None
        self.dynamic_loader = None
        
        # 初始化动态加载器
        if DYNAMIC_LOADER_AVAILABLE:
            self.dynamic_loader = DynamicSWRLLoader(swrl_rules_path)
            print(f"[动态处理器] 已初始化动态规则加载器: {swrl_rules_path}")
        else:
            print(f"[动态处理器] 动态加载器不可用，使用内置规则")
    
    def create_owl_graph(self):
        """创建OWL图并绑定命名空间"""
        self.graph = Graph()
        self.graph.bind("owl", OWL)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("swrl", SWRL)
        self.graph.bind("swrla", SWRLA)
        self.graph.bind("dls", DLS)
        print("[动态处理器] 已创建OWL图")
    
    def create_owl_individuals(self, params):
        """根据JSON参数创建OWL个体"""
        # 创建隧道项目个体
        self.tunnel_individual = DLS.TunnelProject_001
        
        # 添加隧道类型
        tunnel_type = params.get("tunnelType", "TunnelProject")
        type_mapping = {
            "MountainTunnelProject": DLS.MountainTunnelProject,
            "UnderwaterTunnelProject": DLS.UnderwaterTunnelProject,
            "ShallowTunnelProject": DLS.ShallowTunnelProject,
            "DeepTunnelProject": DLS.DeepTunnelProject,
            "UrbanTunnelProject": DLS.UrbanTunnelProject
        }
        ontology_class = type_mapping.get(tunnel_type, DLS.TunnelProject)
        self.graph.add((self.tunnel_individual, RDF.type, ontology_class))
        
        # 添加数据属性
        numeric_properties = ["hasTunnelLength", "hasTunnelDiameter"]
        for prop in numeric_properties:
            if params.get(prop) is not None:
                value = params[prop]
                datatype = XSD.float if isinstance(value, float) else XSD.integer
                self.graph.add((self.tunnel_individual, DLS[prop], 
                              Literal(value, datatype=datatype)))
        
        # 创建地质条件个体
        if params.get("hasGeologicalCondition"):
            gc_individual = DLS.GeologicalCondition_001
            self.graph.add((gc_individual, RDF.type, DLS.GeologicalCondition))
            self.graph.add((self.tunnel_individual, DLS.hasGeologicalCondition, gc_individual))
            
            # 添加围岩等级
            rock_grade = params["hasGeologicalCondition"]
            grade_mapping = {
                "I": DLS.RockGrade_I, "II": DLS.RockGrade_II, "III": DLS.RockGrade_III,
                "IV": DLS.RockGrade_IV, "V": DLS.RockGrade_V, "VI": DLS.RockGrade_VI
            }
            if rock_grade in grade_mapping:
                self.graph.add((gc_individual, DLS.hasRockGrade, grade_mapping[rock_grade]))
            
            # 添加水文条件
            hydro_condition = params.get("hasHydroCondition", "")
            hydro_mapping = {
                "water-rich": DLS.WaterRich, "dry": DLS.Dry
            }
            if hydro_condition in hydro_mapping:
                self.graph.add((gc_individual, DLS.hasHydroCondition, hydro_mapping[hydro_condition]))
        
        # 添加土壤类型
        if params.get("hasSoilType"):
            soil_type = params["hasSoilType"]
            soil_mapping = {
                "StrongSoil": DLS.StrongSoil, "WeakSoil": DLS.WeakSoil, "MediumSoil": DLS.MediumSoil
            }
            if soil_type in soil_mapping:
                self.graph.add((self.tunnel_individual, DLS.hasSoilType, soil_mapping[soil_type]))
        
        print(f"[动态处理器] 已创建隧道个体: {tunnel_type}")
    
    def apply_dynamic_inference(self, params):
        """应用动态推理规则"""
        if self.dynamic_loader:
            # 检查规则文件是否有更新
            if self.dynamic_loader.reload_rules_if_changed():
                print("[动态处理器] 检测到规则文件更新，使用最新规则")
            
            # 显示规则文件信息
            file_info = self.dynamic_loader.get_file_info()
            print(f"[动态处理器] 规则文件状态:")
            print(f"  - 文件路径: {file_info['file_path']}")
            print(f"  - 规则数量: {file_info['rule_count']}")
            print(f"  - 最后修改: {file_info['last_modified']}")
            print(f"  - 最后加载: {file_info['last_load_time']}")
            
            # 应用规则
            results = self.dynamic_loader.apply_rules(params)
            return results
        else:
            # 使用备用推理
            print("[动态处理器] 使用备用推理规则")
            return self._apply_fallback_inference(params)
    
    def _apply_fallback_inference(self, params):
        """备用推理方法"""
        results = {}
        
        # 基本推理逻辑
        tunnel_length = params.get("hasTunnelLength", 0)
        tunnel_diameter = params.get("hasTunnelDiameter", 0)
        rock_grade = params.get("hasGeologicalCondition", "")
        hydro_condition = params.get("hasHydroCondition", "")
        tunnel_type = params.get("tunnelType", "")
        soil_type = params.get("hasSoilType", "")
        
        # 施工方法推理
        if tunnel_length > 3000:
            results["hasConstructionMethod"] = "DrillAndBlast"
        else:
            results["hasConstructionMethod"] = "TBM"
        
        # 简化的衬砌厚度推理
        base_thickness = {
            "I": 20.0, "II": 22.5, "III": 25.0, "IV": 27.5, "V": 30.0
        }.get(rock_grade, 25.0)
        
        if hydro_condition == "water-rich":
            base_thickness += 2.5
        
        if tunnel_type == "DeepTunnelProject":
            base_thickness += 5.0
        elif tunnel_type == "UnderwaterTunnelProject":
            base_thickness += 5.0
        
        results["hasLiningThickness"] = base_thickness
        
        # 其他基本推理
        results["hasSteelArchSpacing"] = 0.8
        results["hasSteelArchThickness"] = 10
        results["hasWaterproofLayerThickness"] = 3.5
        
        if tunnel_diameter > 0:
            bolt_length = tunnel_diameter * 0.3
            results["hasBoltLength"] = round(bolt_length, 2)
            results["hasBoltSpacing"] = round(bolt_length / 2, 2)
        
        print(f"[动态处理器] 备用推理完成，生成 {len(results)} 个结果")
        return results
    
    def add_inference_results_to_graph(self, results):
        """将推理结果添加到OWL图"""
        for property_name, value in results.items():
            if isinstance(value, (int, float)):
                datatype = XSD.float if isinstance(value, float) else XSD.integer
                self.graph.add((self.tunnel_individual, DLS[property_name], 
                              Literal(value, datatype=datatype)))
            else:
                # 对象属性
                if isinstance(value, str):
                    object_uri = DLS[value]
                else:
                    object_uri = value
                self.graph.add((self.tunnel_individual, DLS[property_name], object_uri))
        
        print(f"[动态处理器] 已将 {len(results)} 个推理结果添加到OWL图")
    
    def save_owl_file(self, output_path, format='turtle'):
        """保存OWL文件"""
        if self.graph:
            self.graph.serialize(destination=output_path, format=format)
            return True
        return False
    
    def get_rule_statistics(self):
        """获取规则统计信息"""
        if self.dynamic_loader:
            rules = self.dynamic_loader.get_rules()
            categories = {}
            for rule in rules:
                category = rule.get('logic', {}).get('rule_category', 'unknown')
                categories[category] = categories.get(category, 0) + 1
            
            return {
                'total_rules': len(rules),
                'categories': categories,
                'file_info': self.dynamic_loader.get_file_info()
            }
        return None

def json_to_owl(json_path, swrl_rules_path, output_owl_path=None):
    """
    将JSON隧道参数转换为OWL个体，并应用动态SWRL规则进行推理
    Args:
        json_path: JSON参数文件路径
        swrl_rules_path: SWRL规则文件路径  
        output_owl_path: 输出OWL文件路径（可选）
    """
    try:
        print("="*60)
        print("动态SWRL规则推理系统")
        print("="*60)
        
        # 1. 读取JSON参数
        with open(json_path, 'r', encoding='utf-8') as f:
            params = json.load(f)
        print(f"[主程序] 已读取JSON参数: {params}")
        
        # 2. 创建动态处理器
        processor = DynamicTunnelProcessor(swrl_rules_path)
        
        # 3. 显示规则统计信息
        stats = processor.get_rule_statistics()
        if stats:
            print(f"[主程序] 规则统计:")
            print(f"  - 总规则数: {stats['total_rules']}")
            print(f"  - 类别分布: {stats['categories']}")
        
        # 4. 创建OWL图
        processor.create_owl_graph()
        
        # 5. 创建OWL个体
        processor.create_owl_individuals(params)
        
        # 6. 应用动态推理规则
        print(f"[主程序] 开始应用动态规则...")
        inference_results = processor.apply_dynamic_inference(params)
        print(f"[主程序] 推理完成，得到 {len(inference_results)} 个结果")
        
        # 7. 将推理结果添加到OWL图
        processor.add_inference_results_to_graph(inference_results)
        
        # 8. 保存OWL文件（如果指定了输出路径）
        if output_owl_path:
            success = processor.save_owl_file(output_owl_path)
            if success:
                print(f"[主程序] 已保存OWL文件到 {output_owl_path}")
            else:
                print("[主程序] OWL文件保存失败")
        
        # 9. 保存推理结果为JSON
        base_name = os.path.splitext(os.path.basename(json_path))[0]
        output_json_path = f"{base_name}_dynamic_results.json"
        
        result_data = {
            'timestamp': datetime.now().isoformat(),
            'input_params': params,
            'inference_results': inference_results,
            'rules_file': swrl_rules_path,
            'total_results': len(inference_results),
            'rule_statistics': stats
        }
        
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        print(f"[主程序] 已保存推理结果到 {output_json_path}")
        
        return inference_results
        
    except Exception as e:
        print(f"[主程序] 处理过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"推理失败: {str(e)}"

def watch_and_process(json_path, swrl_rules_path, output_owl_path=None, watch_interval=5):
    """
    监控模式：持续监控规则文件变化并重新处理
    Args:
        json_path: JSON参数文件路径
        swrl_rules_path: SWRL规则文件路径
        output_owl_path: 输出OWL文件路径（可选）
        watch_interval: 监控间隔（秒）
    """
    import time
    
    print(f"[监控模式] 开始监控规则文件: {swrl_rules_path}")
    print(f"[监控模式] 监控间隔: {watch_interval}秒")
    print("[监控模式] 按 Ctrl+C 停止监控")
    
    last_processed = 0
    
    try:
        while True:
            # 检查规则文件是否有更新
            if os.path.exists(swrl_rules_path):
                current_modified = os.path.getmtime(swrl_rules_path)
                
                if current_modified > last_processed:
                    print(f"\n[监控模式] 检测到规则文件更新: {datetime.fromtimestamp(current_modified)}")
                    
                    # 重新处理
                    result = json_to_owl(json_path, swrl_rules_path, output_owl_path)
                    
                    if isinstance(result, dict):
                        print(f"[监控模式] 重新处理完成，生成 {len(result)} 个推理结果")
                    else:
                        print(f"[监控模式] 重新处理失败")
                    
                    last_processed = current_modified
                    print(f"[监控模式] 继续监控...")
            
            time.sleep(watch_interval)
            
    except KeyboardInterrupt:
        print(f"\n[监控模式] 停止监控")

def create_sample_files():
    """创建示例文件"""
    # 创建示例JSON输入文件
    sample_input = {
        "tunnelType": "MountainTunnelProject",
        "hasTunnelLength": 2500,
        "hasTunnelDiameter": 12.0,
        "hasGeologicalCondition": "III",
        "hasHydroCondition": "water-rich",
        "hasSoilType": "MediumSoil"
    }
    
    with open('sample_input.json', 'w', encoding='utf-8') as f:
        json.dump(sample_input, f, ensure_ascii=False, indent=2)
    
    print("已创建示例文件:")
    print("- sample_input.json")
    print("\n请确保pure_swrl_rules.txt文件存在，或使用以下命令创建测试规则文件:")
    print("python json_to_owl_dynamic.py --create-test-rules")

def create_test_rules():
    """创建测试规则文件"""
    test_rules = """纯SWRL规则提取结果
==================================================

总共找到 5 个SWRL规则（测试版本）

规则 1: DLSafe_1 (DLSafeRule)
--------------------------------------------------
完整内容:
<Annotation>
    <AnnotationProperty abbreviatedIRI="rdfs:comment"/>
    <Literal>山岭 + RockGrade III + 富水 → 27.5 cm</Literal>
</Annotation>
<Annotation>
    <AnnotationProperty abbreviatedIRI="rdfs:label"/>
    <Literal>S06-5</Literal>
</Annotation>
<Body>
    <ClassAtom>
        <Class IRI="MountainTunnelProject"/>
        <Variable abbreviatedIRI=":t"/>
    </ClassAtom>
    <ObjectPropertyAtom>
        <ObjectProperty IRI="hasGeologicalCondition"/>
        <Variable abbreviatedIRI=":t"/>
        <Variable abbreviatedIRI=":gc"/>
    </ObjectPropertyAtom>
    <ObjectPropertyAtom>
        <ObjectProperty IRI="hasRockGrade"/>
        <Variable abbreviatedIRI=":gc"/>
        <NamedIndividual IRI="RockGrade_III"/>
    </ObjectPropertyAtom>
    <ObjectPropertyAtom>
        <ObjectProperty IRI="hasHydroCondition"/>
        <Variable abbreviatedIRI=":gc"/>
        <NamedIndividual IRI="WaterRich"/>
    </ObjectPropertyAtom>
</Body>
<Head>
    <DataPropertyAtom>
        <DataProperty IRI="hasLiningThickness"/>
        <Variable abbreviatedIRI=":t"/>
        <Literal datatypeIRI="http://www.w3.org/2001/XMLSchema#float">27.5</Literal>
    </DataPropertyAtom>
</Head>

==================================================

规则 2: DLSafe_2 (DLSafeRule)
--------------------------------------------------
完整内容:
<Annotation>
    <AnnotationProperty abbreviatedIRI="rdfs:comment"/>
    <Literal>隧道长度大于3000m选择钻爆法</Literal>
</Annotation>
<Annotation>
    <AnnotationProperty abbreviatedIRI="rdfs:label"/>
    <Literal>S01</Literal>
</Annotation>
<Body>
    <ClassAtom>
        <Class IRI="TunnelProject"/>
        <Variable abbreviatedIRI=":t"/>
    </ClassAtom>
    <DataPropertyAtom>
        <DataProperty IRI="hasTunnelLength"/>
        <Variable abbreviatedIRI=":t"/>
        <Variable abbreviatedIRI=":len"/>
    </DataPropertyAtom>
    <BuiltInAtom IRI="http://www.w3.org/2003/11/swrlb#greaterThan">
        <Variable abbreviatedIRI=":len"/>
        <Literal datatypeIRI="http://www.w3.org/2001/XMLSchema#integer">3000</Literal>
    </BuiltInAtom>
</Body>
<Head>
    <ObjectPropertyAtom>
        <ObjectProperty IRI="hasConstructionMethod"/>
        <Variable abbreviatedIRI=":t"/>
        <NamedIndividual IRI="DrillAndBlast"/>
    </ObjectPropertyAtom>
</Head>

==================================================

规则 3: DLSafe_3 (DLSafeRule)
--------------------------------------------------
完整内容:
<Annotation>
    <AnnotationProperty abbreviatedIRI="rdfs:comment"/>
    <Literal>隧道长度 ≤ 3000 → 使用TBM</Literal>
</Annotation>
<Annotation>
    <AnnotationProperty abbreviatedIRI="rdfs:label"/>
    <Literal>S02</Literal>
</Annotation>
<Body>
    <ClassAtom>
        <Class IRI="TunnelProject"/>
        <Variable abbreviatedIRI=":t"/>
    </ClassAtom>
    <DataPropertyAtom>
        <DataProperty IRI="hasTunnelLength"/>
        <Variable abbreviatedIRI=":t"/>
        <Variable abbreviatedIRI=":len"/>
    </DataPropertyAtom>
    <BuiltInAtom IRI="http://www.w3.org/2003/11/swrlb#lessThanOrEqual">
        <Variable abbreviatedIRI=":len"/>
        <Literal datatypeIRI="http://www.w3.org/2001/XMLSchema#integer">3000</Literal>
    </BuiltInAtom>
</Body>
<Head>
    <ObjectPropertyAtom>
        <ObjectProperty IRI="hasConstructionMethod"/>
        <Variable abbreviatedIRI=":t"/>
        <NamedIndividual IRI="TBM"/>
    </ObjectPropertyAtom>
</Head>

==================================================
"""
    
    with open('pure_swrl_rules.txt', 'w', encoding='utf-8') as f:
        f.write(test_rules)
    
    print("已创建测试规则文件: pure_swrl_rules.txt")
    print("包含3条测试规则，您可以修改此文件来测试动态加载功能")

def main():
    """主函数"""
    if len(sys.argv) >= 2 and sys.argv[1] == "--create-test-rules":
        create_test_rules()
        return
    
    if len(sys.argv) >= 2 and sys.argv[1] == "--watch":
        if len(sys.argv) < 4:
            print("监控模式用法: python json_to_owl_dynamic.py --watch <json文件> <swrl规则文件> [owl输出文件] [监控间隔秒数]")
            return
        
        json_path = sys.argv[2]
        swrl_rules_path = sys.argv[3]
        output_owl_path = sys.argv[4] if len(sys.argv) > 4 else None
        watch_interval = int(sys.argv[5]) if len(sys.argv) > 5 else 5
        
        watch_and_process(json_path, swrl_rules_path, output_owl_path, watch_interval)
        return
    
    if len(sys.argv) < 3:
        print("用法: python json_to_owl_dynamic.py <json文件路径> <swrl规则文件路径> [输出owl文件路径]")
        print("监控模式: python json_to_owl_dynamic.py --watch <json文件> <swrl规则文件> [owl输出文件] [监控间隔秒数]")
        print("创建测试规则: python json_to_owl_dynamic.py --create-test-rules")
        print("示例: python json_to_owl_dynamic.py input.json pure_swrl_rules.txt output.owl")
        print("\n创建示例文件...")
        create_sample_files()
        return
        
    json_path = sys.argv[1]
    swrl_rules_path = sys.argv[2]
    output_owl_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 检查输入文件
    if not os.path.exists(json_path):
        print(f"[错误] JSON文件不存在: {json_path}")
        return
    
    if not os.path.exists(swrl_rules_path):
        print(f"[错误] SWRL规则文件不存在: {swrl_rules_path}")
        print("使用 --create-test-rules 创建测试规则文件")
        return
    
    # 执行动态推理
    result = json_to_owl(json_path, swrl_rules_path, output_owl_path)
    
    print("\n" + "="*60)
    print("动态推理完成！")
    print("="*60)
    
    if isinstance(result, dict):
        print("推理结果:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        
        print(f"\n💡 提示: 修改 {swrl_rules_path} 文件后重新运行程序，系统会自动使用新的规则")
        print(f"💡 或使用监控模式: python json_to_owl_dynamic.py --watch {json_path} {swrl_rules_path}")
    else:
        print(f"推理失败: {result}")

if __name__ == "__main__":
    main()