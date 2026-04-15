# RAGAS 评测模块实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用 RAGAS 评测框架替换现有的 pytest/OpenJudge/Benchmark 测试评估功能，生成可独立运行的评测模块代码。

**Architecture:** 前端新增 RAGAS 评测配置组件，后端生成独立的 evaluation/ 目录包含评测脚本和依赖，评测结果以 HTML 报告形式输出。

**Tech Stack:** Vue 3 + TypeScript + Element Plus (前端), Python (后端生成代码), RAGAS 框架 (评测)

---

## 文件影响分析

| 文件 | 操作 | 说明 |
|------|------|------|
| `frontend/src/components/RagasEvaluationSettings.vue` | 创建 | 新 RAGAS 评测配置组件 |
| `frontend/src/components/TestGenerationSettings.vue` | 删除 | 移除 pytest 相关 |
| `frontend/src/components/OpenJudgeSettings.vue` | 删除 | 移除 OpenJudge 相关 |
| `frontend/src/components/BenchmarkSettings.vue` | 删除 | 移除 Benchmark 相关 |
| `frontend/src/components/EvaluationSettings.vue` | 删除 | 移除旧评估配置 |
| `frontend/src/components/TestingSettings.vue` | 修改 | 更新引用组件 |
| `frontend/src/components/ConfigurationForm.vue` | 修改 | 更新 step 4 内容 |
| `frontend/src/components/ConfigPreviewPanel.vue` | 修改 | 更新预览面板 |
| `frontend/src/stores/config.ts` | 修改 | 更新数据模型 |
| `frontend/src/types/index.ts` | 修改 | 添加 RagasConfig 类型 |
| `initializr-core/.../metadata/models.py` | 修改 | 添加 ragas 相关字段 |
| `initializr-core/.../converter.py` | 修改 | 添加 ragas 转换逻辑 |
| `initializr-core/.../generator/extensions.py` | 修改 | 生成 evaluation/ 目录代码 |
| `initializr-web/.../router/extensions.py` | 修改 | 更新扩展接口 |

---

## Task 1: 创建 RagasEvaluationSettings.vue 组件

**Files:**
- Create: `initializr-web/frontend/src/components/RagasEvaluationSettings.vue`

- [ ] **Step 1: 创建 RagasEvaluationSettings.vue 组件**

```vue
<template>
  <el-card class="ragas-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <div class="header-left">
          <el-icon :size="20" color="#67C23A"><DataAnalysis /></el-icon>
          <span class="card-title">RAGAS 评测配置</span>
          <el-tag size="small" type="success">可选</el-tag>
        </div>
        <el-switch
          v-model="localForm.enable_ragas_evaluation"
          size="large"
          @change="updateField('enable_ragas_evaluation', $event)"
        />
      </div>
    </template>

    <template v-if="localForm.enable_ragas_evaluation">
      <el-form :model="localForm" label-width="140px" size="large">
        <el-form-item label="数据集文件">
          <el-input
            v-model="localForm.evaluation_csv_filename"
            placeholder="evaluation_data.csv"
            style="width: 280px"
            @change="updateField('evaluation_csv_filename', $event)"
          />
          <span class="hint">CSV 文件需包含: question, answer, context, reference 列</span>
        </el-form-item>

        <el-form-item label="评测指标">
          <el-checkbox-group
            v-model="localForm.evaluation_metrics"
            @change="handleMetricsChange"
          >
            <el-checkbox label="faithfulness">Faithfulness</el-checkbox>
            <el-checkbox label="answer_relevancy">Answer Relevancy</el-checkbox>
            <el-checkbox label="context_precision">Context Precision</el-checkbox>
            <el-checkbox label="context_recall">Context Recall</el-checkbox>
          </el-checkbox-group>
          <span class="hint">选择要计算的评测指标</span>
        </el-form-item>

        <el-divider content-position="left">
          <el-icon><Document /></el-icon>
          生成的文件
        </el-divider>

        <div class="generated-files">
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>evaluation/ragas_evaluator.py</span>
            <el-tag size="small" type="info">评测脚本</el-tag>
          </div>
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>evaluation/requirements.txt</span>
            <el-tag size="small" type="info">依赖</el-tag>
          </div>
          <div class="file-item">
            <el-icon><Document /></el-icon>
            <span>evaluation/README.md</span>
            <el-tag size="small" type="info">使用说明</el-tag>
          </div>
        </div>
      </el-form>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useConfigStore } from '@/stores/config'
import { DataAnalysis, Document } from '@element-plus/icons-vue'

const configStore = useConfigStore()
const form = computed(() => configStore.form)

const localForm = reactive({
  enable_ragas_evaluation: form.value.enable_ragas_evaluation ?? false,
  evaluation_csv_filename: form.value.evaluation_csv_filename || 'evaluation_data.csv',
  evaluation_metrics: form.value.evaluation_metrics || [
    'faithfulness',
    'answer_relevancy',
    'context_precision',
    'context_recall'
  ]
})

const updateField = (field: string, value: any) => {
  configStore.setField(field as any, value)
}

const handleMetricsChange = (value: string[]) => {
  if (value.length === 0) {
    value.push('faithfulness')
  }
  updateField('evaluation_metrics', value)
}
</script>

<style scoped>
.ragas-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
}

.hint {
  font-size: 0.85em;
  color: #909399;
  display: block;
  margin-top: 4px;
  line-height: 1.4;
}

.generated-files {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 6px;
}

.file-item span {
  flex: 1;
  font-family: monospace;
  font-size: 13px;
}

::deep(.el-card__header) {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

::deep(.el-card__body) {
  padding: 20px;
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add initializr-web/frontend/src/components/RagasEvaluationSettings.vue
git commit -m "feat: 添加 RAGAS 评测配置组件"
```

---

## Task 2: 更新 types/index.ts 添加 RagasConfig 类型

**Files:**
- Modify: `initializr-web/frontend/src/types/index.ts`

- [ ] **Step 1: 查看现有类型定义**

```typescript
// 找到 FormConfig 接口定义位置
```

- [ ] **Step 2: 添加 RagasConfig 接口**

```typescript
export interface RagasConfig {
  enable_ragas_evaluation: boolean
  evaluation_csv_filename: string
  evaluation_metrics: string[]
}
```

- [ ] **Step 3: 在 FormConfig 中添加 ragas_config 字段**

在 FormConfig 接口中添加:
```typescript
ragas_config?: RagasConfig
```

- [ ] **Step 4: 提交**

```bash
git add initializr-web/frontend/src/types/index.ts
git commit -m "feat: 添加 RagasConfig 类型定义"
```

---

## Task 3: 更新 stores/config.ts 添加默认值

**Files:**
- Modify: `initializr-web/frontend/src/stores/config.ts`

- [ ] **Step 1: 查找 FormConfig 类型使用位置，添加默认值**

在 config.ts 中添加:
```typescript
enable_ragas_evaluation: false,
evaluation_csv_filename: 'evaluation_data.csv',
evaluation_metrics: ['faithfulness', 'answer_relevancy', 'context_precision', 'context_recall'],
```

- [ ] **Step 2: 提交**

```bash
git add initializr-web/frontend/src/stores/config.ts
git commit -m "feat: 添加 RAGAS 评测配置默认值"
```

---

## Task 4: 更新 ConfigurationForm.vue 替换组件

**Files:**
- Modify: `initializr-web/frontend/src/components/ConfigurationForm.vue`

- [ ] **Step 1: 移除旧组件引入**

删除:
```typescript
import TestGenerationSettings from '@/components/TestGenerationSettings.vue'
import EvaluationSettings from '@/components/EvaluationSettings.vue'
import OpenJudgeSettings from '@/components/OpenJudgeSettings.vue'
import BenchmarkSettings from '@/components/BenchmarkSettings.vue'
```

- [ ] **Step 2: 添加新组件引入**

```typescript
import RagasEvaluationSettings from '@/components/RagasEvaluationSettings.vue'
```

- [ ] **Step 3: 替换模板中的组件**

将 Step 4 中的:
```html
<TestGenerationSettings />
<EvaluationSettings />
<OpenJudgeSettings />
<BenchmarkSettings />
```

替换为:
```html
<RagasEvaluationSettings />
```

- [ ] **Step 4: 提交**

```bash
git add initializr-web/frontend/src/components/ConfigurationForm.vue
git commit -m "feat: 替换测试评估组件为 RAGAS 评测"
```

---

## Task 5: 更新 ConfigPreviewPanel.vue

**Files:**
- Modify: `initializr-web/frontend/src/components/ConfigPreviewPanel.vue`

- [ ] **Step 1: 更新预览面板的评测部分**

找到测试评估相关代码，替换为:
```typescript
if (form.value.enable_ragas_evaluation) {
  lines.push(`ENABLE_RAGAS_EVALUATION=true`)
  lines.push(`EVALUATION_CSV_FILENAME=${form.value.evaluation_csv_filename}`)
  lines.push(`EVALUATION_METRICS=${form.value.evaluation_metrics.join(',')}`)
}
```

- [ ] **Step 2: 提交**

```bash
git add initializr-web/frontend/src/components/ConfigPreviewPanel.vue
git commit -m "feat: 更新预览面板支持 RAGAS 配置"
```

---

## Task 6: 后端 models.py 添加字段

**Files:**
- Modify: `initializr-core/initializr_core/metadata/models.py`

- [ ] **Step 1: 在 Metadata 或相关模型中添加 ragas 配置字段**

```python
@dataclass
class RagasEvaluationConfig:
    enable_ragas_evaluation: bool = False
    evaluation_csv_filename: str = "evaluation_data.csv"
    evaluation_metrics: List[str] = field(default_factory=lambda: [
        "faithfulness", "answer_relevancy", "context_precision", "context_recall"
    ])
```

- [ ] **Step 2: 在主 Metadata 中引用**

```python
ragas_evaluation: Optional[RagasEvaluationConfig] = None
```

- [ ] **Step 3: 提交**

```bash
git add initializr-core/initializr_core/metadata/models.py
git commit -m "feat: 添加 RAGAS 评估配置数据模型"
```

---

## Task 7: 后端 converter.py 添加转换逻辑

**Files:**
- Modify: `initializr-web/initializr_web/converter.py`

- [ ] **Step 1: 添加 ragas 配置转换**

```python
def convert_ragas_config(form_data: dict) -> dict:
    if not form_data.get('enable_ragas_evaluation'):
        return {}
    
    return {
        'enable_ragas_evaluation': True,
        'evaluation_csv_filename': form_data.get('evaluation_csv_filename', 'evaluation_data.csv'),
        'evaluation_metrics': form_data.get('evaluation_metrics', [
            'faithfulness', 'answer_relevancy', 'context_precision', 'context_recall'
        ])
    }
```

- [ ] **Step 2: 在主转换函数中调用**

- [ ] **Step 3: 提交**

```bash
git add initializr-web/initializr_web/converter.py
git commit -m "feat: 添加 RAGAS 配置转换逻辑"
```

---

## Task 8: 更新 extensions.py 生成评测代码

**Files:**
- Modify: `initializr-core/initializr_core/generator/extensions.py`

- [ ] **Step 1: 添加 generate_ragas_evaluation_code 方法**

```python
def generate_ragas_evaluation_code(self, metadata: AgentScopeMetadata) -> str:
    """Generate RAGAS evaluation module code."""
    if not metadata.ragas_evaluation or not metadata.ragas_evaluation.enable_ragas_evaluation:
        return ""

    config = metadata.ragas_evaluation
    metrics_imports = []
    metrics_list = []

    if "faithfulness" in config.evaluation_metrics:
        metrics_imports.append("faithfulness")
        metrics_list.append("faithfulness")
    if "answer_relevancy" in config.evaluation_metrics:
        metrics_imports.append("answer_relevancy")
        metrics_list.append("answer_relevancy")
    if "context_precision" in config.evaluation_metrics:
        metrics_imports.append("context_precision")
        metrics_list.append("context_precision")
    if "context_recall" in config.evaluation_metrics:
        metrics_imports.append("context_recall")
        metrics_list.append("context_recall")

    code = f'''
"""
RAGAS Evaluation Module.

This module provides RAGAS-based evaluation for RAG systems.
Place your evaluation data CSV file in this directory.
"""
import os
import pandas as pd
from datetime import datetime
from ragas import evaluate
from ragas.metrics import {', '.join(metrics_imports)}
from datasets import Dataset

def load_evaluation_data(csv_path: str) -> Dataset:
    """Load evaluation data from CSV file."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Evaluation data file not found: {{csv_path}}")

    df = pd.read_csv(csv_path)
    required_columns = ['question', 'answer', 'context', 'reference']
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {{missing}}")

    return Dataset.from_pandas(df)

def run_evaluation(csv_filename: str = "{config.evaluation_csv_filename}") -> dict:
    """Run RAGAS evaluation."""
    csv_path = os.path.join(os.path.dirname(__file__), csv_filename)

    print(f"Loading evaluation data from: {{csv_path}}")
    dataset = load_evaluation_data(csv_path)

    metrics = [{', '.join(metrics_list)}]

    print(f"Running evaluation with metrics: {{[m.name for m in metrics]}}")
    result = evaluate(dataset, metrics=metrics)

    return result

def generate_html_report(result, output_path: str = "evaluation_report.html"):
    """Generate HTML report from evaluation results."""
    scores = result.scores
    items = result.results if hasattr(result, 'results') else []

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>RAGAS Evaluation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .metric {{ display: inline-block; margin: 10px 20px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #67C23A; }}
        .metric-name {{ font-size: 14px; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #f5f7fa; }}
    </style>
</head>
<body>
    <h1>RAGAS Evaluation Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <div class="summary">
        <h2>Overall Scores</h2>
        {chr(10).join(f'<div class="metric"><div class="metric-value">{{scores.get(m, 0):.4f}}</div><div class="metric-name">{m}</div></div>' for m in ['{', ', '.join(f'"{m}"' for m in metrics_list), '}']) if isinstance(scores, dict) else '<div class="metric-value">N/A</div>'}
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Report generated: {{output_path}}")

if __name__ == "__main__":
    result = run_evaluation()
    generate_html_report(result)
'''

    return code
```

- [ ] **Step 2: 在 engine.py 中调用**

找到生成评测代码的位置，替换为调用新的 generate_ragas_evaluation_code

- [ ] **Step 3: 提交**

```bash
git add initializr-core/initializr_core/generator/extensions.py
git commit -m "feat: 生成 RAGAS 评测模块代码"
```

---

## Task 9: 生成 evaluation/requirements.txt

**Files:**
- Modify: `extensions.py` 添加生成 requirements.txt 的逻辑

- [ ] **Step 1: 添加 generate_ragas_requirements 方法**

```python
def generate_ragas_requirements(self, metadata: AgentScopeMetadata) -> str:
    """Generate requirements.txt for RAGAS evaluation."""
    if not metadata.ragas_evaluation or not metadata.ragas_evaluation.enable_ragas_evaluation:
        return ""

    return """# RAGAS Evaluation Dependencies
ragas>=0.1.0
langchain>=0.1.0
langchain-openai>=0.0.5
pandas>=2.0.0
datasets>=2.14.0
"""
```

- [ ] **Step 2: 提交**

```bash
git add initializr-core/initializr_core/generator/extensions.py
git commit -m "feat: 生成 RAGAS 依赖文件"
```

---

## Task 10: 删除旧组件文件

**Files:**
- Delete:
  - `TestGenerationSettings.vue`
  - `OpenJudgeSettings.vue`
  - `BenchmarkSettings.vue`
  - `EvaluationSettings.vue`

- [ ] **Step 1: 删除文件**

```bash
git rm initializr-web/frontend/src/components/TestGenerationSettings.vue
git rm initializr-web/frontend/src/components/OpenJudgeSettings.vue
git rm initializr-web/frontend/src/components/BenchmarkSettings.vue
git rm initializr-web/frontend/src/components/EvaluationSettings.vue
```

- [ ] **Step 2: 提交**

```bash
git commit -m "feat: 移除旧的测试评估组件"
```

---

## Task 11: 构建并测试

- [ ] **Step 1: 构建 Docker 镜像**

```bash
python3 build_docker.py --arch amd64
```

- [ ] **Step 2: 启动服务测试**

```bash
docker rm -f agentscope; docker run -d -p 8000:8000 --name agentscope agentscope-initializr:latest
curl http://localhost:8000/health
```

- [ ] **Step 3: 验证配置流程**

1. 打开 http://localhost:8000
2. 导航到 Step 4
3. 确认显示 RAGAS 评测配置组件
4. 启用评测，验证配置选项

- [ ] **Step 4: 提交**

```bash
git add -A
git commit -m "feat: 完成 RAGAS 评测模块"
git push
```

---

## 验证清单

- [ ] RAGAS 评测配置组件正确显示
- [ ] CSV 文件名配置生效
- [ ] 评测指标多选框可用
- [ ] 预览面板正确显示配置
- [ ] 生成的代码包含 evaluation/ 目录
- [ ] 生成的 requirements.txt 包含 ragas 依赖
- [ ] 生成的 ragas_evaluator.py 可独立运行
