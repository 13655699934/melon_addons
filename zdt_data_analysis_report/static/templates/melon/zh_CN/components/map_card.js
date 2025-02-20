class MapCard extends HTMLElement {
    shell = null
    map = null
    searchName = ''
    ElderData = []

    constructor() {
        super();
        this.shell = this.render()
        const style = this.css()
        this.setupShadow(this.shell, style)

        this.map = this.drawMap()
    }

    render() {
        const shell = document.createElement('div')
        shell.setAttribute('class', 'map-wrap')
        const map = document.createElement('div')
        map.setAttribute('class', 'map')
        map.setAttribute('id', 'map')

        const searchWrap = document.createElement('div')
        searchWrap.classList.add('search')
        const input = document.createElement('input')
        const button = document.createElement('button')
        input.addEventListener('change', (ev) => {
            this.searchName = ev.target.value;
        })
        button.addEventListener('click', () => {
            this.searchElder(this.searchName)
        })
        button.innerText = "搜索"
        searchWrap.appendChild(input)
        searchWrap.appendChild(button)

        shell.appendChild(map)
        shell.appendChild(searchWrap)

        return shell
    }

    drawMap(options) {
        const map = new BMap.Map(this.shell.querySelector('#map'), {enableMapClick: false})
        // map.centerAndZoom("合肥",15)
        map.enableScrollWheelZoom()

        return map
    }

    pointInstitution(data) {
        const {name, coords} = data
        let point = new BMap.Point(coords[0], coords[1]);
        this.map.centerAndZoom(point, 15);
        let icon = new BMap.Icon(`${publicPath}imgs/melon.png`, new BMap.Size(50, 50))
        let marker = new BMap.Marker(point, {
            icon: icon
        });  // 创建标注
        let infoWindow = new BMap.InfoWindow(`
                <div>
                    <p><span>名称: </span><span>${name}</span></p>
                </div>
            `, {
            width: 200,
            title: '',
        })

        marker.addEventListener('click', () => {
            this.map.openInfoWindow(infoWindow, point) // 开启信息窗口
            this.shell.querySelector('.BMap_pop').style.height = '86px'
        })

        this.map.addOverlay(marker);


    }

    pointElders(data) {

        // const data = {
        //     elders : [
        //         {
        //             name : '',
        //             coords: [1,2],
        //             ...
        //         }
        //     ],
        //
        //     institution : {
        //         name : '',
        //         coords: [1, 2],
        //         ...
        //     }
        // }

        this.ElderData = data

        let icon = new BMap.Icon(`${publicPath}imgs/elder.png`, new BMap.Size(50, 50))
        data.forEach(item => {
            let point = new BMap.Point(item.coords[0], item.coords[1])
            let marker = new BMap.Marker(point, {
                icon: icon
            });  // 创建标注
            let infoWindow = new BMap.InfoWindow(`
                <div>
                    <p><span>姓名: </span><span>${item.name}</span></p>
                    <p><span>年龄:</span><span>${item.age}</span></p>
                    <p><span>入住房型:</span><span>${item.room_type}</span></p>
                    <p><span>护理类型:</span><span>${item.nursing_type}</span></p>
                </div>
            `, {
                width: 200,
                title: '',
            })

            this.map.addOverlay(marker);
            marker.addEventListener('click', () => {
                this.map.openInfoWindow(infoWindow, point) // 开启信息窗口
                this.shell.querySelector('.BMap_pop').style.height = '177px'
            })
        })

    }

    searchElder(name) {
        console.log('name', name)
        let theMan = this.ElderData.find(item => {
            if(item.name === name.trim()){
                return item;
            }
        })

        if(!theMan){
            window.alert('未找到搜索客户')
            return
        }

        let point = new BMap.Point(theMan.coords[0], theMan.coords[1])
        this.map.centerAndZoom(point, 15);
    }

    setupShadow(shell, style) {
        const shadow = this.attachShadow({mode: 'open'})
        shadow.appendChild(style)
        shadow.appendChild(shell)
    }

    css() {
        const style = document.createElement('style')

        style.textContent = `
            .map-wrap{
                position:relative;
                height:50rem;
                width:100%;
            }
            
            .map{
                height:100%;
                width:100%;
            }
            
            .search{
                position:absolute;
                top:2rem;
                right: 1.5rem;
                display:flex;
                align-item:center;
            }
            
            .search input{
                width : 18rem;
                height:3.5rem;
                font-size : 1.8rem;
                color:rgba(0,0,0,0.5);
                padding: 0 .8rem;
                margin-right:1rem;
                border: 1px solid #ddd;
                border-radius: .5rem
            }
            
            .search button{
                background-color: #009688;
                color: #fff;
                border: 1px solid transparent;
                padding: 0 18px;
            }
            
            .BMap_pop{
                width: 252px;
                height: 177px;
                background: rgb(255, 255, 255);
                border: 1px solid #ababab;
                position: relative;
            }
            
            .BMap_pop div{
                border:none !important
            }
        `
        return style
    }

}

customElements.define('map-card', MapCard)
