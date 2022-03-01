package szp.audio.audio_java.Dao;

import org.apache.ibatis.annotations.Mapper;
import szp.audio.audio_java.Entity.ModelHistory;

import java.util.Date;
import java.util.List;

/**
 * @author Nakano Miku
 */
@Mapper
public interface ModelDao {

    /**
     * 插入模型上传历史
     *
     * @param name 文件名
     * @param date 日期
     */
    void insertModelUploadHistory(String name, Date date);

    /**
     * 获取上传模型全部历史
     *
     * @return list
     */
    List<ModelHistory> getModelHistories();

    /**
     * 删除一条记录
     * @param name 名字
     */
    void deleteHistory(String name);

    /**
     * 清楚全部历史记录
     */
    void clearHistory();
}
