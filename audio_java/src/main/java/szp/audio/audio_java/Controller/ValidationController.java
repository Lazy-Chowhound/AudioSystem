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

    /**
     * 获取已有模型
     */
    @RequestMapping("/models")
    public Result getModels() {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_models");
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 按夜获取验证结果
     */
    @RequestMapping("/validationResultsByPage")
    public Result getValidationResultsByPage(@RequestParam(value = "audioSet") String dataset,
                                             @RequestParam(value = "model") String modelName,
                                             @RequestParam(value = "page") String page,
                                             @RequestParam(value = "pageSize") String pageSize) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_validation_results_by_page",
                    dataset, modelName, page, pageSize);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
