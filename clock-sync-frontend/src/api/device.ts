import request from '@/utils/request';
import type { Device, RegisterDevicePayload } from '@/types/device';

export function getDevices(): Promise<Device[]> {
  return request.get<Device[]>('/devices');
}

export function registerDevice(payload: RegisterDevicePayload) {
  return request.post('/devices/register', payload);
}
