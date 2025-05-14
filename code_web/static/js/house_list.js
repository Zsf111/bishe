// 处理筛选表单提交
document.getElementById('filterForm').onsubmit = function(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const params = new URLSearchParams();
    
    for (let [key, value] of formData.entries()) {
        if (value) {  // 只添加有值的参数
            params.append(key, value);
        }
    }
    
    // 保持当前页码为1（重新筛选时）
    params.append('page', '1');
    
    // 跳转到筛选后的URL
    window.location.href = `/house/list?${params.toString()}`;
};

// 分页功能
function changePage(page) {
    const currentUrl = new URL(window.location.href);
    const params = currentUrl.searchParams;
    params.set('page', page);
    window.location.href = `/house/list?${params.toString()}`;
}

// 重置表单并刷新页面
function resetForm() {
    document.getElementById('filterForm').reset();
    window.location.href = '/house/list';
}

// 保持筛选条件的选中状态
window.onload = function() {
    const params = new URLSearchParams(window.location.search);
    for (let [key, value] of params) {
        const element = document.getElementById(key);
        if (element) {
            element.value = value;
        }
    }
    
    // 保持搜索关键词
    const keyword = params.get('keyword');
    if (keyword) {
        document.getElementById('searchInput').value = keyword;
    }
};

// 处理搜索
function handleSearch(event) {
    event.preventDefault();
    const searchInput = document.getElementById('searchInput');
    const keyword = searchInput.value.trim();
    
    // 获取当前的URL参数
    const currentUrl = new URL(window.location.href);
    const params = currentUrl.searchParams;
    
    // 更新或添加关键词参数
    if (keyword) {
        params.set('keyword', keyword);
    } else {
        params.delete('keyword');
    }
    
    // 重置页码到第一页
    params.set('page', '1');
    
    // 跳转到新的URL
    window.location.href = `/house/list?${params.toString()}`;
    return false;
}