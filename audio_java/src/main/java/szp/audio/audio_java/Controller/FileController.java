package szp.audio.audio_java.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import szp.audio.audio_java.Service.DatasetService;
import szp.audio.audio_java.Util.Result;
import szp.audio.audio_java.Util.StatusCode;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * @author Nakano Miku
 */
@RestController
public class FileController {

    @Autowired
    private DatasetService datasetService;

    @Value("${audioset.path}")
    private String audioSetPath;

    @RequestMapping("/uploadDatasetDescription")
    public Result uploadDatasetDescription(@RequestParam("dataset") String dataset,
                                           @RequestParam("language") String language,
                                           @RequestParam("size") String size,
                                           @RequestParam("hour") int hour,
                                           @RequestParam("people") int people,
                                           @RequestParam("form") String form,
                                           @RequestParam("description") String description) {
        int res = datasetService.insertDataset(dataset, language, size, hour, people, form, description);
        if (res == 0) {
            Result.fail(StatusCode.FAIL.getStatus(), "Insert Fail");
        }
        return Result.success(StatusCode.SUCCESS.getStatus(), "Insert Success");
    }

    @RequestMapping("/uploadDataset")
    public Result uploadDataset(@RequestParam("file") MultipartFile file) {
        String originPath = file.getOriginalFilename();
        // 建立文件夹
        String directoryPath = audioSetPath + originPath.substring(0, originPath.lastIndexOf("/"));
        File dir = new File(directoryPath);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        Path filePath = Paths.get(audioSetPath + originPath);
        try {
            file.transferTo(filePath);
        } catch (IOException e) {
            Result.fail(StatusCode.FAIL.getStatus(), "Upload Fail");
        }
        return Result.success(StatusCode.SUCCESS.getStatus(), "Upload Success");
    }
}
