import re
import sys
import html
from rdflib import Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL

# 手动定义命名空间
SWRL = Namespace("http://www.w3.org/2003/11/swrl#")
SWRLA = Namespace("http://swrl.stanford.edu/ontologies/3.3/swrla.owl#")

def extract_rules(xml_content):
    """从XML中提取所有规则"""
    # 使用更精确的正则表达式匹配完整规则结构
    rule_pattern = re.compile(r'(<Rule.*?>.*?</Rule>)', re.DOTALL)
    return rule_pattern.findall(xml_content)

def xml_to_n3(xml_content, base_namespace="http://example.com/dlsafe#"):
    """将SWRL XML格式转换为N3格式"""
    DLS = Namespace(base_namespace)
    
    n3_content = f"""@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix swrl: <http://www.w3.org/2003/11/swrl#>.
@prefix swrla: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#>.
@prefix dls: <{base_namespace}>.

"""
    
    # 提取所有规则
    rules = extract_rules(xml_content)
    if not rules:
        print("警告：未找到规则！")
        return n3_content + "# 未找到规则"
    
    print(f"找到 {len(rules)} 条规则")
    
    # 转换每条规则
    for i, rule_xml in enumerate(rules):
        try:
            # 提取规则名称
            rule_name_match = re.search(r'<AnnotationProperty abbreviatedIRI="rdfs:label"/>\s*<Literal>(.*?)</Literal>', rule_xml)
            rule_name = rule_name_match.group(1) if rule_name_match else f"Rule_{i+1}"
            rule_name = sanitize_name(rule_name)
            
            print(f"处理规则: {rule_name}")
            
            n3_content += f"\n# 规则 {i+1}: {rule_name}\n"
            n3_content += f"dls:{rule_name} a swrl:Rule ;\n"
            
            # 提取规则注释
            comment_match = re.search(r'<AnnotationProperty abbreviatedIRI="rdfs:comment"/>\s*<Literal>(.*?)</Literal>', rule_xml)
            if comment_match:
                comment = escape_special_chars(comment_match.group(1))
                n3_content += f'    rdfs:comment "{comment}" ;\n'
            
            # 提取规则启用状态
            enabled_match = re.search(r'<AnnotationProperty IRI="http://swrl.stanford.edu/ontologies/3.3/swrla.owl#isRuleEnabled"/>\s*<Literal datatypeIRI="http://www.w3.org/2001/XMLSchema#boolean">(.*?)</Literal>', rule_xml)
            if enabled_match:
                enabled = enabled_match.group(1).lower()
                n3_content += f"    swrla:isRuleEnabled {enabled} ;\n"
            
            # 提取规则标签
            n3_content += f'    rdfs:label "{rule_name}" ;\n'
            
            # 提取并处理Body
            body_content = re.search(r'<Body>(.*?)</Body>', rule_xml, re.DOTALL)
            if body_content:
                n3_body = process_body(body_content.group(1), DLS)
                n3_content += f"    swrl:body [\n{n3_body}    ] ;\n"
            else:
                n3_content += "    swrl:body [ ] ;\n"
            
            # 提取并处理Head
            head_content = re.search(r'<Head>(.*?)</Head>', rule_xml, re.DOTALL)
            if head_content:
                n3_head = process_head(head_content.group(1), DLS)
                n3_content += f"    swrl:head [\n{n3_head}    ].\n"
            else:
                n3_content += "    swrl:head [ ].\n"
                
        except Exception as e:
            print(f"警告：处理规则 {i+1} 时出错: {str(e)}")
            continue
    
    return n3_content

def process_body(body_content, namespace):
    """处理规则主体部分"""
    n3_body = ""
    
    # 提取ClassAtom
    class_atoms = re.findall(r'<ClassAtom>(.*?)</ClassAtom>', body_content, re.DOTALL)
    for atom in class_atoms:
        class_iri = extract_iri(atom, "Class IRI")
        variable = extract_variable(atom)
        n3_body += f"        swrl:classAtom [\n"
        n3_body += f"            swrl:class {get_namespaced_uri(class_iri, namespace)} ;\n"
        n3_body += f"            swrl:variable {variable}\n"
        n3_body += "        ] ;\n"
    
    # 提取ObjectPropertyAtom
    object_atoms = re.findall(r'<ObjectPropertyAtom>(.*?)</ObjectPropertyAtom>', body_content, re.DOTALL)
    for atom in object_atoms:
        property_iri = extract_iri(atom, "ObjectProperty IRI")
        variable = extract_variable(atom)
        individual_iri = extract_iri(atom, "NamedIndividual IRI")
        n3_body += f"        swrl:objectPropertyAtom [\n"
        n3_body += f"            swrl:objectProperty {get_namespaced_uri(property_iri, namespace)} ;\n"
        n3_body += f"            swrl:variable {variable} ;\n"
        n3_body += f"            swrl:namedIndividual {get_namespaced_uri(individual_iri, namespace)}\n"
        n3_body += "        ] ;\n"
    
    # 提取DataPropertyAtom
    data_atoms = re.findall(r'<DataPropertyAtom>(.*?)</DataPropertyAtom>', body_content, re.DOTALL)
    for atom in data_atoms:
        property_iri = extract_iri(atom, "DataProperty IRI")
        variable = extract_variable(atom)
        literal, datatype = extract_literal(atom)
        n3_body += f"        swrl:dataPropertyAtom [\n"
        n3_body += f"            swrl:dataProperty {get_namespaced_uri(property_iri, namespace)} ;\n"
        n3_body += f"            swrl:variable {variable} ;\n"
        n3_body += f'            swrl:literal "{escape_special_chars(literal)}"^^xsd:{get_datatype(datatype)}\n'
        n3_body += "        ] ;\n"
    
    # 移除最后一个分号并添加换行
    if n3_body.endswith(";\n"):
        n3_body = n3_body[:-2] + "\n"
    
    return n3_body

def process_head(head_content, namespace):
    """处理规则头部部分"""
    # 头部处理与主体类似
    return process_body(head_content, namespace)

def extract_iri(text, tag_name):
    """从文本中提取IRI"""
    pattern = re.compile(rf'<{tag_name}>(.*?)</{tag_name.split()[0]}>')
    match = pattern.search(text)
    return match.group(1) if match else ""

def extract_variable(text):
    """从文本中提取变量"""
    pattern = re.compile(r'<Variable abbreviatedIRI=":(.*?)"')
    match = pattern.search(text)
    return f":{match.group(1)}" if match else ""

def extract_literal(text):
    """从文本中提取文字值和数据类型"""
    literal_pattern = re.compile(r'<Literal datatypeIRI="(.*?)">(.*?)</Literal>')
    match = literal_pattern.search(text)
    return (match.group(2), match.group(1)) if match else ("", "")

def get_local_name(iri):
    """从IRI中获取本地名称"""
    return iri.split("#")[-1] if "#" in iri else iri.split("/")[-1]

def get_datatype(full_datatype):
    """从完整数据类型IRI获取简写"""
    return full_datatype.split("#")[-1] if "#" in full_datatype else full_datatype.split("/")[-1]

def get_namespaced_uri(iri, namespace):
    """将IRI转换为命名空间前缀形式"""
    local_name = get_local_name(iri)
    if not local_name:
        return iri  # 如果无法提取本地名称，返回原始IRI
    return f"{namespace.prefix}:{local_name}"

def escape_special_chars(text):
    """转义N3中的特殊字符"""
    # 使用HTML转义处理特殊字符
    return html.escape(text)

def sanitize_name(name):
    """清理名称，确保符合N3标识符要求"""
    # 替换非字母数字字符为下划线
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python swrl_xml_to_n3.py <输入XML文件> <输出N3文件> [本体命名空间]")
        print("示例: python swrl_xml_to_n3.py pure_swrl_rules.txt pure_swrl_rules.n3 http://example.com/dlsafe#")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    base_namespace = sys.argv[3] if len(sys.argv) > 3 else "http://example.com/dlsafe#"
    
    print(f"开始转换: {input_file} -> {output_file}")
    print(f"使用命名空间: {base_namespace}")
    
    try:
        # 读取XML文件
        with open(input_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # 转换为N3格式
        n3_content = xml_to_n3(xml_content, base_namespace)
        
        # 写入N3文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(n3_content)
        
        print(f"转换完成！已将 {input_file} 转换为 {output_file}")
        
    except Exception as e:
        print(f"转换过程中出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()