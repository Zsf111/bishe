// 移除浏览记录
function removeHistory(event, houseId) {
    event.stopPropagation(); // 阻止点击事件冒泡到卡片

    fetch(`/user/history/${houseId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            // 移除成功后，移除对应的卡片元素
            const card = document.querySelector(`.history-item[onclick*="${houseId}"]`);
            card.remove();
            
            // 更新记录数量
            const countSpan = document.querySelector('.history-list .text-muted');
            const currentCount = parseInt(countSpan.textContent.match(/\d+/)[0]) - 1;
            countSpan.textContent = `共${currentCount}套房源`;
            
            // 如果没有记录了，显示占位内容
            if (currentCount === 0) {
                const historyHouses = document.querySelector('.history-houses');
                historyHouses.innerHTML = '<div class="list-placeholder"><p class="text-muted">暂无浏览记录</p></div>';
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败，请稍后重试');
    });
}
