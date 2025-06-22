from owlready2 import get_ontology, sync_reasoner_pellet, default_world

# ✅ 加载你的 OWL 文件
onto = get_ontology(r"G:\TUNNEL\Tunnel.owl").load()

# ✅ 打印所有 SWRL 规则
print("📜 本体中的 SWRL 规则：")
for rule in list(onto.swrl_rules()):
    print(rule)

# ✅ 启动 Pellet 推理器（你需要联网）
with onto:
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)

print("✅ 推理完成！")

# ✅ 示例：打印推理出的某个属性（如 BoltLength）
for indiv in onto.individuals():
    if "Tunnel" in indiv.name:
        print(f"📦 {indiv.name}")
        for prop in indiv.get_properties():
            for value in prop[indiv]:
                print(f"  📌 {prop.python_name} → {value}")

