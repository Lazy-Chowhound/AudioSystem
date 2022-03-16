package szp.audio.audio_java.Controller;

import com.alibaba.fastjson.JSONObject;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresAuthentication;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.apache.xmlrpc.XmlRpcException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import szp.audio.audio_java.Rpc.RpcUtil;
import szp.audio.audio_java.ShiroConfig.ShiroUtil;
import szp.audio.audio_java.Util.Result;
import szp.audio.audio_java.Util.StatusCode;

/**
 * @author Nakano Miku
 */
@RestController
public class PatternInfoController {

    @Autowired
    private RpcUtil rpcUtil;

    @Autowired
    private ShiroUtil shiroUtil;

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
    @RequiresAuthentication
    @RequiresPermissions("B:SELECT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/patternTypeSummary")
    public Result getPatternTypeSummary(@RequestHeader("Authorization") String token,
                                        @RequestParam(value = "dataset") String dataset,
                                        @RequestParam(value = "pattern") String pattern) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_pattern_type_summary", dataset, pattern);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONObject("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
