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
                                        @RequestParam(value = "audioName") String audioName,
                                        @RequestParam(value = "formerPattern") String formerPattern,
                                        @RequestParam(value = "formerPatternType") String formerPatternType) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            removeFormerAudio(dataset, audioName, formerPattern, formerPatternType);
            rpcUtil.sendRequest("add_gaussian_noise", path, audioName);
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
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
                                @RequestParam(value = "specificPattern") String specificPattern,
                                @RequestParam(value = "formerPattern") String formerPattern,
                                @RequestParam(value = "formerPatternType", required = false) String formerPatternType) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            removeFormerAudio(dataset, audioName, formerPattern, formerPatternType);
            rpcUtil.sendRequest("add_sound_level", path, audioName, specificPattern);
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Natural Sounds 扰动
     */
    @RequestMapping("/addNaturalSounds")
    public Result addNaturalSounds(@RequestParam(value = "dataset") String dataset,
                                   @RequestParam(value = "audioName") String audioName,
                                   @RequestParam(value = "specificPattern") String specificPattern,
                                   @RequestParam(value = "formerPattern") String formerPattern,
                                   @RequestParam(value = "formerPatternType", required = false) String formerPatternType) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            removeFormerAudio(dataset, audioName, formerPattern, formerPatternType);
            rpcUtil.sendRequest("add_natural_sounds", path, audioName, specificPattern);
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Animal 扰动
     */
    @RequestMapping("/addAnimal")
    public Result addAnimal(@RequestParam(value = "dataset") String dataset,
                            @RequestParam(value = "audioName") String audioName,
                            @RequestParam(value = "specificPattern") String specificPattern,
                            @RequestParam(value = "formerPattern") String formerPattern,
                            @RequestParam(value = "formerPatternType", required = false) String formerPatternType) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            removeFormerAudio(dataset, audioName, formerPattern, formerPatternType);
            rpcUtil.sendRequest("add_animal", path, audioName, specificPattern);
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Sound of things 扰动
     */
    @RequestMapping("/addSoundOfThings")
    public Result addSoundOfThings(@RequestParam(value = "dataset") String dataset,
                                   @RequestParam(value = "audioName") String audioName,
                                   @RequestParam(value = "specificPattern") String specificPattern,
                                   @RequestParam(value = "formerPattern") String formerPattern,
                                   @RequestParam(value = "formerPatternType", required = false) String formerPatternType) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            removeFormerAudio(dataset, audioName, formerPattern, formerPatternType);
            rpcUtil.sendRequest("add_sound_of_things", path, audioName, specificPattern);
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Human sounds 扰动
     */
    @RequestMapping("/addHumanSounds")
    public Result addHumanSounds(@RequestParam(value = "dataset") String dataset,
                                 @RequestParam(value = "audioName") String audioName,
                                 @RequestParam(value = "specificPattern") String specificPattern,
                                 @RequestParam(value = "formerPattern") String formerPattern,
                                 @RequestParam(value = "formerPatternType", required = false) String formerPatternType) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            removeFormerAudio(dataset, audioName, formerPattern, formerPatternType);
            rpcUtil.sendRequest("add_human_sounds", path, audioName, specificPattern);
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 music 扰动
     */
    @RequestMapping("/addMusic")
    public Result addMusic(@RequestParam(value = "dataset") String dataset,
                           @RequestParam(value = "audioName") String audioName,
                           @RequestParam(value = "specificPattern") String specificPattern,
                           @RequestParam(value = "formerPattern") String formerPattern,
                           @RequestParam(value = "formerPatternType", required = false) String formerPatternType) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            removeFormerAudio(dataset, audioName, formerPattern, formerPatternType);
            rpcUtil.sendRequest("add_music", path, audioName, specificPattern);
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    /**
     * 添加 Source-Ambiguous Sounds 扰动
     */
    @RequestMapping("/addSourceAmbiguousSounds")
    public Result addSourceAmbiguousSounds(@RequestParam(value = "dataset") String dataset,
                                           @RequestParam(value = "audioName") String audioName,
                                           @RequestParam(value = "specificPattern") String specificPattern,
                                           @RequestParam(value = "formerPattern") String formerPattern,
                                           @RequestParam(value = "formerPatternType", required = false) String formerPatternType) {
        try {
            String path = "D:/AudioSystem/Audio/" + dataset + "/clips/";
            removeFormerAudio(dataset, audioName, formerPattern, formerPatternType);
            rpcUtil.sendRequest("add_source_ambiguous_sounds", path, audioName, specificPattern);
            return Result.success(StatusCode.SUCCESS.getStatus(), null);
        } catch (XmlRpcException xmlRpcException) {
            return Result.fail(StatusCode.FAIL.getStatus(), xmlRpcException.getMessage());
        }
    }

    private void removeFormerAudio(String dataset, String audioName,
                                   String formerPattern, String formerPatternType) throws XmlRpcException {
        if (formerPatternType == null) {
            rpcUtil.sendRequest("removeFormerAudio", dataset, audioName, formerPattern);
        } else {
            rpcUtil.sendRequest("removeFormerAudio", dataset, audioName, formerPattern, formerPatternType);
        }
    }
}
