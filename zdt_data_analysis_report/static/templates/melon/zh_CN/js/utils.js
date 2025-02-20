//控制rem
function flexible() {
    var docEl = document.documentElement;
    var dpr = window.devicePixelRatio || 1;
    function setRemUnit() {
        var rem = docEl.clientWidth / 192;
        docEl.style.fontSize = rem + "px";
    }
    setRemUnit();

    // reset rem unit on page resize
    window.addEventListener("resize", setRemUnit);
    window.addEventListener("pageshow", function (e) {
        if (e.persisted) {
            setRemUnit();
        }
    });
}

/**
 *
 * @param startTime
 * @param endTime
 * @param rangType
 */
function genDateRange(startTime, endTime, rangType = 'month'){
    let arr = []
    const startArr = startTime.split('-').map(item => Number(item))
    const endArr = endTime.split('-').map(item => Number(item))
    switch (rangType){
        case 'month':
            arr = getMonthBetween(startTime, endTime)
            break;
        case 'year':
            arr = Array(endArr[0] - startArr[0] + 1).fill().map((item, index) => startArr[0] + index)
            break;
    }


    return arr;
}

// 生成某个时间段内所有的月份 '2021-06' '2022-05'
function getMonthBetween (start, end) {
    const result = []
    // 切割起始年月
    const s = start.split('-')
    // 切割结束年月
    const e = end.split('-')
    // 获取时间对象
    const min = new Date()
    const max = new Date()
    // 设置起始时间 第三个参数需要设置成1，否则跨年出现少第一个月的bug
    min.setFullYear(s[0], s[1], 1)
    // 设置结束时间
    max.setFullYear(e[0], e[1], 1)
    // 复制一份起始时间对象
    const curr = min
    // 定义字符串
    let str = ''
    // 起始时间在结束时间之前
    // eslint-disable-next-line
    while (curr <= max) {
        // 获取此时间的月份
        var month = curr.getMonth()
        // 如果月份为0，也就是代表12月份
        if (month === 0) {
            str = (curr.getFullYear() - 1) + '-' + 12
        } else { // 正常月份
            str = curr.getFullYear() + '-' + String(month).padStart(2, '0')
        }
        // 将此年月加入数组
        result.push(str)
        // 更新此时间月份 第二个参数需要设置成1，否则跨年出现少第一个月的bug
        curr.setMonth(month + 1, 1)
    }
    return result
}
