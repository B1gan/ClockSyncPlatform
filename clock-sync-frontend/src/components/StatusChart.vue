<template>
  <el-card class="page-card" shadow="never">
    <template #header><span>设备时间偏差曲线（offset/ms）</span></template>
    <div ref="chartRef" style="width:100%;height:360px;"></div>
  </el-card>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue';
import * as echarts from 'echarts';
import type { OffsetPoint } from '@/types/device';

const props = defineProps<{ data: OffsetPoint[] }>();
const chartRef = ref<HTMLDivElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

function initChart() {
  if (!chartRef.value) return;
  if (!chartInstance) chartInstance = echarts.init(chartRef.value);
  const timestamps = props.data.map((i) => i.timestamp);
  const offsets = props.data.map((i) => i.offset);
  chartInstance.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '8%', containLabel: true },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: timestamps,
      name: '时间',
      axisLabel: { formatter: (v: string) => v.replace('T', ' ') }
    },
    yAxis: { type: 'value', name: 'offset(ms)' },
    series: [{
      name: '时间偏差',
      type: 'line',
      smooth: true,
      data: offsets,
      showSymbol: false,
      lineStyle: { width: 2, color: '#409eff' },
      areaStyle: { color: 'rgba(64,158,255,0.2)' }
    }]
  });
  chartInstance.resize();
}

onMounted(() => {
  window.addEventListener('resize', () => chartInstance?.resize());
  initChart();
});
onBeforeUnmount(() => {
  window.removeEventListener('resize', () => chartInstance?.resize());
  chartInstance?.dispose();
  chartInstance = null;
});
watch(() => props.data, initChart, { deep: true });
</script>
