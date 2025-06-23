#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
隧道结构参数推理系统 (修复版)
使用 Owlready2 进行隧道工程参数推理
"""

import json
import os
from typing import Dict, Any, Optional, List
from owlready2 import *
import tempfile
import datetime

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
    
    def apply_reasoning_rules(self, tunnel_name: str):
        """
        应用推理规则 - 使用 Python 逻辑而非 SWRL
        
        Args:
            tunnel_name: 隧道实例名称
        """
        try:
            tunnel = getattr(self.onto, tunnel_name)
            
            # 获取隧道基本参数
            rock_grade = getattr(tunnel, 'hasRockGrade', [None])[0] if hasattr(tunnel, 'hasRockGrade') else None
            groundwater_level = getattr(tunnel, 'hasGroundwaterLevel', [None])[0] if hasattr(tunnel, 'hasGroundwaterLevel') else None
            water_inflow_rate = getattr(tunnel, 'hasWaterInflowRate', [None])[0] if hasattr(tunnel, 'hasWaterInflowRate') else None
            diameter = getattr(tunnel, 'hasDiameter', [None])[0] if hasattr(tunnel, 'hasDiameter') else None
            depth = getattr(tunnel, 'hasDepth', [None])[0] if hasattr(tunnel, 'hasDepth') else None
            tunnel_type = getattr(tunnel, 'hasTunnelType', [None])[0] if hasattr(tunnel, 'hasTunnelType') else None
            
            # 规则1: 根据岩石等级和直径确定衬砌厚度
            if rock_grade and diameter:
                lining_thickness = self._calculate_lining_thickness(rock_grade, diameter)
                tunnel.hasLiningThickness = [lining_thickness]
            
            # 规则2: 根据地下水位确定排水系统
            if groundwater_level:
                drainage_type = self._determine_drainage_type(groundwater_level)
                tunnel.hasDrainageType = [drainage_type]
            
            # 规则3: 根据隧道类型和深度确定开挖方法
            if tunnel_type and depth:
                excavation_method = self._determine_excavation_method(tunnel_type, depth)
                tunnel.hasExcavationMethod = [excavation_method]
            
            # 规则4: 根据水流量和岩石等级确定支护间距
            if water_inflow_rate and rock_grade:
                support_spacing = self._calculate_support_spacing(water_inflow_rate, rock_grade)
                tunnel.hasSupportSpacing = [support_spacing]
            
            # 规则5: 根据岩石等级和隧道类型确定混凝土强度
            if rock_grade and tunnel_type:
                concrete_strength = self._determine_concrete_strength(rock_grade, tunnel_type)
                tunnel.hasConcreteStrength = [concrete_strength]
            
            print(f"推理规则应用完成: {tunnel_name}")
            
        except Exception as e:
            print(f"应用推理规则失败: {e}")
    
    def _calculate_lining_thickness(self, rock_grade: str, diameter: float) -> float:
        """计算衬砌厚度"""
        base_thickness = diameter * 0.05  # 基础厚度为直径的5%
        
        grade_factors = {
            'I': 0.8,    # 极好岩石
            'II': 1.0,   # 好岩石
            'III': 1.3,  # 中等岩石
            'IV': 1.6,   # 差岩石
            'V': 2.0     # 极差岩石
        }
        
        factor = grade_factors.get(rock_grade, 1.0)
        return round(base_thickness * factor, 2)
    
    def _determine_drainage_type(self, groundwater_level: float) -> str:
        """确定排水系统类型"""
        if groundwater_level > 10.0:
            return "comprehensive"
        elif groundwater_level > 5.0:
            return "moderate"
        else:
            return "simple"
    
    def _determine_excavation_method(self, tunnel_type, depth: float) -> str:
        """确定开挖方法"""
        type_name = tunnel_type.__class__.__name__ if tunnel_type else "Unknown"
        
        if depth > 50.0:
            return "TBM"
        elif depth > 30.0:
            if type_name in ["RoadTunnel", "RailwayTunnel"]:
                return "TBM"
            else:
                return "NATM"
        elif depth > 15.0:
            return "NATM"
        else:
            return "cut_and_cover"
    
    def _calculate_support_spacing(self, water_inflow_rate: float, rock_grade: str) -> float:
        """计算支护间距"""
        base_spacing = 1.5  # 基础间距
        
        # 根据涌水量调整
        if water_inflow_rate > 200.0:
            water_factor = 0.6
        elif water_inflow_rate > 100.0:
            water_factor = 0.8
        else:
            water_factor = 1.0
        
        # 根据岩石等级调整
        grade_factors = {
            'I': 1.5,
            'II': 1.2,
            'III': 1.0,
            'IV': 0.8,
            'V': 0.6
        }
        
        grade_factor = grade_factors.get(rock_grade, 1.0)
        
        return round(base_spacing * water_factor * grade_factor, 2)
    
    def _determine_concrete_strength(self, rock_grade: str, tunnel_type) -> str:
        """确定混凝土强度等级"""
        type_name = tunnel_type.__class__.__name__ if tunnel_type else "Unknown"
        
        # 基础强度等级
        base_strengths = {
            'I': 'C30',
            'II': 'C35',
            'III': 'C40',
            'IV': 'C45',
            'V': 'C50'
        }
        
        base_strength = base_strengths.get(rock_grade, 'C35')
        
        # 根据隧道类型调整
        if type_name in ["RailwayTunnel", "MetroTunnel"]:
            # 铁路和地铁隧道要求更高强度
            strength_upgrade = {
                'C30': 'C35',
                'C35': 'C40',
                'C40': 'C45',
                'C45': 'C50',
                'C50': 'C55'
            }
            return strength_upgrade.get(base_strength, base_strength)
        
        return base_strength
    
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
    
    def execute_reasoning(self, tunnel_name: str = None):
        """
        执行推理
        
        Args:
            tunnel_name: 特定隧道名称，如果为 None 则对所有隧道执行推理
        """
        try:
            if tunnel_name:
                # 对特定隧道执行推理
                self.apply_reasoning_rules(tunnel_name)
            else:
                # 对所有隧道实例执行推理
                for tunnel in self.onto.Tunnel.instances():
                    self.apply_reasoning_rules(tunnel.name)
            
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
                'rock_grade': getattr(tunnel, 'hasRockGrade', [None])[0] if hasattr(tunnel, 'hasRockGrade') else None,
                'groundwater_level': getattr(tunnel, 'hasGroundwaterLevel', [None])[0] if hasattr(tunnel, 'hasGroundwaterLevel') else None,
                'water_inflow_rate': getattr(tunnel, 'hasWaterInflowRate', [None])[0] if hasattr(tunnel, 'hasWaterInflowRate') else None,
                'diameter': getattr(tunnel, 'hasDiameter', [None])[0] if hasattr(tunnel, 'hasDiameter') else None,
                'length': getattr(tunnel, 'hasLength', [None])[0] if hasattr(tunnel, 'hasLength') else None,
                'depth': getattr(tunnel, 'hasDepth', [None])[0] if hasattr(tunnel, 'hasDepth') else None,
                'tunnel_type': tunnel.hasTunnelType[0].__class__.__name__ if hasattr(tunnel, 'hasTunnelType') and tunnel.hasTunnelType else None
            }
            
            # 获取推理结果
            results['structural_parameters'] = {
                'lining_thickness': getattr(tunnel, 'hasLiningThickness', [None])[0] if hasattr(tunnel, 'hasLiningThickness') else None,
                'support_spacing': getattr(tunnel, 'hasSupportSpacing', [None])[0] if hasattr(tunnel, 'hasSupportSpacing') else None,
                'concrete_strength': getattr(tunnel, 'hasConcreteStrength', [None])[0] if hasattr(tunnel, 'hasConcreteStrength') else None,
                'drainage_type': getattr(tunnel, 'hasDrainageType', [None])[0] if hasattr(tunnel, 'hasDrainageType') else None,
                'excavation_method': getattr(tunnel, 'hasExcavationMethod', [None])[0] if hasattr(tunnel, 'hasExcavationMethod') else None,
            }
            
            # 计算衍生参数
            diameter = results['input_parameters']['diameter']
            length = results['input_parameters']['length']
            lining_thickness = results['structural_parameters']['lining_thickness']
            
            if diameter:
                cross_sectional_area = 3.14159 * (diameter / 2) ** 2
                perimeter = 3.14159 * diameter
                
                results['derived_parameters'] = {
                    'cross_sectional_area': round(cross_sectional_area, 2),
                    'perimeter': round(perimeter, 2),
                }
                
                # 计算材料用量
                if length and lining_thickness:
                    inner_diameter = diameter - 2 * lining_thickness
                    inner_area = 3.14159 * (inner_diameter / 2) ** 2
                    lining_volume = (cross_sectional_area - inner_area) * length
                    
                    results['material_estimates'] = {
                        'concrete_volume_m3': round(lining_volume, 2),
                        'inner_diameter': round(inner_diameter, 2),
                        'excavation_volume_m3': round(cross_sectional_area * length, 2)
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
        results['metadata'] = {
            'generated_at': datetime.datetime.now().isoformat(),
            'system_version': '1.1',
            'ontology_uri': str(self.onto.base_iri) if self.onto else None,
            'reasoning_method': 'Python-based rules'
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
# Generated from OWL-based Reasoning System

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math

# Tunnel Parameters from Reasoning
tunnel_data = {json.dumps(results, indent=4)}

# Extract parameters
diameter = tunnel_data['input_parameters']['diameter'] or 10.0
length = tunnel_data['input_parameters']['length'] or 100.0
lining_thickness = tunnel_data['structural_parameters']['lining_thickness'] or 0.5
support_spacing = tunnel_data['structural_parameters']['support_spacing'] or 1.0

# Create tunnel geometry
def create_tunnel_geometry():
    # Main tunnel cylinder
    center_point = rg.Point3d(0, 0, 0)
    
    # Outer cylinder (excavation boundary)
    outer_radius = diameter / 2
    outer_cylinder = rg.Cylinder(
        rg.Circle(center_point, outer_radius),
        length
    )
    
    # Inner cylinder (tunnel void)
    inner_radius = outer_radius - lining_thickness
    inner_cylinder = rg.Cylinder(
        rg.Circle(center_point, inner_radius),
        length
    )
    
    return outer_cylinder, inner_cylinder

def create_support_rings():
    # Create support ring positions
    support_positions = []
    current_pos = 0
    
    while current_pos < length:
        support_positions.append(current_pos)
        current_pos += support_spacing
    
    # Create support rings
    support_rings = []
    for pos in support_positions:
        ring_center = rg.Point3d(pos, 0, 0)
        ring_plane = rg.Plane(ring_center, rg.Vector3d(1, 0, 0))
        ring_circle = rg.Circle(ring_plane, (diameter / 2) - 0.1)
        support_rings.append(ring_circle)
    
    return support_rings

# Execute geometry creation
outer_tunnel, inner_tunnel = create_tunnel_geometry()
support_rings = create_support_rings()

# Output for Grasshopper
a = outer_tunnel.ToBrep(True, True)  # Outer tunnel surface
b = inner_tunnel.ToBrep(True, True)  # Inner tunnel surface  
c = [ring.ToNurbsCurve() for ring in support_rings]  # Support rings
d = tunnel_data  # Complete tunnel data

# Additional outputs for analysis
excavation_volume = tunnel_data['material_estimates']['excavation_volume_m3'] if 'material_estimates' in tunnel_data else 0
concrete_volume = tunnel_data['material_estimates']['concrete_volume_m3'] if 'material_estimates' in tunnel_data else 0

print(f"Tunnel: {{tunnel_data['input_parameters']['name']}}")
print(f"Excavation Method: {{tunnel_data['structural_parameters']['excavation_method']}}")
print(f"Excavation Volume: {{excavation_volume}} m³")
print(f"Concrete Volume: {{concrete_volume}} m³")
'''
        
        return script
    
    def generate_report(self, tunnel_name: str) -> str:
        """
        生成隧道工程报告
        
        Args:
            tunnel_name: 隧道实例名称
            
        Returns:
            格式化的工程报告
        """
        results = self.get_tunnel_results(tunnel_name)
        
        report = f"""
# 隧道工程设计报告

## 项目信息
- **隧道名称**: {results['input_parameters']['name']}
- **隧道类型**: {results['input_parameters']['tunnel_type']}
- **生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 基本参数
- **直径**: {results['input_parameters']['diameter']} m
- **长度**: {results['input_parameters']['length']} m
- **埋深**: {results['input_parameters']['depth']} m
- **岩石等级**: {results['input_parameters']['rock_grade']}
- **地下水位**: {results['input_parameters']['groundwater_level']} m
- **涌水量**: {results['input_parameters']['water_inflow_rate']} L/min

## 设计参数
- **衬砌厚度**: {results['structural_parameters']['lining_thickness']} m
- **支护间距**: {results['structural_parameters']['support_spacing']} m
- **混凝土强度**: {results['structural_parameters']['concrete_strength']}
- **排水系统**: {results['structural_parameters']['drainage_type']}
- **开挖方法**: {results['structural_parameters']['excavation_method']}

## 工程量估算
"""
        
        if 'material_estimates' in results and results['material_estimates']:
            estimates = results['material_estimates']
            report += f"""
- **开挖土方量**: {estimates['excavation_volume_m3']} m³
- **混凝土用量**: {estimates['concrete_volume_m3']} m³
- **净空直径**: {estimates['inner_diameter']} m
"""
        
        if 'derived_parameters' in results and results['derived_parameters']:
            derived = results['derived_parameters']
            report += f"""
## 几何参数
- **横截面积**: {derived['cross_sectional_area']} m²
- **周长**: {derived['perimeter']} m
"""
        
        return report


def main():
    """主函数 - 演示完整流程"""
    print("=== 隧道结构参数推理系统演示 (修复版) ===")
    
    # 1. 初始化系统
    system = TunnelReasoningSystem()
    
    # 2. 创建隧道实例
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
    
    # 3. 执行推理
    success = system.execute_reasoning(tunnel_name)
    
    if success:
        # 4. 获取结果
        results = system.get_tunnel_results(tunnel_name)
        print("\n=== 推理结果 ===")
        print(json.dumps(results, indent=2, ensure_ascii=False))
        
        # 5. 生成报告
        report = system.generate_report(tunnel_name)
        print("\n=== 工程报告 ===")
        print(report)
        
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
        system.execute_reasoning(tunnel_name_2)
        results_2 = system.get_tunnel_results(tunnel_name_2)
        
        print(f"\n第二个隧道 '{tunnel_name_2}' 的推理结果:")
        print(json.dumps(results_2, indent=2, ensure_ascii=False))
        
        # 生成第二个隧道的报告
        report_2 = system.generate_report(tunnel_name_2)
        print(f"\n第二个隧道的工程报告:")
        print(report_2)