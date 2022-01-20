package szp.audio.audio_java;

import org.apache.xmlrpc.XmlRpcException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Nakano Miku
 */
@RestController
public class NoisePatternController {

    @Autowired
    private RpcUtil rpcUtil;

    /**
     * 获取扰动概况
     */
    @RequestMapping("/noisePatternSummary")
    public Result getNoisePatternSummary(@RequestParam(value = "dataset") String dataset) {
        try {
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    rpcUtil.sendRequest("getNoisePatternSummary", dataset));
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
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    rpcUtil.sendRequest("getNoisePatternDetail", dataset, patternType));
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
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    rpcUtil.sendRequest("getAudioSetPattern", dataset));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    @RequestMapping("/test")
    public Result test() throws InterruptedException {
        Thread.sleep(2000);
        return Result.success(StatusCode.SUCCESS.getStatus(), "test");
    }
}
