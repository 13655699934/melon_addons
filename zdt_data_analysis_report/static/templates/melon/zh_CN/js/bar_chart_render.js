import Request from './http.js'

const drawChart = () => {
    const barCharts = ['customer_occ_data']
    Request({
        method: 'post',
        url: '/crm/bar/category/api',
    }).then(res => {
        const {success, data} = res.data
        if (success) {
            barCharts.forEach(item => {
                let chartData = data[item]
                let chart = document.querySelector(`[data-id=${item}]`)
                chart.setData(chartData)
            })
        }
    })
}

drawChart()