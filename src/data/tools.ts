export type Tool = {
  id: string;
  title: string;
  description: string;
  href: string;
  status: '可用' | '即将推出';
};

export const tools: Tool[] = [
  {
    id: 'todo',
    title: '每日待办',
    description: '按天记录任务，新一天自动承接未完成项。',
    href: '/todo/',
    status: '可用',
  },
  {
    id: 'pomodoro',
    title: '番茄钟',
    description: '专注与休息计时，用绝对时间锚点不怕后台节流。',
    href: '/tools/pomodoro/',
    status: '可用',
  },
];

export function getAvailableTools(limit?: number): Tool[] {
  const list = tools.filter((tool) => tool.status === '可用');
  return typeof limit === 'number' ? list.slice(0, limit) : list;
}
