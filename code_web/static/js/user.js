// 移除收藏
function removeFavorite(event, houseId) {
    event.stopPropagation(); // 阻止点击事件冒泡到卡片

    fetch(`/house/${houseId}/favorite`, {
        method: 'POST',
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
        if (data.status === 'removed') {
            // 移除成功后，移除对应的卡片元素
            const card = document.querySelector(`.favorite-item[onclick*="${houseId}"]`);
            card.remove();
            
            // 更新收藏数量
            const countSpan = document.querySelector('.favorite-list .text-muted');
            const currentCount = parseInt(countSpan.textContent.match(/\d+/)[0]) - 1;
            countSpan.textContent = `共${currentCount}套房源`;
            
            // 如果没有收藏了，显示占位内容
            if (currentCount === 0) {
                const favoriteHouses = document.querySelector('.favorite-houses');
                favoriteHouses.innerHTML = '<div class="list-placeholder"><p class="text-muted">暂无收藏的房屋</p></div>';
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败，请稍后重试');
    });
}
