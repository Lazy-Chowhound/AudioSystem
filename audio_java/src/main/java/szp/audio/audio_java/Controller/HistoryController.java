package szp.audio.audio_java.Controller;

import com.alibaba.fastjson.JSON;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authz.annotation.Logical;
import org.apache.shiro.authz.annotation.RequiresAuthentication;
import org.apache.shiro.authz.annotation.RequiresPermissions;
import org.apache.shiro.authz.annotation.RequiresRoles;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import szp.audio.audio_java.Entity.DatasetHistory;
import szp.audio.audio_java.Entity.ModelHistory;
import szp.audio.audio_java.Entity.OperationHistory;
import szp.audio.audio_java.Entity.User;
import szp.audio.audio_java.Service.DatasetService;
import szp.audio.audio_java.Service.ModelService;
import szp.audio.audio_java.Service.OperationService;
import szp.audio.audio_java.ShiroConfig.ShiroUtil;
import szp.audio.audio_java.Util.Result;
import szp.audio.audio_java.Util.StatusCode;

import java.util.Date;
import java.util.List;

@RestController
public class HistoryController {

    @Autowired
    private DatasetService datasetService;

    @Autowired
    private OperationService operationService;

    @Autowired
    private ShiroUtil shiroUtil;

    @Autowired
    private ModelService modelService;

    /**
     * 获取数据集上传历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("A:SELECT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/uploadDatasetHistory")
    public Result getUploadDatasetHistory(@RequestHeader("Authorization") String token) {
        shiroUtil.verifyUserToken(token);
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
    public Result deleteUploadDatasetHistory(@RequestHeader("Authorization") String token,
                                             @RequestParam("name") String name) {
        shiroUtil.verifyUserToken(token);
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
    public Result clearUploadDatasetHistory(@RequestHeader("Authorization") String token) {
        shiroUtil.verifyUserToken(token);
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        datasetService.clearHistory(userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), "Clear Success");
    }

    /**
     * 获取模型上传历史记录
     */
    @RequiresAuthentication
    @RequiresPermissions("C:SELECT")
    @RequiresRoles(value = {"ROOT", "USER"}, logical = Logical.OR)
    @RequestMapping("/uploadModelHistory")
    public Result getUploadModelHistory(@RequestHeader("Authorization") String token) {
        shiroUtil.verifyUserToken(token);
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
    public Result deleteUploadModelHistory(@RequestHeader("Authorization") String token,
                                           @RequestParam("name") String name) {
        shiroUtil.verifyUserToken(token);
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
    public Result clearUploadModelHistory(@RequestHeader("Authorization") String token) {
        shiroUtil.verifyUserToken(token);
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
    public Result getOperationHistories(@RequestHeader("Authorization") String token) {
        shiroUtil.verifyUserToken(token);
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
    public Result deleteOperationHistories(@RequestHeader("Authorization") String token,
                                           @RequestParam("dataset") String dataset,
                                           @RequestParam("audioName") String audioName,
                                           @RequestParam("formerType") String formerType,
                                           @RequestParam("latterType") String latterType,
                                           @RequestParam("time") String time) {
        shiroUtil.verifyUserToken(token);
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
    public Result clearOperationHistory(@RequestHeader("Authorization") String token) {
        shiroUtil.verifyUserToken(token);
        User userInfo = (User) SecurityUtils.getSubject().getPrincipal();
        operationService.clearHistory(userInfo.getName());
        return Result.success(StatusCode.SUCCESS.getStatus(), "Clear Success");
    }
}
