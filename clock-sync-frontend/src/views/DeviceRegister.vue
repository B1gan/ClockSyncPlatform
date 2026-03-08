<template>
  <el-card class="page-card" shadow="never">
    <template #header><span>设备注册</span></template>
    <el-form ref="formRef" :model="form" :rules="rules" label-width="120px" style="max-width:560px;">
      <el-form-item label="设备序列号" prop="device_sn">
        <el-input v-model="form.device_sn" placeholder="请输入设备序列号" />
      </el-form-item>
      <el-form-item label="设备型号" prop="device_model">
        <el-input v-model="form.device_model" placeholder="例如：PTP-1000 / NTP-800" />
      </el-form-item>
      <el-form-item label="IP 地址" prop="ip">
        <el-input v-model="form.ip" placeholder="例如：192.168.1.10" />
      </el-form-item>
      <el-form-item label="固件版本" prop="firmware_version">
        <el-input v-model="form.firmware_version" placeholder="例如：v1.0.0" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="submitting" @click="onSubmit">提交注册</el-button>
        <el-button @click="formRef?.resetFields()">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import { registerDevice } from '@/api/device';
import type { RegisterDevicePayload } from '@/types/device';

const router = useRouter();
const formRef = ref<FormInstance | null>(null);
const form = reactive<RegisterDevicePayload>({
  device_sn: '',
  device_model: '',
  ip: '',
  firmware_version: ''
});
const submitting = ref(false);

const rules: FormRules = {
  device_sn: [{ required: true, message: '请输入设备序列号', trigger: 'blur' }],
  device_model: [{ required: true, message: '请输入设备型号', trigger: 'blur' }],
  ip: [
    { required: true, message: '请输入 IP 地址', trigger: 'blur' },
    { pattern: /^(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}$/, message: 'IP 地址格式不正确', trigger: 'blur' }
  ],
  firmware_version: [{ required: true, message: '请输入固件版本', trigger: 'blur' }]
};

async function onSubmit() {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (!valid) return;
    submitting.value = true;
    try {
      await registerDevice(form);
      ElMessage.success('设备注册成功');
      router.push('/devices');
    } catch {
      ElMessage.error('设备注册失败，请检查后端接口');
    } finally {
      submitting.value = false;
    }
  });
}
</script>
