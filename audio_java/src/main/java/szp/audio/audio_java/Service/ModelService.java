package szp.audio.audio_java.Service;

import szp.audio.audio_java.Entity.ModelHistory;

import java.util.Date;
import java.util.List;

/**
 * @author Nakano Miku
 */
public interface ModelService {
    /**
     * 插入模型上传历史
     *
     * @param name     文件名
     * @param date     日期
     * @param userName 用户名
     */
    void insertModelUploadHistory(String name, Date date, String userName);

    /**
     * 获取上传模型全部历史
     *
     * @param userName 用户名
     * @return list
     */
    List<ModelHistory> getModelHistories(String userName);

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
