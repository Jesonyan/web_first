// $(function () {
//     $("#submit").click(function (event) {
//         event.preventDefault();
//
//         let appid = $("input[name=appid]");
//         let apikey = $("input[name=apikey]");
//
//
//         let appid_val = appid.val();
//         let apikey_val = apikey.val();
//         let files = new FormData($("#upload_file")[0]);
//
//         lfasr_ajax.post({
//             'url': '/',
//             async: true,
//             cache: false,
//             contentType: false,
//             processData:false,
//             'data':{
//                 'appid':appid_val,
//                 'apikey':apikey,
//                 'files':files
//             },
//             'success': function (data) {
//                 if (data["code"] === 200) {
//                     bbs_alert.alertInfoSuccess(msg = data["message"])
//                 } else {
//                     bbs_alert.alertInfoError(msg = data["message"])
//                 }
//             },
//             'fail': function () {
//                 bbs_alert.alertNetworkError()
//             }
//         })
//
//     })
// });