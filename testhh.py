#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
隧道结构参数推理系统
使用 Owlready2 和 SWRL 规则进行隧道工程参数推理
"""

import json
import os
from typing import Dict, Any, Optional, List
from owlready2 import *
import tempfile

class TunnelReasoningSystem:
    """隧道结构参数推理系统主类"""
    
    def __init__(self, ontology_file: Optional[str] = None):
        """
        初始化推理系统
        
        Args:
            ontology_file: 现有的 OWL 文件路径，如果为 None 则创建新本体
        """
        self.ontology_file = ontology_file
        self.onto = None
        self.world = World()
        
        if ontology_file and os.path.exists(ontology_file):
            self.load_ontology(ontology_file)
        else:
            self.create_ontology()
    
    def create_ontology(self):
        """创建隧道工程本体"""
        # 创建本体
        self.onto = self.world.get_ontology("http://tunnel-engineering.org/ontology.owl")
        
        with self.onto:
            # 定义基础类
            class TunnelProject(Thing): pass
            class Tunnel(Thing): pass
            class GeologicalCondition(Thing): pass
            class HydrologicalCondition(Thing): pass
            class TunnelType(Thing): pass
            class StructuralParameter(Thing): pass
            class SupportSystem(Thing): pass
            
            # 地质条件子类
            class RockGrade(GeologicalCondition): pass
            class SoilType(GeologicalCondition): pass
            class WeatheringDegree(GeologicalCondition): pass
            
            # 水文条件子类
            class GroundwaterLevel(HydrologicalCondition): pass
            class WaterInflowRate(HydrologicalCondition): pass
            
            # 隧道类型子类
            class RoadTunnel(TunnelType): pass
            class RailwayTunnel(TunnelType): pass
            class MetroTunnel(TunnelType): pass
            class UtilityTunnel(TunnelType): pass
            
            # 结构参数子类
            class LiningThickness(StructuralParameter): pass
            class ExcavationMethod(StructuralParameter): pass
            class SupportDensity(StructuralParameter): pass
            class DrainageSystem(StructuralParameter): pass
            
            # 支护系统子类
            class SteelSupport(SupportSystem): pass
            class ConcreteSupport(SupportSystem): pass
            class RockBolt(SupportSystem): pass
            class ShotcreteSupport(SupportSystem): pass
            
            # 定义数据属性
            class hasRockGrade(DataProperty):
                domain = [Tunnel]
                range = [str]
            
            class hasGroundwaterLevel(DataProperty):
                domain = [Tunnel]
                range = [float]
            
            class hasWaterInflowRate(DataProperty):
                domain = [Tunnel]
                range = [float]
            
            class hasDiameter(DataProperty):
                domain = [Tunnel]
                range = [float]
            
            class hasLength(DataProperty):
                domain = [Tunnel]
                range = [float]
            
            class hasDepth(DataProperty):
                domain = [Tunnel]
                range = [float]
            
            class hasLiningThickness(DataProperty):
                domain = [Tunnel]
                range = [float]
            
            class hasSupportSpacing(DataProperty):
                domain = [Tunnel]
                range = [float]
            
            class hasConcreteStrength(DataProperty):
                domain = [Tunnel]
                range = [str]
            
            class hasDrainageType(DataProperty):
                domain = [Tunnel]
                range = [str]
            
            class hasExcavationMethod(DataProperty):
                domain = [Tunnel]
                range = [str]
            
            # 定义对象属性
            class hasTunnelType(ObjectProperty):
                domain = [Tunnel]
                range = [TunnelType]
            
            class hasGeologicalCondition(ObjectProperty):
                domain = [Tunnel]
                range = [GeologicalCondition]
            
            class hasHydrologicalCondition(ObjectProperty):
                domain = [Tunnel]
                range = [HydrologicalCondition]
            
            class requiresSupportSystem(ObjectProperty):
                domain = [Tunnel]
                range = [SupportSystem]
        
        print("本体创建完成")
        
    def load_ontology(self, file_path: str):
        """加载现有的 OWL 文件"""
        try:
            self.onto = self.world.get_ontology(f"file://{file_path}").load()
            print(f"成功加载本体文件: {file_path}")
        except Exception as e:
            print(f"加载本体文件失败: {e}")
            self.create_ontology()
    
    def add_swrl_rules(self):
        """添加 SWRL 推理规则"""
        
        with self.onto:
            # 规则1: 根据岩石等级确定衬砌厚度
            rule1 = Imp()
            rule1.set_as_rule([
                "Tunnel(?t)",
                "hasRockGrade(?t, 'I')",
                "hasDiameter(?t, ?d)"
            ], [
                "hasLiningThickness(?t, ?thickness)"
            ])
            
            # 规则2: 根据地下水位确定排水系统
            rule2 = Imp()
            rule2.set_as_rule([
                "Tunnel(?t)",
                "hasGroundwaterLevel(?t, ?level)",
                "greaterThan(?level, 5.0)"
            ], [
                "hasDrainageType(?t, 'comprehensive')"
            ])
            
            # 规则3: 根据隧道类型和深度确定开挖方法
            rule3 = Imp()
            rule3.set_as_rule([
                "Tunnel(?t)",
                "hasTunnelType(?t, RoadTunnel)",
                "hasDepth(?t, ?depth)",
                "greaterThan(?depth, 30.0)"
            ], [
                "hasExcavationMethod(?t, 'TBM')"
            ])
            
            # 规则4: 根据水流量和岩石等级确定支护密度
            rule4 = Imp()
            rule4.set_as_rule([
                "Tunnel(?t)",
                "hasWaterInflowRate(?t, ?rate)",
                "hasRockGrade(?t, ?grade)",
                "greaterThan(?rate, 100.0)"
            ], [
                "hasSupportSpacing(?t, 0.8)"
            ])
    
    def create_tunnel_instance(self, tunnel_data: Dict[str, Any]) -> str:
        """
        创建隧道实例
        
        Args:
            tunnel_data: 隧道初始数据字典
            
        Returns:
            创建的隧道实例名称
        """
        tunnel_name = tunnel_data.get('name', 'tunnel_001')
        
        with self.onto:
            # 创建隧道实例
            tunnel = self.onto.Tunnel(tunnel_name)
            
            # 设置基本属性
            if 'rock_grade' in tunnel_data:
                tunnel.hasRockGrade = [tunnel_data['rock_grade']]
            
            if 'groundwater_level' in tunnel_data:
                tunnel.hasGroundwaterLevel = [tunnel_data['groundwater_level']]
            
            if 'water_inflow_rate' in tunnel_data:
                tunnel.hasWaterInflowRate = [tunnel_data['water_inflow_rate']]
            
            if 'diameter' in tunnel_data:
                tunnel.hasDiameter = [tunnel_data['diameter']]
            
            if 'length' in tunnel_data:
                tunnel.hasLength = [tunnel_data['length']]
            
            if 'depth' in tunnel_data:
                tunnel.hasDepth = [tunnel_data['depth']]
            
            # 设置隧道类型
            if 'tunnel_type' in tunnel_data:
                tunnel_type_name = tunnel_data['tunnel_type']
                if tunnel_type_name == 'road':
                    tunnel_type = self.onto.RoadTunnel()
                elif tunnel_type_name == 'railway':
                    tunnel_type = self.onto.RailwayTunnel()
                elif tunnel_type_name == 'metro':
                    tunnel_type = self.onto.MetroTunnel()
                else:
                    tunnel_type = self.onto.UtilityTunnel()
                
                tunnel.hasTunnelType = [tunnel_type]
        
        print(f"隧道实例 '{tunnel_name}' 创建完成")
        return tunnel_name
    
    def execute_reasoning(self):
        """执行推理"""
        try:
            # 使用内置推理器
            with self.onto:
                sync_reasoner_pellet(self.world, infer_property_values=True)
            
            print("推理执行完成")
            return True
            
        except Exception as e:
            print(f"推理执行失败: {e}")
            return False
    
    def get_tunnel_results(self, tunnel_name: str) -> Dict[str, Any]:
        """
        获取隧道推理结果
        
        Args:
            tunnel_name: 隧道实例名称
            
        Returns:
            包含推理结果的字典
        """
        results = {}
        
        try:
            tunnel = getattr(self.onto, tunnel_name)
            
            # 获取输入参数
            results['input_parameters'] = {
                'name': tunnel_name,
                'rock_grade': getattr(tunnel, 'hasRockGrade', [None])[0],
                'groundwater_level': getattr(tunnel, 'hasGroundwaterLevel', [None])[0],
                'water_inflow_rate': getattr(tunnel, 'hasWaterInflowRate', [None])[0],
                'diameter': getattr(tunnel, 'hasDiameter', [None])[0],
                'length': getattr(tunnel, 'hasLength', [None])[0],
                'depth': getattr(tunnel, 'hasDepth', [None])[0],
            }
            
            # 获取推理结果
            results['structural_parameters'] = {
                'lining_thickness': getattr(tunnel, 'hasLiningThickness', [None])[0],
                'support_spacing': getattr(tunnel, 'hasSupportSpacing', [None])[0],
                'concrete_strength': getattr(tunnel, 'hasConcreteStrength', [None])[0],
                'drainage_type': getattr(tunnel, 'hasDrainageType', [None])[0],
                'excavation_method': getattr(tunnel, 'hasExcavationMethod', [None])[0],
            }
            
            # 计算衍生参数
            diameter = results['input_parameters']['diameter']
            if diameter:
                results['derived_parameters'] = {
                    'cross_sectional_area': 3.14159 * (diameter / 2) ** 2,
                    'perimeter': 3.14159 * diameter,
                }
            
        except Exception as e:
            print(f"获取隧道结果失败: {e}")
            results['error'] = str(e)
        
        return results
    
    def export_to_json(self, tunnel_name: str, output_file: str = None) -> str:
        """
        导出结果为 JSON 格式
        
        Args:
            tunnel_name: 隧道实例名称
            output_file: 输出文件路径，如果为 None 则返回 JSON 字符串
            
        Returns:
            JSON 字符串或文件路径
        """
        results = self.get_tunnel_results(tunnel_name)
        
        # 添加时间戳和元数据
        import datetime
        results['metadata'] = {
            'generated_at': datetime.datetime.now().isoformat(),
            'system_version': '1.0',
            'ontology_uri': str(self.onto.base_iri) if self.onto else None
        }
        
        json_str = json.dumps(results, indent=2, ensure_ascii=False)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_str)
            print(f"结果已导出到: {output_file}")
            return output_file
        else:
            return json_str
    
    def save_ontology(self, file_path: str):
        """保存本体到文件"""
        try:
            self.onto.save(file=file_path, format="rdfxml")
            print(f"本体已保存到: {file_path}")
        except Exception as e:
            print(f"保存本体失败: {e}")
    
    def generate_grasshopper_script(self, tunnel_name: str) -> str:
        """
        生成 Grasshopper 脚本代码
        
        Args:
            tunnel_name: 隧道实例名称
            
        Returns:
            Grasshopper Python 脚本代码
        """
        results = self.get_tunnel_results(tunnel_name)
        
        script = f'''
# Grasshopper Python Script for Tunnel Modeling
# Generated from OWL/SWRL Reasoning System

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math

# Tunnel Parameters from Reasoning
tunnel_data = {json.dumps(results, indent=4)}

# Extract parameters
diameter = tunnel_data['input_parameters']['diameter'] or 10.0
length = tunnel_data['input_parameters']['length'] or 100.0
lining_thickness = tunnel_data['structural_parameters']['lining_thickness'] or 0.5

# Create tunnel geometry
def create_tunnel_geometry():
    # Main tunnel cylinder
    center_point = rg.Point3d(0, 0, 0)
    end_point = rg.Point3d(length, 0, 0)
    
    # Outer cylinder
    outer_radius = diameter / 2
    outer_cylinder = rg.Cylinder(
        rg.Circle(center_point, outer_radius),
        length
    )
    
    # Inner cylinder (for lining)
    inner_radius = outer_radius - lining_thickness
    inner_cylinder = rg.Cylinder(
        rg.Circle(center_point, inner_radius),
        length
    )
    
    return outer_cylinder, inner_cylinder

# Execute geometry creation
outer_tunnel, inner_tunnel = create_tunnel_geometry()

# Output for Grasshopper
a = outer_tunnel.ToBrep(True, True)  # Outer tunnel surface
b = inner_tunnel.ToBrep(True, True)  # Inner tunnel surface
c = tunnel_data  # Complete tunnel data
'''
        
        return script


def main():
    """主函数 - 演示完整流程"""
    print("=== 隧道结构参数推理系统演示 ===")
    
    # 1. 初始化系统
    system = TunnelReasoningSystem()
    
    # 2. 添加推理规则
    system.add_swrl_rules()
    
    # 3. 创建隧道实例
    tunnel_data = {
        'name': 'demo_tunnel',
        'rock_grade': 'III',
        'groundwater_level': 8.5,
        'water_inflow_rate': 150.0,
        'diameter': 12.0,
        'length': 500.0,
        'depth': 45.0,
        'tunnel_type': 'road'
    }
    
    tunnel_name = system.create_tunnel_instance(tunnel_data)
    
    # 4. 执行推理
    success = system.execute_reasoning()
    
    if success:
        # 5. 获取结果
        results = system.get_tunnel_results(tunnel_name)
        print("\n=== 推理结果 ===")
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        # 6. 导出为 JSON
        json_output = system.export_to_json(tunnel_name)
        print(f"\n=== JSON 导出完成 ===")
        
        # 7. 生成 Grasshopper 脚本
        gh_script = system.generate_grasshopper_script(tunnel_name)
        print(f"\n=== Grasshopper 脚本已生成 ===")
        print("脚本长度:", len(gh_script), "字符")
        
        # 8. 保存本体
        system.save_ontology("tunnel_ontology.owl")
        
        return system, results
    else:
        print("推理失败")
        return None, None


if __name__ == "__main__":
    # 运行演示
    system, results = main()
    
    # 交互式使用示例
    if system:
        print("\n=== 交互式使用示例 ===")
        print("系统已初始化，可以继续创建更多隧道实例进行推理")
        
        # 创建第二个隧道实例
        tunnel_data_2 = {
            'name': 'metro_tunnel',
            'rock_grade': 'II',
            'groundwater_level': 3.2,
            'water_inflow_rate': 50.0,
            'diameter': 6.5,
            'length': 1200.0,
            'depth': 25.0,
            'tunnel_type': 'metro'
        }
        
        tunnel_name_2 = system.create_tunnel_instance(tunnel_data_2)
        system.execute_reasoning()
        results_2 = system.get_tunnel_results(tunnel_name_2)
        
        print(f"\n第二个隧道 '{tunnel_name_2}' 的推理结果:")
        print(json.dumps(results_2, indent=2, ensure_ascii=False))