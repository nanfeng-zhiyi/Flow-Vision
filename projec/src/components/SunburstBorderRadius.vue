<template>
  <body style="height: 100%; margin: 0">
    <div>[旭日图]</div>
  <div ref="container" style="height: 100%"></div>
  </body>
</template>

<script setup>
  import * as echarts from 'echarts'
  import {onMounted, ref} from "vue";
  
  let option;
  let mChart = null
  const container = ref(null)
  
  onMounted(() => {
    mChart = echarts.init(container.value, null, {
      renderer: 'canvas',
      useDirtyRect: false
    })
    renderChart()
  })
  
  function renderChart() {
    let data = [
      {
        name: 'Grandpa',
        children: [
          {
            name: 'Uncle Leo',
            value: 15,
            children: [
              {
                name: 'Cousin Jack',
                value: 2
              },
              {
                name: 'Cousin Mary',
                value: 5,
                children: [
                  {
                    name: 'Jackson',
                    value: 2
                  }
                ]
              },
              {
                name: 'Cousin Ben',
                value: 4
              }
            ]
          },
          {
            name: 'Father',
            value: 10,
            children: [
              {
                name: 'Me',
                value: 5
              },
              {
                name: 'Brother Peter',
                value: 1
              }
            ]
          }
        ]
      },
      {
        name: 'Nancy',
        children: [
          {
            name: 'Uncle Nike',
            children: [
              {
                name: 'Cousin Betty',
                value: 1
              },
              {
                name: 'Cousin Jenny',
                value: 2
              }
            ]
          }
        ]
      }
    ];
    option = {
      series: {
        type: 'sunburst',
        data: data,
        radius: [60, '90%'],
        itemStyle: {
          borderRadius: 7,
          borderWidth: 2
        },
        label: {
          show: true
        }
      }
    };

    if (option && typeof option === 'object') {
      mChart.setOption(option);
    }

    window.addEventListener('resize', mChart.resize);
  }
</script>

<style scoped lang="scss">

</style>