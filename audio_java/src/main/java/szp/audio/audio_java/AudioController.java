package szp.audio.audio_java;

import org.apache.xmlrpc.XmlRpcException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Nakano Miku
 */
@RestController
public class AudioController {

    @Autowired
    private RpcUtil rpcUtil;

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
}
