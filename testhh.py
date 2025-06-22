from owlready2 import get_ontology, sync_reasoner
from pathlib import Path
import os

# 你的文件路径 - 已更新
file_path = r"G:\tunnel3dmodeling\Tunnel.owl"

print(f"🔍 检查文件: {file_path}")
print(f"📏 文件大小: {Path(file_path).stat().st_size} 字节")

# 多种加载方式
print("\n🔄 尝试不同的加载方法...")

# 方法1: 直接使用路径
try:
    print("方法1: 直接路径")
    onto = get_ontology(file_path).load()
    print("✅ 成功！")
except Exception as e:
    print(f"❌ 失败: {e}")
    onto = None

# 方法2: 使用 pathlib 的 as_uri
if onto is None:
    try:
        print("方法2: pathlib as_uri")
        file_uri = Path(file_path).as_uri()
        print(f"   URI: {file_uri}")
        onto = get_ontology(file_uri).load()
        print("✅ 成功！")
    except Exception as e:
        print(f"❌ 失败: {e}")

# 方法3: 转换路径分隔符
if onto is None:
    try:
        print("方法3: 转换路径分隔符")
        unix_path = file_path.replace('\\', '/')
        file_url = f"file:///{unix_path}"
        print(f"   URL: {file_url}")
        onto = get_ontology(file_url).load()
        print("✅ 成功！")
    except Exception as e:
        print(f"❌ 失败: {e}")

# 方法4: 使用 os.path.abspath
if onto is None:
    try:
        print("方法4: os.path.abspath")
        abs_path = os.path.abspath(file_path)
        file_url = f"file:///{abs_path.replace(chr(92), '/')}"  # 替换反斜杠
        print(f"   URL: {file_url}")
        onto = get_ontology(file_url).load()
        print("✅ 成功！")
    except Exception as e:
        print(f"❌ 失败: {e}")

# 方法5: 先检查文件内容格式
if onto is None:
    print("\n🔍 检查文件内容...")
    try:
        with open(file_path, 'rb') as f:
            first_100_bytes = f.read(100)
            print(f"前100字节: {first_100_bytes}")
            
        # 检查是否是XML格式
        if b'<?xml' in first_100_bytes or b'<rdf:RDF' in first_100_bytes:
            print("✅ 文件看起来是XML/RDF格式")
            
            # 尝试重命名文件
            new_path = file_path + '.backup'
            print(f"🔄 尝试复制文件到: {new_path}")
            
            import shutil
            shutil.copy2(file_path, new_path)
            
            # 加载重命名后的文件
            onto = get_ontology(new_path).load()
            print("✅ 重命名后加载成功！")
        else:
            print("❌ 文件不是有效的XML/RDF格式")
            
    except Exception as e:
        print(f"❌ 检查文件内容失败: {e}")

# 如果加载成功，继续处理
if onto:
    print("\n🎉 本体加载成功！开始分析...")
    
    # 基本统计 - 使用更安全的方法
    try:
        print("📊 获取本体统计信息...")
        
        # 安全地获取类
        classes = []
        try:
            classes = list(onto.classes())
            print(f"  - 类: {len(classes)}")
        except Exception as e:
            print(f"  ❌ 获取类失败: {e}")
            # 尝试直接查询三元组
            try:
                from owlready2 import Thing
                classes_query = list(onto.world.sparql("""
                    SELECT DISTINCT ?cls WHERE {
                        ?cls rdf:type owl:Class .
                    }
                """))
                print(f"  - 类 (通过SPARQL): {len(classes_query)}")
            except Exception as e2:
                print(f"  ❌ SPARQL查询类也失败: {e2}")
        
        # 安全地获取个体
        individuals = []
        try:
            individuals = list(onto.individuals())
            print(f"  - 个体: {len(individuals)}")
        except Exception as e:
            print(f"  ❌ 获取个体失败: {e}")
            # 尝试直接查询
            try:
                individuals_query = list(onto.world.sparql("""
                    SELECT DISTINCT ?ind WHERE {
                        ?ind rdf:type ?cls .
                        ?cls rdf:type owl:Class .
                    }
                """))
                print(f"  - 个体 (通过SPARQL): {len(individuals_query)}")
            except Exception as e2:
                print(f"  ❌ SPARQL查询个体也失败: {e2}")
        
        # 安全地获取属性
        properties = []
        try:
            properties = list(onto.properties())
            print(f"  - 属性: {len(properties)}")
        except Exception as e:
            print(f"  ❌ 获取属性失败: {e}")
            try:
                props_query = list(onto.world.sparql("""
                    SELECT DISTINCT ?prop WHERE {
                        { ?prop rdf:type owl:ObjectProperty } UNION
                        { ?prop rdf:type owl:DatatypeProperty } UNION
                        { ?prop rdf:type owl:AnnotationProperty }
                    }
                """))
                print(f"  - 属性 (通过SPARQL): {len(props_query)}")
            except Exception as e2:
                print(f"  ❌ SPARQL查询属性也失败: {e2}")
                
    except Exception as e:
        print(f"❌ 统计分析失败: {e}")
    
    # 显示本体基本信息
    print(f"\n📋 本体基本信息:")
    print(f"  - 本体IRI: {onto.base_iri}")
    print(f"  - 命名空间: {onto.name}")
    
    # 尝试显示一些三元组
    print(f"\n🔍 查看本体内容 (前10个三元组):")
    try:
        triples = list(onto.world.sparql("SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"))
        for i, (s, p, o) in enumerate(triples, 1):
            print(f"{i}. {s} -> {p} -> {o}")
    except Exception as e:
        print(f"❌ 无法查询三元组: {e}")
    
    # 推理 - 暂时跳过，因为可能导致同样的元类问题
    print("\n⚠️  暂时跳过推理步骤以避免元类冲突")
    
    # 安全地显示个体
    if individuals:
        print(f"\n👥 个体列表 (前5个):")
        for i, indiv in enumerate(individuals[:5], 1):
            try:
                print(f"{i}. 【{indiv.name}】")
                # 安全地获取属性
                try:
                    props = indiv.get_properties()
                    if props:
                        for prop in list(props)[:2]:
                            try:
                                values = prop[indiv]
                                if values:
                                    print(f"   - {prop.name}: {values}")
                            except:
                                pass
                except:
                    print(f"   (无法获取属性信息)")
            except Exception as e:
                print(f"{i}. 【个体{i}】 (名称获取失败: {e})")
    
else:
    print("\n❌ 所有方法都失败了")
    print("💡 建议:")
    print("1. 检查文件是否损坏")
    print("2. 尝试从Protégé重新导出")
    print("3. 确保文件是有效的OWL/RDF格式")