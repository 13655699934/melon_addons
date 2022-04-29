odoo.define('load_dashboard', function (require) {
    "use strict";
    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var _t = core._t;


    var PyEcharts = AbstractAction.extend({
        template: 'pyecharts_template',
        cssLibs: [
            '/melon_dashboard/static/src/css/lib/icon.css',
            '/melon_dashboard/static/src/css/lib/icons.css',
            '/melon_dashboard/static/src/css/lib/app.css',
        ],
        jsLibs: [
            'melon_dashboard/static/src/js/lib/Chart.min.js',
            'melon_dashboard/static/src/js/lib/Chart.extension.js',
        ],
        events: {
            'click .charts_click_demo': 'charts_click_demo'
        },

        init: function (parent, data) {
            return this._super.apply(this, arguments);
        },

        start: function () {
            $(document).ready(function () {
                // demo begin
                var self = this;
                // demo end
                $(function () {
                    fetchData();
                    var chart_2 = echarts.init(document.getElementById('changedetail'));
                    chart_2.setOption(get_chart1_option());

                    var ctx = document.getElementById("chart5").getContext('2d');
                    var gradientStroke1 = ctx.createLinearGradient(0, 0, 0, 300);
                    gradientStroke1.addColorStop(0, '#f54ea2');
                    gradientStroke1.addColorStop(1, '#ff7676');
                    var gradientStroke2 = ctx.createLinearGradient(0, 0, 0, 300);
                    gradientStroke2.addColorStop(0, '#42e695');
                    gradientStroke2.addColorStop(1, '#3bb2b8');

                    var myChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: [1, 2, 3, 4, 5, 6, 7, 8],
                            datasets: [{
                                label: 'Clothing',
                                data: [40, 30, 60, 35, 60, 25, 50, 40],
                                borderColor: gradientStroke1,
                                backgroundColor: gradientStroke1,
                                hoverBackgroundColor: gradientStroke1,
                                pointRadius: 0,
                                fill: false,
                                borderWidth: 1
                            }, {
                                label: 'Electronic',
                                data: [50, 60, 40, 70, 35, 75, 30, 20],
                                borderColor: gradientStroke2,
                                backgroundColor: gradientStroke2,
                                hoverBackgroundColor: gradientStroke2,
                                pointRadius: 0,
                                fill: false,
                                borderWidth: 1
                            }]
                        },
                        options: {
                            maintainAspectRatio: false,
                            legend: {
                                position: 'bottom',
                                display: false,
                                labels: {
                                    boxWidth: 8
                                }
                            },
                            scales: {
                                xAxes: [{
                                    barPercentage: .5
                                }]
                            },
                            tooltips: {
                                displayColors: false,
                            }
                        }
                    });
                });

                function get_chart1_option() {
                    return {
                        title: {
                            text: 'Area'
                        },
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'cross',
                                label: {
                                    backgroundColor: '#6a7985'
                                }
                            }
                        },
                        legend: {
                            data: ['Email', 'Direct', 'Search Engine']
                        },
                        toolbox: {
                            feature: {
                                saveAsImage: {}
                            }
                        },
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                        },
                        xAxis: [
                            {
                                type: 'category',
                                boundaryGap: false,
                                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                            }
                        ],
                        yAxis: [
                            {
                                type: 'value'
                            }
                        ],
                        series: [
                            {
                                name: 'Email',
                                type: 'line',
                                stack: 'Total',
                                color: 'rgb(13 229 210)',
                                areaStyle: {},
                                emphasis: {
                                    focus: 'series'
                                },
                                data: [120, 132, 101, 134, 90, 230, 210]
                            },
                            {
                                name: 'Direct',
                                type: 'line',
                                stack: 'Total',
                                color: 'rgb(10 61 207 / 97%)',
                                areaStyle: {},
                                emphasis: {
                                    focus: 'series'
                                },
                                data: [320, 332, 301, 334, 390, 330, 320]
                            },
                            {
                                name: 'Search Engine',
                                type: 'line',
                                stack: 'Total',
                                color: 'rgb(243 36 5)',
                                label: {
                                    show: true,
                                    position: 'top'
                                },
                                areaStyle: {},
                                emphasis: {
                                    focus: 'series'
                                },
                                data: [820, 932, 901, 934, 1290, 1330, 1320]
                            }
                        ]
                    };
                };

                function fetchData() {
                    $.ajax({
                        type: "GET",
                        url: "/pyecharts",
                        dataType: 'json',
                        success: function (result) {
                            var count = result.count;
                            var column = result.column;
                            var theme = result.theme;
                            var height = result.height;
                            var col = "col-md-" + String(12 / column);
                            var details = result.details;
                            var ech = document.getElementById("ech");
                            for (var detail in details) {
                                console.log(details[detail]);
                                var detailDiv = document.createElement("div");
                                detailDiv.setAttribute("class", col);
                                var d = document.createElement("div");
                                d.setAttribute("id", details[detail]['sequence']);
                                d.style.width = "100%";
                                d.style.height = height + 'px';
                                // d.style.border = "1px solid #B0E2FF";
                                d.style.marginBottom = "10px";
                                d.style.boxShadow = "0 0 1px rgb(0 0 0 / 13%), 0 1px 3px rgb(0 0 0 / 20%)";
                                detailDiv.appendChild(d);

                                ech.appendChild(detailDiv);
                                var chart = echarts.init(document.getElementById(details[detail]['sequence']), theme, {renderer: 'canvas'});
                                chart.setOption(details[detail]['edata']);
                            }
                        },
                        error: function (request) {
                            console.log("error");
                        },
                    });
                }
            });
            return true;
        },


        charts_click_demo: function (ev) {
            let self = this;
            ev.stopPropagation();
            ev.preventDefault();
            console.log('charts_click_demo')
//            var options = {
//                on_reverse_breadcrumb: this.on_reverse_breadcrumb,
//            };
            this.do_action({
                name: _t("Echarts Dashboard"),
                type: 'ir.actions.act_window',
                res_model: 'melon.dashboard',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
//                domain: [['employee_id','=', this.login_employee.id]],
                domain: [],
                target: 'current', //self on some of them
            });
        },

    });
    core.action_registry.add('load_dashboard', PyEcharts);
});
