package szp.audio.audio_java.Service;

import szp.audio.audio_java.Entity.ModelHistory;
import szp.audio.audio_java.Entity.OperationHistory;

import java.util.Date;
import java.util.List;

/**
 * @author Nakano Miku
 */
public interface OperationService {
    /**
     * 操作历史
     *
     * @param formerType 文件名
     * @param latterType 文件名
     * @param date       日期
     */
    void insertOperationHistory(String formerType, String latterType, Date date);

    /**
     * 获取上传模型全部历史
     *
     * @return list
     */
    List<OperationHistory> getOperationHistories();

    /**
     * 删除一条记录
     *
     * @param formerType 文件名
     * @param latterType 文件名
     * @param date       日期
     */
    void deleteHistory(String formerType, String latterType, Date date);

    /**
     * 清楚全部历史记录
     */
    void clearHistory();
}
