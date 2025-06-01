<template>
  <div id="all" class="bg-cover bg-scroll bg-center h-screen text-white p-2 flex overflow-hidden">
    <div id="left" class="w-1/3">
      <div class="h-1/2 mb-4" style="width: 100%; transform: translateY(-5px)">
        <LineGradient style="width: 100%; height: 200%"></LineGradient>

      </div>
      <div class="h-1/2 flex flex-col justify-center" style="width: 100%; transform: translateY(-10px)">

      </div>
    </div>
    <div id="middle" class="w-1/3 flex flex-col ml-2 mr-2">
      <!-- <div class="h-1/5" style="text-align: center;">{{ name }}详细信息可视化</div> -->
      <!-- <div ref="target" class="w-full h-4/5  flex flec-row justify-center items-center px-4 py-2 rounded-lg"></div> -->
      <div class="w-full h-3/5">
        <HotMap :data="hot_data" class="h-3/5 w-full"></HotMap>
      </div>

      <div class="w-full h-2/5 flex flex-col justify-center">
        <div class="flex flex-col items-center mb-4">
          <!-- <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
         </svg> -->
          <el-button id="submit" style="width: 110px; height: 50px" v-bind:loading="!!upload_loading"
                     v-bind:type="bt_type"
                     @click="() => {
                       if (bt_name === '提交文件') {
                         openFileSelector()
                       } else if (bt_name === '查看结果') {
                         bt_name = '提交文件'
                         bt_type = 'primary'
                         showRes()
                       }
                     }">
            {{ bt_name }}
          </el-button>
          <input ref="fileInput" multiple style="display: none" type="file" @change="handleFileChange">
          <div style="transform: translateY(2vh); font-size: 18px;">提交文件我们后端的模型会帮您预测</div>
        </div>
        <!-- <button class= " mx-auto bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded " @click="showRes">
             查看结果
          </button> -->
      </div>

    </div>
    <div class="w-1/3">
      <div :class="{'items-center': loading_show1}" class="h-1/2 mb-4 flex flex-col justify-center"
           style="width: 100%; transform: translateY(-5px)">
        <LineRace v-show="lin_show" style="width: 100%; height: 100%"></LineRace>
        <loading v-show="loading_show1"></loading>
      </div>
      <div :class="{'items-center': loading_show2}" class="h-1/2 flex flex-col justify-center"
           style="width: 100%; transform: translateY(-10px) ">
        <BarAnimationDelay v-show="bar_show" ref="barAnimationDely"></BarAnimationDelay>
        <loading v-show="loading_show2"></loading>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from "vue";
import {useRoute} from "vue-router"
import LineRace from '../components/LineRace.vue'
import LineGradient from '../components/LineGradient.vue'
import BarAnimationDelay from '../components/BarAnimationDelay.vue'
import HotMap from '../components/HotMap.vue'
import getFlowData from '../api/requestApi'
import axios from 'axios'
import loading from '../components/loading.vue'
import roadLength from '@/assets/mapData/roadLength.json'
import province from '@/assets/mapData/province.json'
import 'element-plus/dist/index.css'
import {ElButton, ElMessage} from 'element-plus'


let bt_name = ref("提交文件")
let bt_type = ref("primary")
let upload_loading = ref(false)

const route = useRoute();
let name = ref(route.query.province)

let province_name = ref(route.query.province)
let bar_show = ref(true)
let lin_show = ref(true)
let loading_show1 = ref(false)
let loading_show2 = ref(false)
console.log(province_name.value)

// let hot_data = ref([])
let cities = ref([])

// const province = province.find(p=>p.name == province.name)

console.log(province)

// 这里要将数据填充到相应的renderchart中
const provinceObject = province.find(p => p.name == province_name.value).city

if (provinceObject) {
  cities.value = provinceObject.map(item => item.name)
} else {
  cities.value = []
}

// console.log('cities1111111111111111111111111111',cities.value)
let hot_data = ref([])

for (let i = 0; i < cities.value.length; ++i) {
  const cityInfo = roadLength.find(item => item.name === cities.value[i]);
  const cityValue = cityInfo ? cityInfo.value : 0;  // 如果找不到对应城市，则默认值为0

  hot_data.value.push({
    'name': cities.value[i],
    'value': cityValue
  });
}
hot_data.value.push({'province': name})


console.log('djskljflksdjklfjlskdjfl', hot_data.value);


// let mapJson = null

// onMounted(()=>{
// mapJson = require('@/assets/mapData/' +  '新疆' + '.json')
// let data = ref(null)
// getFlowData().then(res=>{
//   data = res
// })
// console.log("daoluliuliangshuju ",data)
// })
// console.log(name)

// let mChart = null
// const target = ref(null)
const barAnimationDely = ref(null)

// onMounted(()=>{
//  echarts.registerMap(name.value, mapJson)
//  mChart = echarts.init(target.value)
//  renderChart()
// })
const showRes = async () => {
  if (barAnimationDely.value) {
    loading_show2.value = true; // 开始加载数据
    bar_show.value = false
    const resData = await barAnimationDely.value.getRes();
    setTimeout(async () => {
      if (resData !== null) {
        console.log('获取的结果: ', resData);
        bar_show.value = true;
        console.log('hello worls')
      } else {
        console.error("未能加载数据");
      }
      loading_show2.value = false;
      // bar_show.value = false
      console.log('loading_show2.value', loading_show2.value)
      console.log('bar_show.value', bar_show.value)
    }, 5000);

  }
}


const fileInput = ref(null)

const openFileSelector = () => {
// 打开文件选择器
  fileInput.value.click();
}

// 提交文件
const handleFileChange = (e) => {
  // 处理文件选择变化事件
  const files = e.target.files;
  if (files.length > 0) {
    const formData = new FormData();
    // formData.append("file", file);
    for (const file of files) {
      formData.append("files[]", file)
    }

    upload_loading.value = true
    bt_name.value = "正在分析文件"

    // 发送文件到后端

    axios.post("http://localhost:8088/store/storefile", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
    })
        .then(response => {
          if (response.status === 200) {
            bt_name.value = "查看结果"
            bt_type.value = "success"
            upload_loading.value = false
            console.log("文件上传成功");
            ElMessage({
              message: "文件上传成功",
              type: "success",
            })
          } else {
            ElMessage({
              message: "文件上传失败",
              type: "error",
            })
          }
        }).catch(error => {
      ElMessage({
        message: "文件上传失败",
        type: "error",
      })
      console.log(error)
      upload_loading.value = false
      bt_name.value = "提交文件"
    })
        .catch(error => {
          console.error("上传过程中发生错误", error);
        });
  } else {
    console.error("未选择文件");
    upload_loading = false
  }
}


// const renderChart = () => {
//       const options = {
//          tooltip: {
//           trigger: 'item',
//           formatter: '{b}'
//          },
//          series: [
//            {
//             type: 'map',
//             map: name.value, // 使用注册的地图
//             label: {
//              show: true
//            }
//           },
//           {
//            itemStyle:{
//             normal: {
//               borderColor: 'rgba(147,235,248,1)',
//               borderWidth: 1,
//               areaColor: {
//                 type: 'radial',
//                 x: 0.5,
//                 y: 0.5,
//                 r: 0.5,
//                 colorStops: [{
//                   offset: 0,
//                   color: 'rgba(147,235,248,0)',
//                 }, {
//                   offset: 1,
//                   color: 'rgba(147,235,248,.2)',
//                 }]
//               }
//             },
//           },
//           emphasis: {
//               areaColor: '#389bb7',
//               borderWidth: 0,
//             },
//           }
//          ]
//       }
//       mChart.setOption(options)
// }

getFlowData().then(res => {
  console.log(res)
})


// const renderChart = ()=>{
//  const options = {
//      geo: {
//        show: true,
//        map: name.value, 
//        roam: true,
//        zoom: 0.8,
//        itemStyle: {
//         normal: {
//             borderColor: 'rgba(147,235,248,1)',
//             borderWidth: 1,
//             areaColor: {
//               type: 'radial',
//               x: 0.5,
//               y: 0.5,
//               r: 0.5,
//               colorStops: [{
//                 offset: 0,
//                 color: 'rgba(147,235,248,0)',
//               }, {
//                 offset: 1,
//                 color: 'rgba(147,235,248,.2)',
//               }]
//             }
//           },
//           emphasis: {
//             areaColor: '#389bb7',
//             borderWidth: 0,
//           },
//        }
//      },
//  }
//  mChart.setOption(options)
// }

</script>

<style lang="scss" scoped>
#all {
  background-image: url('@/assets/imgs/bg_2.png');
  // background-color: black;
  background-position: center center;
  overflow: hidden;
  background-repeat: no-repeat;
}
div {
  letter-spacing: 3px
}

</style>

<style>
.left-up-tangle {
  position: relative;
  left: 0;
  top: -100%;
  width: 20px;
  height: 20px;
  border-top: #ffffff solid 2px;
  border-left: #ffffff solid 2px;
}

.right-up-tangle {
  position: relative;
  left: calc(100% - 20px);
  top: calc(-100% - 20px);
  width: 20px;
  height: 20px;
  border-top: #ffffff solid 2px;
  border-right: #ffffff solid 2px;
}

.left-bottom-tangle {
  position: relative;
  top: -60px;
  left: 0;
  width: 20px;
  height: 20px;
  border-bottom: #ffffff solid 2px;
  border-left: #ffffff solid 2px;
}

.right-bottom-tangle {
  position: relative;
  left: calc(100% - 20px);
  top: -80px;
  width: 20px;
  height: 20px;
  border-bottom: #ffffff solid 2px;
  border-right: #ffffff solid 2px;
}

el-button {
  position: absolute;
  width: 250px;
  height: 150px;
}
</style>