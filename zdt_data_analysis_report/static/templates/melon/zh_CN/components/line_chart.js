class LineChart extends HTMLElement{
    shell = null
    chart = null
    constructor() {
        super();
        const type = this.getAttribute('type')
        const data = []
        this.shell = this.render()
        const style = this.css()
        this.setupShadow(this.shell, style)
        if(type === 'simple'){
            this.drawSimpleLine()
        }else if(type === 'multiple'){
            this.drawMultipleLine()
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

    drawSimpleLine(){
        const date = new Date()
        let xAxisData = genDateRange(`${date.getFullYear()}-1`, `${date.getFullYear()}-12`, 'month')

        const option = {
            grid: {
                left: '5%',
                right: '8%',
                bottom: '10%',
                top : '5%',
                containLabel: true
            },
            tooltip: {
                trigger: 'axis'
            },
            dataZoom: [
                {
                    type: 'inside',
                },
                {
                    type : 'slider'
                }
            ],
            xAxis: {
                type: 'category',
                data: xAxisData
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: [],
                    type: 'line',
                    smooth: true
                }
            ]
        }

        this.setupChart(this.shell, option)
    }

    setLineData(startTime, endTime, data, rangeType){
        let xAxisData = genDateRange(startTime, endTime, rangeType)
        const legendData = Object.keys(data)
        const series =  Object.entries(data).map(item => {
            console.log('item', item)
            return {
                name : item[0],
                data : item[1],
                type: 'line',
            }
        })

        console.log('series', series)

        this.chart.setOption({
            legend: {
                show : legendData.length > 1,
                data : legendData
            },
            xAxis: {
                type: 'category',
                data: xAxisData
            },
            series,
        })
    }

    drawMultipleLine() {
        const date = new Date()
        let xAxisData = genDateRange(`${date.getFullYear()}-1`, `${date.getFullYear()}-12`, 'month')

        const option = {
            tooltip: {
                trigger: 'axis'
            },
            dataZoom: [
                {
                    type: 'inside',
                },
                {
                    type : 'slider'
                }
            ],
            legend: {
                left: 'left',
                top: '4%',
                data: [],
                orient : 'vertical',
            },
            grid: {
                left: '120',
                right: '8%',
                bottom: '10%',
                top : '5%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: xAxisData,
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '',
                    type: 'line',
                    data: []
                },
                {
                    name: '',
                    type: 'line',
                    data: []
                },

            ]
        };

        this.setupChart(this.shell, option)
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

customElements.define('line-chart', LineChart)
