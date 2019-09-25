import axios from 'axios'

// 分装axios请求
export function send(url,type,data){
    var d=new FormData()
    for (var key in data){
        d.append(key,data[key])
    }
    return axios({
        url:url,
        method:type,
        data:d,

    })
}