#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SWRL规则推理引擎
将SWRL规则转换为Python可执行的推理系统
"""

import re
import math
from typing import Dict, List, Set, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Atom:
    """SWRL原子基类"""
    pass


@dataclass
class ClassAtom(Atom):
    """类原子：表示个体属于某个类"""
    class_name: str
    individual: str


@dataclass
class ObjectPropertyAtom(Atom):
    """对象属性原子：表示两个个体之间的关系"""
    property_name: str
    subject: str
    object: str


@dataclass
class DataPropertyAtom(Atom):
    """数据属性原子：表示个体的数据属性值"""
    property_name: str
    subject: str
    value: Any


@dataclass
class BuiltInAtom(Atom):
    """内置原子：数学运算等"""
    function_name: str
    variables: List[str]


@dataclass
class SWRLRule:
    """SWRL规则"""
    rule_id: str
    label: str
    comment: str
    body: List[Atom]
    head: List[Atom]


class SWRLParser:
    """SWRL规则解析器"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.rules = []
        
    def parse_file(self) -> List[SWRLRule]:
        """解析SWRL规则文件"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"错误：找不到文件 {self.file_path}")
            print("请确保 pure_swrl_rules.txt 文件在正确的路径下")
            return []
        except Exception as e:
            print(f"读取文件时出错: {e}")
            return []
            
        # 分割规则
        rule_sections = content.split('规则 ')[1:]  # 跳过开头部分
        
        for section in rule_sections:
            rule = self._parse_rule_section(section)
            if rule:
                self.rules.append(rule)
                
        return self.rules
    
    def _parse_rule_section(self, section: str) -> Optional[SWRLRule]:
        """解析单个规则段落"""
        try:
            # 提取规则ID
            id_match = re.search(r'(\d+):', section)
            if not id_match:
                return None
            rule_id = id_match.group(1)
            
            # 提取标签
            label_match = re.search(r'<Literal>([^<]+)</Literal>\s*</Annotation>\s*<Body>', section)
            label = label_match.group(1) if label_match else f"Rule_{rule_id}"
            
            # 提取注释
            comment_match = re.search(r'<Literal>([^<]+)</Literal>\s*</Annotation>\s*<Annotation>', section)
            comment = comment_match.group(1) if comment_match else ""
            
            # 解析Body部分
            body_match = re.search(r'<Body>(.*?)</Body>', section, re.DOTALL)
            body_atoms = self._parse_atoms(body_match.group(1)) if body_match else []
            
            # 解析Head部分
            head_match = re.search(r'<Head>(.*?)</Head>', section, re.DOTALL)
            head_atoms = self._parse_atoms(head_match.group(1)) if head_match else []
            
            return SWRLRule(rule_id, label, comment, body_atoms, head_atoms)
            
        except Exception as e:
            print(f"解析规则时出错: {e}")
            return None
    
    def _parse_atoms(self, atoms_text: str) -> List[Atom]:
        """解析原子列表"""
        atoms = []
        
        # 解析ClassAtom
        class_atoms = re.findall(r'<ClassAtom>\s*<Class IRI="([^"]+)"/>\s*<Variable abbreviatedIRI="([^"]+)"/>\s*</ClassAtom>', atoms_text)
        for class_name, var in class_atoms:
            atoms.append(ClassAtom(class_name, var))
        
        # 解析ObjectPropertyAtom
        obj_prop_atoms = re.findall(r'<ObjectPropertyAtom>\s*<ObjectProperty IRI="([^"]+)"/>\s*<Variable abbreviatedIRI="([^"]+)"/>\s*(?:<Variable abbreviatedIRI="([^"]+)"/>|<NamedIndividual IRI="([^"]+)"/>)\s*</ObjectPropertyAtom>', atoms_text)
        for prop, subj, var_obj, named_obj in obj_prop_atoms:
            obj = var_obj if var_obj else named_obj
            atoms.append(ObjectPropertyAtom(prop, subj, obj))
        
        # 解析DataPropertyAtom
        data_prop_pattern = r'<DataPropertyAtom>\s*<DataProperty IRI="([^"]+)"/>\s*<Variable abbreviatedIRI="([^"]+)"/>\s*<Literal[^>]*>([^<]+)</Literal>\s*</DataPropertyAtom>'
        data_prop_atoms = re.findall(data_prop_pattern, atoms_text)
        for prop, subj, value in data_prop_atoms:
            # 尝试转换数值
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass  # 保持字符串
            atoms.append(DataPropertyAtom(prop, subj, value))
        
        # 解析BuiltInAtom
        builtin_pattern = r'<BuiltInAtom IRI="[^"]*#([^"]+)">\s*((?:<Variable abbreviatedIRI="[^"]+"/>\s*|<Literal[^>]*>[^<]+</Literal>\s*)+)\s*</BuiltInAtom>'
        builtin_atoms = re.findall(builtin_pattern, atoms_text, re.DOTALL)
        for func_name, vars_text in builtin_atoms:
            variables = re.findall(r'abbreviatedIRI="([^"]+)"', vars_text)
            literals = re.findall(r'<Literal[^>]*>([^<]+)</Literal>', vars_text)
            all_vars = variables + literals
            atoms.append(BuiltInAtom(func_name, all_vars))
        
        return atoms


class KnowledgeBase:
    """知识库"""
    
    def __init__(self):
        self.class_facts = defaultdict(set)  # 类事实
        self.object_property_facts = defaultdict(set)  # 对象属性事实
        self.data_property_facts = defaultdict(dict)  # 数据属性事实
        
    def add_class_fact(self, individual: str, class_name: str):
        """添加类事实"""
        self.class_facts[individual].add(class_name)
        
    def add_object_property_fact(self, subject: str, property_name: str, object_val: str):
        """添加对象属性事实"""
        self.object_property_facts[(subject, property_name)].add(object_val)
        
    def add_data_property_fact(self, subject: str, property_name: str, value: Any):
        """添加数据属性事实"""
        if subject not in self.data_property_facts:
            self.data_property_facts[subject] = {}
        self.data_property_facts[subject][property_name] = value
        
    def has_class_fact(self, individual: str, class_name: str) -> bool:
        """检查类事实是否存在"""
        return class_name in self.class_facts.get(individual, set())
        
    def has_object_property_fact(self, subject: str, property_name: str, object_val: str) -> bool:
        """检查对象属性事实是否存在"""
        return object_val in self.object_property_facts.get((subject, property_name), set())
        
    def get_data_property_value(self, subject: str, property_name: str) -> Any:
        """获取数据属性值"""
        return self.data_property_facts.get(subject, {}).get(property_name)


class SWRLInferenceEngine:
    """SWRL推理引擎"""
    
    def __init__(self, rules: List[SWRLRule]):
        self.rules = rules
        self.kb = KnowledgeBase()
        
    def execute_builtin(self, builtin: BuiltInAtom, variable_bindings: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """执行内置函数"""
        func_name = builtin.function_name
        vars_and_literals = builtin.variables
        
        # 解析参数，区分变量和字面量
        args = []
        for var in vars_and_literals:
            if var.startswith(':'):
                # 变量
                var_name = var
                if var_name in variable_bindings:
                    args.append(variable_bindings[var_name])
                else:
                    args.append(None)
            else:
                # 字面量
                try:
                    if '.' in var:
                        args.append(float(var))
                    else:
                        args.append(int(var))
                except ValueError:
                    args.append(var)
        
        # 执行数学运算
        try:
            if func_name == "multiply" and len(args) >= 3:
                if args[1] is not None and args[2] is not None:
                    result = args[1] * args[2]
                    return {vars_and_literals[0]: result}
                    
            elif func_name == "divide" and len(args) >= 3:
                if args[1] is not None and args[2] is not None and args[2] != 0:
                    result = args[1] / args[2]
                    return {vars_and_literals[0]: result}
                    
            elif func_name == "greaterThan" and len(args) >= 2:
                if args[0] is not None and args[1] is not None:
                    return {} if args[0] > args[1] else None
                    
            elif func_name == "lessThanOrEqual" and len(args) >= 2:
                if args[0] is not None and args[1] is not None:
                    return {} if args[0] <= args[1] else None
                    
            elif func_name == "floor" and len(args) >= 2:
                if args[1] is not None:
                    result = math.floor(args[1])
                    return {vars_and_literals[0]: result}
                    
            elif func_name == "round" and len(args) >= 2:
                if args[1] is not None:
                    result = round(args[1])
                    return {vars_and_literals[0]: result}
                    
        except Exception as e:
            print(f"执行内置函数 {func_name} 时出错: {e}")
            
        return None
        
    def match_atom(self, atom: Atom, variable_bindings: Dict[str, Any]) -> List[Dict[str, Any]]:
        """匹配原子"""
        if isinstance(atom, ClassAtom):
            # 如果个体是变量
            if atom.individual.startswith(':'):
                if atom.individual in variable_bindings:
                    individual = variable_bindings[atom.individual]
                    if self.kb.has_class_fact(individual, atom.class_name):
                        return [{}]
                else:
                    # 查找所有属于该类的个体
                    results = []
                    for individual, classes in self.kb.class_facts.items():
                        if atom.class_name in classes:
                            results.append({atom.individual: individual})
                    return results
            else:
                if self.kb.has_class_fact(atom.individual, atom.class_name):
                    return [{}]
                    
        elif isinstance(atom, ObjectPropertyAtom):
            subject = variable_bindings.get(atom.subject, atom.subject) if atom.subject.startswith(':') else atom.subject
            object_val = variable_bindings.get(atom.object, atom.object) if atom.object.startswith(':') else atom.object
            
            if subject and object_val:
                if self.kb.has_object_property_fact(subject, atom.property_name, object_val):
                    return [{}]
            else:
                # 处理变量绑定
                results = []
                for (subj, prop), objects in self.kb.object_property_facts.items():
                    if prop == atom.property_name:
                        for obj in objects:
                            binding = {}
                            if atom.subject.startswith(':') and subject is None:
                                binding[atom.subject] = subj
                            if atom.object.startswith(':') and object_val is None:
                                binding[atom.object] = obj
                            if binding:
                                results.append(binding)
                return results
                
        elif isinstance(atom, DataPropertyAtom):
            subject = variable_bindings.get(atom.subject, atom.subject) if atom.subject.startswith(':') else atom.subject
            if subject:
                stored_value = self.kb.get_data_property_value(subject, atom.property_name)
                if stored_value == atom.value:
                    return [{}]
                    
        elif isinstance(atom, BuiltInAtom):
            result = self.execute_builtin(atom, variable_bindings)
            if result is not None:
                return [result]
                
        return []
        
    def apply_rule(self, rule: SWRLRule) -> bool:
        """应用单个规则"""
        applied = False
        
        def match_body(atoms: List[Atom], bindings: Dict[str, Any] = None) -> List[Dict[str, Any]]:
            if bindings is None:
                bindings = {}
            if not atoms:
                return [bindings]
                
            atom = atoms[0]
            remaining = atoms[1:]
            results = []
            
            matches = self.match_atom(atom, bindings)
            for match in matches:
                new_bindings = {**bindings, **match}
                results.extend(match_body(remaining, new_bindings))
                
            return results
            
        # 匹配规则体
        body_matches = match_body(rule.body)
        
        # 对每个匹配应用规则头
        for bindings in body_matches:
            for head_atom in rule.head:
                if isinstance(head_atom, DataPropertyAtom):
                    subject = bindings.get(head_atom.subject, head_atom.subject)
                    if subject and not subject.startswith(':'):
                        current_value = self.kb.get_data_property_value(subject, head_atom.property_name)
                        if current_value != head_atom.value:
                            self.kb.add_data_property_fact(subject, head_atom.property_name, head_atom.value)
                            applied = True
                            print(f"应用规则 {rule.label}: {subject} {head_atom.property_name} = {head_atom.value}")
                            
                elif isinstance(head_atom, ObjectPropertyAtom):
                    subject = bindings.get(head_atom.subject, head_atom.subject)
                    object_val = bindings.get(head_atom.object, head_atom.object)
                    if subject and object_val and not subject.startswith(':') and not object_val.startswith(':'):
                        if not self.kb.has_object_property_fact(subject, head_atom.property_name, object_val):
                            self.kb.add_object_property_fact(subject, head_atom.property_name, object_val)
                            applied = True
                            print(f"应用规则 {rule.label}: {subject} {head_atom.property_name} {object_val}")
                            
        return applied
        
    def forward_chain(self, max_iterations: int = 100) -> None:
        """前向链推理"""
        for i in range(max_iterations):
            applied_any = False
            for rule in self.rules:
                if self.apply_rule(rule):
                    applied_any = True
            if not applied_any:
                print(f"推理完成，共进行了 {i+1} 轮")
                break
        else:
            print(f"达到最大迭代次数 {max_iterations}")
            
    def query_data_property(self, subject: str, property_name: str) -> Any:
        """查询数据属性值"""
        return self.kb.get_data_property_value(subject, property_name)
        
    def print_knowledge_base(self):
        """打印知识库内容"""
        print("\n=== 知识库内容 ===")
        print("类事实:")
        for individual, classes in self.kb.class_facts.items():
            for class_name in classes:
                print(f"  {individual} 属于 {class_name}")
                
        print("\n对象属性事实:")
        for (subject, prop), objects in self.kb.object_property_facts.items():
            for obj in objects:
                print(f"  {subject} {prop} {obj}")
                
        print("\n数据属性事实:")
        for subject, properties in self.kb.data_property_facts.items():
            for prop, value in properties.items():
                print(f"  {subject} {prop} = {value}")


class RuleExporter:
    """规则导出器：将解析的规则转换为Python可调用格式"""
    
    def __init__(self, rules: List[SWRLRule]):
        self.rules = rules
    
    def export_to_python_module(self, output_file: str = "tunnel_rules.py"):
        """导出规则为Python模块文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('# -*- coding: utf-8 -*-\n')
            f.write('"""\n')
            f.write('自动生成的隧道工程SWRL规则模块\n')
            f.write('包含149个推理规则的Python实现\n')
            f.write('"""\n\n')
            f.write('from typing import Dict, Any, Optional\n')
            f.write('import math\n\n')
            
            # 导出规则数据结构
            f.write('# 规则数据结构\n')
            f.write('TUNNEL_RULES = {\n')
            
            for rule in self.rules:
                f.write(f'    "{rule.rule_id}": {{\n')
                f.write(f'        "label": "{rule.label}",\n')
                f.write(f'        "comment": "{rule.comment}",\n')
                f.write(f'        "body": {self._serialize_atoms(rule.body)},\n')
                f.write(f'        "head": {self._serialize_atoms(rule.head)}\n')
                f.write('    },\n')
            
            f.write('}\n\n')
            
            # 导出快速推理函数
            self._write_quick_inference_functions(f)
            
            # 导出规则应用函数
            self._write_rule_application_functions(f)
            
        print(f"规则已导出到 {output_file}")
    
    def _serialize_atoms(self, atoms: List[Atom]) -> str:
        """序列化原子列表"""
        result = "[\n"
        for atom in atoms:
            if isinstance(atom, ClassAtom):
                result += f'            {{"type": "class", "class_name": "{atom.class_name}", "individual": "{atom.individual}"}},\n'
            elif isinstance(atom, ObjectPropertyAtom):
                result += f'            {{"type": "object_property", "property_name": "{atom.property_name}", "subject": "{atom.subject}", "object": "{atom.object}"}},\n'
            elif isinstance(atom, DataPropertyAtom):
                result += f'            {{"type": "data_property", "property_name": "{atom.property_name}", "subject": "{atom.subject}", "value": {repr(atom.value)}}},\n'
            elif isinstance(atom, BuiltInAtom):
                result += f'            {{"type": "builtin", "function_name": "{atom.function_name}", "variables": {atom.variables}}},\n'
        result += "        ]"
        return result
    
    def _write_quick_inference_functions(self, f):
        """写入快速推理函数"""
        f.write('def infer_lining_thickness(tunnel_type: str, rock_grade: str, hydro_condition: str) -> Optional[float]:\n')
        f.write('    """快速推断衬砌厚度"""\n')
        f.write('    rules_map = {\n')
        
        # 生成衬砌厚度的快速查找表
        for rule in self.rules:
            if any(atom.property_name == "hasLiningThickness" for atom in rule.head if hasattr(atom, 'property_name')):
                tunnel_type_val = self._extract_tunnel_type(rule)
                rock_grade_val = self._extract_rock_grade(rule)
                hydro_condition_val = self._extract_hydro_condition(rule)
                thickness_val = self._extract_thickness_value(rule)
                
                if all([tunnel_type_val, rock_grade_val, hydro_condition_val, thickness_val]):
                    f.write(f'        ("{tunnel_type_val}", "{rock_grade_val}", "{hydro_condition_val}"): {thickness_val},\n')
        
        f.write('    }\n')
        f.write('    return rules_map.get((tunnel_type, rock_grade, hydro_condition))\n\n')
        
        f.write('def infer_steel_arch_spacing(tunnel_type: str, rock_grade: str, hydro_condition: str) -> Optional[float]:\n')
        f.write('    """快速推断钢拱架间距"""\n')
        f.write('    rules_map = {\n')
        
        # 生成钢拱架间距的快速查找表
        for rule in self.rules:
            if any(atom.property_name == "hasSteelArchSpacing" for atom in rule.head if hasattr(atom, 'property_name')):
                tunnel_type_val = self._extract_tunnel_type(rule)
                rock_grade_val = self._extract_rock_grade(rule)
                hydro_condition_val = self._extract_hydro_condition(rule)
                spacing_val = self._extract_spacing_value(rule)
                
                if all([tunnel_type_val, rock_grade_val, hydro_condition_val, spacing_val]):
                    f.write(f'        ("{tunnel_type_val}", "{rock_grade_val}", "{hydro_condition_val}"): {spacing_val},\n')
        
        f.write('    }\n')
        f.write('    return rules_map.get((tunnel_type, rock_grade, hydro_condition))\n\n')
        
        f.write('def infer_waterproof_thickness(tunnel_type: str, soil_type: str, hydro_condition: str) -> Optional[float]:\n')
        f.write('    """快速推断防水层厚度"""\n')
        f.write('    rules_map = {\n')
        
        # 生成防水层厚度的快速查找表
        for rule in self.rules:
            if any(atom.property_name == "hasWaterproofLayerThickness" for atom in rule.head if hasattr(atom, 'property_name')):
                tunnel_type_val = self._extract_tunnel_type(rule)
                soil_type_val = self._extract_soil_type(rule)
                hydro_condition_val = self._extract_hydro_condition(rule)
                thickness_val = self._extract_waterproof_value(rule)
                
                if all([tunnel_type_val, soil_type_val, hydro_condition_val, thickness_val]):
                    f.write(f'        ("{tunnel_type_val}", "{soil_type_val}", "{hydro_condition_val}"): {thickness_val},\n')
        
        f.write('    }\n')
        f.write('    return rules_map.get((tunnel_type, soil_type, hydro_condition))\n\n')
    
    def _write_rule_application_functions(self, f):
        """写入规则应用函数"""
        f.write('def apply_construction_method_rules(tunnel_length: float) -> str:\n')
        f.write('    """根据隧道长度确定施工方法"""\n')
        f.write('    if tunnel_length > 3000:\n')
        f.write('        return "DrillAndBlast_001"\n')
        f.write('    else:\n')
        f.write('        return "TBM_001"\n\n')
        
        f.write('def calculate_bolt_length(tunnel_diameter: float, rock_grade: str) -> float:\n')
        f.write('    """计算锚杆长度"""\n')
        f.write('    multipliers = {\n')
        f.write('        "RockGrade_I": 0.25,\n')
        f.write('        "RockGrade_II": 0.3,\n')
        f.write('        "RockGrade_III": 0.33,\n')
        f.write('        "RockGrade_IV": 0.45,\n')
        f.write('        "RockGrade_V": 0.5\n')
        f.write('    }\n')
        f.write('    return tunnel_diameter * multipliers.get(rock_grade, 0.3)\n\n')
        
        f.write('def calculate_steel_arch_count(tunnel_length: float, spacing: float) -> int:\n')
        f.write('    """计算钢拱架数量"""\n')
        f.write('    if spacing > 0:\n')
        f.write('        return round(tunnel_length / spacing)\n')
        f.write('    return 0\n\n')
        
        f.write('def comprehensive_tunnel_design(tunnel_type: str, tunnel_length: float, tunnel_diameter: float,\n')
        f.write('                                rock_grade: str, hydro_condition: str, \n')
        f.write('                                soil_type: str = "MediumSoil") -> Dict[str, Any]:\n')
        f.write('    """综合隧道设计计算"""\n')
        f.write('    result = {}\n')
        f.write('    \n')
        f.write('    # 基本参数\n')
        f.write('    result["tunnel_type"] = tunnel_type\n')
        f.write('    result["tunnel_length"] = tunnel_length\n')
        f.write('    result["tunnel_diameter"] = tunnel_diameter\n')
        f.write('    \n')
        f.write('    # 衬砌厚度\n')
        f.write('    result["lining_thickness"] = infer_lining_thickness(tunnel_type, rock_grade, hydro_condition)\n')
        f.write('    \n')
        f.write('    # 钢拱架间距\n')
        f.write('    result["steel_arch_spacing"] = infer_steel_arch_spacing(tunnel_type, rock_grade, hydro_condition)\n')
        f.write('    \n')
        f.write('    # 防水层厚度\n')
        f.write('    result["waterproof_thickness"] = infer_waterproof_thickness(tunnel_type, soil_type, hydro_condition)\n')
        f.write('    \n')
        f.write('    # 施工方法\n')
        f.write('    result["construction_method"] = apply_construction_method_rules(tunnel_length)\n')
        f.write('    \n')
        f.write('    # 锚杆长度\n')
        f.write('    result["bolt_length"] = calculate_bolt_length(tunnel_diameter, rock_grade)\n')
        f.write('    \n')
        f.write('    # 钢拱架数量\n')
        f.write('    if result["steel_arch_spacing"]:\n')
        f.write('        result["steel_arch_count"] = calculate_steel_arch_count(tunnel_length, result["steel_arch_spacing"])\n')
        f.write('    \n')
        f.write('    return result\n\n')
    
    def _extract_tunnel_type(self, rule: SWRLRule) -> Optional[str]:
        """从规则中提取隧道类型"""
        for atom in rule.body:
            if isinstance(atom, ClassAtom) and "Tunnel" in atom.class_name:
                return atom.class_name
        return None
    
    def _extract_rock_grade(self, rule: SWRLRule) -> Optional[str]:
        """从规则中提取岩石等级"""
        for atom in rule.body:
            if isinstance(atom, ObjectPropertyAtom) and atom.property_name == "hasRockGrade":
                return atom.object
        return None
    
    def _extract_hydro_condition(self, rule: SWRLRule) -> Optional[str]:
        """从规则中提取水文条件"""
        for atom in rule.body:
            if isinstance(atom, ObjectPropertyAtom) and atom.property_name == "hasHydroCondition":
                return atom.object
        return None
    
    def _extract_soil_type(self, rule: SWRLRule) -> Optional[str]:
        """从规则中提取土壤类型"""
        for atom in rule.body:
            if isinstance(atom, ObjectPropertyAtom) and atom.property_name == "hasSoilType":
                return atom.object
        return None
    
    def _extract_thickness_value(self, rule: SWRLRule) -> Optional[float]:
        """从规则中提取衬砌厚度值"""
        for atom in rule.head:
            if isinstance(atom, DataPropertyAtom) and atom.property_name == "hasLiningThickness":
                return atom.value
        return None
    
    def _extract_spacing_value(self, rule: SWRLRule) -> Optional[float]:
        """从规则中提取钢拱架间距值"""
        for atom in rule.head:
            if isinstance(atom, DataPropertyAtom) and atom.property_name == "hasSteelArchSpacing":
                return atom.value
        return None
    
    def _extract_waterproof_value(self, rule: SWRLRule) -> Optional[float]:
        """从规则中提取防水层厚度值"""
        for atom in rule.head:
            if isinstance(atom, DataPropertyAtom) and atom.property_name == "hasWaterproofLayerThickness":
                return atom.value
        return None
    
    def export_to_json(self, output_file: str = "tunnel_rules.json"):
        """导出规则为JSON格式"""
        import json
        
        rules_data = {}
        for rule in self.rules:
            rules_data[rule.rule_id] = {
                "label": rule.label,
                "comment": rule.comment,
                "body": [self._atom_to_dict(atom) for atom in rule.body],
                "head": [self._atom_to_dict(atom) for atom in rule.head]
            }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(rules_data, f, ensure_ascii=False, indent=2)
        
        print(f"规则已导出到 {output_file}")
    
    def _atom_to_dict(self, atom: Atom) -> Dict[str, Any]:
        """将原子转换为字典"""
        if isinstance(atom, ClassAtom):
            return {"type": "class", "class_name": atom.class_name, "individual": atom.individual}
        elif isinstance(atom, ObjectPropertyAtom):
            return {"type": "object_property", "property_name": atom.property_name, "subject": atom.subject, "object": atom.object}
        elif isinstance(atom, DataPropertyAtom):
            return {"type": "data_property", "property_name": atom.property_name, "subject": atom.subject, "value": atom.value}
        elif isinstance(atom, BuiltInAtom):
            return {"type": "builtin", "function_name": atom.function_name, "variables": atom.variables}
        return {}


def main():
    """主函数：解析SWRL规则并导出为Python可调用格式"""
    
    # 解析SWRL规则文件
    print("=== 解析SWRL规则文件 ===")
    parser = SWRLParser("pure_swrl_rules.txt")
    rules = parser.parse_file()
    print(f"成功解析了 {len(rules)} 个SWRL规则")
    
    if not rules:
        print("没有解析到任何规则，请检查文件路径和格式")
        return
    
    # 导出规则为Python模块
    print("\n=== 导出规则为Python模块 ===")
    exporter = RuleExporter(rules)
    exporter.export_to_python_module("tunnel_rules.py")
    exporter.export_to_json("tunnel_rules.json")
    
    print("\n=== 导出完成 ===")
    print("已生成以下文件：")
    print("1. tunnel_rules.py - Python模块文件，包含快速推理函数")
    print("2. tunnel_rules.json - JSON格式的规则数据")
    print("\n使用示例：")
    print("from tunnel_rules import comprehensive_tunnel_design")
    print('result = comprehensive_tunnel_design("DeepTunnelProject", 5000, 12.0, "RockGrade_I", "Dry")')
    print("print(result)")
    
    # 演示生成的模块的使用
    print("\n=== 演示导出的规则使用 ===")
    try:
        # 导入刚生成的模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("tunnel_rules", "tunnel_rules.py")
        tunnel_rules = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tunnel_rules)
        
        # 测试综合设计函数
        result = tunnel_rules.comprehensive_tunnel_design(
            tunnel_type="DeepTunnelProject",
            tunnel_length=5000,
            tunnel_diameter=12.0,
            rock_grade="RockGrade_I",
            hydro_condition="Dry",
            soil_type="MediumSoil"
        )
        
        print("设计结果：")
        for key, value in result.items():
            if value is not None:
                print(f"  {key}: {value}")
                
    except Exception as e:
        print(f"演示时出错: {e}")
        print("请手动导入 tunnel_rules.py 模块进行测试")


if __name__ == "__main__":
    main()