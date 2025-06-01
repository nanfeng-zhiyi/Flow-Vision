<template>
  <div v-if="data"
    class="bg-[url('assets/imgs/bg.png')] bg-cover bg-scroll bg-center h-screen text-white p-2 flex overflow-hidden">
    <!-- 左 -->
    <div class="flex-1 mr-2 bg-opacity-5 bg-blue-600 p-3 flex flex-col">
      <div style="text-align: center; font-size: 18px;">高速流量峰值</div>
      <div class="flex h-1/3 flex-row justify-center" style="transform: translateY(-4vh)">
        <!-- 两个仪表盘 -->
        <Gauged class="w-1/2 box-border" name="平峰期"></Gauged>
        <Gauge class="w-1/2 box-border" name="高峰期"  style="transform: translateY(-0.5vh)"></Gauge>
      </div>
      <!-- 雷达图 -->
      <RadarBar class="h-1/3 box-border pb-4" :data="riskData" style="transform: translateY(-5vh)"></RadarBar>
      <!-- 横向柱状图 -->
      <HorizontalBar class="h-1/3 box-border pb-4" :data="data" style="transform: translateY(-0.5vh)"></HorizontalBar>
    </div>
    <!-- 中 -->
    <div class="w-1/2 mr-2 flex flex-col">
      <div class="title-bar"></div>
      <div style="font-size:25px; text-align: center; z-index: 100; transform: translateY(-2vh); color: #fff8f8" class="title" @click="goBaidu">FlowVision高速流量洞察可视化平台</div>
      <!-- 数据总览图 -->
      <!-- <TotalData class="bg-opacity-5 bg-blue-500 p-3" :data="totaldata"></TotalData> -->
      <!-- 地图可视化 -->
      <!-- <button @click="goBaidu">全国省份地图动态浏览</button> -->
      <MapChart class="bg-opacity-5 bg-blue-500 p-3 mt-2 flex-1" :data="mapdata"></MapChart>
    </div>
    <!-- 右 -->
    <div class="flex-1 bg-opacity-5 bg-blue-600 p-3 flex flex-col">
      <PieBorderRadius class="h-1/3 box-border pb-4"></PieBorderRadius>
      <!-- 竖向柱状图 -->
      <!-- 环形图 -->
      <VerticalBar class="h-1/3 box-border pb-4" :data="vedata" style="transform: translateY(-3vh)"></VerticalBar>
      <!-- <RingBar class="h-1/3 box-border pb-4" :data="abndata" style="transform: translateY(0.5vh)"></RingBar>
       -->
      <trafficFlow class="h-1/3"></trafficFlow>

  </div>
  </div>
</template>
<script setup>

  import HorizontalBar from '@/components/HorizontalBar.vue'
  import RadarBar from '@/components/RadarBar.vue'
  import MapChart from '@/components/MapChart.vue'
  import VerticalBar from '@/components/VerticalBar.vue'
  import router from '@/router'
  import getData from '../api/requestApi.js'
  import PieBorderRadius from '../components/PieBorderRadius.vue'
  import Gauge from '../components/Gauge.vue'
  import trafficFlow from '../components/trafficFlow.vue'
  import Gauged from '../components/Gauged.vue'

  // import WordCloud from '@/components/WordCloud.vue'
// 这里的数据使用动态请求实现动态性

// let res = 0
getData().then(ans=>{
  console.log(ans)
})

  let data = {
     regions:[
      {name: '分类1', value: 35},
      {name: '分类1', value: 12},
      {name: '分类1', value: 95},
      {name: '分类2', value: 65},
      {name: '分类2', value: 65},
      {name: '分类2', value: 65},
    ]
  }

let mapdata = {
// 时间轴数据，表示不同的年份或其他分类
voltageLevel: ['2019', '2020', '2021'],

// 每个年份或分类下的具体数据
categoryData: {
  '2019': [
    { name: '分类1', value: 10 },
    { name: '分类2', value: 20 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    { name: '分类2', value: 20 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    { name: '分类1', value: 5 },
    { name: '分类2', value: 30 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    { name: '分类2', value: 20 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
  
    
    // 更多分类数据...
  ],
  '2020': [
    { name: '分类1', value: 15 },
    { name: '分类2', value: 25 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    { name: '分类2', value: 20 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    { name: '分类1', value: 5 },
    { name: '分类2', value: 30 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    { name: '分类2', value: 20 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    // 更多分类数据...
  ],
  '2021': [
    { name: '分类1', value: 5 },
    { name: '分类2', value: 30 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    { name: '分类2', value: 20 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    { name: '分类1', value: 5 },
    { name: '分类2', value: 30 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    { name: '分类2', value: 20 },
    { name: '分类3', value: 10 },
    { name: '分类4', value: 20 },
    // 更多分类数据...
  ]
  // 对应其他年份或分类...
},

// 地图上的散点数据，可选
topData: {
  '2019': [
    { name: '地点A', value: [46, 24, 10] },
    { name: '地点A', value: [46, 24, 10] },
    { name: '地点A', value: [46, 24, 10] },
    { name: '地点A', value: [46, 24, 10] },
    { name: '地点A', value: [46, 24, 10] },
    
    // 更多散点数据...
  ],
  // 对应其他年份或分类的散点数据...
},

// 用于不同数据系列的颜色
colors: ['#ff0000', '#00ff00', '#0000ff']
};


const goBaidu = ()=>{
router.push('/home')
}



</script>
<style lang="scss" scoped>
  div {
    letter-spacing: 3px
  }
  .title {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
    padding: 20px;
    color: transparent;
    background: linear-gradient(45deg, #a1c4fd, #c2e9fb);
    -webkit-background-clip: text;
    background-clip: text;
    text-shadow: 3px 3px 3px rgba(0,0,0,0.2);
  }
  .title-bar {
    background-image: url("@/assets/imgs/2.svg");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 260%;
    position: absolute;
    width: 50%;
    height: 15vh;
    left: calc(50% - 50% / 2);
    top: -2.5vh;
    z-index: 1;
  }
</style>