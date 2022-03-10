package szp.audio.audio_java.Service;

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
     * @param dataset    数据集
     * @param audioName  音频名
     * @param formerType 原扰动
     * @param latterType 现扰动
     * @param date       日期
     * @param userName   用户名
     */
    void insertOperationHistory(String dataset, String audioName, String formerType, String latterType, Date date, String userName);

    /**
     * 获取上传模型全部历史
     *
     * @param userName 用户名
     * @return list
     */
    List<OperationHistory> getOperationHistories(String userName);

    /**
     * 删除一条记录
     *
     * @param dataset    数据集
     * @param audioName  音频名
     * @param formerType 原扰动
     * @param latterType 现扰动
     * @param date       日期
     * @param userName   用户名
     */
    void deleteHistory(String dataset, String audioName, String formerType, String latterType, Date date, String userName);

    /**
     * 清楚全部历史记录
     *
     * @param userName 用户名
     */
    void clearHistory(String userName);
}
