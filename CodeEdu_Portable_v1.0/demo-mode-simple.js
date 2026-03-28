/**
 * 演示模式管理器 - 简化版
 * 将demo.html的功能集成到111.html中
 */

class DemoModeManager {
    constructor() {
        this.isDemoMode = false;
        this.demoView = null;
        this.currentDemoStep = 0;
        
        // 演示数据
        this.demoData = {
            stats: { problems: 16, users: 8, contests: 2, classes: 2 },
            roles: ['student', 'teacher', 'admin'],
            features: [
                '后端数据落库（SQLite/ORM）',
                '题目评测隔离、更细判题结果',
                '竞赛规则、班级管理页面完善',
                '前端错误提示 / loading 细节改进'
            ]
        };
    }
    
    /**
     * 初始化演示模式
     */
    init() {
        // 创建演示视图容器
        this.createDemoView();
        
        // 绑定事件
        this.bindEvents();
        
        console.log('演示模式管理器已初始化');
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
                        🎬 CodeEdu 演示模式
                    </div>
                    <div class="text-sm opacity-90">功能展示</div>
                </div>
                
                <div class="flex items-center gap-4">
                    <button id="demoExitBtn" class="px-4 py-2 bg-rose-500 hover:bg-rose-600 text-white rounded text-sm font-medium transition">
                        退出演示
                    </button>
                </div>
            </header>
            
            <!-- 演示内容区域 -->
            <main class="flex-1 overflow-y-auto p-8">
                <div class="max-w-4xl mx-auto">
                    <div class="text-center mb-8">
                        <h1 class="text-4xl font-bold text-slate-800 mb-4">CodeEdu 功能演示</h1>
                        <p class="text-lg text-slate-600">
                            展示111.html的完整功能与demo.html的演示能力整合
                        </p>
                    </div>
                    
                    <!-- 功能对比 -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                        <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
                            <h2 class="text-2xl font-bold text-slate-800 mb-4">111.html 功能</h2>
                            <ul class="space-y-3">
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>完整的在线评测平台</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>多角色系统（学生/教师/管理员）</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>题库管理、比赛管理、班级管理</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>代码编辑器、测试用例管理</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>本地存储、数据导入导出</span>
                                </li>
                            </ul>
                        </div>
                        
                        <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
                            <h2 class="text-2xl font-bold text-slate-800 mb-4">demo.html 功能</h2>
                            <ul class="space-y-3">
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>系统概览展示</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>多角色登录演示</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>代码评测演示（AC/WA/TLE）</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>功能亮点介绍</span>
                                </li>
                                <li class="flex items-start gap-2">
                                    <span class="text-emerald-500">✓</span>
                                    <span>技术架构展示</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                    
                    <!-- 整合优势 -->
                    <div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-8 border border-indigo-100 mb-8">
                        <h2 class="text-2xl font-bold text-slate-800 mb-4">整合优势</h2>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div class="text-center">
                                <div class="w-12 h-12 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center mx-auto mb-3">
                                    🔧
                                </div>
                                <div class="font-medium text-slate-800 mb-2">统一代码库</div>
                                <div class="text-sm text-slate-600">减少维护成本，便于更新</div>
                            </div>
                            <div class="text-center">
                                <div class="w-12 h-12 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto mb-3">
                                    🚀
                                </div>
                                <div class="font-medium text-slate-800 mb-2">增强功能</div>
                                <div class="text-sm text-slate-600">应用+演示一体化</div>
                            </div>
                            <div class="text-center">
                                <div class="w-12 h-12 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mx-auto mb-3">
                                    💫
                                </div>
                                <div class="font-medium text-slate-800 mb-2">提升体验</div>
                                <div class="text-sm text-slate-600">平滑的模式切换</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 演示操作 -->
                    <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
                        <h2 class="text-2xl font-bold text-slate-800 mb-4">演示操作</h2>
                        <div class="space-y-4">
                            <div>
                                <button onclick="demoMode.showFeature('role')" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition">
                                    演示多角色切换
                                </button>
                                <p class="text-sm text-slate-600 mt-1">展示学生、教师、管理员的不同权限</p>
                            </div>
                            <div>
                                <button onclick="demoMode.showFeature('judge')" class="px-4 py-2 bg-emerald-600 text-white rounded hover:bg-emerald-700 transition">
                                    演示代码评测
                                </button>
                                <p class="text-sm text-slate-600 mt-1">展示AC、WA、TLE等不同评测状态</p>
                            </div>
                            <div>
                                <button onclick="demoMode.showFeature('stats')" class="px-4 py-2 bg-amber-600 text-white rounded hover:bg-amber-700 transition">
                                    查看系统统计
                                </button>
                                <p class="text-sm text-slate-600 mt-1">显示题库、用户、比赛等统计数据</p>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        `;
    }
    
    /**
     * 绑定事件
     */
    bindEvents() {
        // 使用事件委托，因为元素是动态创建的
        document.addEventListener('click', (e) => {
            if (e.target.id === 'demoExitBtn') {
                this.exitDemoMode();
            }
        });
    }
    
    /**
     * 进入演示模式
     */
    enterDemoMode() {
        this.isDemoMode = true;
        this.demoView.classList.remove('hidden');
        
        // 隐藏正常视图
        const normalView = document.getElementById('view-dashboard');
        if (normalView) {
            normalView.classList.add('hidden');
        }
        
        console.log('进入演示模式');
    }
    
    /**
     * 退出演示模式
     */
    exitDemoMode() {
        this.isDemoMode = false;
        this.demoView.classList.add('hidden');
        
        // 显示正常视图
        const normalView = document.getElementById('view-dashboard');
        if (normalView) {
            normalView.classList.remove('hidden');
        }
        
        console.log('退出演示模式');
    }
    
    /**
     * 显示特定功能演示
     */
    showFeature(feature) {
        switch(feature) {
            case 'role':
                alert('演示：切换到教师角色，显示班级管理功能');
                // 这里可以调用111.html的changeRole函数
                if (typeof changeRole === 'function') {
                    changeRole('teacher');
                }
                break;
            case 'judge':
                alert('演示：运行代码评测，展示不同结果状态');
                // 这里可以调用111.html的评测功能
                break;
            case 'stats':
                alert(`系统统计：
                - 题目总数: ${this.demoData.stats.problems}
                - 用户总数: ${this.demoData.stats.users}
                - 比赛总数: ${this.demoData.stats.contests}
                - 班级总数: ${this.demoData.stats.classes}`);
                break;
        }
    }
}

// 创建全局实例
const demoMode = new DemoModeManager();

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        demoMode.init();
    });
} else {
    demoMode.init();
}
