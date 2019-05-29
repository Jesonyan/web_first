$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        const appid = $("input[name=appid]");
        const apikey = $("input[name=apikey]");
        const text = $("#tts-content").val();
        const voice_name = $("select[name=voice-name]").val();
        lfasr_ajax.post({
            'url': '/tts/',
            'data': {
                'appid': appid.val(),
                'apikey': apikey.val(),
                'text': text,
                'voice_name': voice_name
            },
            'success': function (data) {
                if (data['code'] === 200 ) {
                    // bbs_alert.alertInfoSuccess("参数上传成功，正在合成");
                    $("#gg").click();
                } else {
                    console.log(data["message"]);
                    bbs_alert.alertInfoError(data["message"] || "参数上传失败，请联系孟岩或重试！")
                }
            },
            'fail': function () {
                bbs_alert.alertNetworkError()
            }
        })
    })
});