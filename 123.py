from owlready2 import *
import os
import sys
from pathlib import Path

# 配置
ONTOLOGY_FILE = "tunnel_ontology.owl"
NAMESPACE = "http://www.semanticweb.org/tunnel#"

class TunnelOntologyBuilder:
    def __init__(self):
        self.world = World()
        self.onto = None
        
    def create_ontology(self):
        """创建隧道工程本体"""
        print("🏗️ 创建隧道工程本体...")
        
        # 创建本体
        self.onto = self.world.get_ontology(NAMESPACE)
        
        with self.onto:
            # 定义基础类
            class TunnelProject(Thing): pass
            class MountainTunnelProject(TunnelProject): pass
            class UnderwaterTunnelProject(TunnelProject): pass
            class ShallowTunnelProject(TunnelProject): pass
            class DeepTunnelProject(TunnelProject): pass
            
            class GeologicalCondition(Thing): pass
            class HydroCondition(Thing): pass
            class SoilType(Thing): pass
            class ConstructionMethod(Thing): pass
            
            # 输入属性（用于推理的前提条件）
            class hasTunnelLength(DataProperty):
                domain = [TunnelProject]
                range = [float]
                
            class hasTunnelDiameter(DataProperty):
                domain = [TunnelProject]
                range = [float]
                
            class hasGeologicalCondition(ObjectProperty):
                domain = [TunnelProject]
                range = [GeologicalCondition]
                
            class hasHydroCondition(ObjectProperty):
                domain = [TunnelProject]
                range = [HydroCondition]
                
            class hasSoilType(ObjectProperty):
                domain = [TunnelProject]
                range = [SoilType]
            
            # 输出属性（推理结果）
            class hasConstructionMethod(ObjectProperty):
                domain = [TunnelProject]
                range = [ConstructionMethod]
                
            class hasBoltLength(DataProperty):
                domain = [TunnelProject]
                range = [float]
                
            class hasBoltRowCount(DataProperty):
                domain = [TunnelProject]
                range = [int]
                
            class hasBoltColumnCount(DataProperty):
                domain = [TunnelProject]
                range = [int]
                
            class hasLiningThickness(DataProperty):
                domain = [TunnelProject]
                range = [float]
                
            class hasSteelArchSpacing(DataProperty):
                domain = [TunnelProject]
                range = [float]
                
            class hasSteelArchCount(DataProperty):
                domain = [TunnelProject]
                range = [int]
                
            class hasSteelArchThickness(DataProperty):
                domain = [TunnelProject]
                range = [float]
                
            class hasWaterproofLayerThickness(DataProperty):
                domain = [TunnelProject]
                range = [float]
            
            # 创建围岩等级实例
            class RockGrade1(GeologicalCondition): pass  # I级围岩
            class RockGrade2(GeologicalCondition): pass  # II级围岩
            class RockGrade3(GeologicalCondition): pass  # III级围岩
            class RockGrade4(GeologicalCondition): pass  # IV级围岩
            class RockGrade5(GeologicalCondition): pass  # V级围岩
            
            # 创建水文条件实例
            class DryCondition(HydroCondition): pass      # 干燥
            class WetCondition(HydroCondition): pass      # 潮湿
            class WaterBearingCondition(HydroCondition): pass  # 含水
            
            # 创建土壤类型实例
            class HardRock(SoilType): pass
            class SoftRock(SoilType): pass
            class Clay(SoilType): pass
            class Sand(SoilType): pass
            
            # 创建施工方法实例
            class TBMMethod(ConstructionMethod): pass      # 盾构法
            class DrillingBlastingMethod(ConstructionMethod): pass  # 钻爆法
            class CutCoverMethod(ConstructionMethod): pass  # 明挖法
            class PipeJackingMethod(ConstructionMethod): pass  # 顶管法
            
        print("✅ 本体结构创建完成")
        return self.onto
    
    def add_swrl_rules(self):
        """添加SWRL推理规则"""
        print("📝 添加SWRL推理规则...")
        
        with self.onto:
            # 规则1: 山岭隧道 + 硬岩 + 大直径 -> 钻爆法
            rule1 = Imp()
            rule1.set_as_rule([
                MountainTunnelProject(?p), 
                hasGeologicalCondition(?p, ?g), 
                RockGrade1(?g),
                hasTunnelDiameter(?p, ?d),
                GreaterThan(?d, 10)
            ], [
                hasConstructionMethod(?p, DrillingBlastingMethod),
                hasBoltLength(?p, 4.0),
                hasBoltRowCount(?p, 3),
                hasBoltColumnCount(?p, 4),
                hasLiningThickness(?p, 0.4),
                hasSteelArchSpacing(?p, 1.5),
                hasSteelArchThickness(?p, 0.2)
            ])
            
            # 规则2: 水下隧道 -> 盾构法
            rule2 = Imp()
            rule2.set_as_rule([
                UnderwaterTunnelProject(?p),
                hasTunnelDiameter(?p, ?d)
            ], [
                hasConstructionMethod(?p, TBMMethod),
                hasWaterproofLayerThickness(?p, 0.8),
                hasLiningThickness(?p, 0.6)
            ])
            
            # 规则3: 浅埋隧道 -> 明挖法
            rule3 = Imp()
            rule3.set_as_rule([
                ShallowTunnelProject(?p),
                hasTunnelLength(?p, ?l),
                LessThan(?l, 500)
            ], [
                hasConstructionMethod(?p, CutCoverMethod),
                hasLiningThickness(?p, 0.3),
                hasSteelArchSpacing(?p, 1.2)
            ])
            
            # 规则4: 根据围岩等级确定锚杆参数
            rule4 = Imp()
            rule4.set_as_rule([
                TunnelProject(?p),
                hasGeologicalCondition(?p, ?g),
                RockGrade4(?g)
            ], [
                hasBoltLength(?p, 3.0),
                hasBoltRowCount(?p, 4),
                hasBoltColumnCount(?p, 5)
            ])
            
            # 规则5: 含水条件下的防水层厚度
            rule5 = Imp()
            rule5.set_as_rule([
                TunnelProject(?p),
                hasHydroCondition(?p, ?h),
                WaterBearingCondition(?h)
            ], [
                hasWaterproofLayerThickness(?p, 1.0)
            ])
            
        print("✅ SWRL规则添加完成")
    
    def save_ontology(self, filename=None):
        """保存本体到文件"""
        if filename is None:
            filename = ONTOLOGY_FILE
            
        try:
            self.onto.save(file=filename, format="rdfxml")
            print(f"✅ 本体已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")

class TunnelProjectCreator:
    def __init__(self, ontology):
        self.onto = ontology
        
    def create_tunnel_project(self, project_data):
        """创建隧道项目实例"""
        print(f"🚧 创建隧道项目: {project_data['name']}")
        
        with self.onto:
            # 根据隧道类型创建实例
            tunnel_type_mapping = {
                'mountain': MountainTunnelProject,
                'underwater': UnderwaterTunnelProject,
                'shallow': ShallowTunnelProject,
                'deep': DeepTunnelProject
            }
            
            tunnel_class = tunnel_type_mapping.get(project_data['type'], TunnelProject)
            project = tunnel_class(project_data['name'])
            
            # 设置基本属性
            project.hasTunnelLength = [project_data['length']]
            project.hasTunnelDiameter = [project_data['diameter']]
            
            # 设置地质条件
            geological_mapping = {
                'grade1': RockGrade1(),
                'grade2': RockGrade2(),
                'grade3': RockGrade3(),
                'grade4': RockGrade4(),
                'grade5': RockGrade5()
            }
            
            if project_data['geological_condition'] in geological_mapping:
                geo_condition = geological_mapping[project_data['geological_condition']]
                project.hasGeologicalCondition = [geo_condition]
            
            # 设置水文条件
            hydro_mapping = {
                'dry': DryCondition(),
                'wet': WetCondition(),
                'water_bearing': WaterBearingCondition()
            }
            
            if project_data['hydro_condition'] in hydro_mapping:
                hydro_condition = hydro_mapping[project_data['hydro_condition']]
                project.hasHydroCondition = [hydro_condition]
            
            # 设置土壤类型
            soil_mapping = {
                'hard_rock': HardRock(),
                'soft_rock': SoftRock(),
                'clay': Clay(),
                'sand': Sand()
            }
            
            if project_data['soil_type'] in soil_mapping:
                soil_type = soil_mapping[project_data['soil_type']]
                project.hasSoilType = [soil_type]
            
            print(f"✅ 项目创建完成: {project}")
            return project

class TunnelReasoner:
    def __init__(self, ontology):
        self.onto = ontology
        
    def perform_reasoning(self):
        """执行推理"""
        print("🧠 开始SWRL推理...")
        
        try:
            # 执行推理
            with self.onto:
                sync_reasoner_pellet(infer_property_values=True, 
                                   infer_data_property_values=True,
                                   debug=1)
            
            print("✅ 推理完成")
            return True
            
        except Exception as e:
            print(f"❌ 推理失败: {e}")
            if "java" in str(e).lower():
                print("💡 提示: 请确保Java环境正确安装")
            return False
    
    def get_project_results(self, project_name):
        """获取项目的推理结果"""
        print(f"📊 获取项目推理结果: {project_name}")
        
        # 查找项目实例
        project = None
        for individual in self.onto.individuals():
            if individual.name == project_name:
                project = individual
                break
        
        if not project:
            print(f"❌ 未找到项目: {project_name}")
            return None
        
        # 收集结果
        results = {
            'project_name': project_name,
            'input_parameters': {},
            'inferred_parameters': {}
        }
        
        # 输入参数
        if hasattr(project, 'hasTunnelLength') and project.hasTunnelLength:
            results['input_parameters']['tunnel_length'] = project.hasTunnelLength[0]
            
        if hasattr(project, 'hasTunnelDiameter') and project.hasTunnelDiameter:
            results['input_parameters']['tunnel_diameter'] = project.hasTunnelDiameter[0]
        
        # 推理结果
        inference_properties = {
            'hasConstructionMethod': 'construction_method',
            'hasBoltLength': 'bolt_length',
            'hasBoltRowCount': 'bolt_row_count',
            'hasBoltColumnCount': 'bolt_column_count',
            'hasLiningThickness': 'lining_thickness',
            'hasSteelArchSpacing': 'steel_arch_spacing',
            'hasSteelArchCount': 'steel_arch_count',
            'hasSteelArchThickness': 'steel_arch_thickness',
            'hasWaterproofLayerThickness': 'waterproof_layer_thickness'
        }
        
        for prop_name, result_key in inference_properties.items():
            if hasattr(project, prop_name):
                prop_value = getattr(project, prop_name)
                if prop_value:
                    if isinstance(prop_value[0], Thing):
                        results['inferred_parameters'][result_key] = prop_value[0].name
                    else:
                        results['inferred_parameters'][result_key] = prop_value[0]
        
        return results

def display_results(results):
    """显示推理结果"""
    if not results:
        print("❌ 没有结果可显示")
        return
    
    print(f"\n🎯 项目推理结果: {results['project_name']}")
    print("=" * 50)
    
    print("📋 输入参数:")
    for key, value in results['input_parameters'].items():
        print(f"  • {key}: {value}")
    
    print("\n🔍 推理结果:")
    if results['inferred_parameters']:
        for key, value in results['inferred_parameters'].items():
            print(f"  • {key}: {value}")
    else:
        print("  ❌ 未推理出任何参数")

def main():
    print("🚇 隧道工程本体构建与SWRL推理系统")
    print("=" * 60)
    
    # 1. 创建本体
    builder = TunnelOntologyBuilder()
    onto = builder.create_ontology()
    builder.add_swrl_rules()
    builder.save_ontology()
    
    # 2. 创建示例项目
    creator = TunnelProjectCreator(onto)
    
    # 示例项目数据
    project_data = {
        'name': 'TestTunnel1',
        'type': 'mountain',
        'length': 2000.0,
        'diameter': 12.0,
        'geological_condition': 'grade1',
        'hydro_condition': 'water_bearing',
        'soil_type': 'hard_rock'
    }
    
    project = creator.create_tunnel_project(project_data)
    
    # 3. 执行推理
    reasoner = TunnelReasoner(onto)
    reasoning_success = reasoner.perform_reasoning()
    
    # 4. 获取和显示结果
    if reasoning_success:
        results = reasoner.get_project_results('TestTunnel1')
        display_results(results)
    
    print(f"\n📊 系统运行完成")
    print(f"  - 本体创建: ✅")
    print(f"  - 规则添加: ✅") 
    print(f"  - 项目创建: ✅")
    print(f"  - 推理执行: {'✅' if reasoning_success else '❌'}")

if __name__ == "__main__":
    main()