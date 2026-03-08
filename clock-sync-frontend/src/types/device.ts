export interface Device {
  device_sn: string;
  device_model: string;
  ip: string;
  firmware_version: string;
}

export interface RegisterDevicePayload {
  device_sn: string;
  device_model: string;
  ip: string;
  firmware_version: string;
}

export interface OffsetPoint {
  timestamp: string;
  offset: number;
}

export interface StatusOverview {
  total_devices: number;
  online_devices: number;
  sync_ok: number;
  sync_warning: number;
  sync_error: number;
  offsets: OffsetPoint[];
}
