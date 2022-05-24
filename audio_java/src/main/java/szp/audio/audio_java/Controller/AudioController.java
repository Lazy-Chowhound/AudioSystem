package szp.audio.audio_java.Controller;

import com.alibaba.fastjson.JSONObject;
import org.apache.shiro.SecurityUtils;
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
import szp.audio.audio_java.Entity.User;
import szp.audio.audio_java.Rpc.RpcUtil;
import szp.audio.audio_java.Util.Result;
import szp.audio.audio_java.ShiroConfig.ShiroUtil;
import szp.audio.audio_java.Util.StatusCode;

/**
 * @author Nakano Miku
 */
@RestController
public class AudioController {

    @Autowired
    private RpcUtil rpcUtil;

    @Autowired
    private ShiroUtil shiroUtil;

    /**
     * 获取音频数据集列表
     */
    @RequiresAuthentication
    @RequiresRoles(value = {"ROOT", "USER", "VISITOR"}, logical = Logical.OR)
    @RequestMapping("/audioSetsList")
    public Result getAudioSetsList(@RequestHeader("Authorization") String token) {
        shiroUtil.verifyUserToken(token);
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_audio_sets_list", userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取音频数据集属性
     */
    @RequiresAuthentication
    @RequiresRoles(value = {"ROOT", "USER", "VISITOR"}, logical = Logical.OR)
    @RequestMapping("/audioSetsProperties")
    public Result getAudioSetsProperties(@RequestHeader("Authorization") String token) {
        shiroUtil.verifyUserToken(token);
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_audio_sets_properties", userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取音频列表和属性
     */
    @RequiresAuthentication
    @RequiresPermissions("A:SELECT")
    @RequiresRoles(value = {"ROOT", "USER", "VISITOR"}, logical = Logical.OR)
    @RequestMapping("/audioClipsPropertiesByPage")
    public Result getAudioClipsPropertiesByPage(@RequestHeader("Authorization") String token,
                                                @RequestParam(value = "audioSet") String dataset,
                                                @RequestParam(value = "page") String page,
                                                @RequestParam(value = "pageSize") String pageSize) {

        shiroUtil.verifyUserToken(token);
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_audio_clips_properties_by_page",
                    dataset, page, pageSize);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取波形图
     */
    @RequiresAuthentication
    @RequiresPermissions("A:SELECT")
    @RequiresRoles(value = {"ROOT", "USER", "VISITOR"}, logical = Logical.OR)
    @RequestMapping("/waveFormGraph")
    public Result getWaveFormGraph(@RequestHeader("Authorization") String token,
                                   @RequestParam(value = "audioSet") String audioSet,
                                   @RequestParam(value = "audioName") String audioName) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_waveform_graph", audioSet, audioName);
            return Result.success(StatusCode.SUCCESS.getStatus(), jsonObject.getString("data"));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取 Mel 频谱图
     */
    @RequiresAuthentication
    @RequiresPermissions("A:SELECT")
    @RequiresRoles(value = {"ROOT", "USER", "VISITOR"}, logical = Logical.OR)
    @RequestMapping("/melSpectrum")
    public Result getMelSpectrum(@RequestHeader("Authorization") String token,
                                 @RequestParam(value = "audioSet") String audioSet,
                                 @RequestParam(value = "audioName") String audioName) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_mel_spectrum", audioSet, audioName);
            return Result.success(StatusCode.SUCCESS.getStatus(), jsonObject.getString("data"));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 属性图前后对比
     */
    @RequiresAuthentication
    @RequiresPermissions("A:SELECT")
    @RequiresRoles(value = {"ROOT", "USER", "VISITOR"}, logical = Logical.OR)
    @RequestMapping("/propertyContrast")
    public Result propertyContrast(@RequestHeader("Authorization") String token,
                                 @RequestParam(value = "audioSet") String audioSet,
                                 @RequestParam(value = "audioName") String audioName) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_contrast_graph", audioSet, audioName);
            return Result.success(StatusCode.SUCCESS.getStatus(), jsonObject.getString("data"));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    @RequestMapping("/removeImage")
    public Result removeImage(@RequestParam(value = "path") String path) {
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("remove_image", path);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    jsonObject.getString("data"));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }
}
