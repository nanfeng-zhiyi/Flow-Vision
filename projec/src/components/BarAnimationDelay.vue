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
  
  onMounted(() => {
    mChart = echarts.init(container.value)
    window.addEventListener('resize', mChart.resize);
  })
  
  let xAxisData = ref([])
  
  let week1 = ref(null)
  let week2 = ref(null)
  const getRes = async () => {
  try {
    // 使用 async-await 确保请求完成后再继续
    const response = await axios.get("http://localhost:8001/getres");
    // 确保响应有效且有数据
    if (response && response.data) {
      console.log("获取数据成功: ", response.data);
      // xAxisData.value.push(2); // 假设这里的逻辑是基于获取的数据
      week1.value = response.data['1']
      week2.value = response.data['2']
      // console.log(week1.value)
      console.log('responseData',response.data)
      renderChart(); // 更新图表应该在确认有新数据后调用

    } else {
      console.error("未获取到有效数据");
      return null; // 明确返回 null 表示没有数据
    }
  } catch (error) {
    console.error("请求数据失败: ", error);
    return null; // 出错时返回 null
  }
};

  defineExpose({getRes})
   


  function renderChart() {
    // let xAxisData = []; 
    let data1 = [];
    let data2 = [];
    for (let i = 1; i < 8; i++) {
      xAxisData.value.push(i)
      console.log('week1', week1)
     if(week1.value)
     {
       data1.push(week1.value[i - 1]);
      data2.push(week2.value[i - 1]);
      console.log(week1.value)
     }
     
    }
    option = {
      title: {
        text: '预测结果展示',
        textStyle: {
          color: '#FFFFFF'
        },
      },

      legend: {
        data: ['week1', 'week2'],
        textStyle: {
          color: '#FFFFFF'
        }
      },
      toolbox: {
        // y: 'bottom',
        feature: {
          magicType: {
            type: ['stack']
          },
          dataView: {},
          saveAsImage: {
            pixelRatio: 2
          }
        }
      },
      tooltip: {},
      xAxis: {
        data: xAxisData.value,
        splitLine: {
          show: false
        },
        axisLabel:{
          color:'#FFFFFF'
        }
      },
      yAxis: {
        axisLabel:{
          color: '#FFFFFF'
        }
      },
      series: [
        {
          name: 'week1',
          type: 'bar',
          data: data1,
          emphasis: {
            focus: 'series'
          },
          animationDelay: function (idx) {
            return idx * 10;
          },
          itemStyle:{
            color: '#FFFFFF'
          }
        },
        {
          name: 'week2',
          right: 2,
          type: 'bar',
          data: data2,
          emphasis: {
            focus: 'series'
          },
          animationDelay: function (idx) {
            return idx * 10 + 100;
          }
        }
      ],
      animationEasing: 'elasticOut',
      animationDelayUpdate: function (idx) {
        return idx * 5;
      }
    };
    mChart.setOption(option)
    // mChart.resize()
    // window.addEventListener('resize', mChart.resize);

  }

</script>

<style scoped>
/* .pannel{
  backdrop-filter: blur(100px);
} */

</style>