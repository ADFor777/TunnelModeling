"""
dynamic_swrl_loader.py
动态SWRL规则加载器
实时读取pure_swrl_rules.txt文件，支持规则文件的热更新
"""

import os
import re
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

class DynamicSWRLLoader:
    """动态SWRL规则加载器"""
    
    def __init__(self, rules_file_path: str = "pure_swrl_rules.txt"):
        self.rules_file_path = rules_file_path
        self.last_modified = 0
        self.cached_rules = []
        self.rule_count = 0
        self.last_load_time = None
        
        # 首次加载
        self.reload_rules_if_changed()
    
    def reload_rules_if_changed(self) -> bool:
        """检查文件是否有变化，如有变化则重新加载规则"""
        if not os.path.exists(self.rules_file_path):
            print(f"[动态加载器] 警告: 规则文件不存在 {self.rules_file_path}")
            return False
        
        # 检查文件修改时间
        current_modified = os.path.getmtime(self.rules_file_path)
        
        if current_modified != self.last_modified:
            print(f"[动态加载器] 检测到规则文件变化，重新加载...")
            success = self._load_rules()
            if success:
                self.last_modified = current_modified
                self.last_load_time = datetime.now()
                print(f"[动态加载器] 成功加载 {self.rule_count} 条规则")
                return True
            else:
                print(f"[动态加载器] 规则加载失败")
                return False
        
        return False  # 文件未变化
    
    def _load_rules(self) -> bool:
        """加载规则文件"""
        try:
            with open(self.rules_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析规则
            self.cached_rules = self._parse_rules(content)
            self.rule_count = len(self.cached_rules)
            
            return True
            
        except Exception as e:
            print(f"[动态加载器] 加载规则文件失败: {str(e)}")
            return False
    
    def _parse_rules(self, content: str) -> List[Dict[str, Any]]:
        """解析规则内容"""
        rules = []
        
        # 按规则分割
        rule_pattern = r'规则\s+(\d+):\s*([^(]+?)\s*\([^)]*\)\s*\n--+\s*\n完整内容:\s*\n(.*?)(?=\n\n=+|$)'
        matches = re.findall(rule_pattern, content, re.DOTALL)
        
        for rule_number, rule_name, rule_content in matches:
            rule = self._parse_single_rule(rule_number, rule_name, rule_content)
            if rule:
                rules.append(rule)
        
        return rules
    
    def _parse_single_rule(self, rule_number: str, rule_name: str, rule_content: str) -> Optional[Dict[str, Any]]:
        """解析单个规则"""
        try:
            rule = {
                'rule_number': int(rule_number),
                'rule_name': rule_name.strip(),
                'rule_id': self._extract_rule_id(rule_content),
                'description': self._extract_description(rule_content),
                'label': self._extract_label(rule_content),
                'conditions': self._extract_conditions(rule_content),
                'conclusions': self._extract_conclusions(rule_content),
                'logic': self._parse_rule_logic(rule_content),
                'raw_content': rule_content
            }
            
            return rule
            
        except Exception as e:
            print(f"[动态加载器] 解析规则 {rule_number} 失败: {str(e)}")
            return None
    
    def _extract_rule_id(self, content: str) -> str:
        """提取规则ID"""
        # 查找DLSafe_X格式
        match = re.search(r'DLSafe_(\d+)', content)
        if match:
            return f"DLSafe_{match.group(1)}"
        
        # 查找S系列规则
        match = re.search(r'<Literal[^>]*>([^<]*?S\d+(?:-\d+)?)[^<]*</Literal>', content)
        if match:
            s_match = re.search(r'S\d+(?:-\d+)?', match.group(1))
            if s_match:
                return s_match.group(0)
        
        return "UnknownRule"
    
    def _extract_description(self, content: str) -> str:
        """提取规则描述"""
        # 查找注释中的描述
        pattern = r'<Literal[^>]*>([^<]+)</Literal>'
        matches = re.findall(pattern, content)
        
        for match in matches:
            if '→' in match or '->' in match:
                return match.strip()
        
        if matches:
            return matches[0].strip()
        
        return ""
    
    def _extract_label(self, content: str) -> str:
        """提取规则标签"""
        # 查找标签
        pattern = r'<AnnotationProperty abbreviatedIRI="rdfs:label"/>\s*<Literal[^>]*>([^<]+)</Literal>'
        match = re.search(pattern, content)
        if match:
            return match.group(1).strip()
        
        return ""
    
    def _extract_conditions(self, content: str) -> List[str]:
        """提取规则条件"""
        conditions = []
        
        # 查找Body部分
        body_match = re.search(r'<Body>(.*?)</Body>', content, re.DOTALL)
        if not body_match:
            return conditions
        
        body_content = body_match.group(1)
        
        # 提取ClassAtom
        class_atoms = re.findall(r'<Class IRI="([^"]+)"/>', body_content)
        for class_name in class_atoms:
            conditions.append(f"Type: {class_name}")
        
        # 提取ObjectPropertyAtom
        obj_props = re.findall(r'<ObjectProperty IRI="([^"]+)"/>.*?<NamedIndividual IRI="([^"]+)"/>', body_content, re.DOTALL)
        for prop, individual in obj_props:
            conditions.append(f"{prop}: {individual}")
        
        # 提取DataPropertyAtom
        data_props = re.findall(r'<DataProperty IRI="([^"]+)"/>', body_content)
        for prop in data_props:
            conditions.append(f"DataProperty: {prop}")
        
        # 提取BuiltinAtom
        builtins = re.findall(r'swrlb:(\w+)', body_content)
        for builtin in builtins:
            conditions.append(f"Builtin: {builtin}")
        
        return conditions
    
    def _extract_conclusions(self, content: str) -> List[str]:
        """提取规则结论"""
        conclusions = []
        
        # 查找Head部分
        head_match = re.search(r'<Head>(.*?)</Head>', content, re.DOTALL)
        if not head_match:
            return conclusions
        
        head_content = head_match.group(1)
        
        # 提取DataPropertyAtom结论
        data_conclusions = re.findall(r'<DataProperty IRI="([^"]+)"/>.*?<Literal[^>]*>([^<]+)</Literal>', head_content, re.DOTALL)
        for prop, value in data_conclusions:
            conclusions.append(f"{prop}: {value}")
        
        # 提取ObjectPropertyAtom结论
        obj_conclusions = re.findall(r'<ObjectProperty IRI="([^"]+)"/>.*?<NamedIndividual IRI="([^"]+)"/>', head_content, re.DOTALL)
        for prop, individual in obj_conclusions:
            conclusions.append(f"{prop}: {individual}")
        
        return conclusions
    
    def _parse_rule_logic(self, content: str) -> Dict[str, Any]:
        """解析规则逻辑"""
        logic = {
            'tunnel_type': None,
            'rock_grade': None,
            'hydro_condition': None,
            'soil_type': None,
            'length_condition': None,
            'diameter_condition': None,
            'output_property': None,
            'output_value': None,
            'rule_category': None
        }
        
        # 分析隧道类型
        tunnel_types = ['DeepTunnelProject', 'MountainTunnelProject', 'ShallowTunnelProject', 
                       'UnderwaterTunnelProject', 'UrbanTunnelProject']
        for tunnel_type in tunnel_types:
            if tunnel_type in content:
                logic['tunnel_type'] = tunnel_type
                break
        
        # 分析围岩等级
        rock_grades = ['RockGrade_I', 'RockGrade_II', 'RockGrade_III', 'RockGrade_IV', 'RockGrade_V']
        for grade in rock_grades:
            if grade in content:
                logic['rock_grade'] = grade.replace('RockGrade_', '')
                break
        
        # 分析水文条件
        if 'WaterRich' in content:
            logic['hydro_condition'] = 'water-rich'
        elif 'Dry' in content:
            logic['hydro_condition'] = 'dry'
        
        # 分析土壤类型
        soil_types = ['StrongSoil', 'MediumSoil', 'WeakSoil']
        for soil in soil_types:
            if soil in content:
                logic['soil_type'] = soil
                break
        
        # 分析长度条件
        if 'greaterThan' in content and '3000' in content:
            logic['length_condition'] = '> 3000'
        elif 'lessThanOrEqual' in content and '3000' in content:
            logic['length_condition'] = '<= 3000'
        
        # 提取输出属性和值
        head_match = re.search(r'<Head>(.*?)</Head>', content, re.DOTALL)
        if head_match:
            head_content = head_match.group(1)
            data_conclusion = re.search(r'<DataProperty IRI="([^"]+)"/>.*?<Literal[^>]*>([^<]+)</Literal>', head_content, re.DOTALL)
            if data_conclusion:
                logic['output_property'] = data_conclusion.group(1)
                logic['output_value'] = data_conclusion.group(2).strip()
            
            obj_conclusion = re.search(r'<ObjectProperty IRI="([^"]+)"/>.*?<NamedIndividual IRI="([^"]+)"/>', head_content, re.DOTALL)
            if obj_conclusion:
                logic['output_property'] = obj_conclusion.group(1)
                logic['output_value'] = obj_conclusion.group(2)
        
        # 确定规则类别
        logic['rule_category'] = self._determine_rule_category(content)
        
        return logic
    
    def _determine_rule_category(self, content: str) -> str:
        """确定规则类别"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['construction', 'tbm', 'drill', '施工方法']):
            return 'construction_method'
        elif any(keyword in content_lower for keyword in ['lining', 'thickness', '衬砌厚度']):
            return 'lining_thickness'
        elif any(keyword in content_lower for keyword in ['steel', 'arch', 'spacing', '钢拱架间距']):
            return 'steel_arch_spacing'
        elif any(keyword in content_lower for keyword in ['steel', 'arch', 'thickness', '钢拱架厚度']):
            return 'steel_arch_thickness'
        elif any(keyword in content_lower for keyword in ['waterproof', '防水层']):
            return 'waterproof_thickness'
        elif any(keyword in content_lower for keyword in ['bolt', 'length', '锚杆长度']):
            return 'bolt_length'
        elif any(keyword in content_lower for keyword in ['bolt', 'spacing', '锚杆间距']):
            return 'bolt_spacing'
        elif any(keyword in content_lower for keyword in ['bolt', 'count', '锚杆数量']):
            return 'bolt_count'
        else:
            return 'general'
    
    def get_rules(self, force_reload: bool = False) -> List[Dict[str, Any]]:
        """获取所有规则（支持强制重新加载）"""
        if force_reload or not self.cached_rules:
            self._load_rules()
        else:
            self.reload_rules_if_changed()
        
        return self.cached_rules
    
    def get_rules_by_category(self, category: str) -> List[Dict[str, Any]]:
        """按类别获取规则"""
        self.reload_rules_if_changed()
        return [rule for rule in self.cached_rules 
                if rule.get('logic', {}).get('rule_category') == category]
    
    def get_rule_by_id(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取规则"""
        self.reload_rules_if_changed()
        for rule in self.cached_rules:
            if rule.get('rule_id') == rule_id:
                return rule
        return None
    
    def apply_rules(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """应用所有适用的规则"""
        # 确保使用最新的规则
        self.reload_rules_if_changed()
        
        results = {}
        applied_rules = []
        
        # 多轮推理，处理规则间的依赖关系
        max_iterations = 5
        for iteration in range(max_iterations):
            current_params = {**params, **results}
            new_results = {}
            
            for rule in self.cached_rules:
                if self._rule_applies(rule, current_params):
                    rule_result = self._execute_rule(rule, current_params)
                    if rule_result:
                        new_results.update(rule_result)
                        if rule.get('rule_id') not in applied_rules:
                            applied_rules.append(rule.get('rule_id'))
            
            # 如果没有新结果，退出循环
            if not new_results or new_results == results:
                break
            
            results.update(new_results)
        
        print(f"[动态加载器] 应用了 {len(applied_rules)} 条规则: {', '.join(applied_rules)}")
        return results
    
    def _rule_applies(self, rule: Dict[str, Any], params: Dict[str, Any]) -> bool:
        """判断规则是否适用"""
        logic = rule.get('logic', {})
        
        # 检查隧道类型
        if logic.get('tunnel_type') and logic['tunnel_type'] != 'TunnelProject':
            if params.get('tunnelType') != logic['tunnel_type']:
                return False
        
        # 检查围岩等级
        if logic.get('rock_grade'):
            if params.get('hasGeologicalCondition') != logic['rock_grade']:
                return False
        
        # 检查水文条件
        if logic.get('hydro_condition'):
            if params.get('hasHydroCondition') != logic['hydro_condition']:
                return False
        
        # 检查土壤类型
        if logic.get('soil_type'):
            if params.get('hasSoilType') != logic['soil_type']:
                return False
        
        # 检查长度条件
        if logic.get('length_condition'):
            length = params.get('hasTunnelLength', 0)
            if '> 3000' in logic['length_condition'] and length <= 3000:
                return False
            elif '<= 3000' in logic['length_condition'] and length > 3000:
                return False
        
        return True
    
    def _execute_rule(self, rule: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """执行规则"""
        logic = rule.get('logic', {})
        
        if logic.get('output_property') and logic.get('output_value'):
            prop = logic['output_property']
            value = logic['output_value']
            
            # 尝试转换数值
            try:
                if '.' in str(value):
                    value = float(value)
                elif str(value).replace('-', '').isdigit():
                    value = int(value)
            except:
                pass  # 保持原始格式
            
            return {prop: value}
        
        return {}
    
    def get_file_info(self) -> Dict[str, Any]:
        """获取文件信息"""
        return {
            'file_path': self.rules_file_path,
            'exists': os.path.exists(self.rules_file_path),
            'last_modified': datetime.fromtimestamp(self.last_modified) if self.last_modified else None,
            'last_load_time': self.last_load_time,
            'rule_count': self.rule_count,
            'file_size': os.path.getsize(self.rules_file_path) if os.path.exists(self.rules_file_path) else 0
        }

# 全局动态加载器实例
_dynamic_loader = None

def get_dynamic_loader(rules_file_path: str = "pure_swrl_rules.txt") -> DynamicSWRLLoader:
    """获取动态加载器实例（单例模式）"""
    global _dynamic_loader
    if _dynamic_loader is None or _dynamic_loader.rules_file_path != rules_file_path:
        _dynamic_loader = DynamicSWRLLoader(rules_file_path)
    return _dynamic_loader

def apply_dynamic_rules(params: Dict[str, Any], rules_file_path: str = "pure_swrl_rules.txt") -> Dict[str, Any]:
    """动态应用规则的便捷函数"""
    loader = get_dynamic_loader(rules_file_path)
    return loader.apply_rules(params)

def reload_rules(rules_file_path: str = "pure_swrl_rules.txt") -> bool:
    """强制重新加载规则的便捷函数"""
    loader = get_dynamic_loader(rules_file_path)
    return loader._load_rules()

if __name__ == "__main__":
    # 测试动态加载器
    print("测试动态SWRL规则加载器...")
    
    loader = DynamicSWRLLoader("pure_swrl_rules.txt")
    
    # 显示文件信息
    info = loader.get_file_info()
    print(f"文件信息: {info}")
    
    # 测试参数
    test_params = {
        "tunnelType": "MountainTunnelProject",
        "hasTunnelLength": 2500,
        "hasTunnelDiameter": 12.0,
        "hasGeologicalCondition": "III",
        "hasHydroCondition": "water-rich",
        "hasSoilType": "MediumSoil"
    }
    
    print(f"测试参数: {test_params}")
    
    # 应用规则
    results = loader.apply_rules(test_params)
    print(f"推理结果: {results}")
    
    print("\n提示: 修改pure_swrl_rules.txt文件，然后重新运行程序查看规则变化效果")