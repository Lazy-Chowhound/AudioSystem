package szp.audio.audio_java.Controller;

import com.alibaba.fastjson.JSONObject;
import org.apache.xmlrpc.XmlRpcException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import szp.audio.audio_java.Rpc.RpcUtil;
import szp.audio.audio_java.Util.Result;
import szp.audio.audio_java.Util.StatusCode;

/**
 * @author Nakano Miku
 */

@RestController
public class ValidationController {

    @Autowired
    private RpcUtil rpcUtil;

    @RequestMapping("/audioSetContrastContentByPage")
    public Result getAudioSetContrastContentByPage(@RequestParam(value = "dataset") String dataset,
                                                   @RequestParam(value = "page") String page,
                                                   @RequestParam(value = "pageSize") String pageSize) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_audio_set_contrast_content_by_page",
                    dataset, page, pageSize);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
