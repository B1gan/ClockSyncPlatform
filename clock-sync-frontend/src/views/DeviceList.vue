<template>
  <div>
    <el-card class="page-card" shadow="never">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span>设备列表</span>
          <div>
            <el-button type="primary" @click="router.push('/register')" style="margin-right:8px;">注册新设备</el-button>
            <el-button @click="fetchDevices">刷新</el-button>
          </div>
        </div>
      </template>
      <p style="margin:0 0 8px 0;color:#909399;font-size:13px;">当前共 {{ devices.length }} 台设备。</p>
    </el-card>
    <DeviceTable :devices="devices" :loading="loading" @refresh="fetchDevices" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { getDevices } from '@/api/device';
import type { Device } from '@/types/device';
import DeviceTable from '@/components/DeviceTable.vue';

const router = useRouter();
const devices = ref<Device[]>([]);
const loading = ref(false);

async function fetchDevices() {
  loading.value = true;
  try {
    devices.value = await getDevices();
  } catch {
    ElMessage.error('获取设备列表失败，请检查后端服务是否启动');
  } finally {
    loading.value = false;
  }
}

onMounted(fetchDevices);
</script>
