# Temperature 配置区域改进设计

## 新布局设计

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🤖 Model Parameters                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Temperature Configuration                                      │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │                                                         │   │   │
│  │  │  Temperature  📊                                           │   │   │
│  │  │  ┌───────────────────────────────────────────────────┐  │   │   │
│  │  │  │  [0.7] 💾           数值输入框                   │  │   │   │
│  │  │  │  ↑              ↑                               │  │   │   │
│  │  │  │  当前值        保存/重置按钮                      │  │   │   │
│  │  │  └───────────────────────────────────────────────────┘  │   │   │
│  │  │                                                         │   │   │
│  │  │  ┌─────────────────────────────────────────────────┐   │   │   │
│  │  │  │  📝 说明 & 限制                                     │   │   │   │
│  │  │  │                                                  │   │   │   │
│  │  │  │  ✅ 取值范围: 0.0 - 1.0                          │   │   │   │
│  │  │  │  📍 默认值: 0.7                                   │   │   │   │
│  │  │  │                                                  │   │   │   │
│  │  │  │  参考说明：                                         │   │   │   │
│  │  │  │  • 0.0 - 0.3: 输出更确定、集中（Focused）        │   │   │   │
│  │  │  │  • 0.4 - 0.6: 平衡确定性和多样性（Balanced）    │   │   │   │
│  │  │  │  • 0.7 - 1.0: 输出更多样、创意（Creative）       │   │   │   │
│  │  │  │                                                  │   │   │   │
│  │  │  │  💡 推荐设置：                                       │   │   │   │
│  │  │  │  • 代码生成: 0.2 - 0.4                           │   │   │   │
│  │  │  │  • 对话应用: 0.7 - 0.9                           │   │   │   │
│  │  │  │  • 创意写作: 0.8 - 1.0                           │   │   │   │
│  │  │  └─────────────────────────────────────────────────┘   │   │   │
│  │  │                                                         │   │   │
│  │  │  ┌─────────────────────────────────────────────────┐   │   │   │
│  │  │  │  ⚡ 快速预设                                       │   │   │   │
│  │  │  │  ┌──────────┬──────────┬──────────┐            │   │   │   │
│  │  │  │  │ Focused  │ Balanced │ Creative │            │   │   │   │
│  │  │  │  │  0.3     │  0.7     │  0.9     │            │   │   │   │
│  │  │  │  └──────────┴──────────┴──────────┘            │   │   │   │
│  │  │  │  ↑ 点击快速应用常用值                            │   │   │   │
│  │  │  └─────────────────────────────────────────────────┘   │   │   │
│  │  │                                                         │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Max Tokens  📏                                                  │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │  [2000]                                    [+][-]         │   │   │
│  │  │  ↑ 数值输入框                                 微调按钮      │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  │  ✅ 范围: 1 - 128000                                        │   │
│  │  📍 默认值: 2000                                             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

图例说明：
- 📊 参数类型图标
- 💾 保存按钮
- ⚡ 快速预设按钮
- ✅ 已验证配置
- 📍 默认值
```

## 交互说明

### 1. Temperature 输入框
```
初始状态：
  [0.7] 💾    ← 显示当前值（默认0.7）

点击输入框：
  [0.7] 💾    ← 变为可编辑状态
  ↑ 聚焦状态
  
输入新值：
  [0.85] 💾 ✓ ← 输入0.85，显示验证通过标记

超出范围：
  [1.5] 💾 ❌ ← 输入1.5，显示错误提示
  ⚠️ 温度值必须在 0.0 到 1.0 之间
```

### 2. 快速预设按钮
```
点击 "Focused" 按钮：
  → 自动填入 0.3
  → 输入框显示 [0.3] 💾 ✓
  → 提示：适用于代码生成等需要确定性的场景

点击 "Balanced" 按钮：
  → 自动填入 0.7（默认值）
  → 输入框显示 [0.7] 💾 ✓
  → 提示：适用于大多数对话场景

点击 "Creative" 按钮：
  → 自动填入 0.9
  → 输入框显示 [0.9] 💾 ✓
  → 提示：适用于创意写作等需要多样性的场景
```

### 3. 实时验证反馈
```
有效输入：
  [0.5] 💾 ✓
  └─ 绿色勾号，表示配置有效

无效输入：
  [1.2] 💾 ❌
  └─ 红色叉号，显示错误提示
  └─ "温度值必须在 0.0 到 1.0 之间"

空值：
  [] 💾 ⚠️
  └─ 黄色警告，使用默认值 0.7
```

## UI 组件结构

### 选项 1：使用 el-input-number
```vue
<el-input-number
  v-model="temperature"
  :min="0"
  :max="1"
  :step="0.1"
  :precision="2"
  :controls-position="right"
  placeholder="0.7"
/>
```

### 选项 2：使用 el-input + 验证（推荐）
```vue
<el-input
  v-model="temperature"
  type="number"
  :min="0"
  :max="1"
  :step="0.1"
  :precision="2"
  placeholder="0.7"
>
  <template #append>
    <el-button @click="resetTemperature">重置</el-button>
  </template>
</el-input>
```

### 选项 3：使用 el-slider + el-input 组合
```vue
<el-space>
  <el-slider
    v-model="temperature"
    :min="0"
    :max="1"
    :step="0.1"
    :show-tooltip="false"
    style="width: 200px"
  />
  <el-input-number
    v-model="temperature"
    :min="0"
    :max="1"
    :step="0.1"
    :precision="2"
    :controls-position="right"
    style="width: 120px"
  />
</el-space>
```

## 推荐实现方案

**最佳方案**：el-input-number + 快速预设按钮

```vue
<el-form-item label="Temperature" required>
  <div class="temperature-config">
    <!-- 数值输入 -->
    <el-input-number
      v-model="temperature"
      :min="0"
      :max="1"
      :step="0.1"
      :precision="2"
      :controls-position="right"
      placeholder="0.7"
      style="width: 150px"
      @change="updateModelConfig('temperature', $event)"
    />

    <!-- 快速预设 -->
    <el-button-group style="margin-left: 12px">
      <el-button size="small" @click="setTemperature(0.3)">Focused</el-button>
      <el-button size="small" @click="setTemperature(0.7)">Balanced</el-button>
      <el-button size="small" @click="setTemperature(0.9)">Creative</el-button>
    </el-button-group>
  </div>

  <!-- 说明和限制 -->
  <template #hint>
    <div class="parameter-hint">
      <div class="hint-row">
        <el-tag type="info" size="small">✓ 取值范围: 0.0 - 1.0</el-tag>
        <el-tag type="success" size="small">📍 默认值: 0.7</el-tag>
      </div>
      <div class="hint-description">
        <span>• 0.0-0.3: 输出更确定（适合代码生成）</span>
        <span>• 0.4-0.6: 平衡确定性和多样性</span>
        <span>• 0.7-1.0: 输出更多样（适合创意写作）</span>
      </div>
    </div>
  </template>
</el-form-item>
```

## CSS 样式建议

```css
.temperature-config {
  display: flex;
  align-items: center;
  gap: 12px;
}

.parameter-hint {
  margin-top: 8px;
}

.hint-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.hint-description {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.85em;
  color: #606266;
}

.hint-description span {
  display: block;
  line-height: 1.5;
}

/* 输入框状态样式 */
:deep(.el-input-number.is-error .el-input__inner) {
  border-color: #f56c6c;
}

:deep(.el-input-number.is-success .el-input__inner) {
  border-color: #67c23a;
}
```

需要我开始实现这个改进吗？
