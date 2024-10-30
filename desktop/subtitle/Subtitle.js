const outputElement = document.getElementById('subtitle');
const output = {value: ''};  // 创建一个对象来存储输出

Object.defineProperty(output, 'value', {
    set: function (newValue) {
        outputElement.innerText = newValue;  // 更新显示内容
    }
});

async function fetchOutput() {
    window.pywebview.api.get_message().then(function (response) {
        output.value = response;  // 更新输出
    });
}

//setInterval(fetchOutput, 1000);  // 每秒请求一
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

//隐藏窗口
function hideSubtitle() {
    console.log("hideSubtitle")
    window.pywebview.api.hideSubtitle()
    window.pywebview.api.stopClient()
}

//置顶窗口
let isTop = true;

function topSubtitle() {
    if (isTop) {
        isTop = !isTop
        window.pywebview.api.topSubtitle(isTop)
    } else {
        isTop = !isTop
        window.pywebview.api.topSubtitle(isTop)
    }

}