<template>
  <div class="home">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>AgentScope Initializr</h1>
          <nav class="nav-menu">
            <router-link to="/configure">创建项目</router-link>
            <router-link to="/skills">
              <el-icon><Collection /></el-icon>
              Skill 管理
            </router-link>
          </nav>
        </div>
      </el-header>
      <el-main>
        <el-card class="welcome-card">
          <h2>Welcome to AgentScope Initializr</h2>
          <p>Scaffold AgentScope agent projects with a web interface</p>
          <el-button type="primary" size="large" @click="startConfiguration">
            Start Creating Project
          </el-button>
        </el-card>

        <el-divider />

        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <h3>⚡ Fast Setup</h3>
              <p>Configure and generate projects in minutes</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <h3>🎯 Multiple Templates</h3>
              <p>Basic, multi-agent, research, and browser automation</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <h3>🔧 Flexible Configuration</h3>
              <p>Configure all AgentScope extension points</p>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Collection } from '@element-plus/icons-vue'

const router = useRouter()

const startConfiguration = () => {
  router.push('/configure')
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.el-header {
  margin-bottom: 40px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  margin: 0;
  font-size: 2.5em;
}

.nav-menu {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-menu a {
  color: #409eff;
  text-decoration: none;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-menu a:hover {
  background-color: #ecf5ff;
}

.welcome-card {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-card h2 {
  margin-top: 0;
}
</style>
