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
public class NoisePatternController {

    @Autowired
    private RpcUtil rpcUtil;

    /**
     * 添加高斯白噪声
     */
    @RequestMapping("/addGaussianNoise")
    public Result addGaussianWhiteNoise(@RequestParam(value = "dataset") String dataset,
                                        @RequestParam(value = "audioName") String audioName) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    rpcUtil.sendRequest("add_gaussian_noise", path, audioName));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Sound level 扰动
     */
    @RequestMapping("/addSoundLevel")
    public Result addSoundLevel(@RequestParam(value = "dataset") String dataset,
                                @RequestParam(value = "audioName") String audioName,
                                @RequestParam(value = "specificPattern") String specificPattern) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    rpcUtil.sendRequest("add_natural_sounds", path, audioName, specificPattern));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
