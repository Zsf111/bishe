function submitData() {
    const username = document.getElementById('username').value;
    const profile = document.getElementById('profile').value;
    const responseDiv = document.getElementById('response');

    // 先隐藏提示框
    responseDiv.classList.add('d-none');

    const data = {
        username: username,
        profile: profile
    };

    fetch('/user/edit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        const status = response.status;
        return response.json().then(data => {
            return {
                status: status,
                data: data
            };
        });
    })
    .then(result => {
        // 显示提示框
        responseDiv.classList.remove('d-none');
        
        if (result.status === 200) {
            // 修改成功显示绿色提示
            responseDiv.className = 'alert alert-success';
            responseDiv.innerHTML = '资料修改成功，正在跳转...';
            setTimeout(() => {
                window.location.href = '/';
            }, 500);
        } else {
            // 修改失败显示红色提示
            responseDiv.className = 'alert alert-danger';
            switch(result.status) {
                case 400:
                    responseDiv.innerHTML = result.data.error; // 用户名已存在
                    break;
                case 401:
                    responseDiv.innerHTML = '请先登录';
                    break;
                case 404:
                    responseDiv.innerHTML = '用户不存在';
                    break;
                default:
                    responseDiv.innerHTML = '修改失败，请稍后重试';
            }
        }
    })
    .catch(error => {
        responseDiv.classList.remove('d-none');
        responseDiv.className = 'alert alert-danger';
        responseDiv.innerHTML = `系统错误: ${error.message}`;
    });
}