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
import szp.audio.audio_java.Service.OperationService;
import szp.audio.audio_java.Util.Result;
import szp.audio.audio_java.ShiroConfig.ShiroUtil;
import szp.audio.audio_java.Util.StatusCode;

import java.util.Date;

/**
 * @author Nakano Miku
 */
@RestController
public class NoisePatternController {

    private static final String CODE = "code";

    @Autowired
    private RpcUtil rpcUtil;

    @Autowired
    private OperationService operationService;

    @Autowired
    private ShiroUtil shiroUtil;

    /**
     * 添加扰动时获取某数据集所有音频扰动情况
     */
    @RequiresAuthentication
    @RequiresPermissions("B:SELECT")
    @RequiresRoles(value = {"ROOT", "USER", "VISITOR"}, logical = Logical.OR)
    @RequestMapping("/audioClipsPattern")
    public Result getAudioClipsPattern(@RequestHeader("Authorization") String token,
                                       @RequestParam(value = "dataset") String dataset) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_audio_clips_pattern", dataset);
            return Result.success(StatusCode.SUCCESS.getStatus(),
                    JSONObject.toJSONString(jsonObject.getJSONArray("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加高斯白噪声
     */
    @RequiresAuthentication
    @RequiresPermissions(value = {"B:UPDATE", "B:DELETE"}, logical = Logical.AND)
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/addGaussianNoise")
    public Result addGaussianWhiteNoise(@RequestHeader("Authorization") String token,
                                        @RequestParam(value = "dataset") String dataset,
                                        @RequestParam(value = "audioName") String audioName,
                                        @RequestParam(value = "currentPattern") String currentPattern,
                                        @RequestParam(value = "currentPatternType") String currentPatternType,
                                        @RequestParam(value = "snr") String snr) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject response = rpcUtil.sendRequest("add_gaussian_noise", dataset, audioName,snr);
            if ((int) response.get(CODE) == StatusCode.FAIL.getCode()) {
                return Result.fail(StatusCode.FAIL.getStatus(), response.get("data"));
            }
            removeCurrentNoiseAudioClip(dataset, audioName, currentPattern, currentPatternType);
            User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
            operationService.insertOperationHistory(dataset, audioName, currentPattern + " " + currentPatternType,
                    "Gaussian noise", new Date(), userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Sound level 扰动
     */
    @RequiresAuthentication
    @RequiresPermissions(value = {"B:UPDATE", "B:DELETE"}, logical = Logical.AND)
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/addSoundLevel")
    public Result addSoundLevel(@RequestHeader("Authorization") String token,
                                @RequestParam(value = "dataset") String dataset,
                                @RequestParam(value = "audioName") String audioName,
                                @RequestParam(value = "specificPattern") String specificPattern,
                                @RequestParam(value = "currentPattern") String currentPattern,
                                @RequestParam(value = "currentPatternType", required = false) String currentPatternType) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject response = rpcUtil.sendRequest("add_sound_level", dataset, audioName, specificPattern);
            if ((int) response.get(CODE) == StatusCode.FAIL.getCode()) {
                return Result.fail(StatusCode.FAIL.getStatus(), response.get("data"));
            }
            removeCurrentNoiseAudioClip(dataset, audioName, currentPattern, currentPatternType);
            User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
            operationService.insertOperationHistory(dataset, audioName,
                    currentPattern + (currentPatternType != null ? " " + currentPatternType : ""),
                    "Sound level " + specificPattern, new Date(), userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Natural Sounds 扰动
     */
    @RequiresAuthentication
    @RequiresPermissions(value = {"B:UPDATE", "B:DELETE"}, logical = Logical.AND)
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/addNaturalSounds")
    public Result addNaturalSounds(@RequestHeader("Authorization") String token,
                                   @RequestParam(value = "dataset") String dataset,
                                   @RequestParam(value = "audioName") String audioName,
                                   @RequestParam(value = "specificPattern") String specificPattern,
                                   @RequestParam(value = "currentPattern") String currentPattern,
                                   @RequestParam(value = "currentPatternType", required = false) String currentPatternType,
                                   @RequestParam(value = "snr") String snr) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject response = rpcUtil.sendRequest("add_natural_sounds", dataset, audioName, specificPattern,snr);
            if ((int) response.get(CODE) == StatusCode.FAIL.getCode()) {
                return Result.fail(StatusCode.FAIL.getStatus(), response.get("data"));
            }
            removeCurrentNoiseAudioClip(dataset, audioName, currentPattern, currentPatternType);
            User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
            operationService.insertOperationHistory(dataset, audioName,
                    currentPattern + (currentPatternType != null ? " " + currentPatternType : ""),
                    "Natural Sounds " + specificPattern, new Date(), userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Animal 扰动
     */
    @RequiresAuthentication
    @RequiresPermissions(value = {"B:UPDATE", "B:DELETE"}, logical = Logical.AND)
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/addAnimal")
    public Result addAnimal(@RequestHeader("Authorization") String token,
                            @RequestParam(value = "dataset") String dataset,
                            @RequestParam(value = "audioName") String audioName,
                            @RequestParam(value = "specificPattern") String specificPattern,
                            @RequestParam(value = "currentPattern") String currentPattern,
                            @RequestParam(value = "currentPatternType", required = false) String currentPatternType,
                            @RequestParam(value = "snr") String snr) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject response = rpcUtil.sendRequest("add_animal", dataset, audioName, specificPattern,snr);
            if ((int) response.get(CODE) == StatusCode.FAIL.getCode()) {
                return Result.fail(StatusCode.FAIL.getStatus(), response.get("data"));
            }
            removeCurrentNoiseAudioClip(dataset, audioName, currentPattern, currentPatternType);
            User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
            operationService.insertOperationHistory(dataset, audioName,
                    currentPattern + (currentPatternType != null ? " " + currentPatternType : ""),
                    "Animal " + specificPattern, new Date(), userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Sound of things 扰动
     */
    @RequiresAuthentication
    @RequiresPermissions(value = {"B:UPDATE", "B:DELETE"}, logical = Logical.AND)
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/addSoundOfThings")
    public Result addSoundOfThings(@RequestHeader("Authorization") String token,
                                   @RequestParam(value = "dataset") String dataset,
                                   @RequestParam(value = "audioName") String audioName,
                                   @RequestParam(value = "specificPattern") String specificPattern,
                                   @RequestParam(value = "currentPattern") String currentPattern,
                                   @RequestParam(value = "currentPatternType", required = false) String currentPatternType,
                                   @RequestParam(value = "snr") String snr) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject response = rpcUtil.sendRequest("add_sound_of_things", dataset, audioName, specificPattern,snr);
            if ((int) response.get(CODE) == StatusCode.FAIL.getCode()) {
                return Result.fail(StatusCode.FAIL.getStatus(), response.get("data"));
            }
            removeCurrentNoiseAudioClip(dataset, audioName, currentPattern, currentPatternType);
            User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
            operationService.insertOperationHistory(dataset, audioName,
                    currentPattern + (currentPatternType != null ? " " + currentPatternType : ""),
                    "Sound of things " + specificPattern, new Date(), userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Human sounds 扰动
     */
    @RequiresAuthentication
    @RequiresPermissions(value = {"B:UPDATE", "B:DELETE"}, logical = Logical.AND)
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/addHumanSounds")
    public Result addHumanSounds(@RequestHeader("Authorization") String token,
                                 @RequestParam(value = "dataset") String dataset,
                                 @RequestParam(value = "audioName") String audioName,
                                 @RequestParam(value = "specificPattern") String specificPattern,
                                 @RequestParam(value = "currentPattern") String currentPattern,
                                 @RequestParam(value = "currentPatternType", required = false) String currentPatternType,
                                 @RequestParam(value = "snr") String snr) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject response = rpcUtil.sendRequest("add_human_sounds", dataset, audioName, specificPattern,snr);
            if ((int) response.get(CODE) == StatusCode.FAIL.getCode()) {
                return Result.fail(StatusCode.FAIL.getStatus(), response.get("data"));
            }
            removeCurrentNoiseAudioClip(dataset, audioName, currentPattern, currentPatternType);
            User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
            operationService.insertOperationHistory(dataset, audioName,
                    currentPattern + (currentPatternType != null ? " " + currentPatternType : ""),
                    "Human sounds " + specificPattern, new Date(), userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 music 扰动
     */
    @RequiresAuthentication
    @RequiresPermissions(value = {"B:UPDATE", "B:DELETE"}, logical = Logical.AND)
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/addMusic")
    public Result addMusic(@RequestHeader("Authorization") String token,
                           @RequestParam(value = "dataset") String dataset,
                           @RequestParam(value = "audioName") String audioName,
                           @RequestParam(value = "specificPattern") String specificPattern,
                           @RequestParam(value = "currentPattern") String currentPattern,
                           @RequestParam(value = "currentPatternType", required = false) String currentPatternType,
                           @RequestParam(value = "snr") String snr) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject response = rpcUtil.sendRequest("add_music", dataset, audioName, specificPattern,snr);
            if ((int) response.get(CODE) == StatusCode.FAIL.getCode()) {
                return Result.fail(StatusCode.FAIL.getStatus(), response.get("data"));
            }
            removeCurrentNoiseAudioClip(dataset, audioName, currentPattern, currentPatternType);
            User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
            operationService.insertOperationHistory(dataset, audioName,
                    currentPattern + (currentPatternType != null ? " " + currentPatternType : ""),
                    "Music " + specificPattern, new Date(), userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Source-Ambiguous Sounds 扰动
     */
    @RequiresAuthentication
    @RequiresPermissions(value = {"B:UPDATE", "B:DELETE"}, logical = Logical.AND)
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/addSourceAmbiguousSounds")
    public Result addSourceAmbiguousSounds(@RequestHeader("Authorization") String token,
                                           @RequestParam(value = "dataset") String dataset,
                                           @RequestParam(value = "audioName") String audioName,
                                           @RequestParam(value = "specificPattern") String specificPattern,
                                           @RequestParam(value = "currentPattern") String currentPattern,
                                           @RequestParam(value = "currentPatternType", required = false)
                                           String currentPatternType,
                                           @RequestParam(value = "snr") String snr) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject response = rpcUtil.sendRequest("add_source_ambiguous_sounds",
                    dataset, audioName, specificPattern,snr);
            if ((int) response.get(CODE) == StatusCode.FAIL.getCode()) {
                return Result.fail(StatusCode.FAIL.getStatus(), response.get("data"));
            }
            removeCurrentNoiseAudioClip(dataset, audioName, currentPattern, currentPatternType);
            User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
            operationService.insertOperationHistory(dataset, audioName,
                    currentPattern + (currentPatternType != null ? " " + currentPatternType : ""),
                    "Source ambiguous sounds " + specificPattern, new Date(), userInfo.getName());
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 获取现扰动音频数量和原音频数量
     */
    @RequiresAuthentication
    @RequiresPermissions(value = {"B:SELECT"})
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/clipsAndNoiseClips")
    public Result getNumOfClipsAndNoiseClips(@RequestHeader("Authorization") String token,
                                             @RequestParam("dataset") String dataset) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("get_num_of_clips_and_noise_clips",
                    dataset);
            return Result.success(StatusCode.SUCCESS.getStatus(), JSONObject.toJSONString(jsonObject.getJSONArray("data")));
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }

    }

    @RequiresAuthentication
    @RequiresPermissions(value = {"B:UPDATE", "B:INSERT"}, logical = Logical.AND)
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/addNoiseRandomlyMultiProcess")
    public Result addRandomlyMultiProcess(@RequestHeader("Authorization") String token,
                                          @RequestParam("dataset") String dataset) {
        shiroUtil.verifyUserToken(token);
        try {
            JSONObject jsonObject = rpcUtil.sendRequest("add_randomly_multiProcess",
                    dataset, "8");
            return Result.success(StatusCode.SUCCESS.getStatus(), "");
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    private void removeCurrentNoiseAudioClip(String dataset, String audioName,
                                             String currentPattern, String currentPatternType) throws XmlRpcException {
        if (currentPatternType == null) {
            rpcUtil.sendRequest("remove_current_noise_audio_clip", dataset, audioName, currentPattern);
        } else {
            rpcUtil.sendRequest("remove_current_noise_audio_clip", dataset, audioName,
                    currentPattern, currentPatternType);
        }
    }
}
