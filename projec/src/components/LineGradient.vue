<template>
  <body style="height: 100%; margin: 0">
  <div ref="container" style="height: 100%" class="pannel"></div>
  <div class="left-up-tangle"></div>
  <div class="right-up-tangle"></div>
  <div class="left-bottom-tangle"></div>
  <div class="right-bottom-tangle"></div>
  </body>
</template>

<script setup>
  import * as echarts from 'echarts'
  import {onMounted, ref} from "vue";
  import axios from 'axios'

  let option;
  let mChart = null
  const container = ref(null)
  
  let data = ref(null)
  let data2 = ref(null)
  onMounted(() => {
    mChart = echarts.init(container.value, null, {
      renderer: 'canvas',
      useDirtyRect: false
    })
    axios.get("http://localhost:8001/getTwo_week").then(res=>{
      data.value = res.data
      console.log(data.value)

      axios.get("http://localhost:8001/getOne_week").then(res=>{
         data2.value = res.data
         renderChart()
      })
    
    })

   

  })
  const renderChart = () => {
    // if(!data.value)return
    console.log('data', data.value)
    const dateList = data.value.map(function (item) {
      return item.name;
    });
    const valueList = data.value.map(function (item) {
      return item.value;
    });

    const dateList2 = data2.value.map(function (item) {
      return item.name;
    });
    const valueList2 = data2.value.map(function (item) {
      return item.value;
    });

    option = {
      // Make gradient line here
      visualMap: [
        {
          show: false,
          type: 'continuous',
          seriesIndex: 0,
          min: 0,
          max: 400
        },
        {
          show: false,
          type: 'continuous',
          seriesIndex: 1,
          dimension: 0,
          min: 0,
          max: dateList.length - 1
        }
      ],
      title: [
        {
          left: 'center',
          text: '第一周流量数据',
          textStyle:{
            color:'#ffffff',
            fontWeight: 'normal',
            lineHeight: 30
          }
        },
        {
          top: '55%',
          left: 'center',
          text: '第二周流量数据',
          textStyle:{
            color:'#ffffff',
            fontWeight: 'normal',
            lineHeight: 10
          }
        },
      ],
      tooltip: {
        trigger: 'axis',
        textStyle:{
          color: 'white'
        }
      },
      xAxis: [
        {
          data: dateList,
          axisLine: {
            lineStyle: {
              color: 'white' // X轴颜色
            },
          }
        },
        {
          data: dateList2,
          gridIndex: 1,
          axisLine: {
            lineStyle: {
              color: 'white' // X轴颜色
            }
        },
        axisLabel:{
          color:'white'
        }
      }
      ],
      yAxis: [
        {
          axisLine: {
            lineStyle: {
              color: 'white' // Y轴颜色
            }
          },
          axisLabel: {
            color: 'white' // Y轴文本颜色
          }
        },
        {
          gridIndex: 1,
          axisLine: {
            lineStyle: {
              color: 'white' // Y轴颜色
            }
          },
          axisLabel: {
            color: 'white' // Y轴文本颜色
          }
        },
        
      ],
      grid: [
        {
          bottom: '60%'
        },
        {
          top: '60%'
        }
      ],
      series: [
        {
          type: 'line',
          showSymbol: false,
          data: valueList
        },
        {
          type: 'line',
          showSymbol: false,
          data: valueList2,
          xAxisIndex: 1,
          yAxisIndex: 1
        }
      ]
    };

    if (option && typeof option === 'object') {
      mChart.setOption(option);
    }

    window.addEventListener('resize', mChart.resize);
  }

  

</script>

<style scoped lang="scss">

</style>