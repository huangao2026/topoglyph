// ===== 全局变量 =====
const API_BASE_URL = window.location.origin;
let currentLanguage = 'zh';
let uploadedImage = null;

// ===== 初始化 =====
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initTextAnalysis();
    initImageUpload();
    initLanguageSelector();
    loadTools();
});

// ===== 导航切换 =====
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.content-section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // 更新导航状态
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // 切换内容区域
            const targetSection = link.dataset.section;
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === `${targetSection}-section`) {
                    section.classList.add('active');
                }
            });
        });
    });
}

// ===== 文本分析功能 =====
function initTextAnalysis() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const clearBtn = document.getElementById('clear-btn');
    const textInput = document.getElementById('text-input');
    const resultContainer = document.getElementById('text-result');
    const resultContent = document.getElementById('text-result-content');

    // 分析按钮
    analyzeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        
        if (!text) {
            showNotification('请输入要分析的内容', 'warning');
            return;
        }

        try {
            showLoading('正在分析中...');
            
            const response = await fetch(`${API_BASE_URL}/api/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    language: currentLanguage
                })
            });

            const data = await response.json();
            
            hideLoading();
            
            if (data.status === 'success') {
                resultContent.innerHTML = formatMarkdown(data.result.content);
                resultContainer.classList.remove('hidden');
                showNotification('分析完成', 'success');
            } else {
                showNotification(`分析失败: ${data.error || '未知错误'}`, 'error');
            }
        } catch (error) {
            hideLoading();
            showNotification(`网络错误: ${error.message}`, 'error');
            console.error('Analysis error:', error);
        }
    });

    // 清空按钮
    clearBtn.addEventListener('click', () => {
        textInput.value = '';
        resultContainer.classList.add('hidden');
        resultContent.innerHTML = '';
    });
}

// ===== 图像上传功能 =====
function initImageUpload() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const imagePreview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const removeImageBtn = document.getElementById('remove-image');
    const analyzeImageBtn = document.getElementById('analyze-image-btn');
    const imageResult = document.getElementById('image-result');
    const imageResultContent = document.getElementById('image-result-content');

    // 点击上传
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // 文件选择
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleImageUpload(file);
        }
    });

    // 拖拽上传
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImageUpload(file);
        } else {
            showNotification('请上传图片文件', 'warning');
        }
    });

    // 移除图片
    removeImageBtn.addEventListener('click', () => {
        uploadedImage = null;
        imagePreview.classList.add('hidden');
        dropZone.classList.remove('hidden');
        fileInput.value = '';
        analyzeImageBtn.disabled = true;
        imageResult.classList.add('hidden');
    });

    // 分析图片
    analyzeImageBtn.addEventListener('click', async () => {
        if (!uploadedImage) {
            showNotification('请先上传图片', 'warning');
            return;
        }

        try {
            showLoading('正在识别图片...');

            const formData = new FormData();
            formData.append('image', uploadedImage);
            formData.append('params', JSON.stringify({
                language: currentLanguage
            }));

            const response = await fetch(`${API_BASE_URL}/api/analyze/image`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            hideLoading();

            if (data.status === 'success') {
                imageResultContent.innerHTML = formatMarkdown(data.result.content);
                imageResult.classList.remove('hidden');
                showNotification('识别完成', 'success');
            } else {
                showNotification(`识别失败: ${data.error || '未知错误'}`, 'error');
            }
        } catch (error) {
            hideLoading();
            showNotification(`网络错误: ${error.message}`, 'error');
            console.error('Image analysis error:', error);
        }
    });
}

// 处理图片上传
function handleImageUpload(file) {
    // 验证文件大小
    if (file.size > 10 * 1024 * 1024) {
        showNotification('图片大小不能超过10MB', 'warning');
        return;
    }

    uploadedImage = file;

    // 显示预览
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        document.getElementById('drop-zone').classList.add('hidden');
        document.getElementById('image-preview').classList.remove('hidden');
        document.getElementById('analyze-image-btn').disabled = false;
    };
    reader.readAsDataURL(file);
}

// ===== 语言选择器 =====
function initLanguageSelector() {
    const selector = document.getElementById('language-selector');
    
    selector.addEventListener('change', (e) => {
        currentLanguage = e.target.value;
        showNotification(`已切换至 ${selector.options[selector.selectedIndex].text}`, 'info');
    });
}

// ===== 加载工具列表 =====
async function loadTools() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/tools`);
        const data = await response.json();
        
        if (data.tools) {
            renderTools(data.tools);
        }
    } catch (error) {
        console.error('Failed to load tools:', error);
    }
}

// 渲染工具列表
function renderTools(tools) {
    const toolsGrid = document.getElementById('tools-grid');
    toolsGrid.innerHTML = '';

    Object.entries(tools).forEach(([category, categoryData]) => {
        const card = document.createElement('div');
        card.className = 'tool-card';
        
        card.innerHTML = `
            <span class="tool-type">${categoryData.name}</span>
            <h3>${categoryData.name}</h3>
            <ul>
                ${categoryData.tools.map(tool => `
                    <li>
                        <strong>${tool.name}</strong>
                        <br>
                        <small><a href="${tool.url}" target="_blank">${tool.url}</a></small>
                    </li>
                `).join('')}
            </ul>
        `;
        
        toolsGrid.appendChild(card);
    });
}

// ===== 格式化Markdown =====
function formatMarkdown(text) {
    if (!text) return '';
    
    // 简单的Markdown格式化
    return text
        // 标题
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        // 粗体
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // 斜体
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // 链接
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
        // 代码
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // 列表
        .replace(/^\- (.*$)/gim, '<li>$1</li>')
        .replace(/^\d+\. (.*$)/gim, '<li>$1</li>')
        // 分隔线
        .replace(/^---$/gim, '<hr>')
        // 段落
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
}

// ===== 显示加载遮罩 =====
function showLoading(text = '加载中...') {
    const overlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    
    loadingText.textContent = text;
    overlay.classList.remove('hidden');
}

// ===== 隐藏加载遮罩 =====
function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

// ===== 显示通知 =====
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // 添加样式
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem 1.5rem',
        borderRadius: '0.5rem',
        backgroundColor: getNotificationColor(type),
        color: 'white',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        zIndex: '10000',
        animation: 'slideIn 0.3s ease-out'
    });

    // 添加到页面
    document.body.appendChild(notification);

    // 自动移除
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);

    // 添加动画样式
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}

// 获取通知颜色
function getNotificationColor(type) {
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    return colors[type] || colors.info;
}

// ===== 复制功能 =====
document.addEventListener('click', (e) => {
    if (e.target.closest('.btn-icon')) {
        const btn = e.target.closest('.btn-icon');
        const resultContent = btn.closest('.result-container')?.querySelector('.result-content');
        
        if (resultContent) {
            navigator.clipboard.writeText(resultContent.textContent)
                .then(() => showNotification('已复制到剪贴板', 'success'))
                .catch(() => showNotification('复制失败', 'error'));
        }
    }
});
