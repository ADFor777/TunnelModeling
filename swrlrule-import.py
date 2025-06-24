from owlready2 import *
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# 配置文件路径
OWL_FILE_PATH = r"G:\TUNNEL\Tunnel.owl"

def extract_pure_swrl_rules(file_path):
    """专门提取纯SWRL规则"""
    print("\n🎯 专门提取SWRL规则...")
    
    swrl_rules = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 分析文件: {len(content)} 字符")
        
        # 1. 提取完整的SWRL规则 (swrl:Imp)
        print("🔍 搜索 swrl:Imp 规则...")
        imp_pattern = r'<swrl:Imp[^>]*>(.*?)</swrl:Imp>'
        imp_matches = re.findall(imp_pattern, content, re.DOTALL)
        
        if imp_matches:
            print(f"✅ 找到 {len(imp_matches)} 个 swrl:Imp 规则")
            for i, rule in enumerate(imp_matches, 1):
                swrl_rules.append({
                    'type': 'swrl:Imp',
                    'id': f'Rule_{i}',
                    'content': rule.strip()
                })
        
        # 2. 提取DLSafeRule规则
        print("🔍 搜索 DLSafeRule 规则...")
        dlsafe_pattern = r'<DLSafeRule[^>]*>(.*?)</DLSafeRule>'
        dlsafe_matches = re.findall(dlsafe_pattern, content, re.DOTALL)
        
        if dlsafe_matches:
            print(f"✅ 找到 {len(dlsafe_matches)} 个 DLSafeRule 规则")
            for i, rule in enumerate(dlsafe_matches, 1):
                swrl_rules.append({
                    'type': 'DLSafeRule',
                    'id': f'DLSafe_{i}',
                    'content': rule.strip()
                })
        
        # 3. 提取RuleML格式的规则
        print("🔍 搜索 RuleML 格式规则...")
        ruleml_pattern = r'<ruleml:imp[^>]*>(.*?)</ruleml:imp>'
        ruleml_matches = re.findall(ruleml_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if ruleml_matches:
            print(f"✅ 找到 {len(ruleml_matches)} 个 RuleML 规则")
            for i, rule in enumerate(ruleml_matches, 1):
                swrl_rules.append({
                    'type': 'RuleML',
                    'id': f'RuleML_{i}',
                    'content': rule.strip()
                })
        
        # 4. 搜索其他SWRL规则格式
        print("🔍 搜索其他SWRL规则格式...")
        other_patterns = [
            (r'<swrlx:Rule[^>]*>(.*?)</swrlx:Rule>', 'swrlx:Rule'),
            (r'<Rule[^>]*rdf:about[^>]*swrl[^>]*>(.*?)</Rule>', 'SWRL_Rule'),
        ]
        
        for pattern, rule_type in other_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            if matches:
                print(f"✅ 找到 {len(matches)} 个 {rule_type} 规则")
                for i, rule in enumerate(matches, 1):
                    swrl_rules.append({
                        'type': rule_type,
                        'id': f'{rule_type}_{i}',
                        'content': rule.strip()
                    })
        
    except Exception as e:
        print(f"❌ 提取失败: {e}")
    
    return swrl_rules

def parse_swrl_rule_structure(rule_content):
    """解析SWRL规则的body和head结构"""
    try:
        # 提取body部分
        body_pattern = r'<swrl:body[^>]*>(.*?)</swrl:body>'
        body_match = re.search(body_pattern, rule_content, re.DOTALL)
        body = body_match.group(1).strip() if body_match else "未找到body"
        
        # 提取head部分
        head_pattern = r'<swrl:head[^>]*>(.*?)</swrl:head>'
        head_match = re.search(head_pattern, rule_content, re.DOTALL)
        head = head_match.group(1).strip() if head_match else "未找到head"
        
        return {
            'body': body,
            'head': head,
            'has_structure': body_match and head_match
        }
    except:
        return {
            'body': "解析失败",
            'head': "解析失败", 
            'has_structure': False
        }

def extract_swrl_atoms(content):
    """提取SWRL原子（atoms）"""
    atoms = []
    
    atom_patterns = {
        'ClassAtom': r'<swrl:classPredicate[^>]*>(.*?)</swrl:classPredicate>',
        'PropertyAtom': r'<swrl:propertyPredicate[^>]*>(.*?)</swrl:propertyPredicate>',
        'SameIndividualAtom': r'<swrl:sameIndividualAtom[^>]*>(.*?)</swrl:sameIndividualAtom>',
        'DifferentIndividualsAtom': r'<swrl:differentIndividualsAtom[^>]*>(.*?)</swrl:differentIndividualsAtom>',
        'BuiltinAtom': r'<swrl:builtin[^>]*>(.*?)</swrl:builtin>',
    }
    
    for atom_type, pattern in atom_patterns.items():
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            atoms.extend([(atom_type, match.strip()) for match in matches])
    
    return atoms

def display_swrl_rules(swrl_rules):
    """格式化显示SWRL规则"""
    if not swrl_rules:
        print("❌ 没有找到任何SWRL规则")
        return
    
    print(f"\n🎉 总共找到 {len(swrl_rules)} 个纯SWRL规则")
    print("=" * 60)
    
    for i, rule in enumerate(swrl_rules, 1):
        print(f"\n📋 规则 {i}: {rule['id']} ({rule['type']})")
        print("-" * 40)
        
        # 解析规则结构
        structure = parse_swrl_rule_structure(rule['content'])
        
        if structure['has_structure']:
            print("🔸 Body (前提条件):")
            print(f"   {structure['body'][:200]}...")
            print("🔸 Head (结论):")
            print(f"   {structure['head'][:200]}...")
        else:
            print("🔸 规则内容:")
            print(f"   {rule['content'][:300]}...")
        
        # 提取原子
        atoms = extract_swrl_atoms(rule['content'])
        if atoms:
            print(f"🔸 包含 {len(atoms)} 个原子:")
            for atom_type, atom_content in atoms[:3]:  # 只显示前3个
                print(f"   • {atom_type}: {atom_content[:100]}...")

def save_pure_swrl_rules(swrl_rules, output_file="pure_swrl_rules.txt"):
    """保存纯SWRL规则到文件"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("纯SWRL规则提取结果\n")
            f.write("=" * 50 + "\n\n")
            
            if not swrl_rules:
                f.write("未找到任何SWRL规则\n")
                return
            
            f.write(f"总共找到 {len(swrl_rules)} 个SWRL规则\n\n")
            
            for i, rule in enumerate(swrl_rules, 1):
                f.write(f"规则 {i}: {rule['id']} ({rule['type']})\n")
                f.write("-" * 50 + "\n")
                
                # 解析并保存结构化内容
                structure = parse_swrl_rule_structure(rule['content'])
                
                if structure['has_structure']:
                    f.write("Body (前提条件):\n")
                    f.write(structure['body'] + "\n\n")
                    f.write("Head (结论):\n")
                    f.write(structure['head'] + "\n\n")
                else:
                    f.write("完整内容:\n")
                    f.write(rule['content'] + "\n\n")
                
                f.write("=" * 50 + "\n\n")
        
        print(f"✅ 纯SWRL规则已保存到: {output_file}")
        
    except Exception as e:
        print(f"❌ 保存失败: {e}")

def generate_swrl_summary(swrl_rules):
    """生成SWRL规则摘要统计"""
    if not swrl_rules:
        return
    
    print(f"\n📊 SWRL规则统计摘要:")
    print("-" * 30)
    
    # 按类型统计
    type_counts = {}
    for rule in swrl_rules:
        rule_type = rule['type']
        type_counts[rule_type] = type_counts.get(rule_type, 0) + 1
    
    for rule_type, count in type_counts.items():
        print(f"  📌 {rule_type}: {count} 个")
    
    # 统计有完整结构的规则
    structured_rules = 0
    for rule in swrl_rules:
        structure = parse_swrl_rule_structure(rule['content'])
        if structure['has_structure']:
            structured_rules += 1
    
    print(f"  📌 有完整Body/Head结构: {structured_rules} 个")
    print(f"  📌 总规则数: {len(swrl_rules)} 个")

def main():
    print("🎯 纯SWRL规则提取器")
    print("=" * 60)
    
    # 检查文件
    if not os.path.exists(OWL_FILE_PATH):
        print(f"❌ 文件不存在: {OWL_FILE_PATH}")
        return
    
    print(f"✅ 目标文件: {OWL_FILE_PATH}")
    print(f"📁 文件大小: {os.path.getsize(OWL_FILE_PATH)} bytes")
    
    # 提取纯SWRL规则
    swrl_rules = extract_pure_swrl_rules(OWL_FILE_PATH)
    
    # 显示规则
    display_swrl_rules(swrl_rules)
    
    # 生成统计摘要
    generate_swrl_summary(swrl_rules)
    
    # 保存规则到文件
    if swrl_rules:
        save_pure_swrl_rules(swrl_rules)
        print(f"\n💡 提示: 可以用文本编辑器打开 'pure_swrl_rules.txt' 查看完整的规则内容")
    else:
        print(f"\n💡 建议:")
        print(f"  1. 检查OWL文件是否确实包含SWRL规则")
        print(f"  2. 使用Protégé验证规则的存在")
        print(f"  3. 确认规则使用的是标准SWRL格式")

if __name__ == "__main__":
    main()