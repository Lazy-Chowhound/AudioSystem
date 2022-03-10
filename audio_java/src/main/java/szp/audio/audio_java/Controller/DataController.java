package szp.audio.audio_java.Controller;

import com.alibaba.fastjson.JSON;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresAuthentication;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import szp.audio.audio_java.Entity.DatasetHistory;
import szp.audio.audio_java.Entity.ModelHistory;
import szp.audio.audio_java.Entity.OperationHistory;
import szp.audio.audio_java.Entity.User;
import szp.audio.audio_java.Service.DatasetService;
import szp.audio.audio_java.Service.ModelService;
import szp.audio.audio_java.Service.OperationService;
import szp.audio.audio_java.Util.Result;
import szp.audio.audio_java.Util.StatusCode;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Date;
import java.util.List;

/**
 * @author Nakano Miku
 */
@RestController
public class DataController {

    @Autowired
    private DatasetService datasetService;

    @Autowired
    private ModelService modelService;

    @Autowired
    private OperationService operationService;

    @Value("${audioset.path}")
    private String audioSetPath;

    @Value("${model.path}")
    private String modelPath;

    /**
     * 上传数据集属性
     */
    @RequiresAuthentication
    @RequiresPermissions("A:INSERT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/uploadDatasetDescription")
    public Result uploadDatasetDescription(@RequestParam("dataset") String dataset,
                                           @RequestParam("language") String language,
                                           @RequestParam("size") String size,
                                           @RequestParam("hour") float hour,
                                           @RequestParam("people") int people,
                                           @RequestParam("form") String form,
                                           @RequestParam("description") String description) {
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
     * 获取数据集上传历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("A:SELECT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/uploadDatasetHistory")
    public Result getUploadDatasetHistory() {
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        List<DatasetHistory> datasetHistories = datasetService.getDatasetHistories(userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), JSON.toJSONString(datasetHistories));
    }

    /**
     * 删除某数据集上传历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("A:DELETE")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/deleteDatasetHistory")
    public Result deleteUploadDatasetHistory(@RequestParam("name") String name) {
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        datasetService.deleteHistory(name, userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), "Delete Success");
    }

    /**
     * 清空数据集上传历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("A:DELETE")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/clearDatasetHistory")
    public Result clearUploadDatasetHistory() {
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        datasetService.clearHistory(userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), "Clear Success");
    }

    /**
     * 上传模型
     */
    @RequiresAuthentication
    @RequiresPermissions("C:INSERT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/uploadModel")
    public Result uploadModel(@RequestParam("file") MultipartFile file) {
        Path filePath = mkPath(file, modelPath);
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        System.out.println(userInfo.getName());
        modelService.insertModelUploadHistory(file.getOriginalFilename(), new Date(), userInfo.getName());
        try {
            file.transferTo(filePath);
        } catch (IOException e) {
            Result.fail(StatusCode.FAIL.getStatus(), "Upload Model Fail");
        }
        return Result.success(StatusCode.SUCCESS.getStatus(), "Upload Model Success");
    }

    /**
     * 获取模型上传历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("C:SELECT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/uploadModelHistory")
    public Result getUploadModelHistory() {
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        List<ModelHistory> modelHistories = modelService.getModelHistories(userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), JSON.toJSONString(modelHistories));
    }

    /**
     * 删除某条模型上传历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("C:DELETE")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/deleteModelHistory")
    public Result deleteUploadModelHistory(@RequestParam("name") String name) {
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        modelService.deleteHistory(name, userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), "Delete Success");
    }

    /**
     * 清空模型上传历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("C:DELETE")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/clearModelHistory")
    public Result clearUploadModelHistory() {
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        modelService.clearHistory(userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), "Clear Success");
    }

    /**
     * 获取扰动操作记录
     */
    @RequiresAuthentication
    @RequiresPermissions("B:SELECT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/operationHistory")
    public Result getOperationHistories() {
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        List<OperationHistory> operationHistories = operationService.getOperationHistories(userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), JSON.toJSONString(operationHistories));
    }

    /**
     * 删除某条扰动修改历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("B:SELECT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/deleteOperationHistory")
    public Result deleteOperationHistories(@RequestParam("dataset") String dataset,
                                           @RequestParam("audioName") String audioName,
                                           @RequestParam("formerType") String formerType,
                                           @RequestParam("latterType") String latterType,
                                           @RequestParam("time") String time) {
        Date date = new Date(Long.parseLong(time));
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        operationService.deleteHistory(dataset, audioName, formerType, latterType, date, userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), "Delete Success");
    }


    /**
     * 清空扰动修改历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("B:SELECT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/clearOperationHistory")
    public Result clearOperationHistory() {
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        operationService.clearHistory(userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), "Clear Success");
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
