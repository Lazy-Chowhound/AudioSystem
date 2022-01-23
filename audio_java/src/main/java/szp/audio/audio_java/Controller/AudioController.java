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
public class AudioController {

    @Autowired
    private RpcUtil rpcUtil;

    /**
     * 获取音频数据集列表
     */
    @RequestMapping("/audioSetList")
    public Result getAudioSetList(@RequestParam(value = "path") String path) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("getAudioSetList", path);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
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
            JSONObject jsonObject = rpcUtil.sendRequest("getAudioSet");
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
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
            JSONObject jsonObject = rpcUtil.sendRequest("getAudio", audioSet, page, pageSize);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
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
            JSONObject jsonObject = rpcUtil.sendRequest("getWaveForm", audioSet, audioName);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    jsonObject.getString("data"));
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
            JSONObject jsonObject = rpcUtil.sendRequest("getMelSpectrum", audioSet, audioName);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getString("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    @RequestMapping("/removeImage")
    public Result removeImage(@RequestParam(value = "path") String path) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("removeImage", path);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    jsonObject.getString("data"));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
