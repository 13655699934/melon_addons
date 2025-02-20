class StatesCard extends HTMLElement {
    shell = null

    constructor() {
        super();
        let tag = this.getAttribute('tag')
        let src = this.getAttribute('src')
        let label = this.getAttribute('label')
        this.shell = this.render(tag, src, label)
        const style = this.css()
        this.setupShadow(this.shell, style)

    }

    render(tag, src, label) {
        const shell = document.createElement('div')
        shell.setAttribute('class', 'stats-card-wrap')
        shell.innerHTML = `
            <section class="card stats-card">

                <div class="stats-card-top">
                    <div class="stats-card-top-left">

                        <span class="tag"><slot name="tag"></slot></span>
                        <span class="num">--</span>
                        <span class="label">${label}</span>

                    </div>

                    <figure class="stats-card-top-right">
                        <img src="${publicPath}${src}">
                    </figure>
                </div>

                <div class="stats-card-bottom">
                    <span>当月新增</span>
                    <span class="count">--</span>
                </div>

            </section>
        `

        return shell
    }

    setData(data){
        const {total, count} = data
        console.log('data-->', data)
        const numLabel = this.shell.querySelector('.num')
        const countLabel = this.shell.querySelector('.count')
        numLabel.innerText = total
        countLabel.innerText = count
    }

    setupShadow(shell, style) {
        const shadow = this.attachShadow({mode: 'open'})
        shadow.appendChild(style)
        shadow.appendChild(shell)
    }

    css() {
        const style = document.createElement('style')
        style.textContent = `
            @import "${publicPath}css/states_card.css";
            @import "${publicPath}css/card.css";
        `
        return style
    }

}

customElements.define('states-card', StatesCard)
