// 收藏功能
function houseFavorite() {
    const favoriteBtn = document.querySelector('.btn-outline-primary');
    const favoriteText = document.getElementById('favoriteText');
    const houseId = window.location.pathname.split('/').pop(); // 从URL获取房屋ID

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
        if (data.status === 'added') {
            favoriteBtn.classList.add('active');
            favoriteText.textContent = '已收藏';
        } else if (data.status === 'removed') {
            favoriteBtn.classList.remove('active');
            favoriteText.textContent = '收藏';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('操作失败，请稍后重试');
    });
}
