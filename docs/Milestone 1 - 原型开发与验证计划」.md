# Polymarket信号分析 - 初始规范与原型开发计划
## 1. 项目核心目标
我们实证检测Polymarket平台内异常赔率波动，识别潜在的市场操纵行为，输出可量化的异常信号指标。

## 2. 数据流水线规范
### 2.1 核心接口定义
| 接口名称         | 数据源          | 调用频率 | 核心返回字段                          |
|------------------|-----------------|----------|---------------------------------------|
| 市场基础信息接口 | Polymarket Public API | 10分钟/次 | market_id, title, category, status    |
| 赔率/成交量接口  | Polymarket Public API | 1分钟/次  | timestamp, yes_price, no_price, 24h_volume, liquidity |

### 2.2 标准化数据模型（CSV/Parquet）
| 字段名          | 数据类型 | 说明                                  |
|-----------------|----------|---------------------------------------|
| market_id       | string   | 市场唯一标识（如"us-president-2024"） |
| timestamp       | datetime | 数据采集时间（UTC+0）                 |
| yes_price       | float    | YES选项赔率（0-1）                    |
| no_price        | float    | NO选项赔率（0-1）                     |
| 24h_volume      | float    | 24小时成交量（USD）                   |
| liquidity       | float    | 市场总流动性（USD）                   |
| category        | string   | 市场分类（如"Politics"）              |
| odds_change     | float    | 5分钟赔率变动百分比（计算字段）       |

## 3. 原型开发计划（Milestone 2交付）
### 3.1 开发节点
| 阶段 | 时间窗口 | 交付物                          | 验收标准                                  |
|------|----------|---------------------------------|-------------------------------------------|
| 1    | 1周      | Python爬虫脚本（polymarket_scraper.py） | 稳定抓取3个目标市场数据，每小时生成1份CSV |
| 2    | 1周      | 基础异常检测脚本（anomaly_detection.py） | 识别出赔率变动≥20%的异常数据并标记        |
| 3    | 0.5周    | 测试用例与验证报告              | 异常检测准确率≥90%（人工核对）            |

### 3.2 技术栈
- 数据采集：requests + schedule
- 数据处理：pandas + numpy
- 存储：本地CSV（Milestone 2）→ PostgreSQL（后续阶段）
- 测试：pytest