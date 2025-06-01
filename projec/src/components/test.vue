<template>
    <div style="width: 100%; height: 100vh;" class="w-full h-full" >
      <div ref="target" class="w-full h-full">你好世界</div>
    </div>
  </template>
  
  <script setup>
  import {ref, onMounted} from 'vue'
  import * as echarts from 'echarts' 
  import mapJson from '@/assets/mapData/china.json'
//   console.log('hello world')
  console.log(mapJson)
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
  };
  
  var BJData = [
      [{
          name: '北京'
      }, {
          name: '哈尔滨',
          value: 200
      }],
      [{
          name: '北京'
      }, {
          name: '上海',
          value: 90
      }],
       [{
          name: '北京'
      }, {
          name: '香港',
          value: 90
      }],
      [{
          name: '北京'
      }, {
          name: '福州',
          value: 90
      }],
      [{
          name: '北京'
      }, {
          name: '拉萨',
          value: 30
      }],
      [{
          name: '北京'
      }, {
          name: '重庆',
          value: 100
      }],
      [{
          name: '北京'
      }, {
          name: '乌鲁木齐',
          value: 40
      }],
  ];
  
  var SHData = [
       [{
          name: '九江'
      }, {
          name: '九江',
          value: 200
      }],
      
      [{
          name: '九江'
      }, {
          name: '长沙',
          value: 95
      }],
      [{
          name: '九江'
      }, {
          name: '武汉',
          value: 30
      }],
      [{
          name: '九江'
      }, {
          name: '南昌',
          value: 20
      }],
      [{
          name: '九江'
      }, {
          name: '合肥',
          value: 70
      }],
      [{
          name: '九江'
      }, {
          name: '南京',
          value: 60
      }],
      [{
          name: '九江'
      }, {
          name: '福州',
          value: 50
      }],
      [{
          name: '九江'
      }, {
          name: '上海',
          value: 100
      }],
      [{
          name: '九江'
      }, {
          name: '深圳',
          value: 100
      }],
     
  ];
  
  var GZData = [
      [{
          name: '新疆玛纳斯基地'
      }, {
          name: '新疆玛纳斯基地',
          value: 200
      }],
      [{
          name: '新疆玛纳斯基地'
      }, {
          name: '  ',
          value: 90
      }],
      [{
          name: '新疆玛纳斯基地'
      }, {
          name: ' ',
          value: 40
      }],
      [{
          name: '新疆玛纳斯基地'
      }, {
          name: '呼和浩特',
          value: 90
      }],
      [{
          name: '新疆玛纳斯基地'
      }, {
          name: '昆明',
          value: 40
      }],
      [{
          name: '新疆玛纳斯基地'
      }, {
          name: '成都',
          value: 10
      }],
      [{
          name: '新疆玛纳斯基地'
      }, {
          name: '兰州',
          value: 95
      }],
      [{
          name: '新疆玛纳斯基地'
      }, {
          name: '银川',
          value: 90
      }],
      [{
          name: '新疆玛纳斯基地'
      }, {
          name: '西宁',
          value: 80
      }],
  
  ];
  
  var planePath = 'path://M.6,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705';
  
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
  
  let mChart = null
  const target = ref(null)
  console.log('hello world')
  onMounted(()=>{
    echarts.registerMap('china', mapJson)
    mChart = echarts.init(target.value)
    console.log('已经进入到钩子函数了')
    renderChart()
  })
  
  
  var color = ['#3ed4ff', '#ffa022', '#a6c84c'];
  var series = [];
  [
      ['北京', BJData],
    //   ['九江', SHData],
    //   ['新疆', GZData]
  ].forEach(function(item, i) {
      series.push({
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
      }, {
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
          data: item[1].map(function(dataItem) {
              return {
                  name: dataItem[1].name,
                  value: geoCoordMap[dataItem[1].name].concat([dataItem[1].value])
              };
          })
      });
  });
      const renderChart = ()=>{
        const options = {
            backgroundColor: '#080a20',
      title: {
          text: '模拟迁徙',
          subtext: '数据纯属虚构',
          left: 'left',
          textStyle: {
              color: '#fff'
          }
      },
      tooltip: {
          trigger: 'item'
      },
      legend: {
          orient: 'vertical',
          top: 'bottom',
          left: 'right',
          data: ['北京 Top10', '上海 Top10', '广州 Top10'],
          textStyle: {
              color: '#fff'
          },
          selectedMode: 'single'
      },
      geo: {
          map: 'china',
          show: true,
          label: {
              emphasis: {
                  show: false
              }
          },
          roam: true,
          itemStyle: {
              normal: {
                  areaColor: '#132937',
                  borderColor: '#0692a4'
              },
              emphasis: {
                  areaColor: '#0b1c2d'
              }
          }
      },
      series: series
        }
        mChart.setOption(options)
        console.log('设置已经完成了');
      } 
      
         
  </script>
  
  <style lang="scss" scoped>
  
  </style>