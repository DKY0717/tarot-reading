class ReadingHistory {
    constructor() {
        this.readings = [];
        this.init();
    }
    
    init() {
        this.loadReadings();
        this.bindEvents();
    }
    
    loadReadings() {
        const readingItems = document.querySelectorAll('.history-item');
        this.readings = Array.from(readingItems).map(item => ({
            id: item.dataset.id,
            element: item
        }));
    }
    
    bindEvents() {
        const deleteButtons = document.querySelectorAll('.delete-btn');
        deleteButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const readingId = btn.dataset.id;
                this.deleteReading(readingId);
            });
        });
        
        const searchInput = document.getElementById('historySearch');
        if (searchInput) {
            searchInput.addEventListener('input', debounce((e) => {
                this.filterReadings(e.target.value);
            }, 300));
        }
    }
    
    async deleteReading(readingId) {
        if (!confirm('确定要删除这条占卜记录吗？')) {
            return;
        }
        
        try {
            const response = await fetch(`/api/reading/${readingId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                const readingItem = document.querySelector(`.history-item[data-id="${readingId}"]`);
                if (readingItem) {
                    readingItem.style.animation = 'fadeOut 0.3s ease forwards';
                    setTimeout(() => {
                        readingItem.remove();
                        this.readings = this.readings.filter(r => r.id !== readingId);
                        
                        if (this.readings.length === 0) {
                            this.showEmptyState();
                        }
                    }, 300);
                }
                
                showToast('记录已删除', 'success');
            } else {
                showToast('删除失败，请重试', 'error');
            }
        } catch (error) {
            console.error('删除失败:', error);
            showToast('删除失败，请重试', 'error');
        }
    }
    
    filterReadings(keyword) {
        const lowerKeyword = keyword.toLowerCase();
        
        this.readings.forEach(reading => {
            const text = reading.element.textContent.toLowerCase();
            if (text.includes(lowerKeyword) || keyword === '') {
                reading.element.style.display = '';
                reading.element.style.animation = 'fadeIn 0.3s ease';
            } else {
                reading.element.style.display = 'none';
            }
        });
    }
    
    showEmptyState() {
        const container = document.querySelector('.history-list');
        if (container) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📜</div>
                    <h3 class="empty-title">暂无占卜记录</h3>
                    <p class="empty-text">开始你的第一次占卜吧</p>
                    <a href="/" class="btn btn-primary">
                        <span class="btn-icon">✦</span>
                        开始占卜
                    </a>
                </div>
            `;
        }
    }
}

class ReadingDetail {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindShareButton();
        this.bindPrintButton();
    }
    
    bindShareButton() {
        const shareBtn = document.getElementById('shareBtn');
        if (shareBtn) {
            shareBtn.addEventListener('click', () => {
                this.shareReading();
            });
        }
    }
    
    bindPrintButton() {
        const printBtn = document.getElementById('printBtn');
        if (printBtn) {
            printBtn.addEventListener('click', () => {
                this.printReading();
            });
        }
    }
    
    shareReading() {
        const url = window.location.href;
        
        if (navigator.share) {
            navigator.share({
                title: '塔罗牌占卜结果',
                text: '看看我的塔罗牌占卜结果！',
                url: url
            }).catch(err => {
                console.log('分享失败:', err);
                this.copyToClipboard(url);
            });
        } else {
            this.copyToClipboard(url);
        }
    }
    
    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('链接已复制到剪贴板', 'success');
        }).catch(err => {
            console.error('复制失败:', err);
            showToast('复制失败，请手动复制链接', 'error');
        });
    }
    
    printReading() {
        window.print();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.history-section')) {
        new ReadingHistory();
    }
    
    if (document.querySelector('.reading-detail-section')) {
        new ReadingDetail();
    }
});
