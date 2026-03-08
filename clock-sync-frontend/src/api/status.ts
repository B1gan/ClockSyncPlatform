import request from '@/utils/request';
import type { StatusOverview } from '@/types/device';

export function getStatus(): Promise<StatusOverview> {
  return request.get<StatusOverview>('/status');
}
