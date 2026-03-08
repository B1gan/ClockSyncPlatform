<template>
  <div>
    <el-card class="page-card" shadow="never">
      <template #header><span>Dashboard 仪表盘</span></template>
      <el-row :gutter="16">
        <el-col :span="6">
          <el-card shadow="hover">
            <div style="font-size:13px;color:#909399;">设备总数</div>
            <div style="font-size:24px;font-weight:600;margin-top:8px;">{{ totalDevices }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div style="font-size:13px;color:#909399;">在线设备数</div>
            <div style="font-size:24px;font-weight:600;margin-top:8px;color:#67c23a;">{{ onlineDevices }}</div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover">
            <div style="font-size:13px;color:#909399;margin-bottom:8px;">同步状态统计</div>
            <el-row>
              <el-col :span="8">
                <div style="font-size:13px;color:#67c23a;">同步正常</div>
                <div style="font-size:20px;font-weight:600;">{{ syncOk }}</div>
              </el-col>
              <el-col :span="8">
                <div style="font-size:13px;color:#e6a23c;">偏差预警</div>
                <div style="font-size:20px;font-weight:600;">{{ syncWarning }}</div>
              </el-col>
              <el-col :span="8">
                <div style="font-size:13px;color:#f56c6c;">同步异常</div>
                <div style="font-size:20px;font-weight:600;">{{ syncError }}</div>
              </el-col>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
    <StatusChart :data="offsetData" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { getStatus } from '@/api/status';
import StatusChart from '@/components/StatusChart.vue';
import type { OffsetPoint, StatusOverview } from '@/types/device';

const totalDevices = ref(0);
const onlineDevices = ref(0);
const syncOk = ref(0);
const syncWarning = ref(0);
const syncError = ref(0);
const offsetData = ref<OffsetPoint[]>([]);

function buildMockData(): StatusOverview {
  const now = new Date();
  const offsets: OffsetPoint[] = [];
  for (let i = 0; i < 20; i++) {
    const t = new Date(now.getTime() - (19 - i) * 60 * 1000);
    offsets.push({ timestamp: t.toISOString().slice(0, 19), offset: Math.round((Math.random() * 2 - 1) * 5 * 10) / 10 });
  }
  return { total_devices: 12, online_devices: 10, sync_ok: 8, sync_warning: 2, sync_error: 2, offsets };
}

async function loadStatus() {
  try {
    const res = await getStatus();
    totalDevices.value = res.total_devices;
    onlineDevices.value = res.online_devices;
    syncOk.value = res.sync_ok;
    syncWarning.value = res.sync_warning;
    syncError.value = res.sync_error;
    offsetData.value = res.offsets;
  } catch {
    const mock = buildMockData();
    totalDevices.value = mock.total_devices;
    onlineDevices.value = mock.online_devices;
    syncOk.value = mock.sync_ok;
    syncWarning.value = mock.sync_warning;
    syncError.value = mock.sync_error;
    offsetData.value = mock.offsets;
    ElMessage.warning('获取状态失败，已使用模拟数据展示');
  }
}

onMounted(loadStatus);
</script>
