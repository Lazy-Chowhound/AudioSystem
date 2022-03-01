package szp.audio.audio_java.Service;

import szp.audio.audio_java.Entity.DatasetHistory;
import szp.audio.audio_java.Entity.ModelHistory;

import java.util.Date;
import java.util.List;

/**
 * @author Nakano Miku
 */
public interface DatasetService {
    /**
     * 插入数据集
     *
     * @param datasetName 数据集名称
     * @param language 语言
     * @param size 大小
     * @param hour 时长
     * @param people 人数
     * @param form 格式
     * @param description 描述
     * @return 插入条数
     */
    int insertDataset(String datasetName, String language, String size, int hour, int people, String form, String description);

    /**
     * 插入数据集上传历史
     * @param name 文件名
     * @param date 日期
     */
    void insertDatasetUploadHistory(String name, Date date);

    /**
     * 获取上传数据集全部历史
     * @return list
     */
    List<DatasetHistory> getDatasetHistories();

    /**
     * 清楚全部历史记录
     */
    void clearHistory();
}
