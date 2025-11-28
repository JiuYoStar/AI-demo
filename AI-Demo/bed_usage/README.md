# Bed Usage Analysis System

## 简介
这是一个基于 Flask 和 Pandas 的医院床位使用情况分析系统。系统通过读取 Excel 数据文件，计算各医院和科室的床位使用率、空闲情况等指标，并提供 RESTful API 供前端展示。系统实现了完善的缓存机制，以提高大规模数据处理时的响应速度。

## 系统架构流程图

```mermaid
graph TD
    %% 定义样式
    classDef process fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef storage fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef decision fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rhombus;
    classDef interface fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef log fill:#424242,stroke:#000,stroke-width:1px,color:#fff;

    subgraph Client ["客户端 / API 调用"]
        API_Req[("HTTP 请求<br>(/api/hospital_usage 等)")]:::interface
    end

    subgraph App_Layer ["Flask 应用层 (app.py)"]
        Start(应用启动):::process
        Route_Handler(路由处理):::process
        Mem_Cache[("内存缓存<br>(_cache)")]:::storage
        Async_Task(异步预计算线程):::process
    end

    subgraph Service_Layer ["数据服务层 (data_service.py)"]
        Precompute(precompute_data<br>预计算聚合逻辑):::process
        Load_Excel(load_data<br>读取 Excel):::process
        Calc_Stats(计算统计/热力图):::process
    end

    subgraph Cache_Layer ["缓存管理层 (cache_manager.py)"]
        Check_Update{Excel<br>是否更新?}:::decision
        Check_Cache_File{缓存文件<br>是否存在/更新?}:::decision
        Load_File_Cache(load_cache_from_file):::process
        Save_File_Cache(save_cache_to_file):::process
        MD5_Check(MD5 / 时间戳校验):::process
    end

    subgraph File_System ["文件系统"]
        Excel_File[("hospital_bed_usage_data.xlsx")]:::storage
        Cache_File[("caches/data_cache.pkl<br>caches/metadata.json")]:::storage
        Log_File[("configs/logs/app.log")]:::log
    end

    %% 启动流程
    Start --> Check_Cache_File
    Check_Cache_File -- 是 --> Load_File_Cache
    Check_Cache_File -- 否 --> Async_Task
    Load_File_Cache --> Mem_Cache
    Load_File_Cache --> Check_Update
    Check_Update -- 是 (过期) --> Async_Task
    Check_Update -- 否 (有效) --> App_Ready[应用就绪]

    %% API 请求流程
    API_Req --> Route_Handler
    Route_Handler --> Mem_Cache
    Mem_Cache -- 命中 --> Return_JSON[返回 JSON 数据]:::interface
    Mem_Cache -- 未命中 --> Load_File_Cache
    Load_File_Cache -- 成功 --> Return_JSON
    Load_File_Cache -- 失败 --> Async_Task
    Async_Task -.-> Return_Empty[返回空数据/状态]:::interface

    %% 数据处理与缓存流程
    Async_Task --> Precompute
    Precompute --> Load_Excel
    Load_Excel --> Excel_File
    Precompute --> Calc_Stats
    Calc_Stats --> Save_File_Cache
    Save_File_Cache --> Cache_File
    Save_File_Cache --> Mem_Cache

    %% 日志记录
    Start -.-> Log_File
    Precompute -.-> Log_File
    API_Req -.-> Log_File
    Error_Handler -.-> Log_File

```

## 核心逻辑说明

### 1. 缓存策略 (Cache Strategy)
系统采用 **内存 + 文件** 的二级缓存策略：
1.  **一级缓存 (内存)**: `_cache` 字典，最快访问速度。
2.  **二级缓存 (文件)**: `pickle` 序列化文件，用于持久化和跨重启共享。
3.  **缓存失效**: 通过对比 Excel 文件的 **修改时间** 和 **MD5** 值来判断缓存是否过期。

### 2. 数据预计算 (Precomputation)
为了避免每次请求都解析庞大的 Excel 文件，系统在后台进行预计算：
*   **触发时机**: 应用启动时、缓存过期时、或 API 请求未命中缓存时。
*   **计算内容**: 医院/科室床位总数、占用率、热力图数据等。
*   **并发控制**: 使用 `threading` 和 `_cache['precomputing']` 标志位防止重复计算。

### 3. 日志系统 (Logging)
*   使用 `RotatingFileHandler` 实现日志轮转（10MB/文件，保留5个）。
*   同时输出到控制台和 `configs/logs/app.log`。
*   记录关键操作：启动、数据加载、缓存更新、错误堆栈。

## 目录结构
*   `app.py`: Flask 应用入口，路由定义。
*   `data_service.py`: 核心业务逻辑，数据计算与处理。
*   `caches/cache_manager.py`: 缓存文件读写与校验工具。
*   `configs/logger.py`: 日志配置。
*   `precompute_data.py`: 独立的可执行脚本，用于定时任务或手动触发预计算。
