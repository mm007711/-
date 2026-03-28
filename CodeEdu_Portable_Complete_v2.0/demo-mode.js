/**
 * 演示模式管理器
 * 将demo.html的功能集成到111.html中
 */

class DemoModeManager {
    constructor() {
        this.isDemoMode = false;
        this.demoView = null;
        this.normalView = null;
        
        // 演示数据
        this.demoData = {
            stats: {
                problems: 16,
                users: 8,
                contests: 2,
                classes: 2,
                submissions: 0
            },
            roles: [
                { id: 'student', name: '学生', username: 'test_student', password: 'test123' },
                { id: 'teacher', name: '教师', username: 'test_teacher', password: 'test123' },
                { id: 'admin', name: '管理员', username: 'test_admin', password: 'test123' }
            ],
            demoProblems: [
                { id: '1', title: '两数之和', difficulty: '简单', status: 'AC' },
                { id: '20', title: '有效的括号', difficulty: '简单', status: 'WA' },
                { id: '3', title: '无重复字符的最长子串', difficulty: '中等', status: 'TLE' }
            ],
            features: [
                { title: '后端数据落库', description: '使用SQLite数据库，支持ORM操作，数据持久化存储' },
                { title: '题目评测隔离', description: '每个评测在独立环境中运行，避免相互影响' },
                { title: '更细判题结果', description: '详细的测试用例反馈，包括AC、WA、TLE、RE等状态' },
                { title: '竞赛规则管理', description: '支持多种竞赛模式，时间限制，题目顺序等' },
                { title: '班级管理页面', description: '完整的班级管理功能，支持学生导入导出' },
                { title: '前端错误提示', description: '友好的错误提示和loading状态显示' }
            ],
            techStack: {
                frontend: ['Vue 3', 'TypeScript', 'Tailwind CSS', 'Vite'],
                backend: ['Python Flask', 'SQLite', 'SQLAlchemy ORM'],
                judge: ['Python沙箱', 'Docker隔离', '多语言支持'],
                deployment: ['Docker', 'Nginx', '云服务器']
            }
        };
        
        this.currentDemoStep = 0;
        this.demoSteps = [
            { title: '系统概览', duration: 120 },
            { title: '多角色演示', duration: 180 },
            { title: '代码评测演示', duration: 180 },
            { title: '功能亮点', duration: 120 },
            { title: '技术架构', duration: 120 },
            { title: 'Q&A环节', duration: 180 }
        ];
        
        this.currentRole = 'student';
    }
    
    /**
     * 初始化演示模式
     */
    init() {
        // 创建演示视图容器
        this.createDemoView();
        
        // 绑定事件
        this.bindEvents();
        
        // 检查是否有演示模式参数
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('demo') === 'true') {
            this.enterDemoMode();
        }
    }
    
    /**
     * 创建演示视图
     */
    createDemoView() {
        // 如果已经存在，先移除
        const existingDemoView = document.getElementById('demoView');
        if (existingDemoView) {
            existingDemoView.remove();
        }
        
        // 创建演示视图容器
        const demoView = document.createElement('div');
        demoView.id = 'demoView';
        demoView.className = 'fixed inset-0 z-[100] bg-white hidden flex-col overflow-hidden';
        demoView.innerHTML = this.getDemoViewHTML();
        
        document.body.appendChild(demoView);
        this.demoView = demoView;
        
        // 保存正常视图的引用
        this.normalView = document.getElementById('view-dashboard');
    }
    
    /**
     * 获取演示视图HTML
     */
    getDemoViewHTML() {
        return `
            <!-- 演示模式头部 -->
            <header class="h-16 shrink-0 bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-8 flex items-center justify-between shadow-lg">
                <div class="flex items-center gap-4">
                    <div class="text-xl font-bold flex items-center gap-2">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                        </svg>
                        CodeEdu 演示模式
                    </div>
                    <div class="text-sm opacity-90">15分钟完整展示</div>
                </div>
                
                <div class="flex items-center gap-4">
                    <!-- 演示进度 -->
                    <div class="flex items-center gap-2">
                        <div class="text-sm">步骤: <span id="demoStepCurrent">1</span>/<span id="demoStepTotal">${this.demoSteps.length}</span></div>
                        <div class="w-32 h-2 bg-white/30 rounded-full overflow-hidden">
                            <div id="demoProgressBar" class="h-full bg-white transition-all duration-300" style="width: ${100/this.demoSteps.length}%"></div>
                        </div>
                    </div>
                    
                    <!-- 演示控制按钮 -->
                    <div class="flex items-center gap-2">
                        <button id="demoPrevBtn" class="px-3 py-1 bg-white/20 hover:bg-white/30 rounded text-sm transition">
                            上一步
                        </button>
                        <button id="demoNextBtn" class="px-3 py-1 bg-white hover:bg-white/90 text-purple-600 rounded text-sm font-medium transition">
                            下一步
                        </button>
                        <button id="demoExitBtn" class="px-3 py-1 bg-rose-500 hover:bg-rose-600 text-white rounded text-sm font-medium transition ml-2">
                            退出演示
                        </button>
                    </div>
                </div>
            </header>
            
            <!-- 演示内容区域 -->
            <main class="flex-1 overflow-y-auto p-8">
                <div class="max-w-6xl mx-auto">
                    <!-- 步骤1: 系统概览 -->
                    <div id="demoStep1" class="demo-step space-y-8">
                        <div class="text-center mb-8">
                            <h1 class="text-4xl font-bold text-slate-800 mb-4">CodeEdu 在线编程教学平台</h1>
                            <p class="text-lg text-slate-600 max-w-3xl mx-auto">
                                一个功能完整的全栈在线评测系统，支持编程教学、算法竞赛、班级管理和成绩跟踪
                            </p>
                        </div>
                        
                        <!-- 统计数据 -->
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                            <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm text-center">
                                <div class="text-3xl font-bold text-indigo-600 mb-2">${this.demoData.stats.problems}</div>
                                <div class="text-sm text-slate-500">题目总数</div>
                            </div>
                            <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm text-center">
                                <div class="text-3xl font-bold text-emerald-600 mb-2">${this.demoData.stats.users}</div>
                                <div class="text-sm text-slate-500">用户总数</div>
                            </div>
                            <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm text-center">
                                <div class="text-3xl font-bold text-amber-600 mb-2">${this.demoData.stats.contests}</div>
                                <div class="text-sm text-slate-500">比赛总数</div>
                            </div>
                            <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm text-center">
                                <div class="text-3xl font-bold text-rose-600 mb-2">${this.demoData.stats.classes}</div>
                                <div class="text-sm text-slate-500">班级总数</div>
                            </div>
                        </div>
                        
                        <!-- 核心价值 -->
                        <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-8 border border-indigo-100">
                            <h2 class="text-2xl font-bold text-slate-800 mb-4">核心价值</h2>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div class="space-y-3">
                                    <div class="flex items-start gap-3">
                                        <div class="w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center shrink-0">
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                            </svg>
                                        </div>
                                        <div>
                                            <div class="font-medium text-slate-800">提升教学质量</div>
                                            <div class="text-sm text-slate-600">通过实时评测和反馈，帮助学生快速掌握编程技能</div>
                                        </div>
                                    </div>
                                    <div class="flex items-start gap-3">
                                        <div class="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center shrink-0">
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                            </svg>
                                        </div>
                                        <div>
                                            <div class="font-medium text-slate-800">节省教师时间</div>
                                            <div class="text-sm text-slate-600">自动批改和成绩统计，减少重复性工作</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="space-y-3">
                                    <div class="flex items-start gap-3">
                                        <div class="w-8 h-8 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center shrink-0">
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                                            </svg>
                                        </div>
                                        <div>
                                            <div class="font-medium text-slate-800">保障数据安全</div>
                                            <div class="text-sm text-slate-600">本地化部署，数据完全自主可控</div>
                                        </div>
                                    </div>
                                    <div class="flex items-start gap-3">
                                        <div class="w-8 h-8 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center shrink-0">
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path>
                                            </svg>
                                        </div>
                                        <div>
                                            <div class="font-medium text-slate-800">支持扩展定制</div>
                                            <div class="text-sm text-slate-600">模块化设计，可根据需求灵活扩展功能</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 步骤2: 多角色演示 -->
                    <div id="demoStep2" class="demo-step hidden space-y-8">
                        <div class="text-center mb-8">
                            <h2 class="text-3xl font-bold text-slate-800 mb-4">多角色系统演示</h2>
                            <p class="text-lg text-slate-600 max-w-3xl mx-auto">
                                系统支持学生、教师、管理员三种角色，每种角色拥有不同的权限和功能
                            </p>
                        </div>
                        
                        <!-- 角色切换演示 -->
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            ${this.demoData.roles.map(role => `
                                <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow cursor-pointer" onclick="demoMode.switchRole('${role.id}')">
                                    <div class="flex items-center gap-4 mb-4">
                                        <div class="w-12 h-12 rounded-full ${this.getRoleColor(role.id)} flex items-center justify-center text-white text-xl">
                                            ${role.id === 'student' ? '👨‍🎓' : role.id === 'teacher' ? '👩‍🏫' : '👨‍💼'}
                                        </div>
                                        <div>
                                            <div class="text-lg font-bold text-slate-800">${role.name}</div>
                                            <div class="text-sm text-slate-500">账号: ${role.username}</div>
                                        </div>
                                    </div>
                                    <div class="space-y-2">
                                        <div class="text-sm text-slate-700">
                                            <strong>主要功能:</strong>
                                            <ul class="list-disc pl-5 mt-1 space-y-1">
                                                ${this.getRoleFeatures(role.id).map(feature => `<li>${feature}</li>`).join('')}
                                            </ul>
                                        </div>
                                    </div>
                                    <div class="mt-4 pt-4 border-t border-slate-100">
                                        <button class="w-full py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition">
                                            切换为${role.name}
                                        </button>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        
                        <!-- 当前角色功能展示 -->
                        <div class="bg-slate-50 rounded-xl p-6 border border-slate-200">
                            <h3 class="text-xl font-bold text-slate-800 mb-4">当前角色功能演示</h3>
                            <div id="currentRoleDemo" class="space-y-4">
                                <!-- 动态内容由JavaScript填充 -->
                            </div>
                        </div>
                    </div>
                    
                    <!-- 步骤3: 代码评测演示 -->
                    <div id="demoStep3" class="demo-step hidden space-y-8">
                        <div class="text-center mb-8">
                            <h2 class="text-3xl font-bold text-slate-800 mb-4">智能代码评测系统</h2>
                            <p class="text-lg text-slate-600 max-w-3xl mx-auto">
                                支持多种编程语言，提供详细的评测反馈，包括正确、错误、超时等不同状态
                            </p>
                        </div>
                        
                        <!-- 评测状态演示 -->
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            ${this.demoData.demoProblems.map(problem => `
                                <div class="bg-white border ${this.getProblemBorderColor(problem.status)} rounded-xl p-6 shadow-sm">
                                    <div class="flex items-center justify-between mb-4">
                                        <div>
                                            <div class="text-lg font-bold text-slate-800">${problem.title}</div>
                                            <div class="text-sm text-slate-500">No.${problem.id}</div>
                                        </div>
                                        <span class="px-3 py-1 text-xs rounded-full ${this.getProblemStatusColor(problem.status)}">
                                            ${problem.status}
                                        </span>
                                    </div>
                                    <div class="mb-4">
                                        <div class="text-sm text-slate-600 mb-2">难度: <span class="font-medium">${problem.difficulty}</span></div>
                                        <div class="text-sm text-slate-600">${this.getProblemDescription(problem.id)}</div>
                                    </div>
                                    <div class="space-y-3">
                                        <div class="text-xs text-s
