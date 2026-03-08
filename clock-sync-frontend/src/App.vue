<template>
  <el-container class="app-layout">
    <el-header height="56px" style="background:#1f2d3d;display:flex;align-items:center;padding:0 20px;">
      <div>
        <div class="app-header-title">工业物联网时钟同步设备管理平台</div>
        <div class="app-header-subtitle">Clock Sync Management Console</div>
      </div>
    </el-header>
    <el-container>
      <el-aside width="220px" class="app-aside">
        <el-menu :default-active="activePath" router background-color="#fff" text-color="#303133" active-text-color="#409eff">
          <el-menu-item index="/dashboard">Dashboard 仪表盘</el-menu-item>
          <el-menu-item index="/devices">设备列表</el-menu-item>
          <el-menu-item index="/register">设备注册</el-menu-item>
        </el-menu>
        <!-- 左下角：用户注册/登录扩展壳，暂不实现逻辑 -->
        <div class="user-area">
          <div class="user-area-title">用户</div>
          <div class="user-area-actions">
            <el-button type="primary" size="small" text @click="onLogin">登录</el-button>
            <span class="user-area-divider">/</span>
            <el-button type="primary" size="small" text @click="onRegister">注册</el-button>
          </div>
          <div class="user-area-tip">（功能扩展预留）</div>
        </div>
      </el-aside>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';

const route = useRoute();
const activePath = computed(() => {
  if (route.path.startsWith('/dashboard')) return '/dashboard';
  if (route.path.startsWith('/devices')) return '/devices';
  if (route.path.startsWith('/register')) return '/register';
  return '/dashboard';
});

/** 登录入口，预留扩展 */
function onLogin() {
  ElMessage.info('登录功能扩展中');
}

/** 注册入口，预留扩展 */
function onRegister() {
  ElMessage.info('注册功能扩展中');
}
</script>

<style scoped>
.user-area {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  border-top: 1px solid #e4e7ed;
  background: #fafafa;
}
.user-area-title {
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
}
.user-area-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}
.user-area-divider {
  color: #c0c4cc;
  font-size: 12px;
}
.user-area-tip {
  font-size: 11px;
  color: #c0c4cc;
  margin-top: 4px;
}
.app-aside {
  position: relative;
  padding-bottom: 80px;
}
</style>
