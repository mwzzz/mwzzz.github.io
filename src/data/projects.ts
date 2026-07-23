export interface Project {
  title: string;
  description: string;
  status: '进行中' | '已完成' | '搁置';
  href?: string;
  stack: string[];
}

export const projects: Project[] = [
  {
    title: 'ONE',
    description: '个人学习工作台与技术笔记站点，用 Astro 静态构建并部署到 GitHub Pages。',
    status: '进行中',
    href: 'https://github.com/mwzzz/mwzzz.github.io',
    stack: ['Astro', 'TypeScript', 'GitHub Pages'],
  },
  {
    title: '学习笔记整理',
    description: '把零散踩坑与知识点沉淀成可检索的 Markdown 笔记，形成长期知识库。',
    status: '进行中',
    stack: ['Markdown', 'Content Collections'],
  },
  {
    title: '小工具试验田',
    description: '记录日常脚本与效率工具想法，挑几个做成可复用的小项目。',
    status: '搁置',
    stack: ['Python', 'Node.js'],
  },
];
