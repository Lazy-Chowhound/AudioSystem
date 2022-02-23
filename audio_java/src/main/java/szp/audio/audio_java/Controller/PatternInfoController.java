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
public class PatternInfoController {

    @Autowired
    private RpcUtil rpcUtil;

    /**
     * 获取扰动概况
     */
    @RequestMapping("/patternSummary")
    public Result getPatternSummary(@RequestParam(value = "dataset") String dataset) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_pattern_summary", dataset);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONObject("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取扰动详情
     */
    @RequestMapping("/patternTypeSummary")
    public Result getPatternTypeSummary(@RequestParam(value = "dataset") String dataset,
                                        @RequestParam(value = "pattern") String pattern) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_pattern_type_summary", dataset, pattern);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONObject("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
