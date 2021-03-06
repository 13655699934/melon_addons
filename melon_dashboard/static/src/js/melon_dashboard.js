odoo.define('melon_dashboard.melon_dashboard',function(require){
     "user strict";
     
     var core = require('web.core');
     var data = require('web.data');
     var time = require('web.time');
     var AbstractAction = require('web.AbstractAction');
     var datepicker = require('web.datepicker');
     var BasicModel = require('web.BasicModel');
     var Widget =require('web.Widget');

     var QWeb = core.qweb;
     var _t = core._t;

     var Dashboard = AbstractAction.extend({
         events:{
             'change #dashboard_block1_date':'block1_date_change',
             'change #dashboard_block2_date':'block2_date_change',
             'change #dashboard_block3_date':'block3_date_change',
         },

         init:function(){
              this._super.apply(this,arguments);
         },
         start:function(){
              this._super.apply(this,arguments);
              var self=this;
              this._rpc({
                   model:'melon.dashboard',
                   method:'get_data',
              }).then(function(result){
                 self.render_data = result;
                 self.show();
              });
         },

         show:function(){
              var self=this;
              this.$el.html(QWeb.render('melon_dashboard.mo_dashboard',{widget:self}));
              var $dashboard_main=this.$el.find('#mo_dashboard_main');

              self.Chart1=echarts.init(self.$el.find('#mo_chart1')[0]);
              self.Chart1.setOption(self.get_chart1_option(self.render_data.block1));

              self.Chart2=echarts.init(self.$el.find('#mo_chart2')[0]);
              self.Chart2.setOption(self.get_chart2_option(self.render_data.block2));

              self.Chart3=echarts.init(self.$el.find('#mo_chart3')[0]);
              self.Chart3.setOption(self.get_chart3_option(self.render_data.block3));

              self.Chart5=echarts.init(self.$el.find('#mo_chart5')[0]);
              self.Chart5.setOption(self.get_chart5_option());

              var year = moment().year();
              var $datepicker=self.$el.find('#dashboard_block1_date');
              var $datepicker2=self.$el.find('#dashboard_block2_date');
              var $datepicker3=self.$el.find('#dashboard_block3_date');

              self.year_widget($datepicker);
              self.year_widget($datepicker2);
              self.year_widget($datepicker3);
         },

         year_widget:function($datepicker){
              $datepicker.datetimepicker({
                     pickTime:false,
                     useSeconds:false,
                     startDate:moment({y:1900}),
                     endDate:moment().add(200,"y"),
                     calendarWeeks:true,
                     icons:{
                        time:'fa fa-clock-o',
                        date:'fa fa-calendar',
                        up:'fa fa-chevron-up',
                        down:'fa fa-chevron-down'
                     },
                     language:moment.locale(),
                     format:'YYYY???',
                     viewMode:'years',
                     minViewMode:'years'
              });
         },

         block1_date_change:function(e){
                var self = this;
                var year = moment(e.target.value,'YYYY???').year();
                this._rpc({
                     model:'melon.dashboard',
                     method:'get_data_block1',
                     args:[year]
                })
                .then(function(result){
                      self.Chart1.setOption(self.get_chart1_option(result));
                });

         },

         block2_date_change:function(e){
                var self = this;
                var year = moment(e.target.value,'YYYY???').year();
                this._rpc({
                     model:'melon.dashboard',
                     method:'get_data_block2',
                     args:[year]
                })
                .then(function(result){
                      self.Chart2.setOption(self.get_chart2_option(result));
                });

         },

//         $('.yearpicker').datepicker({
//			 startView: 'decade',
//			 minView: 'decade',
//			 format: 'yyyy',
//			 maxViewMode: 2,
//			 minViewMode:2,
//			 autoclose: true
//		 });

         block3_date_change:function(e){
                var self = this;
                var year = moment(e.target.value,'YYYY???').year();
                this._rpc({
                     model:'melon.dashboard',
                     method:'get_data_block3',
                     args:[year]
                })
                .then(function(result){
                      self.Chart3.setOption(self.get_chart3_option(result));
                });

         },

         get_chart1_option:function(block){
             return{
                  tooltip:{
                     trigger:'axis',
                     axisPointer:{
                         type:'line'
                     }
                  },
                  legend:{
                      data:['????????????']
                  },
                  toolbox:{
                      show:true,
                      feature:{
                            dataView:{show:true,readOnly:false},
                            magicType:{show:true,type:['line','bar']},
                            restore:{show:true},
                            saveAsImage:{show:true}
                      }
                  },
                  calculable:true,
                  xAxis:{
                     name:'??????',
                     type:'category',
                     data:['1???','2???','3???','4???','5???','6???','7???','8???','9???','10???','11???','12???']
                  },
                  yAxis:{
                     name:'??????',
                     type:'value',
                  },
                  series:[{
                     name:'????????????',
                     color:["#e40524"],
                     data:block.order_num,
                     type:'line'
                  }],
             };
         },


         get_chart1_option:function(block){
             return{
                  tooltip:{
                     trigger:'axis',
                     axisPointer:{
                         type:'line'
                     }
                  },
                  legend:{
                      data:['????????????']
                  },
                  toolbox:{
                      show:true,
                      feature:{
                            dataView:{show:true,readOnly:false},
                            magicType:{show:true,type:['line','bar']},
                            restore:{show:true},
                            saveAsImage:{show:true}
                      }
                  },
                  calculable:true,
                  xAxis:{
                     name:'??????',
                     type:'category',
                     data:['1???','2???','3???','4???','5???','6???','7???','8???','9???','10???','11???','12???']
                  },
                  yAxis:{
                     name:'??????',
                     type:'value',
                  },
                  series:[{
                     name:'????????????',
                     color:["#e40524"],
                     data:block.order_num,
                     type:'line'
                  }],
             };
         },

         get_chart2_option:function(block){
             return{
                  tooltip:{
                     trigger:'axis',
                     axisPointer:{
                         type:'shadow'
                     }
                  },
                  legend:{
                      data:['????????????','????????????']
                  },
                  toolbox:{
                      show:true,
                      feature:{
                            dataView:{show:true,readOnly:false},
                            magicType:{show:true,type:['line','bar']},
                            restore:{show:true},
                            saveAsImage:{show:true}
                      }
                  },
                  calculable:true,
                  grid:{
                     left:'3%',
                     right:'4%',
                     bottom:'3%',
                     containLabel:true
                  },
                  xAxis:[{
                     name:'??????',
                     type:'category',
                     data:['1???','2???','3???','4???','5???','6???','7???','8???','9???','10???','11???','12???'],
                     axisTick:{
                         alignWithLabel:true
                     }
                  }],
                  yAxis:[{
                     name:'??????',
                     type:'value',
                  }],
                  series:[{
                     name:'????????????',
                     barWidth:'30%',
                     data:block.total,
                     type:'bar',
                     color:['#3fdde3'],
                  },{
                     name:'????????????',
                     barWidth:'30%',
                     data:block.pay,
                     type:'bar',
                     color:['#e41906'],
                  }],
             };
         },

         get_chart3_option:function(block){
             return{
                  tooltip:{
                     trigger:'item',
                     formatter:"{a} <br/> {b}: {c} (%)"
                  },
                  legend:{
                      orient: 'vertical',
                      left: 'left',
                      data:['??????','???????????????','????????????']
                  },
                  toolbox:{
                      show:true,
                      feature:{
                            dataView:{show:true,readOnly:false},
                            saveAsImage:{show:true},
                      }
                  },
                  series: [
                    {
                        name: '????????????',
                        type: 'pie',
                        radius: '55%',
                        center:['50%','60%'],
                        color:['#e40523',"#56e42f","#a414e4"],
                        data: [
                            {value: block['type_num']['A'], name: '??????'},
                            {value: block['type_num']['B'], name: '???????????????'},
                            {value: block['type_num']['C'], name: '????????????'}
                        ],
                        itemStyle: {
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
             };
         },
         get_chart5_option:function(block){
             return {
//                title: {
//                    text: 'Graph ????????????'
//                },
                tooltip: {},
                animationDurationUpdate: 1500,
                animationEasingUpdate: 'quinticInOut',
                series: [
                    {
                        type: 'graph',
                        layout: 'none',
                        symbolSize: 80,
                        roam: true,
                        label: {
                            show: true
                        },
                        edgeSymbol: ['circle', 'arrow'],
                        edgeSymbolSize: [4, 10],
                        edgeLabel: {
                            fontSize: 20
                        },
                        data: [{
                            name: '??????1',
                            value:'test1',
                            x: 300,
                            y: 300,
                            itemStyle: {
                               color: '#008dca',
                            }
                            }, {
                            name: '??????2',
                            value:'test2',
                            x: 400,
                            y: 300,
                            itemStyle: {
                               color: 'yellow',
                            }
                            }, {
                            name: '??????3',
                            value:'test3',
                            x: 500,
                            y: 300,
                            itemStyle: {
                               color: 'green',
                            }
                            }, {
                            name: '??????4',
                            value:'test4',
                            x: 600,
                            y: 300,
                            itemStyle: {
                                color: 'red',
                            }
                            },{
                            name: '??????5',
                            value:'test5',
                            x: 700,
                            y: 300,
                            itemStyle: {
                                color: 'blue',
                            }
                        }],
                        // links: [],
                        links: [{
                            source: 0,
                            target: 1,
                            symbolSize: [5, 20],
                        }, {
                            source: '??????1',
                            target: '??????2'
                        }, {
                            source: '??????2',
                            target: '??????3'
                        }, {
                            source: '??????3',
                            target: '??????4'
                        }, {
                            source: '??????4',
                            target: '??????5'
                        }],
                        lineStyle: {
                            opacity: 0.9,
                            width: 5,
                            color:'red',
                            curveness: 0
                        }
                    }
                ]
            };
         },
     });
     core.action_registry.add('action_melon_dashboard',Dashboard);
     return Dashboard;
});