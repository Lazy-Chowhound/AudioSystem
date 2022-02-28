package szp.audio.audio_java.Dao;

import org.apache.ibatis.annotations.Mapper;

/**
 * @author Nakano Miku
 */
@Mapper
public interface DatasetDao {
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
}
