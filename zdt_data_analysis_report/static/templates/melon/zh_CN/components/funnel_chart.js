class FunnelChart extends HTMLElement{
    shell = null
    chart = null
    constructor() {
        super();
        const data = []
        this.shell = this.render()
        const style = this.css()
        this.setupShadow(this.shell, style)

        this.drawPie()
    }

    render(){
        const shell = document.createElement('div')
        shell.setAttribute('class', 'chart')
        return shell
    }

    setupChart(shell, option){
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

    drawPie(){
        const option = {
            tooltip: {
                trigger: 'item',
                formatter: (params) => {
                    return `${params.name}<br />${params.marker} 数量：${params.value}`
                }
            },
            // legend: {
            //   data: ['Show', 'Click', 'Visit', 'Inquiry', 'Order']
            // },
            series: [
                {
                    name: 'Funnel',
                    type: 'funnel',
                    left: '10%',
                    top: 60,
                    bottom: 60,
                    width: '80%',
                    min: 0,
                    max: 100,
                    minSize: '0%',
                    maxSize: '100%',
                    sort: 'descending',
                    gap: 2,
                    label: {
                        show: true,
                        position: 'inside'
                    },
                    labelLine: {
                        length: 10,
                        lineStyle: {
                            width: 1,
                            type: 'solid'
                        }
                    },
                    itemStyle: {
                        borderColor: '#fff',
                        borderWidth: 1
                    },
                    emphasis: {
                        label: {
                            fontSize: 20
                        }
                    },
                    data: [
                        { value: 10, name: '' },
                        { value: 20, name: '' },
                        { value: 30, name: '' },
                        { value: 40, name: '' },
                        { value: 50, name: '' }
                    ]
                }
            ]
        };

        this.setupChart(this.shell, option)
    }

    setData(data){
        this.chart.setOption({
            series : [
                {
                    data,
                }
            ]
        })
    }


    setupShadow(shell, style){
        const shadow = this.attachShadow({mode : 'open'})
        shadow.appendChild(style)
        shadow.appendChild(shell)
    }

    css(){
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

customElements.define('funnel-chart', FunnelChart)
