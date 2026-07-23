export const site = {
  name: 'ONE',
  tagline: '个人学习工作台',
  description: 'ONE · 个人学习工作台：记录笔记、整理项目、持续进步。',
};

export function pageTitle(page: string): string {
  return `${page} · ${site.name}`;
}
