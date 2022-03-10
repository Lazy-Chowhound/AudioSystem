package szp.audio.audio_java.Service;

import szp.audio.audio_java.Entity.DatasetHistory;

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
     * @param language    语言
     * @param size        大小
     * @param hour        时长
     * @param people      人数
     * @param form        格式
     * @param description 描述
     * @return 插入条数
     */
    int insertDataset(String datasetName, String language, String size, float hour, int people, String form, String description);

    /**
     * 插入数据集上传历史
     *
     * @param name     文件名
     * @param date     日期
     * @param userName 用户名
     */
    void insertDatasetUploadHistory(String name, Date date, String userName);

    /**
     * 获取上传数据集全部历史
     *
     * @param userName 用户名
     * @return list
     */
    List<DatasetHistory> getDatasetHistories(String userName);

    /**
     * 删除一条记录
     *
     * @param userName 用户名
     * @param name     名字
     */
    void deleteHistory(String name, String userName);

    /**
     * 清楚全部历史记录
     *
     * @param userName 用户名
     */
    void clearHistory(String userName);
}
