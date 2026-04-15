# RAGAS 评测模块设计

## 概述

用 RAGAS 评测框架替换现有的 pytest/OpenJudge/Benchmark 测试评估相关功能，生成独立的评测模块代码。

## 需求

- **数据来源**：用户手动上传 CSV 文件（包含 question, answer, context, reference）
- **结果展示**：生成 HTML 报告文件
- **评测指标**：综合评估（Faithfulness、Answer Relevancy、Context Precision、Context Recall）
- **执行方式**：用户下载代码后，在本地运行评测脚本

## 前端改动

### 移除的组件
- `TestGenerationSettings.vue` - pytest 测试生成
- `OpenJudgeSettings.vue` - OpenJudge 集成
- `BenchmarkSettings.vue` - 基准测试
- `EvaluationSettings.vue` - 旧评估配置

### 新增组件
**RagasEvaluationSettings.vue**

配置项：
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| enable_ragas_evaluation | boolean | false | 是否启用 RAGAS 评测 |
| evaluation_csv_filename | string | "evaluation_data.csv" | CSV 文件名 |
| evaluation_metrics | string[] | ["faithfulness", "answer_relevancy", "context_precision", "context_recall"] | 评测指标 |

### 数据模型

```typescript
interface RagasConfig {
  enable_ragas_evaluation: boolean
  evaluation_csv_filename: string
  evaluation_metrics: string[]
}
```

## 后端生成代码结构

生成的项目中新增 `evaluation/` 目录：

```
project/
├── evaluation/
│   ├── __init__.py
│   ├── ragas_evaluator.py    # 主评测脚本
│   ├── metrics_config.py     # 指标配置
│   └── requirements.txt      # ragas 依赖
├── tests/                    # 现有测试目录（保留）
├── agentscope/
├── config.yaml
└── README.md
```

### ragas_evaluator.py 功能

1. 读取 CSV 文件
2. 转换为 RAGAS Dataset 格式
3. 执行评测（多指标）
4. 生成 HTML 报告

### requirements.txt 依赖

```
ragas>=0.1.0
langchain>=0.1.0
pandas>=2.0.0
datasets>=2.14.0
```

## 评测执行流程

1. 用户在 AgentScope Initializr 中生成项目代码（勾选 RAGAS 评测）
2. 用户将 CSV 数据文件放入 `evaluation/` 目录
3. 用户安装依赖：`pip install -r evaluation/requirements.txt`
4. 用户运行：`python -m evaluation.ragas_evaluator`
5. 生成 `evaluation_report.html`
6. 用户在浏览器中打开查看评测结果

## CSV 格式要求

```csv
question,answer,context,reference
"问题1","回答1","上下文1","参考答案1"
"问题2","回答2","上下文2","参考答案2"
```

## HTML 报告内容

- 各项指标得分（雷达图/柱状图）
- 每条数据的详细评分
- 综合评分
- 生成时间

## 实现步骤

1. 创建 `RagasEvaluationSettings.vue` 组件
2. 更新 `config.ts` 和 `types/index.ts` 数据模型
3. 更新 `extensions.py` 生成评测代码
4. 更新 `converter.py` 数据转换
5. 更新 `models.py` 元数据模型
6. 移除旧的测试评估相关组件
7. 更新 `ConfigurationForm.vue` 移除旧组件引用
8. 更新 `ConfigPreviewPanel.vue` 预览面板
9. 编写测试
10. 更新文档
