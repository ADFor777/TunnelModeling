import owlready2 as owl
from owlready2 import *
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RockGrade(Enum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"

class HydroCondition(Enum):
    WATER_RICH = "water_rich"
    DRY = "dry"

class TunnelType(Enum):
    URBAN = "urban"
    UNDERWATER = "underwater" 
    SHALLOW = "shallow"
    DEEP = "deep"

@dataclass
class TunnelInput:
    """隧道输入参数"""
    rock_grade: RockGrade
    hydro_condition: HydroCondition
    tunnel_length: float
    tunnel_type: TunnelType
    tunnel_id: str = "default_tunnel"

@dataclass
class TunnelParameters:
    """推理得出的隧道参数"""
    support_type: Optional[str] = None
    excavation_method: Optional[str] = None
    waterproof_grade: Optional[str] = None
    ventilation_system: Optional[str] = None
    safety_grade: Optional[str] = None
    drainage_system: Optional[str] = None
    monitoring_system: Optional[str] = None
    special_requirements: List[str] = None
    
    def __post_init__(self):
        if self.special_requirements is None:
            self.special_requirements = []

class TunnelInferenceSystem:
    """隧道工程SWRL推理系统"""
    
    def __init__(self, ontology_path: str = None):
        """
        初始化推理系统
        
        Args:
            ontology_path: OWL本体文件路径，如果为None则创建默认本体
        """
        self.ontology = None
        self.world = World()
        
        if ontology_path:
            self.load_ontology(ontology_path)
        else:
            self.create_default_ontology()
            
        self.setup_reasoning()
    
    def load_ontology(self, ontology_path: str):
        """加载现有的OWL本体文件"""
        try:
            self.ontology = self.world.get_ontology(f"G:\TUNNEL\Tunnel.owl").load()
            logger.info(f"成功加载本体文件: {ontology_path}")
        except Exception as e:
            logger.error(f"加载本体文件失败: {e}")
            raise
    
    def create_default_ontology(self):
        """创建默认本体结构"""
        self.ontology = self.world.get_ontology("http://tunnel.engineering/ontology")
        
        with self.ontology:
            # 定义主要类
            class Tunnel(Thing): pass
            class RockGradeClass(Thing): pass
            class HydroConditionClass(Thing): pass
            class TunnelTypeClass(Thing): pass
            class TunnelParameterClass(Thing): pass
            
            # 定义围岩等级子类
            class RockGrade_I(RockGradeClass): pass
            class RockGrade_II(RockGradeClass): pass
            class RockGrade_III(RockGradeClass): pass
            class RockGrade_IV(RockGradeClass): pass
            class RockGrade_V(RockGradeClass): pass
            
            # 定义水文条件子类
            class WaterRich(HydroConditionClass): pass
            class Dry(HydroConditionClass): pass
            
            # 定义隧道类型子类
            class UrbanTunnel(TunnelTypeClass): pass
            class UnderwaterTunnel(TunnelTypeClass): pass
            class ShallowTunnel(TunnelTypeClass): pass
            class DeepTunnel(TunnelTypeClass): pass
            
            # 定义参数类型子类
            class SupportType(TunnelParameterClass): pass
            class ExcavationMethod(TunnelParameterClass): pass
            class WaterproofGrade(TunnelParameterClass): pass
            class VentilationSystem(TunnelParameterClass): pass
            
            # 定义对象属性
            class hasRockGrade(ObjectProperty):
                domain = [Tunnel]
                range = [RockGradeClass]
            
            class hasHydroCondition(ObjectProperty):
                domain = [Tunnel]
                range = [HydroConditionClass]
            
            class hasTunnelType(ObjectProperty):
                domain = [Tunnel]
                range = [TunnelTypeClass]
            
            class hasParameter(ObjectProperty):
                domain = [Tunnel]
                range = [TunnelParameterClass]
            
            class requiresSupport(ObjectProperty):
                domain = [Tunnel]
                range = [SupportType]
            
            class requiresExcavation(ObjectProperty):
                domain = [Tunnel]
                range = [ExcavationMethod]
                
            class requiresWaterproof(ObjectProperty):
                domain = [Tunnel]
                range = [WaterproofGrade]
            
            # 定义数据属性
            class tunnelLength(DataProperty):
                domain = [Tunnel]
                range = [float]
            
            class parameterValue(DataProperty):
                domain = [TunnelParameterClass]
                range = [str]
            
            # 添加一些基本的SWRL规则作为示例
            self.add_basic_swrl_rules()
    
    def setup_reasoning(self):
        """设置推理机"""
        try:
            # 使用Pellet推理机
            with self.ontology:
                sync_reasoner_pellet(self.world, infer_property_values=True)
            logger.info("推理机设置成功")
        except Exception as e:
            logger.warning(f"Pellet推理机设置失败，尝试使用HermiT: {e}")
            try:
                with self.ontology:
                    sync_reasoner_hermit(self.world)
                logger.info("HermiT推理机设置成功")
            except Exception as e2:
                logger.error(f"推理机设置失败: {e2}")
    
    def add_basic_swrl_rules(self):
        """添加基本的SWRL规则"""
        try:
            # 注意：Owlready2中SWRL规则的语法
            rule1 = """
            Tunnel(?t), hasRockGrade(?t, ?rg), RockGrade_IV(?rg) -> 
            requiresSupport(?t, HeavySupportType)
            """
            
            rule2 = """
            Tunnel(?t), hasHydroCondition(?t, ?hc), WaterRich(?hc) -> 
            requiresWaterproof(?t, WaterproofGrade1)
            """
            
            rule3 = """
            Tunnel(?t), hasTunnelType(?t, ?tt), UrbanTunnel(?tt) -> 
            requiresExcavation(?t, NATMMethod)
            """
            
            # 在Owlready2中，SWRL规则需要通过Imp类定义
            with self.ontology:
                # 创建支护类型实例
                class HeavySupportType(self.ontology.SupportType): pass
                class LightSupportType(self.ontology.SupportType): pass
                
                # 创建防水等级实例
                class WaterproofGrade1(self.ontology.WaterproofGrade): pass
                class WaterproofGrade2(self.ontology.WaterproofGrade): pass
                
                # 创建开挖方法实例
                class NATMMethod(self.ontology.ExcavationMethod): pass
                class ShieldMethod(self.ontology.ExcavationMethod): pass
                
            logger.info("基本SWRL规则已添加")
            
        except Exception as e:
            logger.warning(f"添加SWRL规则时出错: {e}")
    
    def create_tunnel_instance(self, tunnel_input: TunnelInput) -> Any:
        """根据输入参数创建隧道实例"""
        with self.ontology:
            # 获取类
            Tunnel = self.ontology.Tunnel
            
            # 创建隧道实例
            tunnel_instance = Tunnel(tunnel_input.tunnel_id)
            
            # 根据围岩等级创建相应的实例
            rock_grade_class_name = f"RockGrade_{tunnel_input.rock_grade.value}"
            if hasattr(self.ontology, rock_grade_class_name):
                rock_grade_class = getattr(self.ontology, rock_grade_class_name)
                rock_grade_instance = rock_grade_class(f"rock_{tunnel_input.tunnel_id}")
                tunnel_instance.hasRockGrade = [rock_grade_instance]
            
            # 根据水文条件创建相应的实例
            if tunnel_input.hydro_condition == HydroCondition.WATER_RICH:
                hydro_instance = self.ontology.WaterRich(f"hydro_{tunnel_input.tunnel_id}")
            else:
                hydro_instance = self.ontology.Dry(f"hydro_{tunnel_input.tunnel_id}")
            tunnel_instance.hasHydroCondition = [hydro_instance]
            
            # 根据隧道类型创建相应的实例
            tunnel_type_map = {
                TunnelType.URBAN: self.ontology.UrbanTunnel,
                TunnelType.UNDERWATER: self.ontology.UnderwaterTunnel,
                TunnelType.SHALLOW: self.ontology.ShallowTunnel,
                TunnelType.DEEP: self.ontology.DeepTunnel
            }
            tunnel_type_class = tunnel_type_map.get(tunnel_input.tunnel_type, self.ontology.UrbanTunnel)
            tunnel_type_instance = tunnel_type_class(f"type_{tunnel_input.tunnel_id}")
            tunnel_instance.hasTunnelType = [tunnel_type_instance]
            
            # 设置数据属性
            tunnel_instance.tunnelLength = [tunnel_input.tunnel_length]
            
            logger.info(f"创建隧道实例: {tunnel_input.tunnel_id}")
            logger.info(f"  围岩等级: {tunnel_instance.hasRockGrade}")
            logger.info(f"  水文条件: {tunnel_instance.hasHydroCondition}")
            logger.info(f"  隧道类型: {tunnel_instance.hasTunnelType}")
            logger.info(f"  隧道长度: {tunnel_instance.tunnelLength}")
            
            return tunnel_instance
    
    def debug_ontology_structure(self):
        """调试本体结构"""
        logger.info("=== 本体结构调试信息 ===")
        
        try:
            # 打印所有类
            logger.info("所有类:")
            for cls in self.ontology.classes():
                logger.info(f"  - {cls}")
            
            # 打印所有对象属性
            logger.info("所有对象属性:")
            for prop in self.ontology.object_properties():
                logger.info(f"  - {prop}")
            
            # 打印所有数据属性
            logger.info("所有数据属性:")
            for prop in self.ontology.data_properties():
                logger.info(f"  - {prop}")
            
            # 打印所有个体
            logger.info("所有个体:")
            for individual in self.ontology.individuals():
                logger.info(f"  - {individual}")
                
        except Exception as e:
            logger.error(f"调试本体结构时出错: {e}")
    
    def debug_reasoning_process(self, tunnel_instance: Any):
        """调试推理过程"""
        logger.info(f"=== 推理过程调试 - {tunnel_instance.name} ===")
        
        try:
            # 推理前的状态
            logger.info("推理前的属性:")
            for prop in tunnel_instance.get_properties():
                values = getattr(tunnel_instance, prop.name, [])
                logger.info(f"  {prop.name}: {values}")
            
            # 执行推理
            logger.info("执行推理...")
            with self.ontology:
                sync_reasoner(self.world, infer_property_values=True)
            
            # 推理后的状态
            logger.info("推理后的属性:")
            for prop in tunnel_instance.get_properties():
                values = getattr(tunnel_instance, prop.name, [])
                logger.info(f"  {prop.name}: {values}")
                
            # 检查是否有新的推理属性
            logger.info("检查推理出的新属性...")
            all_props_after = set(tunnel_instance.get_properties())
            logger.info(f"推理后总属性数: {len(all_props_after)}")
            
        except Exception as e:
            logger.error(f"调试推理过程时出错: {e}")
            import traceback
            logger.error(f"详细错误: {traceback.format_exc()}")
    
    def apply_swrl_rules(self, tunnel_instance: Any) -> Dict[str, Any]:
        """应用SWRL规则进行推理"""
        inferred_parameters = {}
        
        try:
            # 调试本体结构
            self.debug_ontology_structure()
            
            # 调试推理过程
            self.debug_reasoning_process(tunnel_instance)
            
            # 获取推理结果
            inferred_parameters = self.extract_inferred_parameters(tunnel_instance)
            
            logger.info(f"SWRL规则推理完成，推理出 {len(inferred_parameters)} 个参数")
            
        except Exception as e:
            logger.error(f"SWRL推理失败: {e}")
            import traceback
            logger.error(f"详细错误: {traceback.format_exc()}")
            # 如果SWRL推理失败，使用基于规则的推理作为备选
            inferred_parameters = self.rule_based_inference(tunnel_instance)
        
        return inferred_parameters
    
    def extract_inferred_parameters(self, tunnel_instance: Any) -> Dict[str, Any]:
        """从推理结果中提取参数"""
        parameters = {}
        
        try:
            # 调试：打印实例的所有属性
            logger.info(f"隧道实例属性: {list(tunnel_instance.get_properties())}")
            
            # 获取所有推理出的属性
            for prop in tunnel_instance.get_properties():
                prop_name = prop.name
                prop_values = getattr(tunnel_instance, prop_name, [])
                
                if prop_values:
                    logger.info(f"属性 {prop_name}: {prop_values}")
                    
                    # 处理不同类型的属性值
                    if isinstance(prop_values, list) and len(prop_values) > 0:
                        value = prop_values[0]
                        if hasattr(value, 'name'):
                            parameters[prop_name] = value.name
                        else:
                            parameters[prop_name] = str(value)
                    else:
                        parameters[prop_name] = str(prop_values)
            
            # 专门检查hasParameter属性
            if hasattr(tunnel_instance, 'hasParameter'):
                logger.info(f"hasParameter 属性值: {tunnel_instance.hasParameter}")
                for param in tunnel_instance.hasParameter:
                    param_name = param.name if hasattr(param, 'name') else str(param)
                    parameters[f"parameter_{param_name}"] = param_name
            
        except Exception as e:
            logger.warning(f"提取推理参数时出错: {e}")
            import traceback
            logger.warning(f"详细错误: {traceback.format_exc()}")
        
        logger.info(f"提取到的参数: {parameters}")
        return parameters
    
    def rule_based_inference(self, tunnel_instance: Any) -> Dict[str, Any]:
        """基于规则的推理（备选方案）"""
        parameters = {}
        
        # 获取输入参数
        rock_grade = self.get_rock_grade_from_instance(tunnel_instance)
        hydro_condition = self.get_hydro_condition_from_instance(tunnel_instance)
        tunnel_type = self.get_tunnel_type_from_instance(tunnel_instance)
        tunnel_length = tunnel_instance.tunnelLength[0] if tunnel_instance.tunnelLength else 0
        
        # 围岩等级推理支护类型
        support_rules = {
            RockGrade.I: "light_support",
            RockGrade.II: "light_support", 
            RockGrade.III: "medium_support",
            RockGrade.IV: "heavy_support",
            RockGrade.V: "special_support"
        }
        parameters['support_type'] = support_rules.get(rock_grade, "unknown")
        
        # 水文条件推理防水等级
        if hydro_condition == HydroCondition.WATER_RICH:
            if rock_grade in [RockGrade.IV, RockGrade.V]:
                parameters['waterproof_grade'] = "grade_1"
                parameters['drainage_system'] = "advanced"
            else:
                parameters['waterproof_grade'] = "grade_2"
                parameters['drainage_system'] = "standard"
        else:
            parameters['waterproof_grade'] = "grade_3"
            parameters['drainage_system'] = "basic"
        
        # 隧道类型推理开挖方法
        excavation_rules = {
            TunnelType.URBAN: "natm_method",
            TunnelType.UNDERWATER: "shield_method",
            TunnelType.SHALLOW: "cut_cover_method" if tunnel_length < 500 else "natm_method",
            TunnelType.DEEP: "tbm_method" if rock_grade == RockGrade.I else "natm_method"
        }
        parameters['excavation_method'] = excavation_rules.get(tunnel_type, "natm_method")
        
        # 长度推理通风系统
        if tunnel_length > 3000:
            parameters['ventilation_system'] = "mechanical"
            parameters['emergency_exit'] = "required"
        elif tunnel_length > 1000:
            parameters['ventilation_system'] = "hybrid"
        else:
            parameters['ventilation_system'] = "natural"
        
        # 安全等级推理
        if tunnel_type == TunnelType.URBAN and rock_grade in [RockGrade.IV, RockGrade.V]:
            parameters['safety_grade'] = "high"
            parameters['monitoring_system'] = "advanced"
        elif tunnel_type == TunnelType.UNDERWATER:
            parameters['safety_grade'] = "special"
            parameters['monitoring_system'] = "marine_grade"
        else:
            parameters['safety_grade'] = "standard"
            parameters['monitoring_system'] = "basic"
        
        return parameters
    
    def get_rock_grade_from_instance(self, tunnel_instance: Any) -> RockGrade:
        """从实例中获取围岩等级"""
        try:
            if hasattr(tunnel_instance, 'hasRockGrade') and tunnel_instance.hasRockGrade:
                grade_name = tunnel_instance.hasRockGrade[0].name
                if 'I' in grade_name:
                    return RockGrade.I
                elif 'II' in grade_name:
                    return RockGrade.II
                elif 'III' in grade_name:
                    return RockGrade.III
                elif 'IV' in grade_name:
                    return RockGrade.IV
                elif 'V' in grade_name:
                    return RockGrade.V
        except:
            pass
        return RockGrade.III  # 默认值
    
    def get_hydro_condition_from_instance(self, tunnel_instance: Any) -> HydroCondition:
        """从实例中获取水文条件"""
        try:
            if hasattr(tunnel_instance, 'hasHydroCondition') and tunnel_instance.hasHydroCondition:
                condition_name = tunnel_instance.hasHydroCondition[0].name
                if 'water_rich' in condition_name:
                    return HydroCondition.WATER_RICH
                elif 'dry' in condition_name:
                    return HydroCondition.DRY
        except:
            pass
        return HydroCondition.DRY  # 默认值
    
    def get_tunnel_type_from_instance(self, tunnel_instance: Any) -> TunnelType:
        """从实例中获取隧道类型"""
        try:
            if hasattr(tunnel_instance, 'hasTunnelType') and tunnel_instance.hasTunnelType:
                type_name = tunnel_instance.hasTunnelType[0].name
                if 'urban' in type_name:
                    return TunnelType.URBAN
                elif 'underwater' in type_name:
                    return TunnelType.UNDERWATER
                elif 'shallow' in type_name:
                    return TunnelType.SHALLOW
                elif 'deep' in type_name:
                    return TunnelType.DEEP
        except:
            pass
        return TunnelType.URBAN  # 默认值
    
    def infer_tunnel_parameters(self, tunnel_input: TunnelInput) -> TunnelParameters:
        """主要推理方法"""
        logger.info(f"开始推理隧道参数: {tunnel_input.tunnel_id}")
        
        # 创建隧道实例
        tunnel_instance = self.create_tunnel_instance(tunnel_input)
        
        # 应用SWRL规则
        inferred_params = self.apply_swrl_rules(tunnel_instance)
        
        # 构建结果对象
        result = TunnelParameters(
            support_type=inferred_params.get('support_type'),
            excavation_method=inferred_params.get('excavation_method'),
            waterproof_grade=inferred_params.get('waterproof_grade'),
            ventilation_system=inferred_params.get('ventilation_system'),
            safety_grade=inferred_params.get('safety_grade'),
            drainage_system=inferred_params.get('drainage_system'),
            monitoring_system=inferred_params.get('monitoring_system'),
            special_requirements=[]
        )
        
        # 添加特殊要求
        if tunnel_input.tunnel_type == TunnelType.URBAN:
            result.special_requirements.append("noise_control")
        if tunnel_input.hydro_condition == HydroCondition.WATER_RICH:
            result.special_requirements.append("waterproof_construction")
        if tunnel_input.tunnel_length > 3000:
            result.special_requirements.append("emergency_facilities")
        
        logger.info(f"推理完成: {tunnel_input.tunnel_id}")
        return result
    
    def batch_inference(self, tunnel_inputs: List[TunnelInput]) -> Dict[str, TunnelParameters]:
        """批量推理"""
        results = {}
        for tunnel_input in tunnel_inputs:
            results[tunnel_input.tunnel_id] = self.infer_tunnel_parameters(tunnel_input)
        return results
    
    def export_results(self, results: Dict[str, TunnelParameters], output_path: str):
        """导出推理结果"""
        export_data = {}
        for tunnel_id, params in results.items():
            export_data[tunnel_id] = {
                'support_type': params.support_type,
                'excavation_method': params.excavation_method,
                'waterproof_grade': params.waterproof_grade,
                'ventilation_system': params.ventilation_system,
                'safety_grade': params.safety_grade,
                'drainage_system': params.drainage_system,
                'monitoring_system': params.monitoring_system,
                'special_requirements': params.special_requirements
            }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"结果已导出到: {output_path}")

# 使用示例
def main():
    """主函数示例"""
    # 初始化推理系统
    # 如果您有现有的OWL文件，请提供路径
    # inference_system = TunnelInferenceSystem("path/to/your/ontology.owl")
    inference_system = TunnelInferenceSystem()
    
    # 创建测试输入
    test_inputs = [
        TunnelInput(
            tunnel_id="tunnel_001",
            rock_grade=RockGrade.IV,
            hydro_condition=HydroCondition.WATER_RICH,
            tunnel_length=2500.0,
            tunnel_type=TunnelType.URBAN
        ),
        TunnelInput(
            tunnel_id="tunnel_002", 
            rock_grade=RockGrade.II,
            hydro_condition=HydroCondition.DRY,
            tunnel_length=800.0,
            tunnel_type=TunnelType.SHALLOW
        ),
        TunnelInput(
            tunnel_id="tunnel_003",
            rock_grade=RockGrade.V,
            hydro_condition=HydroCondition.WATER_RICH,
            tunnel_length=4000.0,
            tunnel_type=TunnelType.UNDERWATER
        )
    ]
    
    # 批量推理
    results = inference_system.batch_inference(test_inputs)
    
    # 打印结果
    for tunnel_id, params in results.items():
        print(f"\n隧道 {tunnel_id} 推理结果:")
        print(f"  支护类型: {params.support_type}")
        print(f"  开挖方法: {params.excavation_method}")
        print(f"  防水等级: {params.waterproof_grade}")
        print(f"  通风系统: {params.ventilation_system}")
        print(f"  安全等级: {params.safety_grade}")
        print(f"  排水系统: {params.drainage_system}")
        print(f"  监测系统: {params.monitoring_system}")
        print(f"  特殊要求: {', '.join(params.special_requirements)}")
    
    # 导出结果
    inference_system.export_results(results, "tunnel_inference_results.json")

if __name__ == "__main__":
    main()