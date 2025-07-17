import json

def process_casebook():
    try:
        # 读取JSON文件
        print("正在读取 Casebook.json...")
        with open('Casebook.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        print(f"读取到 {len(data)} 个案例")
        
        processed_count = 0
        skipped_count = 0
        
        # 处理每个案例
        for index, case_item in enumerate(data):
            try:
                # 安全获取案例名称
                case_name = case_item.get('name', f"案例{index + 1}")
                case_id = case_item.get('id', 'Unknown')
                
                # 检查必要的字段
                if 'condition' not in case_item:
                    print(f"跳过案例 {index + 1} ({case_name}): 缺少 condition 字段")
                    skipped_count += 1
                    continue
                    
                if 'solution' not in case_item:
                    print(f"跳过案例 {index + 1} ({case_name}): 缺少 solution 字段")
                    skipped_count += 1
                    continue
                
                # 检查是否存在 hasConstructionMethod
                if 'hasConstructionMethod' in case_item['condition']:
                    # 移动 hasConstructionMethod 到 solution
                    construction_method = case_item['condition']['hasConstructionMethod']
                    case_item['solution']['hasConstructionMethod'] = construction_method
                    del case_item['condition']['hasConstructionMethod']
                    
                    print(f"✓ 处理案例 {index + 1} ({case_name}): {construction_method}")
                    processed_count += 1
                else:
                    print(f"- 案例 {index + 1} ({case_name}): 未找到 hasConstructionMethod")
                    skipped_count += 1
                    
            except Exception as e:
                print(f"处理案例 {index + 1} 时出错: {str(e)}")
                skipped_count += 1
        
        # 保存处理后的文件
        print("\n正在保存处理后的文件...")
        with open('Casebook_updated.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        # 输出统计结果
        print(f"\n处理完成！")
        print(f"总案例数: {len(data)}")
        print(f"成功处理: {processed_count}")
        print(f"跳过案例: {skipped_count}")
        print(f"文件已保存为: Casebook_updated.json")
        
    except FileNotFoundError:
        print("错误: 找不到 Casebook.json 文件")
        print("请确保文件在当前目录中")
    except json.JSONDecodeError as e:
        print(f"错误: JSON文件格式不正确 - {str(e)}")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")

if __name__ == "__main__":
    process_casebook()