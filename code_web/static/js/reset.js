function submitData() {
    const old_password = document.getElementById('old_password').value;
    const new_password = document.getElementById('new_password').value;
    const responseDiv = document.getElementById('response');

    // 先隐藏提示框
    responseDiv.classList.add('d-none');

    const data = {
        old_password: old_password,
        new_password: new_password
    };

    fetch('/auth/reset', {
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
            responseDiv.innerHTML = '密码修改成功，正在跳转...';
            setTimeout(() => {
                window.location.href = '/auth/login';
            }, 500);
        } else {
            // 修改失败显示红色提示
            responseDiv.className = 'alert alert-danger';
            switch(result.status) {
                case 401:
                    responseDiv.innerHTML = result.data.error; // 原密码错误
                    break;
                case 400:
                    responseDiv.innerHTML = '请填写完整的信息';
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