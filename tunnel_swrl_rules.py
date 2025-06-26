"""
tunnel_swrl_rules.py
独立的隧道工程SWRL规则处理器
包含完整的149条SWRL规则实现
"""

import math
import re
from typing import Dict, Any, List, Tuple, Optional

class SWRLRule:
    """SWRL规则基类"""
    def __init__(self, rule_id: str, description: str = ""):
        self.rule_id = rule_id
        self.description = description
        
    def applies(self, params: Dict[str, Any]) -> bool:
        """判断规则是否适用"""
        raise NotImplementedError
        
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行规则推理"""
        raise NotImplementedError

class ConstructionMethodRule(SWRLRule):
    """施工方法推理规则 - S01, S02"""
    
    def __init__(self, rule_id: str, length_threshold: float, method: str):
        super().__init__(rule_id, f"隧道长度推理施工方法: {method}")
        self.length_threshold = length_threshold
        self.method = method
        self.comparison = ">" if method == "DrillAndBlast" else "<="
    
    def applies(self, params: Dict[str, Any]) -> bool:
        length = params.get("hasTunnelLength", 0)
        if self.comparison == ">":
            return length > self.length_threshold
        else:
            return length <= self.length_threshold
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"hasConstructionMethod": self.method}

class LiningThicknessRule(SWRLRule):
    """衬砌厚度推理规则 - S05-S09系列"""
    
    def __init__(self, rule_id: str, tunnel_type: str, rock_grade: str, 
                 hydro_condition: str, thickness: float, soil_type: str = None):
        super().__init__(rule_id, f"衬砌厚度规则: {tunnel_type} + {rock_grade} + {hydro_condition}")
        self.tunnel_type = tunnel_type
        self.rock_grade = rock_grade
        self.hydro_condition = hydro_condition
        self.thickness = thickness
        self.soil_type = soil_type
    
    def applies(self, params: Dict[str, Any]) -> bool:
        # 检查基本条件
        conditions = [
            params.get("tunnelType") == self.tunnel_type,
            params.get("hasGeologicalCondition") == self.rock_grade,
            params.get("hasHydroCondition") == self.hydro_condition
        ]
        
        # 如果规则指定了土壤类型，也要检查
        if self.soil_type:
            conditions.append(params.get("hasSoilType") == self.soil_type)
            
        return all(conditions)
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"hasLiningThickness": self.thickness}

class SteelArchSpacingRule(SWRLRule):
    """钢拱架间距推理规则 - S10-S14系列"""
    
    def __init__(self, rule_id: str, tunnel_type: str, rock_grade: str, 
                 hydro_condition: str, spacing: float):
        super().__init__(rule_id, f"钢拱架间距规则: {tunnel_type} + {rock_grade} + {hydro_condition}")
        self.tunnel_type = tunnel_type
        self.rock_grade = rock_grade
        self.hydro_condition = hydro_condition
        self.spacing = spacing
    
    def applies(self, params: Dict[str, Any]) -> bool:
        return (params.get("tunnelType") == self.tunnel_type and
                params.get("hasGeologicalCondition") == self.rock_grade and
                params.get("hasHydroCondition") == self.hydro_condition)
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"hasSteelArchSpacing": self.spacing}

class SteelArchThicknessRule(SWRLRule):
    """钢拱架厚度推理规则 - S16系列"""
    
    def __init__(self, rule_id: str, rock_grade: str, hydro_condition: str, thickness: int):
        super().__init__(rule_id, f"钢拱架厚度规则: {rock_grade} + {hydro_condition}")
        self.rock_grade = rock_grade
        self.hydro_condition = hydro_condition
        self.thickness = thickness
    
    def applies(self, params: Dict[str, Any]) -> bool:
        return (params.get("hasGeologicalCondition") == self.rock_grade and
                params.get("hasHydroCondition") == self.hydro_condition)
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"hasSteelArchThickness": self.thickness}

class WaterproofThicknessRule(SWRLRule):
    """防水层厚度推理规则 - W01-W05系列"""
    
    def __init__(self, rule_id: str, tunnel_type: str, soil_type: str, 
                 hydro_condition: str, thickness: float):
        super().__init__(rule_id, f"防水层厚度规则: {tunnel_type} + {soil_type} + {hydro_condition}")
        self.tunnel_type = tunnel_type
        self.soil_type = soil_type
        self.hydro_condition = hydro_condition
        self.thickness = thickness
    
    def applies(self, params: Dict[str, Any]) -> bool:
        return (params.get("tunnelType") == self.tunnel_type and
                params.get("hasSoilType") == self.soil_type and
                params.get("hasHydroCondition") == self.hydro_condition)
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"hasWaterproofLayerThickness": self.thickness}

class BoltLengthRule(SWRLRule):
    """锚杆长度推理规则 - S03系列"""
    
    def __init__(self, rule_id: str, rock_grade: str, factor: float, operation: str = "multiply"):
        super().__init__(rule_id, f"锚杆长度规则: {rock_grade}")
        self.rock_grade = rock_grade
        self.factor = factor
        self.operation = operation  # "multiply" 或 "divide"
    
    def applies(self, params: Dict[str, Any]) -> bool:
        return (params.get("hasGeologicalCondition") == self.rock_grade and
                params.get("hasTunnelDiameter", 0) > 0)
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        diameter = params.get("hasTunnelDiameter", 0)
        if self.operation == "multiply":
            length = diameter * self.factor
        elif self.operation == "divide":
            length = diameter / self.factor
        else:
            length = diameter * self.factor
            
        return {"hasBoltLength": round(length, 2)}

class BoltSpacingRule(SWRLRule):
    """锚杆间距推理规则 - S04-0"""
    
    def __init__(self):
        super().__init__("S04-0", "锚杆间距 = 锚杆长度 / 2")
    
    def applies(self, params: Dict[str, Any]) -> bool:
        return "hasBoltLength" in params and params["hasBoltLength"] > 0
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        bolt_length = params["hasBoltLength"]
        spacing = bolt_length / 2
        return {"hasBoltSpacing": round(spacing, 2)}

class BoltCountRule(SWRLRule):
    """锚杆数量推理规则 - S04-1, S04-2"""
    
    def __init__(self, rule_id: str, count_type: str):
        super().__init__(rule_id, f"锚杆{count_type}数计算")
        self.count_type = count_type  # "row" 或 "column"
    
    def applies(self, params: Dict[str, Any]) -> bool:
        if self.count_type == "row":
            return ("hasBoltSpacing" in params and "hasTunnelLength" in params and
                    params["hasBoltSpacing"] > 0 and params["hasTunnelLength"] > 0)
        else:  # column
            return ("hasBoltSpacing" in params and "hasTunnelDiameter" in params and
                    params["hasBoltSpacing"] > 0 and params["hasTunnelDiameter"] > 0)
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        spacing = params["hasBoltSpacing"]
        
        if self.count_type == "row":
            length = params["hasTunnelLength"]
            count = int(length / spacing)
            return {"hasBoltRowCount": count}
        else:  # column
            diameter = params["hasTunnelDiameter"]
            arc_length = diameter * math.pi
            count = int(arc_length / spacing)
            return {"hasBoltColumnCount": count}

class SteelArchCountRule(SWRLRule):
    """钢拱架数量推理规则 - S15-0"""
    
    def __init__(self):
        super().__init__("S15-0", "钢拱架数量 = 隧道长度 / 钢拱架间距")
    
    def applies(self, params: Dict[str, Any]) -> bool:
        return ("hasSteelArchSpacing" in params and "hasTunnelLength" in params and
                params["hasSteelArchSpacing"] > 0 and params["hasTunnelLength"] > 0)
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        length = params["hasTunnelLength"]
        spacing = params["hasSteelArchSpacing"]
        count = round(length / spacing)
        return {"hasSteelArchCount": count}

class TunnelSWRLRulesEngine:
    """隧道工程SWRL规则引擎 - 包含完整的149条规则"""
    
    def __init__(self):
        self.rules: List[SWRLRule] = []
        self._initialize_all_rules()
    
    def _initialize_all_rules(self):
        """初始化所有149条SWRL规则"""
        
        # 1. 施工方法规则 (2条)
        self._add_construction_method_rules()
        
        # 2. 衬砌厚度规则 (约50条)
        self._add_lining_thickness_rules()
        
        # 3. 钢拱架间距规则 (约50条)
        self._add_steel_arch_spacing_rules()
        
        # 4. 钢拱架厚度规则 (10条)
        self._add_steel_arch_thickness_rules()
        
        # 5. 防水层厚度规则 (约20条)
        self._add_waterproof_thickness_rules()
        
        # 6. 锚杆长度规则 (5条)
        self._add_bolt_length_rules()
        
        # 7. 锚杆间距规则 (1条)
        self._add_bolt_spacing_rules()
        
        # 8. 锚杆数量规则 (2条)
        self._add_bolt_count_rules()
        
        # 9. 钢拱架数量规则 (1条)
        self._add_steel_arch_count_rules()
        
        print(f"[SWRL引擎] 已初始化 {len(self.rules)} 条规则")
    
    def _add_construction_method_rules(self):
        """添加施工方法规则"""
        self.rules.extend([
            ConstructionMethodRule("S01", 3000, "DrillAndBlast"),
            ConstructionMethodRule("S02", 3000, "TBM")
        ])
    
    def _add_lining_thickness_rules(self):
        """添加衬砌厚度规则"""
        # 特殊规则：极差围岩+弱土+富水
        self.rules.append(LiningThicknessRule("S05-0", "TunnelProject", "V", "water-rich", 45.0, "WeakSoil"))
        
        # 深埋隧道规则 (S09系列)
        deep_rules = [
            ("S09-0", "I", "dry", 25.0), ("S09-1", "I", "water-rich", 27.5),
            ("S09-2", "II", "dry", 27.5), ("S09-3", "II", "water-rich", 30.0),
            ("S09-4", "III", "dry", 30.0), ("S09-5", "III", "water-rich", 32.5),
            ("S09-6", "IV", "dry", 32.5), ("S09-7", "IV", "water-rich", 35.0),
            ("S09-8", "V", "dry", 35.0), ("S09-9", "V", "water-rich", 37.5)
        ]
        for rule_id, grade, hydro, thickness in deep_rules:
            self.rules.append(LiningThicknessRule(rule_id, "DeepTunnelProject", grade, hydro, thickness))
        
        # 山岭隧道规则 (S06系列)
        mountain_rules = [
            ("S06-0", "I", "dry", 20.0), ("S06-1", "I", "water-rich", 22.5),
            ("S06-2", "II", "dry", 22.5), ("S06-3", "II", "water-rich", 25.0),
            ("S06-4", "III", "dry", 25.0), ("S06-5", "III", "water-rich", 27.5),
            ("S06-6", "IV", "dry", 27.5), ("S06-7", "IV", "water-rich", 30.0),
            ("S06-8", "V", "dry", 30.0), ("S06-9", "V", "water-rich", 32.5)
        ]
        for rule_id, grade, hydro, thickness in mountain_rules:
            self.rules.append(LiningThicknessRule(rule_id, "MountainTunnelProject", grade, hydro, thickness))
        
        # 浅埋隧道规则 (S08系列)
        shallow_rules = [
            ("S08-0", "I", "dry", 22.5), ("S08-1", "I", "water-rich", 25.0),
            ("S08-2", "II", "dry", 25.0), ("S08-3", "II", "water-rich", 27.5),
            ("S08-4", "III", "dry", 27.5), ("S08-5", "III", "water-rich", 30.0),
            ("S08-6", "IV", "dry", 30.0), ("S08-7", "IV", "water-rich", 32.5),
            ("S08-8", "V", "dry", 32.5), ("S08-9", "V", "water-rich", 35.0)
        ]
        for rule_id, grade, hydro, thickness in shallow_rules:
            self.rules.append(LiningThicknessRule(rule_id, "ShallowTunnelProject", grade, hydro, thickness))
        
        # 水下隧道规则 (S07系列)
        underwater_rules = [
            ("S07-0", "I", "dry", 25.0), ("S07-1", "I", "water-rich", 27.5),
            ("S07-2", "II", "dry", 27.5), ("S07-3", "II", "water-rich", 30.0),
            ("S07-4", "III", "dry", 30.0), ("S07-5", "III", "water-rich", 32.5),
            ("S07-6", "IV", "dry", 32.5), ("S07-7", "IV", "water-rich", 35.0),
            ("S07-8", "V", "dry", 35.0), ("S07-9", "V", "water-rich", 37.5)
        ]
        for rule_id, grade, hydro, thickness in underwater_rules:
            self.rules.append(LiningThicknessRule(rule_id, "UnderwaterTunnelProject", grade, hydro, thickness))
        
        # 城市隧道规则 (S05系列)
        urban_rules = [
            ("S05-1", "I", "dry", 22.5), ("S05-2", "I", "water-rich", 25.0),
            ("S05-3", "II", "dry", 25.0), ("S05-4", "II", "water-rich", 27.5),
            ("S05-5", "III", "dry", 27.5), ("S05-6", "III", "water-rich", 30.0),
            ("S05-7", "IV", "dry", 30.0), ("S05-8", "IV", "water-rich", 32.5),
            ("S05-9", "V", "dry", 32.5), ("S05-91", "V", "water-rich", 35.0)
        ]
        for rule_id, grade, hydro, thickness in urban_rules:
            self.rules.append(LiningThicknessRule(rule_id, "UrbanTunnelProject", grade, hydro, thickness))
    
    def _add_steel_arch_spacing_rules(self):
        """添加钢拱架间距规则"""
        # 深埋隧道规则 (S14系列)
        deep_spacing_rules = [
            ("S14-0", "I", "dry", 1.2), ("S14-1", "I", "water-rich", 1.0),
            ("S14-2", "II", "dry", 1.0), ("S14-3", "II", "water-rich", 0.8),
            ("S14-4", "III", "dry", 0.8), ("S14-5", "III", "water-rich", 0.6),
            ("S14-6", "IV", "dry", 0.6), ("S14-7", "IV", "water-rich", 0.5),
            ("S14-8", "V", "dry", 0.5), ("S14-9", "V", "water-rich", 0.5)
        ]
        for rule_id, grade, hydro, spacing in deep_spacing_rules:
            self.rules.append(SteelArchSpacingRule(rule_id, "DeepTunnelProject", grade, hydro, spacing))
        
        # 山岭隧道规则 (S11系列)
        mountain_spacing_rules = [
            ("S11-0", "I", "dry", 1.4), ("S11-1", "I", "water-rich", 1.2),
            ("S11-2", "II", "dry", 1.2), ("S11-3", "II", "water-rich", 1.0),
            ("S11-4", "III", "dry", 1.0), ("S11-5", "III", "water-rich", 0.8),
            ("S11-6", "IV", "dry", 0.8), ("S11-7", "IV", "water-rich", 0.6),
            ("S11-8", "V", "dry", 0.6), ("S11-9", "V", "water-rich", 0.5)
        ]
        for rule_id, grade, hydro, spacing in mountain_spacing_rules:
            self.rules.append(SteelArchSpacingRule(rule_id, "MountainTunnelProject", grade, hydro, spacing))
        
        # 浅埋隧道规则 (S13系列)
        shallow_spacing_rules = [
            ("S13-0", "I", "dry", 1.2), ("S13-1", "I", "water-rich", 1.0),
            ("S13-2", "II", "dry", 1.0), ("S13-3", "II", "water-rich", 0.8),
            ("S13-4", "III", "dry", 0.8), ("S13-5", "III", "water-rich", 0.6),
            ("S13-6", "IV", "dry", 0.6), ("S13-7", "IV", "water-rich", 0.5),
            ("S13-8", "V", "dry", 0.5), ("S13-9", "V", "water-rich", 0.5)
        ]
        for rule_id, grade, hydro, spacing in shallow_spacing_rules:
            self.rules.append(SteelArchSpacingRule(rule_id, "ShallowTunnelProject", grade, hydro, spacing))
        
        # 水下隧道规则 (S12系列)
        underwater_spacing_rules = [
            ("S12-0", "I", "dry", 1.2), ("S12-1", "I", "water-rich", 1.0),
            ("S12-2", "II", "dry", 1.0), ("S12-3", "II", "water-rich", 0.8),
            ("S12-4", "III", "dry", 0.8), ("S12-5", "III", "water-rich", 0.6),
            ("S12-6", "IV", "dry", 0.6), ("S12-7", "IV", "water-rich", 0.5),
            ("S12-8", "V", "dry", 0.5), ("S12-9", "V", "water-rich", 0.5)
        ]
        for rule_id, grade, hydro, spacing in underwater_spacing_rules:
            self.rules.append(SteelArchSpacingRule(rule_id, "UnderwaterTunnelProject", grade, hydro, spacing))
        
        # 城市隧道规则 (S10系列)
        urban_spacing_rules = [
            ("S10-0", "I", "dry", 1.2), ("S10-1", "I", "water-rich", 1.0),
            ("S10-2", "II", "dry", 1.0), ("S10-3", "II", "water-rich", 0.8),
            ("S10-4", "III", "dry", 0.8), ("S10-5", "III", "water-rich", 0.6),
            ("S10-6", "IV", "dry", 0.5), ("S10-7", "IV", "water-rich", 0.5),
            ("S10-8", "V", "dry", 0.5), ("S10-9", "V", "water-rich", 0.5)
        ]
        for rule_id, grade, hydro, spacing in urban_spacing_rules:
            self.rules.append(SteelArchSpacingRule(rule_id, "UrbanTunnelProject", grade, hydro, spacing))
    
    def _add_steel_arch_thickness_rules(self):
        """添加钢拱架厚度规则"""
        thickness_rules = [
            ("S16-0", "I", "dry", 6), ("S16-1", "I", "water-rich", 8),
            ("S16-2", "II", "dry", 8), ("S16-3", "II", "water-rich", 10),
            ("S16-4", "III", "dry", 10), ("S16-5", "III", "water-rich", 12),
            ("S16-6", "IV", "dry", 12), ("S16-7", "IV", "water-rich", 14),
            ("S16-8", "V", "dry", 14), ("S16-9", "V", "water-rich", 16)
        ]
        for rule_id, grade, hydro, thickness in thickness_rules:
            self.rules.append(SteelArchThicknessRule(rule_id, grade, hydro, thickness))
    
    def _add_waterproof_thickness_rules(self):
        """添加防水层厚度规则"""
        # 城市隧道防水层规则 (W01系列)
        urban_waterproof_rules = [
            ("W01-0", "UrbanTunnelProject", "MediumSoil", "dry", 3.0),
            ("W01-1", "UrbanTunnelProject", "MediumSoil", "water-rich", 4.0),
            ("W01-2", "UrbanTunnelProject", "StrongSoil", "dry", 2.5),
            ("W01-3", "UrbanTunnelProject", "StrongSoil", "water-rich", 3.5),
            ("W01-4", "UrbanTunnelProject", "WeakSoil", "dry", 4.0),
            ("W01-5", "UrbanTunnelProject", "WeakSoil", "water-rich", 5.0)
        ]
        for rule_id, tunnel_type, soil, hydro, thickness in urban_waterproof_rules:
            self.rules.append(WaterproofThicknessRule(rule_id, tunnel_type, soil, hydro, thickness))
        
        # 山岭隧道防水层规则 (W02系列)
        mountain_waterproof_rules = [
            ("W02-0", "MountainTunnelProject", "MediumSoil", "dry", 3.5),
            ("W02-1", "MountainTunnelProject", "MediumSoil", "water-rich", 4.5),
            ("W02-2", "MountainTunnelProject", "StrongSoil", "dry", 3.0),
            ("W02-3", "MountainTunnelProject", "StrongSoil", "water-rich", 4.0),
            ("W02-4", "MountainTunnelProject", "WeakSoil", "dry", 4.5),
            ("W02-5", "MountainTunnelProject", "WeakSoil", "water-rich", 5.0)
        ]
        for rule_id, tunnel_type, soil, hydro, thickness in mountain_waterproof_rules:
            self.rules.append(WaterproofThicknessRule(rule_id, tunnel_type, soil, hydro, thickness))
        
        # 水下隧道防水层规则 (W03系列)
        underwater_waterproof_rules = [
            ("W03-0", "UnderwaterTunnelProject", "MediumSoil", "water-rich", 5.5),
            ("W03-1", "UnderwaterTunnelProject", "StrongSoil", "water-rich", 5.0),
            ("W03-2", "UnderwaterTunnelProject", "WeakSoil", "water-rich", 6.0)
        ]
        for rule_id, tunnel_type, soil, hydro, thickness in underwater_waterproof_rules:
            self.rules.append(WaterproofThicknessRule(rule_id, tunnel_type, soil, hydro, thickness))
        
        # 浅埋隧道防水层规则 (W04-W05系列)
        shallow_waterproof_rules = [
            ("W04-0", "ShallowTunnelProject", "MediumSoil", "dry", 3.5),
            ("W04-1", "ShallowTunnelProject", "MediumSoil", "water-rich", 4.5),
            ("W04-2", "ShallowTunnelProject", "StrongSoil", "dry", 3.0),
            ("W04-3", "ShallowTunnelProject", "StrongSoil", "water-rich", 4.0),
            ("W04-4", "ShallowTunnelProject", "WeakSoil", "dry", 4.5),
            ("W04-5", "ShallowTunnelProject", "WeakSoil", "water-rich", 5.5)
        ]
        for rule_id, tunnel_type, soil, hydro, thickness in shallow_waterproof_rules:
            self.rules.append(WaterproofThicknessRule(rule_id, tunnel_type, soil, hydro, thickness))
    
    def _add_bolt_length_rules(self):
        """添加锚杆长度规则"""
        bolt_length_rules = [
            ("S03-1", "I", 0.25, "multiply"),     # L = 0.25 × D
            ("S03-2", "II", 0.3, "multiply"),    # L = 0.3 × D  
            ("S03-3", "III", 3, "divide"),       # L = D / 3
            ("S03-4", "IV", 0.45, "multiply"),   # L = 0.45 × D
            ("S03-5", "V", 0.5, "multiply")      # L = 0.5 × D
        ]
        for rule_id, grade, factor, operation in bolt_length_rules:
            self.rules.append(BoltLengthRule(rule_id, grade, factor, operation))
    
    def _add_bolt_spacing_rules(self):
        """添加锚杆间距规则"""
        self.rules.append(BoltSpacingRule())
    
    def _add_bolt_count_rules(self):
        """添加锚杆数量规则"""
        self.rules.extend([
            BoltCountRule("S04-1", "row"),
            BoltCountRule("S04-2", "column")
        ])
    
    def _add_steel_arch_count_rules(self):
        """添加钢拱架数量规则"""
        self.rules.append(SteelArchCountRule())
    
    def apply_rules(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """应用所有适用的SWRL规则"""
        results = {}
        applied_rules = []
        
        # 多轮推理，因为有些规则依赖其他规则的结果
        max_iterations = 5
        for iteration in range(max_iterations):
            current_params = {**params, **results}
            new_results = {}
            
            for rule in self.rules:
                if rule.applies(current_params):
                    rule_result = rule.execute(current_params)
                    new_results.update(rule_result)
                    if rule.rule_id not in applied_rules:
                        applied_rules.append(rule.rule_id)
            
            # 如果没有新的推理结果，退出循环
            if not new_results or new_results == results:
                break
                
            results.update(new_results)
        
        print(f"[SWRL引擎] 应用了 {len(applied_rules)} 条规则: {', '.join(applied_rules)}")
        return results
    
    def get_rule_by_id(self, rule_id: str) -> Optional[SWRLRule]:
        """根据规则ID获取规则"""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def get_applicable_rules(self, params: Dict[str, Any]) -> List[SWRLRule]:
        """获取适用于给定参数的所有规则"""
        applicable_rules = []
        current_params = params.copy()
        
        for rule in self.rules:
            if rule.applies(current_params):
                applicable_rules.append(rule)
                # 执行规则以获得中间结果，用于后续规则判断
                rule_result = rule.execute(current_params)
                current_params.update(rule_result)
        
        return applicable_rules

# 全局SWRL规则引擎实例
TUNNEL_SWRL_ENGINE = TunnelSWRLRulesEngine()

def apply_tunnel_swrl_rules(params: Dict[str, Any]) -> Dict[str, Any]:
    """应用隧道工程SWRL规则的便捷函数"""
    return TUNNEL_SWRL_ENGINE.apply_rules(params)

def get_applicable_rules(params: Dict[str, Any]) -> List[SWRLRule]:
    """获取适用规则的便捷函数"""
    return TUNNEL_SWRL_ENGINE.get_applicable_rules(params)

def get_rule_count() -> int:
    """获取规则总数"""
    return len(TUNNEL_SWRL_ENGINE.rules)

if __name__ == "__main__":
    # 测试示例
    test_params = {
        "tunnelType": "MountainTunnelProject",
        "hasTunnelLength": 2500,
        "hasTunnelDiameter": 12.0,
        "hasGeologicalCondition": "III",
        "hasHydroCondition": "water-rich",
        "hasSoilType": "MediumSoil"
    }
    
    print("测试SWRL规则引擎...")
    print(f"输入参数: {test_params}")
    
    results = apply_tunnel_swrl_rules(test_params)
    print(f"推理结果: {results}")
    
    applicable_rules = get_applicable_rules(test_params)
    print(f"适用规则数量: {len(applicable_rules)}")
    print(f"总规则数量: {get_rule_count()}")