<template>
  <div class="configure">
    <el-container>
      <el-header>
        <h1>Configure Your Project</h1>
      </el-header>
      <el-main>
        <ConfigurationForm />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import ConfigurationForm from '@/components/ConfigurationForm.vue'
</script>

<style scoped>
.configure {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.el-header h1 {
  text-align: center;
}
</style>

