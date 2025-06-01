// used to connect front and back

import axios from 'axios'

// const url = 'http://127.0.0.1'

// 测试链接
const getData = async ()=> {
    const res = await axios.get("http://127.0.0.1:8088/test/test1")
    return res.data
}

// 测试数据链接
export const getFlowData = async() => {
    const res = await axios.get("http://localhost:8001/test")
    console.log(res.data)
    return res.data
}


export default getData
