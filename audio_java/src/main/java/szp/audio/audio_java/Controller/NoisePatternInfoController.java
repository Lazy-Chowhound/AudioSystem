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
public class NoisePatternInfoController {

    @Autowired
    private RpcUtil rpcUtil;

    /**
     * 获取扰动概况
     */
    @RequestMapping("/noisePatternSummary")
    public Result getNoisePatternSummary(@RequestParam(value = "dataset") String dataset) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("getNoisePatternSummary", dataset);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONObject("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取扰动详情
     */
    @RequestMapping("/noisePatternDetail")
    public Result getNoisePatternDetail(@RequestParam(value = "dataset") String dataset,
                                        @RequestParam(value = "patternType") String patternType) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("getNoisePatternDetail", dataset, patternType);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONObject("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取某数据集所有音频扰动情况
     */
    @RequestMapping("/audioSetPattern")
    public Result getAudioSetPattern(@RequestParam(value = "dataset") String dataset) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("getAudioSetPattern", dataset);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
