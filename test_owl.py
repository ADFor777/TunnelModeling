import owlready2
import sys
import os

def check_owlready2_optimization():
    """检查和尝试启用 Owlready2 优化模块"""
    
    print("=== Owlready2 优化模块检查 ===")
    
    # 尝试获取版本信息
    try:
        version = owlready2.__version__
        print(f"Owlready2 版本: {version}")
    except AttributeError:
        try:
            import pkg_resources
            version = pkg_resources.get_distribution("owlready2").version
            print(f"Owlready2 版本: {version}")
        except:
            print("Owlready2 版本: 无法获取")
    
    print(f"Python 版本: {sys.version}")
    print(f"安装路径: {owlready2.__file__}")
    
    # 方法1: 检查是否已经有编译好的优化模块
    try:
        import owlready2_optimized
        print("✓ 找到预编译的优化模块 owlready2_optimized")
        return True
    except ImportError:
        print("✗ 未找到预编译的优化模块")
    
    # 方法2: 尝试通过 Cython 编译
    try:
        import Cython
        print(f"✓ Cython 可用，版本: {Cython.__version__}")
        
        # 尝试使用 pyximport 编译
        try:
            import pyximport
            pyximport.install()
            print("✓ pyximport 设置成功")
            
            # 尝试导入优化模块
            from owlready2 import namespace
            print("✓ 优化模块可能已启用")
            return True
            
        except Exception as e:
            print(f"✗ pyximport 编译失败: {e}")
            
    except ImportError:
        print("✗ Cython 未安装")
    
    # 方法3: 手动编译（需要开发环境）
    print("\n=== 手动编译建议 ===")
    print("如果需要最佳性能，可以尝试以下方法：")
    print("1. 安装编译依赖: pip install Cython")
    print("2. 重新安装 owlready2: pip uninstall owlready2 && pip install owlready2")
    print("3. 或者从源码编译: pip install owlready2 --no-binary :all:")
    
    return False

def setup_owlready2_performance():
    """设置 Owlready2 的性能优化选项"""
    
    print("\n=== 性能优化设置 ===")
    
    # 设置推理机
    try:
        owlready2.JAVA_EXE = None  # 如果没有 Java，设置为 None
        print("✓ Java 推理机设置")
    except:
        pass
    
    # 设置 SQLite 优化
    try:
        # 启用 WAL 模式和其他 SQLite 优化
        owlready2.default_world.set_backend(filename=":memory:")
        print("✓ 使用内存数据库以提高速度")
    except Exception as e:
        print(f"数据库优化设置: {e}")
    
    # 禁用一些调试功能以提高性能
    try:
        owlready2.set_log_level(9)  # 减少日志输出
        print("✓ 优化日志级别")
    except:
        pass

def alternative_performance_tips():
    """提供其他性能优化建议"""
    
    print("\n=== 替代性能优化建议 ===")
    print("即使没有 Cython 优化，也可以通过以下方式提升性能：")
    print("1. 使用内存数据库而不是文件数据库")
    print("2. 批量操作而不是逐个操作")
    print("3. 合理使用 with 语句管理世界状态")
    print("4. 避免不必要的推理操作")
    print("5. 使用适当的索引和查询优化")

def main():
    """主函数：检查并尝试优化 Owlready2"""
    
    # 检查优化模块
    optimization_available = check_owlready2_optimization()
    
    # 设置性能优化
    setup_owlready2_performance()
    
    # 提供替代建议
    alternative_performance_tips()
    
    # 简单的性能测试
    print("\n=== 简单性能测试 ===")
    import time
    
    start_time = time.time()
    
    # 创建一个简单的本体进行测试
    onto = owlready2.get_ontology("http://test.org/test.owl")
    
    with onto:
        class TestClass(owlready2.Thing):
            pass
        
        # 创建一些实例
        for i in range(100):
            TestClass(f"instance_{i}")
    
    end_time = time.time()
    print(f"创建 100 个实例耗时: {end_time - start_time:.4f} 秒")
    
    if optimization_available:
        print("✓ 优化模块可能已启用，性能应该较好")
    else:
        print("! 使用纯 Python 实现，性能可能较慢但功能完整")

if __name__ == "__main__":
    main()

