package szp.audio.audio_java.Controller;

import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresAuthentication;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import szp.audio.audio_java.Entity.User;
import szp.audio.audio_java.Service.DatasetService;
import szp.audio.audio_java.Service.ModelService;
import szp.audio.audio_java.ShiroConfig.ShiroUtil;
import szp.audio.audio_java.Util.Result;
import szp.audio.audio_java.Util.StatusCode;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Date;

/**
 * @author Nakano Miku
 */
@RestController
public class UploadController {

    @Autowired
    private DatasetService datasetService;

    @Autowired
    private ModelService modelService;

    @Value("${audioset.path}")
    private String audioSetPath;

    @Value("${model.path}")
    private String modelPath;

    @Autowired
    private ShiroUtil shiroUtil;

    /**
     * 上传数据集属性
     */
    @RequiresAuthentication
    @RequiresPermissions("A:INSERT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/uploadDatasetDescription")
    public Result uploadDatasetDescription(@RequestHeader("Authorization") String token,
                                           @RequestParam("dataset") String dataset,
                                           @RequestParam("language") String language,
                                           @RequestParam("size") String size,
                                           @RequestParam("hour") float hour,
                                           @RequestParam("people") int people,
                                           @RequestParam("form") String form,
                                           @RequestParam("description") String description) {
        shiroUtil.verifyUserToken(token);
        int res = datasetService.insertDataset(dataset, language, size, hour, people, form, description);
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        datasetService.insertDatasetUploadHistory(dataset, new Date(), userInfo.getName());
        if (res == 0) {
            Result.fail(StatusCode.FAIL.getStatus(), "Insert Fail");
        }
        return Result.success(StatusCode.SUCCESS.getStatus(), "Insert Success");
    }

    /**
     * 上传数据集
     */
    @RequiresAuthentication
    @RequiresPermissions("A:INSERT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/uploadDataset")
    public Result uploadDataset(@RequestParam("file") MultipartFile file) {
        Path filePath = mkPath(file, audioSetPath);
        try {
            file.transferTo(filePath);
        } catch (IOException e) {
            Result.fail(StatusCode.FAIL.getStatus(), "Upload Dataset Fail");
        }
        return Result.success(StatusCode.SUCCESS.getStatus(), "Upload Dataset Success");
    }

    /**
     * 上传模型记录
     */
    @RequiresAuthentication
    @RequiresPermissions("C:INSERT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/modelHistory")
    public Result uploadModelHistory(@RequestHeader("Authorization") String token,
                                     @RequestParam("model") String model) {
        shiroUtil.verifyUserToken(token);
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        modelService.insertModelUploadHistory(model, new Date(), userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), "Insert Model History Success");
    }

    /**
     * 上传模型
     */
    @RequiresAuthentication
    @RequiresPermissions("C:INSERT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/uploadModel")
    public Result uploadModel(@RequestHeader("Authorization") String token,
                              @RequestParam("file") MultipartFile file) {
        shiroUtil.verifyUserToken(token);
        Path filePath = mkPath(file, modelPath);
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        try {
            file.transferTo(filePath);
        } catch (IOException e) {
            Result.fail(StatusCode.FAIL.getStatus(), "Upload Model Fail");
        }
        return Result.success(StatusCode.SUCCESS.getStatus(), "Upload Model Success");
    }


    /**
     * 生成所必须的文件夹
     */
    private Path mkPath(MultipartFile file, String uploadPath) {
        String originPath = file.getOriginalFilename();
        String directoryPath = uploadPath + originPath.substring(0, originPath.lastIndexOf("/"));
        File dir = new File(directoryPath);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        return Paths.get(uploadPath + originPath);
    }
}
