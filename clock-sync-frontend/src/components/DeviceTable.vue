<template>
  <el-card class="page-card" shadow="never">
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span>设备列表</span>
        <el-button type="primary" size="small" @click="$emit('refresh')">刷新</el-button>
      </div>
    </template>
    <el-table :data="devices" border stripe v-loading="loading" empty-text="暂无设备数据">
      <el-table-column prop="device_sn" label="设备序列号" min-width="180" />
      <el-table-column prop="device_model" label="设备型号" min-width="140" />
      <el-table-column prop="ip" label="IP 地址" min-width="140" />
      <el-table-column prop="firmware_version" label="固件版本" min-width="140" />
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import type { Device } from '@/types/device';
defineProps<{ devices: Device[]; loading: boolean }>();
defineEmits<{ (e: 'refresh'): void }>();
</script>
