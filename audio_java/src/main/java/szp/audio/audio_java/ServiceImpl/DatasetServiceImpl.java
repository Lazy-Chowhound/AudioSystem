package szp.audio.audio_java.ServiceImpl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import szp.audio.audio_java.Dao.DatasetMapper;
import szp.audio.audio_java.Service.DatasetService;

/**
 * @author Nakano Miku
 */
@Service
public class DatasetServiceImpl implements DatasetService {

    @Autowired
    private DatasetMapper datasetMapper;

    @Override
    public int insertDataset(String datasetName, String language, String size, int hour, int people, String form, String description) {
        return datasetMapper.insertDataset(datasetName, language, size, hour, people, form, description);
    }
}