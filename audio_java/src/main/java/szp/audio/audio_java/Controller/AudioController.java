package szp.audio.audio_java.Controller;

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
public class AudioController {

    @Autowired
    private RpcUtil rpcUtil;

    /**
     * 获取音频数据集列表
     */
    @RequestMapping("/audioSetList")
    public Result getAudioSetList(@RequestParam(value = "path") String path) {
        try {
            return Result.success(StatusCode.SUCCESS.getStatus(), rpcUtil.sendRequest("getAudioSetList", path));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取音频数据集属性
     */
    @RequestMapping("/audioSetDescription")
    public Result getAudioSetDescription() {
        try {
            return Result.success(StatusCode.SUCCESS.getStatus(), rpcUtil.sendRequest("getAudioSet"));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取音频属性
     */
    @RequestMapping("/audioDescription")
    public Result getAudioDescription(@RequestParam(value = "audioSet") String audioSet,
                                      @RequestParam(value = "page") String page,
                                      @RequestParam(value = "pageSize") String pageSize) {
        try {
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    rpcUtil.sendRequest("getAudio", audioSet, page, pageSize));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取波形图
     */
    @RequestMapping("/getWaveForm")
    public Result getAudioWaveForm(@RequestParam(value = "audioSet") String audioSet,
                                   @RequestParam(value = "audioName") String audioName) {
        try {
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    rpcUtil.sendRequest("getWaveForm", audioSet, audioName));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取 Mel 频谱图
     */
    @RequestMapping("/getMelSpectrum")
    public Result getMelSpectrum(@RequestParam(value = "audioSet") String audioSet,
                                 @RequestParam(value = "audioName") String audioName) {
        try {
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    rpcUtil.sendRequest("getMelSpectrum", audioSet, audioName));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    @RequestMapping("/removeImage")
    public Result removeImage(@RequestParam(value = "path") String path) {
        try {
            return Result.success(StatusCode.SUCCESS.getStatus(), rpcUtil.sendRequest("removeImage", path));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
