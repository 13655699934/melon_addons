import {baseURL} from './http.js'

layui.use('table', function () {
    var table = layui.table;

    //方法级渲染
    table.render({
        elem: '#LAY_table_user',
        // url: `../../demo/table/user/-page=1&limit=30.js`,
        url: `${baseURL}/crm/customer/order/api`,
        cols: [[
            {field: 'username', title: '客户姓名', align: 'center'},
            {field: 'phone_number', title: '联系方式'},
            {field: 'age', title: '年龄'},
            {field: 'state', title: '状态'}
        ]],
        id: 'userTable',
        height: 310,
        limit: 5,
        response: {
            statusCode: 200 //重新规定成功的状态码为 200，table 组件默认为 0
        },
        parseData: function (res) { //将原始数据解析成 table 组件所规定的数据
            return {
                "code": res.code, //解析接口状态
                "msg": res.message, //解析提示文本
                "count": res.count, //解析数据长度
                "data": res.data //解析数据列表
            };
        },
        page: { //支持传入 laypage 组件的所有参数（某些参数除外，如：jump/elem） - 详见文档
            layout: ['count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
            , groups: 1 //只显示 1 个连续页码
            , first: false //不显示首页
            , last: false //不显示尾页
        }
    });

    const active = {
        reload: function () {
            const tableReload = document.getElementById('tableReload');

            //执行重载
            table.reload('userTable', {
                page: { //支持传入 laypage 组件的所有参数（某些参数除外，如：jump/elem） - 详见文档
                    layout: ['count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
                    , groups: 1 //只显示 1 个连续页码
                    , first: false //不显示首页
                    , last: false, //不显示尾页
                    curr: 1
                }
                , where: {
                    username: tableReload.value
                }
            });
        }
    };

    document.getElementById('table_search').addEventListener('click', function () {
        let type = this.dataset.type
        active[type] && active[type].call(this)
    });
});