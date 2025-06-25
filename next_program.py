import sys
import json
import os
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
from owlrl import OWLRL

# 定义命名空间
OWL = Namespace("http://www.w3.org/2002/07/owl#")
SWRL = Namespace("http://www.w3.org/2003/11/swrl#")
SWRLA = Namespace("http://swrl.stanford.edu/ontologies/3.3/swrla.owl#")
DLS = Namespace("http://example.com/dlsafe#")  # 假设的本体命名空间

def json_to_owl(json_path, swrl_rules_path, output_owl_path=None):
    """
    将JSON隧道参数转换为OWL个体，并应用SWRL规则进行推理
    
    Args:
        json_path: JSON参数文件路径
        swrl_rules_path: SWRL规则文件路径
        output_owl_path: 输出OWL文件路径（可选）
    """
    try:
        # 1. 读取JSON参数
        with open(json_path, 'r', encoding='utf-8') as f:
            params = json.load(f)
        print(f"[推理程序] 已读取JSON参数: {params}")
        
        # 2. 创建OWL图
        g = Graph()
        
        # 3. 添加命名空间声明
        g.bind("owl", OWL)
        g.bind("rdf", RDF)
        g.bind("rdfs", RDFS)
        g.bind("swrl", SWRL)
        g.bind("swrla", SWRLA)
        g.bind("dls", DLS)
        
        # 4. 创建隧道项目个体
        tunnel_individual = URIRef("http://example.com/tunnel/1")
        
        # 添加隧道类型
        if params.get("tunnelType"):
            tunnel_type = params["tunnelType"]
            # 映射到本体中的类
            class_map = {
                "MountainTunnelProject": DLS.MountainTunnelProject,
                "UnderwaterTunnelProject": DLS.UnderwaterTunnelProject,
                "ShallowTunnelProject": DLS.ShallowTunnelProject,
                "DeepTunnelProject": DLS.DeepTunnelProject
            }
            ontology_class = class_map.get(tunnel_type, DLS.TunnelProject)
            g.add((tunnel_individual, RDF.type, ontology_class))
        else:
            g.add((tunnel_individual, RDF.type, DLS.TunnelProject))
        
        # 5. 添加隧道参数作为个体属性
        if params.get("hasTunnelLength"):
            g.add((tunnel_individual, DLS.hasTunnelLength, 
                  Literal(params["hasTunnelLength"], datatype=XSD.float)))
        
        if params.get("hasTunnelDiameter"):
            g.add((tunnel_individual, DLS.hasTunnelDiameter, 
                  Literal(params["hasTunnelDiameter"], datatype=XSD.float)))
        
        # 添加土壤类型
        if params.get("hasSoilType"):
            soil_type = params["hasSoilType"]
            # 映射到本体中的个体
            soil_map = {
                "StrongSoil": DLS.StrongSoil,
                "WeakSoil": DLS.WeakSoil,
                "MediumSoil": DLS.MediumSoil
            }
            soil_individual = soil_map.get(soil_type, DLS.UnknownSoil)
            g.add((tunnel_individual, DLS.hasSoilType, soil_individual))
        
        # 添加水文条件
        if params.get("hasHydroCondition"):
            hydro_condition = params["hasHydroCondition"]
            # 映射到本体中的个体
            hydro_map = {
                "water-rich": DLS.WaterRich,
                "dry": DLS.Dry
            }
            hydro_individual = hydro_map.get(hydro_condition, DLS.UnknownHydroCondition)
            g.add((tunnel_individual, DLS.hasHydroCondition, hydro_individual))
        
        # 添加围岩等级
        if params.get("hasGeologicalCondition"):
            rock_grade = params["hasGeologicalCondition"]
            # 映射到本体中的个体
            grade_map = {
                "I": DLS.RockGradeI,
                "II": DLS.RockGradeII,
                "III": DLS.RockGradeIII,
                "IV": DLS.RockGradeIV,
                "V": DLS.RockGradeV,
                "VI": DLS.RockGradeVI
            }
            grade_individual = grade_map.get(rock_grade, DLS.UnknownRockGrade)
            g.add((tunnel_individual, DLS.hasGeologicalCondition, grade_individual))
        
        # 6. 加载SWRL规则
        with open(swrl_rules_path, 'r', encoding='utf-8') as f:
            swrl_rules = f.read()
        
        # 将SWRL规则添加到图中
        g.parse(data=swrl_rules, format='xml')
        print(f"[推理程序] 已加载SWRL规则")
        
        # 7. 执行OWLRL推理
        OWLRL.infer(g)
        print(f"[推理程序] 已完成OWLRL推理")
        
        # 8. 保存包含推理结果的OWL文件（如果指定）
        if output_owl_path:
            g.serialize(destination=output_owl_path, format='xml')
            print(f"[推理程序] 已保存推理结果到 {output_owl_path}")
        
        # 9. 提取推理结果
        results = extract_inference_results(g, tunnel_individual)
        return results
        
    except Exception as e:
        print(f"[推理程序] 处理过程中出错: {str(e)}")
        return f"推理失败: {str(e)}"

def extract_inference_results(graph, tunnel_individual):
    """从图中提取推理结果"""
    results = []
    
    # 提取防水层厚度推理结果
    for s, p, o in graph.triples((tunnel_individual, DLS.hasWaterproofLayerThickness, None)):
        results.append(f"防水层厚度: {o} 毫米")
    
    # 提取其他推理结果
    for s, p, o in graph.triples((tunnel_individual, RDF.type, None)):
        if o not in [DLS.TunnelProject, DLS.MountainTunnelProject, 
                     DLS.UnderwaterTunnelProject, DLS.ShallowTunnelProject, DLS.DeepTunnelProject]:
            results.append(f"推理出的类别: {o.split('#')[-1]}")
    
    if not results:
        return "未发现推理结果"
    
    return "推理结果:\n" + "\n".join(results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[推理程序] 用法: python next_program.py <json文件路径> [输出owl文件路径]")
        print("[推理程序] 注意: SWRL规则文件应放在当前目录下，命名为 pure_swrl_rules.n3")
        sys.exit(1)
    
    json_path = sys.argv[1]
    swrl_rules_path = "pure_swrl_rules.n3"  # 假设规则文件在当前目录
    output_owl_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = json_to_owl(json_path, swrl_rules_path, output_owl_path)
    print(result)
    sys.exit(0)