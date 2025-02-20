class PieChart extends HTMLElement{
    shell = null
    chart = null
    constructor() {
        super();
        const type = this.getAttribute('type')
        const data = []
        this.shell = this.render()
        const style = this.css()
        this.setupShadow(this.shell, style)

        if(type === 'pie'){
            this.drawPie()
        }else if(type === 'rose'){
            this.drawRose()
        }
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
                formatter: (params) =>{
                    console.log('params?.percent', params?.percent)
                    let tips = `${params.name}<br />${params.marker} 占比：${params?.percent || 0}%<br />${params.marker} 数量：${params.value}`
                    return tips

                }
            },
            legend: {
                left: 'left',
                top: '4%',
                orient : 'vertical',
            },
            series: [
                {
                    type: 'pie',
                    radius: ['50%', '90%'],
                    center : ['67%', '50%'],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 5,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: false,
                            fontSize: '15',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: [
                        { value: 1, name: '' },
                    ]
                }
            ]
        }

        this.setupChart(this.shell, option)
    }

    drawRose(){
        const option = {
            tooltip: {
                trigger: 'item',
                formatter: (params) =>{
                    let tips = `${params.name}<br />${params.marker} 占比：${params?.percent || 0}%<br />${params.marker} 数量：${params.value}`
                    return tips

                }
            },
            legend: {
                left: 'left',
                top: '4%',
                orient : 'vertical',
            },
            series: [
                {
                    type: 'pie',
                    roseType: 'radius',
                    radius: ['20%', '90%'],
                    center : ['67%', '50%'],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 2,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: false,
                            fontSize: '15',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: [
                        { value: 1, name: '' },
                    ]
                }
            ]
        }

        this.setupChart(this.shell, option)
    }

    setData(data){
        console.log('this.chart', this.chart)
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
                height:20rem;
                width:100%;
                color:red;
            }
        `
        return style
    }

}

customElements.define('pie-chart', PieChart)
