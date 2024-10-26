        const outputElement = document.getElementById('subtitle');
        const output = { value: '' };  // 创建一个对象来存储输出

        Object.defineProperty(output, 'value', {
            set: function(newValue) {
                outputElement.innerText = newValue;  // 更新显示内容
            }
        });

        function fetchOutput() {
            window.pywebview.api.get_message().then(function(response) {
                output.value = response;  // 更新输出
            });
        }

        setInterval(fetchOutput, 1000);  // 每秒请求一
        const floatingWindow = document.getElementById('floatingWindow');
const buttons = document.getElementById('buttons');

// 鼠标移入悬浮窗时显示按钮
floatingWindow.addEventListener('mouseenter', () => {
    buttons.style.opacity = '1';
});

// 鼠标移出悬浮窗时隐藏按钮
floatingWindow.addEventListener('mouseleave', () => {
    buttons.style.opacity = '0';
});

// 置顶功能
function topWindow() {
    alert('置顶功能尚未实现！');
}

// 关闭功能
function closeWindow() {
    floatingWindow.style.display = 'none';
}

    // 实现拖动窗口
    let isMouseDown = false;
    let offset = { x: 0, y: 0 };

    document.body.addEventListener('mousedown', (e) => {
        isMouseDown = true;
        offset.x = e.clientX;
        offset.y = e.clientY;
    });

    document.body.addEventListener('mousemove', (e) => {
        if (isMouseDown) {
            const x = e.screenX - offset.x;
            const y = e.screenY - offset.y;
            window.pywebview.api.move_window(x, y);
        }
    });

    document.body.addEventListener('mouseup', () => {
        isMouseDown = false;
    });