class PolarBarChart extends HTMLElement {
    shell = null
    chart = null

    constructor() {
        super();
        const title = this.getAttribute('title')
        const data = []
        this.shell = this.render()
        const style = this.css()
        this.setupShadow(this.shell, style)

        this.drawPolar(title)
    }

    render() {
        const shell = document.createElement('div')
        shell.setAttribute('class', 'chart')
        return shell
    }

    setupChart(shell, option) {
        const chart = echarts.init(shell)
        chart.setOption(option)
        setTimeout(() => {
            chart.resize();
        }, 100)
        window.addEventListener("resize", function () {
            setTimeout(() => {
                chart.resize();
            }, 100)
        })
        this.chart = chart
        return chart
    }

    drawPolar(title) {
        const data = [
            {
                name: '价格',
                category: [
                    {
                        name: '基础月费',
                        value: 1
                    },
                    {
                        name: '会员卡费',
                        value: 2
                    },
                    {
                        name: '押金费用',
                        value: 3
                    },
                    {
                        name: '餐饮费用',
                        value: 4
                    },
                ]
            },
            {
                name: '环境',
                category: [
                    {
                        name: '活动场地',
                        value: 1
                    },
                    {
                        name: '居住条件',
                        value: 2
                    },
                ]
            },
            {
                name: '服务',
                category: []
            },
            {
                name: '医疗',
                category: []
            },
            {
                name: '交通',
                category: []
            },
            {
                name: '设施',
                category: []
            },
            {
                name: '其他',
                category: []
            },
        ]

        const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
        const series = data.reduce((total, item,index) => {
            let result = item.category.map((category, categoryIndex) => {
                let data = new Array(index + 1).fill(0)
                data[index] = category.value
                let obj = {
                    type: 'bar',
                    name: category.name,
                    data: data,
                    itemStyle : {
                        color : colors[categoryIndex % colors.length]
                    },
                    coordinateSystem: 'polar',
                    stack: 'a',
                    emphasis: {
                        focus: 'series'
                    }
                }

                return obj
            })

            total = total.concat(result)
            return total
        }, [])
        console.log('series', series)

        const option = {
            title: {
                text: title,
                left: 'center',
                top: '20'
            },
            tooltip: {
                trigger: 'axis',
                formatter: (params) => {
                    let result = `${params[0].axisValue}<br />`;
                    params.forEach(item => {
                        let str = `${item.marker} ${item.seriesName}: ${item.value}<br />`
                        if(item.value !== 0){
                            result = result.concat(str)
                        }
                    })
                    return result
                }
            },
            angleAxis: {
                type: 'category',
                data: data.map(item => item.name)
            },
            radiusAxis: {},
            polar: {},
            series : [
                {
                    type: 'bar',
                    data: [],
                    coordinateSystem: 'polar',
                    stack: 'a',
                    emphasis: {
                        focus: 'series'
                    }
                }
            ],

            // series: [
            //     {
            //         type: 'bar',
            //         data: [1,2,3,4,5,6,7],
            //         coordinateSystem: 'polar',
            //         // name: '基础月费',
            //         stack: 'a',
            //         emphasis: {
            //             focus: 'series'
            //         }
            //     },
            //     {
            //         type: 'bar',
            //         data: [4],
            //         coordinateSystem: 'polar',
            //         name: '会员卡费',
            //         stack: 'a',
            //         emphasis: {
            //             focus: 'series'
            //         }
            //     },
            //     {
            //         type: 'bar',
            //         data: [0,8],
            //         coordinateSystem: 'polar',
            //         name: '活动场地',
            //         stack: 'a',
            //         emphasis: {
            //             focus: 'series'
            //         }
            //     }
            //
            // ],
        };

        this.setupChart(this.shell, option)
    }

    setData(data){
        // const data = [
        //     {
        //         name: '价格',
        //         category: [
        //             {
        //                 name: '基础月费',
        //                 value: 1
        //             },
        //             {
        //                 name: '会员卡费',
        //                 value: 2
        //             },
        //             {
        //                 name: '押金费用',
        //                 value: 3
        //             },
        //             {
        //                 name: '餐饮费用',
        //                 value: 4
        //             },
        //         ]
        //     },
        //     {
        //         name: '环境',
        //         category: [
        //             {
        //                 name: '活动场地',
        //                 value: 1
        //             },
        //             {
        //                 name: '居住条件',
        //                 value: 2
        //             },
        //         ]
        //     },
        //     {
        //         name: '服务',
        //         category: []
        //     },
        //     {
        //         name: '医疗',
        //         category: []
        //     },
        //     {
        //         name: '交通',
        //         category: []
        //     },
        //     {
        //         name: '设施',
        //         category: []
        //     },
        //     {
        //         name: '其他',
        //         category: []
        //     },
        // ]

        const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
        const series = data.reduce((total, item,index) => {
            let result = item.category.map((category, categoryIndex) => {
                let data = new Array(index + 1).fill(0)
                data[index] = category.value
                let obj = {
                    type: 'bar',
                    name: category.name,
                    data: data,
                    itemStyle : {
                        color : colors[categoryIndex % colors.length]
                    },
                    coordinateSystem: 'polar',
                    stack: 'a',
                    emphasis: {
                        focus: 'series'
                    }
                }

                return obj
            })

            total = total.concat(result)
            return total
        }, [])

        console.log('series-001', series)

        this.chart.setOption({
            angleAxis: {
                type: 'category',
                data: data.map(item => item.name)
            },
            series,
        })
    }

    setupShadow(shell, style) {
        const shadow = this.attachShadow({mode: 'open'})
        shadow.appendChild(style)
        shadow.appendChild(shell)
    }

    css() {
        const style = document.createElement('style')

        style.textContent = `
            .chart{
                height:50rem;
                width:100%;
                color:red;
            }
        `
        return style
    }

}

customElements.define('polar-bar-chart', PolarBarChart)
