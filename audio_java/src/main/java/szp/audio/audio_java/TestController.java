package szp.audio.audio_java;

import org.apache.xmlrpc.XmlRpcException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Nakano Miku
 */
@RestController
public class TestController {

    @Autowired
    private RpcUtil rpcUtil;

    @RequestMapping("/test")
    public Result test() {
        return Result.success(StatusCode.SUCCESS.getStatus(), 1);
    }

    @RequestMapping("/rpc")
    public Result get() {
        try {
            return Result.success(StatusCode.SUCCESS.getStatus(), rpcUtil.sendRequest("getTSum", "5", "6", "7"));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
