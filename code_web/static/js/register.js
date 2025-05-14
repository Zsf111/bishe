function submitData() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;
    const responseDiv = document.getElementById('response');

    // 先隐藏提示框
    responseDiv.classList.add('d-none');

    const data = {
        username: username,
        password: password,
        email: email
    };

    fetch('/auth/register', {
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
        
        if (result.status === 201) {
            // 注册成功显示绿色提示
            responseDiv.className = 'alert alert-success';
            responseDiv.innerHTML = '注册成功，正在跳转...';
            setTimeout(() => {
                window.location.href = '/auth/login';
            }, 500);
        } else {
            // 注册失败显示红色提示
            responseDiv.className = 'alert alert-danger';
            switch(result.status) {
                case 400:
                    responseDiv.innerHTML = result.data.error; // 用户名或邮箱已存在
                    break;
                default:
                    responseDiv.innerHTML = '注册失败，请稍后重试';
            }
        }
    })
    .catch(error => {
        responseDiv.classList.remove('d-none');
        responseDiv.className = 'alert alert-danger';
        responseDiv.innerHTML = `系统错误: ${error.message}`;
    });
}