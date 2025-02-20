import Request from './http.js'

const map = document.getElementById('map')

const drawMap = () => {
    Request({
        method: 'post',
        url: '/crm/map/data/api',
    }).then(res => {
        const {success, data} = res.data
        if (success) {
            const {customer, institution} = data
            map.pointElders(customer)
            map.pointInstitution(institution)
        }
    })
}

drawMap()