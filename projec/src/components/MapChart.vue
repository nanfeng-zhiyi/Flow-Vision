<!-- 地图可视化 -->
<template>
    <div ref="target" class="w-full h-full"></div>
</template>
<script setup>
  import { ref, onMounted } from 'vue'
  import * as echarts from 'echarts'
  import { useRouter } from 'vue-router'

  const router = useRouter();

  // const route = useRoute();
  // getData().then(res=>{
  //   console.log('this is the res',res)
  // })
  
  // 地图导入
  import mapJson from '@/assets/mapData/china.json'
  
  var geoCoordMap = {

'上海': [121.4648, 31.2891],
'乌鲁木齐': [87.9236, 43.5883],
'兰州': [103.5901, 36.3043],
'北京': [116.4551, 40.2539],
'北海': [109.314, 21.6211],
'南京': [118.8062, 31.9208],
'厦门': [118.1689, 24.6478],
'合肥': [117.29, 32.0581],
'哈尔滨': [127.9688, 45.368],
'大连': [122.2229, 39.4409],
'天津': [117.4219, 39.4189],
'太原': [112.3352, 37.9413],
'威海': [121.9482, 37.1393],
'广州': [113.5107, 23.2196],
'廊坊': [116.521, 39.0509],
'张家口': [115.1477, 40.8527],
'成都': [103.9526, 30.7617],
'拉萨': [91.1865, 30.1465],
'无锡': [120.3442, 31.5527],
'日照': [119.2786, 35.5023],
'昆明': [102.9199, 25.4663],
'杭州': [119.5313, 29.8773],
'枣庄': [117.323, 34.8926],
'柳州': [109.3799, 24.9774],
'株洲': [113.5327, 27.0319],
'武汉': [114.3896, 30.6628],
'汕头': [117.1692, 23.3405],
'江门': [112.6318, 22.1484],
'海口': [110.3893, 19.8516],
'淄博': [118.0371, 36.6064],
'淮安': [118.927, 33.4039],
'深圳': [114.5435, 22.5439],
'烟台': [120.7397, 37.5128],
'玉溪': [101.9312, 23.8898],
'盐城': [120.2234, 33.5577],
'石家庄': [114.4995, 38.1006],
'福州': [119.4543, 25.9222],
'苏州': [120.6519, 31.3989],
'西安': [109.1162, 34.2004],
'重庆': [107.7539, 30.1904],
'香港': [114.1694, 22.3193],
'青岛':[120.3826, 36.0671],
'银川':[106.2065, 38.5026],
'瑞丽': [24.0128, 97.8519],
 '连云港': [34.5967, 119.2216]
};
// 包含首都放射线， 上海的两条  以及青岛的两条
// 背景
var BJData = [
[{
    name: '北京',
    value: 200
}, {
    name: '哈尔滨',
}],

 [{
  name: '北京',
    value: 200

}, {
    name: '香港',
}],
[{
  name: '北京',
    value: 200
}, {
    name: '福州',
}],
[{
  name: '北京',
    value: 200
}, {
    name: '拉萨',
}],
[{
  name: '北京',
    value: 200
}, {
    name: '重庆',
}],
[{
  name: '北京',
    value: 200
}, {
    name: '乌鲁木齐',
}],
[{
  name: '北京',
    value: 200
}, {
    name: '上海',
}],
];
//上海
var sData = [
[{
    name: '上海',
    value: 150
}, {
    name: '西安',
}],
[{
    name: '上海',
    value: 150
}, {
    name: '成都',
}],
[{
     name: '上海',
     value: 150
}, {
    name: '重庆'
}],
[{
    name: '上海',
    value: 150
}, {
    name: '昆明'
}],

]
// 青岛
var qData = [
[{
    name: '青岛',
    value: 120
}, {
    name: '兰州',
}],
[{
    name: '青岛',
    value: 120
}, {
    name: '银川',
}],
]

var yData = [
[{
    name: '银川',
    value: 120
}, {
    name: '白色',
}],
[{
    name: '银川',
    value: 120
}, {
    name: '昆明',
}],
]

var kData = [
[{
    name: '昆明',
    value: 120
}, {
    name: '广州',
}],
]

var hData = [
[{
    name: '杭州',
    value: 90
}, {
    name: '长沙',
}],
]

var hhData = [
[{
    name: '哈尔滨',
    value: 90
}, {
    name: '大连',
}],
]



var seriess = []  // 就是一个配置数组


var planePath = 'path://M.6,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705'

var color = ['#ffa022','#3ed4ff', '#a6c84c'];


  const props = defineProps({
    data: {
      typeof: Object,
      required: true,
    }
  })

  // 1. 初始化 echarts 实例
  let mChart = null
  const target = ref(null)

  var convertData = function(data) {
      var res = [];
      for (var i = 0; i < data.length; i++) {
          var dataItem = data[i]; // 拿到每一个元素
          var fromCoord = geoCoordMap[dataItem[0].name];// 找到的是第一个元素的经纬度
          var toCoord = geoCoordMap[dataItem[1].name]; // 找到的是目的地的经纬度
          if (fromCoord && toCoord) {
              res.push([{
                  coord: fromCoord // 起点
              }, {
                  coord: toCoord // 终点
              }]);
          }
      }
      return res;
  };
  //  console.log('aaaa' + a[1][0][0].value)
  onMounted(() => {
    // 地图注册
    echarts.registerMap('china', mapJson)
    mChart = echarts.init(target.value)
    renderChart()

    mChart.on('click', function(province){
      console.log(province.name);
      // if(province.type == 'geo'){
        // 如果类型是省份的名字
        if(province.componentType == 'geo'){
        router.push({path:'/details', query:{province: province.name}})
        }
        
      // }
    })
  })
  ;[
      ['北京', BJData],
      ['上海', sData],
      ['青岛', qData],
      ['银川', yData],
      ['昆明', kData],
      ['杭州', hData],
      ['哈尔滨', hhData]
      // ['青岛', qData]
    //   ['九江', SHData],
    //   ['新疆', GZData]
  ].forEach(function(item, i) {
      seriess.push(
        {
          name: item[0] + ' Top10',
          type: 'lines',
          zlevel: 1,
          effect: {
              show: true,
              period: 6,
              trailLength: 0.7,
              color: '#fff',
              symbolSize: 3
          },
          lineStyle: {
              normal: {
                  color: color[i],
                  width: 0,
                  curveness: 0.2
              }
          },
          data: convertData(item[1]) // 所以这里遍历的时起点和终点
      }, 
      {
          name: item[0] + ' Top10',
          type: 'lines',
          zlevel: 2,
          effect: {
              show: true,
              period: 6,
              trailLength: 0,
              symbol: planePath,
              symbolSize: 15
          },
          lineStyle: {
              normal: {
                  color: color[i],
                  width: 1,
                  opacity: 0.4,
                  curveness: 0.2
              }
          },
          data: convertData(item[1]) // 这里表示的是另外一种线条格式
      }, {
          name: item[0] + ' Top10',
          type: 'effectScatter',
          coordinateSystem: 'geo',
          zlevel: 2,
          rippleEffect: {
              brushType: 'stroke'
          },
          label: {
              normal: {
                  show: true,
                  position: 'right',
                  formatter: '{b}'
              }
          },
          symbolSize: function(val) {
              return val[2] / 8;
          },
          itemStyle: {
              normal: {
                  color: color[i]
              }
          },
          // data: item[1].map(function(dataItem) {
          //     return {
          //         name: dataItem[1].name,
          //         value: geoCoordMap[dataItem[0].name].concat([dataItem[0].value])
          //     };)
          data:[{
            name: item[0],
            value: geoCoordMap[item[0]].concat([item[1][0][0].value])
          },
        ]

      });
  });


  // 2. 构建 option 配置对象 
  const renderChart = () => {
    const options = {
      // 时间轴
      timeline: {
        data: props.data.voltageLevel,
        axisType: 'category',
        autoPlay: true,
        playInterval: 3500,
        left: '10%',
        right: '10%',
        bottom: '0%',
        width: '80%',
        label: {
          normal: {
            textStyle: {
              color: '#ddd'
            }
          },
          emphasis: {
            textStyle: {
              color: '#fff'
            }
          }
        },
        symbolSize: 10,
        lineStyle: {
          color: '#555'
        },
        checkpointStyle: {
          borderColor: '#888',
          borderWidth: 2
        },
        controlStyle: {
          showNextBtn: true,
          showPrevBtn: true,
          normal: {
            color: '#666',
            borderColor: '#666'
          },
          emphasis: {
            color: '#aaa',
            borderColor: '#aaa'
          }
        }
      },
      // 基础配置
      baseOption: {
        grid: {
          top: '15%',
          right: '2%',
          bottom: '10%',
          width: '20%',
        },
        // 地图配置
        geo: {
          show: true,
          map: 'china',
          roam: true,
          zoom: 1.25,
          center: [104.114129, 37.150339],
          itemStyle: {
            normal: {
              borderColor: 'rgba(147,235,248,1)',
              borderWidth: 1,
              areaColor: {
                type: 'radial',
                x: 0.5,
                y: 0.5,
                r: 0.5,
                colorStops: [{
                  offset: 0,
                  color: 'rgba(147,235,248,0)',
                }, {
                  offset: 1,
                  color: 'rgba(147,235,248,.2)',
                }]
              }
            },
            emphasis: {
              areaColor: '#389bb7',
              borderWidth: 0,
            },
          },
        },
        // series: seriess
      },
     
      // 动态配置
      options: [],
     
    }

    // 遍历年份
    props.data.voltageLevel.forEach((item, index) => {
      options.options.push({
        backgroudColor: '#142037',
        title: [
          {
            text: '2019-2021 年度数据统计',
            left: '28%',
            top: '0%',
            textStyle: {
              color: '#ccc',
              fontSize: 30
            }
          },
          //  {
          //   id: 'statistic',
          //   text: item + '年度数据统计情况',
          //   right: '0%',
          //   top: '4%',
          //   textStyle: {
          //     color: '#ccc',
          //     fontSize: 20
          //   }
          // }
        ],
        // xAxis: {
        //   type: 'value',
        //   scale: true,
        //   position: 'top',
        //   splitLine: {
        //     show: false,
        //   },
        //   axisTick: {
        //     show: false,
        //   },
        //   axisLabel: {
        //     margin: 2,
        //     textStyle: {
        //       color: '#aaa'
        //     }
        //   }
        // },
        // yAxis: {
        //   type: 'category',
        //   axisLine: {
        //     show: true,
        //     lineStyle: {
        //       color: '#ddd'
        //     }
        //   },
        //   axisTick: {
        //     show: false,
        //   },
        //   axisLabel: {
        //     interval: 0,
        //     textStyle: {
        //       color: '#ddd'
        //     }
        //   },
        //   data: props.data.categoryData[item].map(item => item.name)
        // },
        series: [
           ...seriess
        //   ,{
        //   type: 'bar',
        //   zlevel: 2.5,
        //   itemStyle: {
        //     normal: {
        //       color: props.data.colors[index]
        //     }
        //   },
        //   data: props.data.categoryData[item].map(item => item.value)
        // },
    ],
 


    
    // toolbox: 
    // {
    //    tooltip:{
    //   show:true,
    //   trigger:'axis',
    //   formatter:function(param){
    //      return "<div>"+param.title+'按钮'+"</div>";
    //   },
    // },
    //    feature :{
    //      myTool: {
    //         show: true,
    //         title: 'show',
    //         iconStyle:{
    //         opacity:0.5,
    //         borderWidth:1,
    //         borderColor:'red',
    //       },
    //         onclick: function(params){
              
    //            if(params.checked){
    //                 //  options.series[2].data = highwayData
    //                 //  console.log(options.series[2].data)
    //                 console.log('hellldfjjdsfs')
    //            }else{
    //               //  console.log(options.series.length)
    //               //  options.series[1].data = []
    //               //  console.log(options.series[1].data)
    //            }
    //         }

    //      }
    //    }
    //    ,
    //    icon:'path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891'
    //   }
      })

    // console.log(options.options[index].series)
    // console.log('seriess', seriess)
    //  options.options[index].series.push(seriess)
    })
    // 3. 通过 实例.setOptions(option)
    // console.log(seriess)
    console.log(options.series)
    // options.options.series.push(seriess)
    mChart.setOption(options)
  }

</script>
<style lang="scss" scoped>

</style>