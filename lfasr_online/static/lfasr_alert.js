let bbs_alert = {
    /*
    功能：修改成功提示信息
    参数:
         - msg：可选
    */
    'alertInfoSuccess': function (msg) {
        swal({
            title: '提示',
            text: msg,
            type: 'success',
            timer: 2000,
            showConfirmButton: 'false'
        })
    },
    /*
    功能：修改失败提示信息
    参数:
         - msg：可选
    */
    'alertInfoError': function (msg) {
        swal({
            title: '提示',
            text: msg,
            type: 'error',
            timer: 2000,
            showConfirmButton: 'false'
        })
    },
    /*
    功能：网络错误
    参数:
         - msg：可选
    */
    'alertNetworkError': function () {
        swal('提示', '网络错误', 'error')
    }
};