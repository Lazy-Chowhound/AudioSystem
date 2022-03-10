package szp.audio.audio_java.ServiceImpl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import szp.audio.audio_java.Dao.DatasetDao;
import szp.audio.audio_java.Entity.DatasetHistory;
import szp.audio.audio_java.Service.DatasetService;

import java.util.Date;
import java.util.List;

/**
 * @author Nakano Miku
 */
@Service
public class DatasetServiceImpl implements DatasetService {

    @Autowired
    private DatasetDao datasetDao;

    @Override
    public int insertDataset(String datasetName, String language, String size, float hour, int people, String form, String description) {
        return datasetDao.insertDataset(datasetName, language, size, hour, people, form, description);
    }

    @Override
    public void insertDatasetUploadHistory(String name, Date date, String userName) {
        datasetDao.insertDatasetUploadHistory(name, date, userName);
    }

    @Override
    public List<DatasetHistory> getDatasetHistories(String userName) {
        return datasetDao.getDatasetHistories(userName);
    }

    @Override
    public void deleteHistory(String name, String userName) {
        datasetDao.deleteHistory(name, userName);
    }

    @Override
    public void clearHistory(String userName) {
        datasetDao.clearHistory(userName);
    }
}
