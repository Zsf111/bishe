function submitData() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const responseDiv = document.getElementById('response');

    // 先隐藏提示框
    responseDiv.classList.add('d-none');

    const data = {
        username: username,
        password: password
    };

    fetch('/auth/login', {
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
            // 登录成功显示浅色提示
            responseDiv.className = 'alert alert-success';
            responseDiv.innerHTML = '登录成功，正在跳转...';
            setTimeout(() => {
                window.location.href = '/';
            }, 500);
        } else {
            // 登录失败显示红色提示
            responseDiv.className = 'alert alert-danger';
            switch(result.status) {
                case 400:
                    responseDiv.innerHTML = result.data.error; // 用户名或密码为空
                    break;
                case 401:
                    responseDiv.innerHTML = result.data.error; // 用户名或密码错误
                    break;
                default:
                    responseDiv.innerHTML = '登录失败，请稍后重试';
            }
        }
    })
    .catch(error => {
        responseDiv.classList.remove('d-none');
        responseDiv.className = 'alert alert-danger';
        responseDiv.innerHTML = `系统错误: ${error.message}`;
    });
}