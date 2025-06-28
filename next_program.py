import sys
import json
import os
import math
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL

# 定义命名空间
OWL = Namespace("http://www.w3.org/2002/07/owl#")
SWRL = Namespace("http://www.w3.org/2003/11/swrl#")
SWRLA = Namespace("http://swrl.stanford.edu/ontologies/3.3/swrla.owl#")
DLS = Namespace("http://example.com/dlsafe#")

class TunnelSWRLInference:
    """隧道工程SWRL规则推理引擎"""
    
    def __init__(self):
        self.results = {}
        
    def apply_all_rules(self, params):
        """应用所有SWRL规则进行推理"""
        self.results = {}
        
        # 获取基本参数
        tunnel_type = params.get("tunnelType", "TunnelProject")
        rock_grade = params.get("hasGeologicalCondition", "")
        hydro_condition = params.get("hasHydroCondition", "")
        soil_type = params.get("hasSoilType", "")
        tunnel_length = params.get("hasTunnelLength", 0)
        tunnel_diameter = params.get("hasTunnelDiameter", 0)
        
        # 1. 施工方法推理
        self._infer_construction_method(tunnel_length)
        
        # 2. 衬砌厚度推理
        self._infer_lining_thickness(tunnel_type, rock_grade, hydro_condition, soil_type)
        
        # 3. 钢拱架间距推理
        self._infer_steel_arch_spacing(tunnel_type, rock_grade, hydro_condition)
        
        # 4. 钢拱架厚度推理
        self._infer_steel_arch_thickness(rock_grade, hydro_condition)
        
        # 5. 防水层厚度推理
        self._infer_waterproof_thickness(tunnel_type, soil_type, hydro_condition)
        
        # 6. 锚杆长度推理
        self._infer_bolt_length(rock_grade, tunnel_diameter)
        
        # 7. 锚杆间距推理
        if "hasBoltLength" in self.results:
            self._infer_bolt_spacing(self.results["hasBoltLength"])
        
        # 8. 锚杆行列数推理
        if "hasBoltSpacing" in self.results:
            self._infer_bolt_counts(tunnel_length, tunnel_diameter, self.results["hasBoltSpacing"])
        
        # 9. 钢拱架数量推理
        if "hasSteelArchSpacing" in self.results:
            self._infer_steel_arch_count(tunnel_length, self.results["hasSteelArchSpacing"])
        
        return self.results
    
    def _infer_construction_method(self, tunnel_length):
        """推理施工方法 - 规则S01, S02"""
        if tunnel_length > 3000:
            self.results["hasConstructionMethod"] = "DrillAndBlast"
        else:
            self.results["hasConstructionMethod"] = "TBM"
    
    def _infer_lining_thickness(self, tunnel_type, rock_grade, hydro_condition, soil_type):
        """推理衬砌厚度 - 基于149条规则中的衬砌厚度规则"""
        
        # 特殊规则：极差围岩+弱土+富水条件
        if rock_grade == "V" and soil_type == "WeakSoil" and hydro_condition == "water-rich":
            self.results["hasLiningThickness"] = 45.0
            return
        
        # 深埋隧道规则 (S09系列)
        if tunnel_type == "DeepTunnelProject":
            thickness_map = {
                ("I", "dry"): 25.0, ("I", "water-rich"): 27.5,
                ("II", "dry"): 27.5, ("II", "water-rich"): 30.0,
                ("III", "dry"): 30.0, ("III", "water-rich"): 32.5,
                ("IV", "dry"): 32.5, ("IV", "water-rich"): 35.0,
                ("V", "dry"): 35.0, ("V", "water-rich"): 37.5
            }
        
        # 山岭隧道规则 (S06系列)
        elif tunnel_type == "MountainTunnelProject":
            thickness_map = {
                ("I", "dry"): 20.0, ("I", "water-rich"): 22.5,
                ("II", "dry"): 22.5, ("II", "water-rich"): 25.0,
                ("III", "dry"): 25.0, ("III", "water-rich"): 27.5,
                ("IV", "dry"): 27.5, ("IV", "water-rich"): 30.0,
                ("V", "dry"): 30.0, ("V", "water-rich"): 32.5
            }
        
        # 浅埋隧道规则 (S08系列)
        elif tunnel_type == "ShallowTunnelProject":
            thickness_map = {
                ("I", "dry"): 22.5, ("I", "water-rich"): 25.0,
                ("II", "dry"): 25.0, ("II", "water-rich"): 27.5,
                ("III", "dry"): 27.5, ("III", "water-rich"): 30.0,
                ("IV", "dry"): 30.0, ("IV", "water-rich"): 32.5,
                ("V", "dry"): 32.5, ("V", "water-rich"): 35.0
            }
        
        # 水下隧道规则 (S07系列)
        elif tunnel_type == "UnderwaterTunnelProject":
            thickness_map = {
                ("I", "dry"): 25.0, ("I", "water-rich"): 27.5,
                ("II", "dry"): 27.5, ("II", "water-rich"): 30.0,
                ("III", "dry"): 30.0, ("III", "water-rich"): 32.5,
                ("IV", "dry"): 32.5, ("IV", "water-rich"): 35.0,
                ("V", "dry"): 35.0, ("V", "water-rich"): 37.5
            }
        
        # 城市隧道规则 (S05系列)
        elif tunnel_type == "UrbanTunnelProject":
            thickness_map = {
                ("I", "dry"): 22.5, ("I", "water-rich"): 25.0,
                ("II", "dry"): 25.0, ("II", "water-rich"): 27.5,
                ("III", "dry"): 27.5, ("III", "water-rich"): 30.0,
                ("IV", "dry"): 30.0, ("IV", "water-rich"): 32.5,
                ("V", "dry"): 32.5, ("V", "water-rich"): 35.0
            }
        
        # 默认规则
        else:
            thickness_map = {
                ("I", "dry"): 20.0, ("I", "water-rich"): 22.5,
                ("II", "dry"): 22.5, ("II", "water-rich"): 25.0,
                ("III", "dry"): 25.0, ("III", "water-rich"): 27.5,
                ("IV", "dry"): 27.5, ("IV", "water-rich"): 30.0,
                ("V", "dry"): 30.0, ("V", "water-rich"): 32.5
            }
        
        key = (rock_grade, hydro_condition)
        self.results["hasLiningThickness"] = thickness_map.get(key, 25.0)
    
    def _infer_steel_arch_spacing(self, tunnel_type, rock_grade, hydro_condition):
        """推理钢拱架间距 - 基于S10-S14系列规则"""
        
        # 深埋隧道规则 (S14系列)
        if tunnel_type == "DeepTunnelProject":
            spacing_map = {
                ("I", "dry"): 1.2, ("I", "water-rich"): 1.0,
                ("II", "dry"): 1.0, ("II", "water-rich"): 0.8,
                ("III", "dry"): 0.8, ("III", "water-rich"): 0.6,
                ("IV", "dry"): 0.6, ("IV", "water-rich"): 0.5,
                ("V", "dry"): 0.5, ("V", "water-rich"): 0.5
            }
        
        # 山岭隧道规则 (S11系列)
        elif tunnel_type == "MountainTunnelProject":
            spacing_map = {
                ("I", "dry"): 1.4, ("I", "water-rich"): 1.2,
                ("II", "dry"): 1.2, ("II", "water-rich"): 1.0,
                ("III", "dry"): 1.0, ("III", "water-rich"): 0.8,
                ("IV", "dry"): 0.8, ("IV", "water-rich"): 0.6,
                ("V", "dry"): 0.6, ("V", "water-rich"): 0.5
            }
        
        # 浅埋隧道规则 (S13系列)
        elif tunnel_type == "ShallowTunnelProject":
            spacing_map = {
                ("I", "dry"): 1.2, ("I", "water-rich"): 1.0,
                ("II", "dry"): 1.0, ("II", "water-rich"): 0.8,
                ("III", "dry"): 0.8, ("III", "water-rich"): 0.6,
                ("IV", "dry"): 0.6, ("IV", "water-rich"): 0.5,
                ("V", "dry"): 0.5, ("V", "water-rich"): 0.5
            }
        
        # 水下隧道规则 (S12系列)
        elif tunnel_type == "UnderwaterTunnelProject":
            spacing_map = {
                ("I", "dry"): 1.2, ("I", "water-rich"): 1.0,
                ("II", "dry"): 1.0, ("II", "water-rich"): 0.8,
                ("III", "dry"): 0.8, ("III", "water-rich"): 0.6,
                ("IV", "dry"): 0.6, ("IV", "water-rich"): 0.5,
                ("V", "dry"): 0.5, ("V", "water-rich"): 0.5
            }
        
        # 城市隧道规则 (S10系列)
        elif tunnel_type == "UrbanTunnelProject":
            spacing_map = {
                ("I", "dry"): 1.2, ("I", "water-rich"): 1.0,
                ("II", "dry"): 1.0, ("II", "water-rich"): 0.8,
                ("III", "dry"): 0.8, ("III", "water-rich"): 0.6,
                ("IV", "dry"): 0.5, ("IV", "water-rich"): 0.5,
                ("V", "dry"): 0.5, ("V", "water-rich"): 0.5
            }
        
        # 默认规则
        else:
            spacing_map = {
                ("I", "dry"): 1.2, ("I", "water-rich"): 1.0,
                ("II", "dry"): 1.0, ("II", "water-rich"): 0.8,
                ("III", "dry"): 0.8, ("III", "water-rich"): 0.6,
                ("IV", "dry"): 0.6, ("IV", "water-rich"): 0.5,
                ("V", "dry"): 0.5, ("V", "water-rich"): 0.5
            }
        
        key = (rock_grade, hydro_condition)
        self.results["hasSteelArchSpacing"] = spacing_map.get(key, 0.8)
    
    def _infer_steel_arch_thickness(self, rock_grade, hydro_condition):
        """推理钢拱架厚度 - 基于S16系列规则"""
        thickness_map = {
            ("I", "dry"): 6, ("I", "water-rich"): 8,
            ("II", "dry"): 8, ("II", "water-rich"): 10,
            ("III", "dry"): 10, ("III", "water-rich"): 12,
            ("IV", "dry"): 12, ("IV", "water-rich"): 14,
            ("V", "dry"): 14, ("V", "water-rich"): 16
        }
        
        key = (rock_grade, hydro_condition)
        self.results["hasSteelArchThickness"] = thickness_map.get(key, 10)
    
    def _infer_waterproof_thickness(self, tunnel_type, soil_type, hydro_condition):
        """推理防水层厚度 - 基于W01-W05系列规则"""
        
        # 城市隧道 (W01系列)
        if tunnel_type == "UrbanTunnelProject":
            thickness_map = {
                ("MediumSoil", "dry"): 3.0, ("MediumSoil", "water-rich"): 4.0,
                ("StrongSoil", "dry"): 2.5, ("StrongSoil", "water-rich"): 3.5,
                ("WeakSoil", "dry"): 4.0, ("WeakSoil", "water-rich"): 5.0
            }
        
        # 山岭隧道 (W02系列)
        elif tunnel_type == "MountainTunnelProject":
            thickness_map = {
                ("MediumSoil", "dry"): 3.5, ("MediumSoil", "water-rich"): 4.5,
                ("StrongSoil", "dry"): 3.0, ("StrongSoil", "water-rich"): 4.0,
                ("WeakSoil", "dry"): 4.5, ("WeakSoil", "water-rich"): 5.0
            }
        
        # 水下隧道 (W03系列)
        elif tunnel_type == "UnderwaterTunnelProject":
            thickness_map = {
                ("MediumSoil", "water-rich"): 5.5,
                ("StrongSoil", "water-rich"): 5.0,
                ("WeakSoil", "water-rich"): 6.0
            }
        
        # 浅埋隧道 (W04-W05系列)
        elif tunnel_type == "ShallowTunnelProject":
            thickness_map = {
                ("MediumSoil", "dry"): 3.5, ("MediumSoil", "water-rich"): 4.5,
                ("StrongSoil", "dry"): 3.0, ("StrongSoil", "water-rich"): 4.0,
                ("WeakSoil", "dry"): 4.5, ("WeakSoil", "water-rich"): 5.5
            }
        
        # 默认规则
        else:
            thickness_map = {
                ("MediumSoil", "dry"): 3.5, ("MediumSoil", "water-rich"): 4.5,
                ("StrongSoil", "dry"): 3.0, ("StrongSoil", "water-rich"): 4.0,
                ("WeakSoil", "dry"): 4.5, ("WeakSoil", "water-rich"): 5.5
            }
        
        key = (soil_type, hydro_condition)
        self.results["hasWaterproofLayerThickness"] = thickness_map.get(key, 3.5)
    
    def _infer_bolt_length(self, rock_grade, tunnel_diameter):
        """推理锚杆长度 - 基于S03系列规则"""
        if tunnel_diameter <= 0:
            return
            
        # 规则S03系列：锚杆长度与围岩等级的关系
        if rock_grade == "I":
            # L = 0.25 × D
            bolt_length = tunnel_diameter * 0.25
        elif rock_grade == "II":
            # L = 0.3 × D
            bolt_length = tunnel_diameter * 0.3
        elif rock_grade == "III":
            # L = D / 3
            bolt_length = tunnel_diameter / 3
        elif rock_grade == "IV":
            # L = 0.45 × D
            bolt_length = tunnel_diameter * 0.45
        elif rock_grade == "V":
            # L = 0.5 × D
            bolt_length = tunnel_diameter * 0.5
        else:
            bolt_length = tunnel_diameter * 0.3  # 默认值
        
        self.results["hasBoltLength"] = round(bolt_length, 2)
    
    def _infer_bolt_spacing(self, bolt_length):
        """推理锚杆间距 - 规则S04-0：间距=长度/2"""
        bolt_spacing = bolt_length / 2
        self.results["hasBoltSpacing"] = round(bolt_spacing, 2)
    
    def _infer_bolt_counts(self, tunnel_length, tunnel_diameter, bolt_spacing):
        """推理锚杆行列数 - 规则S04-1, S04-2"""
        if bolt_spacing <= 0:
            return
        
        # 计算行数（隧道长度 / 锚杆间距）
        row_count = int(tunnel_length / bolt_spacing)
        self.results["hasBoltRowCount"] = row_count
        
        # 计算列数（圆弧长度 / 间距）
        if tunnel_diameter > 0:
            arc_length = tunnel_diameter * math.pi
            col_count = int(arc_length / bolt_spacing)
            self.results["hasBoltColumnCount"] = col_count
    
    def _infer_steel_arch_count(self, tunnel_length, steel_arch_spacing):
        """推理钢拱架数量 - 规则S15-0"""
        if steel_arch_spacing <= 0:
            return
        
        count = round(tunnel_length / steel_arch_spacing)
        self.results["hasSteelArchCount"] = count


def json_to_owl_inference(json_path, output_json_path=None):
    """
    将JSON隧道参数转换为OWL个体，并应用SWRL规则进行推理
    """
    try:
        # 1. 读取JSON参数
        with open(json_path, 'r', encoding='utf-8') as f:
            params = json.load(f)
        print(f"[推理程序] 已读取JSON参数: {params}")
        
        # 2. 创建SWRL推理引擎
        inference_engine = TunnelSWRLInference()
        
        # 3. 应用所有SWRL规则
        results = inference_engine.apply_all_rules(params)
        
        # 4. 输出JSON结果
        if output_json_path:
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"[推理程序] 已保存推理结果到 {output_json_path}")
            
        return results
        
    except Exception as e:
        print(f"[推理程序] 处理过程中出错: {str(e)}")
        return f"推理失败: {str(e)}"


def create_sample_input():
    """创建示例输入文件"""
    sample_data = {
        "tunnelType": "MountainTunnelProject",
        "hasTunnelLength": 2500,
        "hasTunnelDiameter": 12.0,
        "hasGeologicalCondition": "III",
        "hasHydroCondition": "water-rich",
        "hasSoilType": "MediumSoil"
    }
    
    with open('sample_input.json', 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    print("已创建示例输入文件：sample_input.json")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[推理程序] 用法: python tunnel_swrl_inference.py <json文件路径> [输出json文件路径]")
        print("[推理程序] 示例: python tunnel_swrl_inference.py input.json output.json")
        print("[推理程序] 创建示例输入文件...")
        create_sample_input()
        sys.exit(1)
        
    json_path = sys.argv[1]
    output_json_path = sys.argv[2] if len(sys.argv) > 2 else "swrl_inference_results.json"
    
    # 执行SWRL推理
    result = json_to_owl_inference(json_path, output_json_path)
    
    print("\n[推理程序] SWRL推理完成！")
    print("推理结果:")
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print(result)
        
    sys.exit(0)