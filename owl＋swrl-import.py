from owlready2 import *
import os
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# 配置文件路径
OWL_FILE_PATH = r"G:\TUNNEL\Tunnel.owl"

def extract_swrl_rules_comprehensive(file_path):
    """全面的SWRL规则提取方法"""
    print("\n🔍 执行全面的SWRL规则搜索...")
    
    rules_found = []
    
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 文件大小: {len(content)} 字符")
        
        # 扩展的SWRL相关模式搜索
        swrl_patterns = {
            'SWRL规则标签': [
                r'<swrl:Imp[^>]*>.*?</swrl:Imp>',
                r'<ruleml:imp[^>]*>.*?</ruleml:imp>',
                r'<DLSafeRule[^>]*>.*?</DLSafeRule>',
                r'<swrlx:Rule[^>]*>.*?</swrlx:Rule>',
            ],
            'SWRL组件': [
                r'<swrl:body[^>]*>.*?</swrl:body>',
                r'<swrl:head[^>]*>.*?</swrl:head>',
                r'<swrl:classPredicate[^>]*>.*?</swrl:classPredicate>',
                r'<swrl:propertyPredicate[^>]*>.*?</swrl:propertyPredicate>',
                r'<swrl:sameIndividualAtom[^>]*>.*?</swrl:sameIndividualAtom>',
                r'<swrl:differentIndividualsAtom[^>]*>.*?</swrl:differentIndividualsAtom>',
            ],
            'SWRL内置函数': [
                r'<swrlb:[^>]*>.*?</swrlb:[^>]*>',
                r'swrlb:\w+',
            ],
            'SWRL变量和参数': [
                r'<swrl:variable[^>]*>.*?</swrl:variable>',
                r'<swrl:argument[^>]*>.*?</swrl:argument>',
            ]
        }
        
        # 搜索所有模式
        for category, patterns in swrl_patterns.items():
            print(f"\n🔎 搜索 {category}...")
            category_matches = []
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
                if matches:
                    print(f"  ✅ 模式 '{pattern[:30]}...' 找到 {len(matches)} 个匹配")
                    category_matches.extend(matches)
            
            if category_matches:
                rules_found.extend([(category, match) for match in category_matches])
            else:
                print(f"  ❌ {category} 未找到匹配项")
        
        # 使用XML解析器进行更精确的搜索
        print(f"\n🔍 使用XML解析器搜索...")
        try:
            root = ET.fromstring(content)
            
            # 定义SWRL相关的命名空间
            namespaces = {
                'swrl': 'http://www.w3.org/2003/11/swrl#',
                'swrlb': 'http://www.w3.org/2003/11/swrlb#',
                'ruleml': 'http://www.ruleml.org/spec',
                'owl': 'http://www.w3.org/2002/07/owl#',
                'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            }
            
            # 搜索SWRL元素
            swrl_elements = []
            for prefix, uri in namespaces.items():
                elements = root.findall(f".//{{{uri}}}*")
                if elements:
                    print(f"  ✅ {prefix} 命名空间找到 {len(elements)} 个元素")
                    swrl_elements.extend([(prefix, elem) for elem in elements])
            
            if swrl_elements:
                for prefix, elem in swrl_elements:
                    rules_found.append((f"{prefix}元素", ET.tostring(elem, encoding='unicode')))
            
        except ET.ParseError as e:
            print(f"  ❌ XML解析失败: {e}")
            # 尝试修复常见的XML问题
            print("  🔧 尝试修复XML格式...")
            try:
                # 移除可能的问题字符
                cleaned_content = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', content)
                root = ET.fromstring(cleaned_content)
                print("  ✅ XML修复成功")
            except:
                print("  ❌ XML修复失败")
        
        # 搜索人类可读的规则描述
        print(f"\n🔍 搜索规则注释和标签...")
        annotation_patterns = [
            r'<rdfs:label[^>]*>.*?(rule|规则).*?</rdfs:label>',
            r'<rdfs:comment[^>]*>.*?(rule|规则|if|then|implies).*?</rdfs:comment>',
            r'<owl:annotationProperty[^>]*>.*?(rule|规则).*?</owl:annotationProperty>',
        ]
        
        for pattern in annotation_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            if matches:
                print(f"  ✅ 找到 {len(matches)} 个规则相关注释")
                rules_found.extend([("注释", match) for match in matches])
        
    except Exception as e:
        print(f"❌ 文件读取失败: {e}")
    
    return rules_found

def analyze_rule_structure(rules_found):
    """分析找到的规则结构"""
    print(f"\n📊 规则结构分析:")
    
    if not rules_found:
        print("❌ 没有找到规则进行分析")
        return
    
    # 按类型分组
    rule_types = {}
    for rule_type, rule_content in rules_found:
        if rule_type not in rule_types:
            rule_types[rule_type] = []
        rule_types[rule_type].append(rule_content)
    
    # 显示统计信息
    for rule_type, rules in rule_types.items():
        print(f"  📋 {rule_type}: {len(rules)} 项")
        
        # 显示前几个示例（截断显示）
        for i, rule in enumerate(rules[:3], 1):
            truncated_rule = rule[:100].replace('\n', ' ').replace('\t', ' ')
            print(f"    {i}. {truncated_rule}...")
    
    return rule_types

def suggest_debugging_steps():
    """提供调试建议"""
    print(f"\n💡 调试建议:")
    print(f"  1. 使用Protégé打开OWL文件，查看'Rules'标签页")
    print(f"  2. 检查文件是否使用了自定义的规则表示方法")
    print(f"  3. 搜索文件中的'→'、'->'、'implies'等关键词")
    print(f"  4. 检查是否有内嵌的JavaScript或其他格式的规则")
    print(f"  5. 查看OWL文件的导出设置，确保包含了SWRL规则")

def create_rule_report(rules_found, output_file="swrl_rules_report.txt"):
    """生成详细的规则报告"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("SWRL规则提取报告\n")
            f.write("=" * 50 + "\n\n")
            
            if not rules_found:
                f.write("未找到任何SWRL规则\n")
                return
            
            f.write(f"总共找到 {len(rules_found)} 个规则相关项\n\n")
            
            for i, (rule_type, rule_content) in enumerate(rules_found, 1):
                f.write(f"规则 {i} ({rule_type}):\n")
                f.write("-" * 30 + "\n")
                f.write(rule_content)
                f.write("\n\n")
        
        print(f"✅ 规则报告已保存到: {output_file}")
        
    except Exception as e:
        print(f"❌ 保存报告失败: {e}")

def main():
    print("🎯 增强版SWRL规则分析器")
    print("=" * 60)
    
    # 检查文件
    if not os.path.exists(OWL_FILE_PATH):
        print(f"❌ 文件不存在: {OWL_FILE_PATH}")
        return
    
    print(f"✅ 文件存在: {OWL_FILE_PATH}")
    print(f"📁 文件大小: {os.path.getsize(OWL_FILE_PATH)} bytes")
    
    # 执行全面的规则提取
    rules_found = extract_swrl_rules_comprehensive(OWL_FILE_PATH)
    
    # 分析规则结构
    rule_types = analyze_rule_structure(rules_found)
    
    # 生成报告
    if rules_found:
        create_rule_report(rules_found)
    
    # 提供调试建议
    suggest_debugging_steps()
    
    print(f"\n📊 最终统计:")
    print(f"  - 总规则项数: {len(rules_found)}")
    print(f"  - 规则类型数: {len(rule_types) if rules_found else 0}")

if __name__ == "__main__":
    main()