import request from '@/utils/request.js'

// 获取相应的实时数据
export const getVisualization = () => {
  return request({
    url: '/visualization',
  })
}
