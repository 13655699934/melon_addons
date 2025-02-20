import Request from './http.js'

const statesCardWrap = document.getElementById('states-card-wrap')

const tryCard = statesCardWrap.querySelector("[data-id='try']")
const consultCard = statesCardWrap.querySelector("[data-id='consult']")
const conversionCard = statesCardWrap.querySelector("[data-id='conversion']")
const occupancyCard = statesCardWrap.querySelector("[data-id='occupancy']")

Request({
    method: 'post',
    url : '/crm/sale/api',
}).then(res => {
    console.log('res', res)
    const {success, data} = res.data
    if(success){
        let {try_data, consul_data, conversion_data, occupancy_data} = data
        conversion_data.count = conversion_data.count + '%'
        conversion_data.total = conversion_data.total + '%'
        occupancy_data.count = occupancy_data.count + '%'
        occupancy_data.total = occupancy_data.total + '%'
        tryCard.setData(try_data)
        consultCard.setData(consul_data)
        conversionCard.setData(conversion_data)
        occupancyCard.setData(occupancy_data)
    }
})