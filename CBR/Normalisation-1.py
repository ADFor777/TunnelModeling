import json
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 1. 加载现有文件
with open("g:/02/TUNNEL/TunnelModeling/CBR/Casebook.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 添加或删除案例
# 举个例子：删除最后一个案例
data.pop()  # 删除最后一个案例

# 或者添加新的案例
new_case = {
    "id": 5,
    "condition": {
        "hasTunnelLength": 3500,
        "hasTunnelDiameter": 11.5,
        "hasTunnelType": "ShallowTunnelProject",
        "hasGeologicalCondition": "II",
        "hasHydroCondition": "Medium",
        "hasSoilType": "StrongSoil",
        "hasConstructionMethod": "DrillBlast"
    },
    "solution": {
        "hasBoltLength": 3.6,
        "hasBoltRowCount": 3,
        "hasBoltColumnCount": 3,
        "hasLiningThickness": 28,
        "hasSteelArchSpacing": 1.0,
        "hasSteelArchCount": 30,
        "hasSteelArchThickness": 9,
        "hasWaterproofLayerThickness": 7
    }
}
data.append(new_case)

# 3. 对所有案例进行归一化（重新计算）
# 提取 condition 部分并转换为数值
condition_fields = [
    "hasTunnelLength", "hasTunnelDiameter", "hasTunnelType", "hasGeologicalCondition", 
    "hasHydroCondition", "hasSoilType", "hasConstructionMethod"
]
category_maps = {
    "hasTunnelType": {"ShallowTunnelProject": 1, "MountainTunnelProject": 2, "UnderwaterTunnelProject": 3, "UrbanTunnelProject": 4, "DeepTunnelProject": 5},
    "hasGeologicalCondition": {"I": 1, "II": 2, "III": 3, "IV": 4,"V": 5},
    "hasHydroCondition": {"Dry": 1, "Medium": 2, "WaterRich": 3},
    "hasSoilType": {"WeakSoil": 1, "Medium Soil": 2, "StrongSoil": 3},
    "hasConstructionMethod": {"DrillBlast": 1, "Shield": 2}
}

# 转换为向量
vectors = []
for case in data:
    vec = []
    condition = case["condition"]
    for field in condition_fields:
        value = condition.get(field)
        if isinstance(value, str):
            encoded = category_maps.get(field, {}).get(value, 0)
            vec.append(encoded)
        else:
            vec.append(value)
    vectors.append(vec)

# 4. 归一化
scaler = MinMaxScaler()
normalized_vectors = scaler.fit_transform(np.array(vectors))

# 5. 保存到文件
with open("Casebook.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 6. 保存归一化后的向量为 CSV 文件
import pandas as pd
df = pd.DataFrame(normalized_vectors, columns=condition_fields)
df.to_csv("normalized_case_vectors.csv", index=False, encoding="utf-8-sig")

print("✅ 文件已更新并保存！")
