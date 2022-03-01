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
    public int insertDataset(String datasetName, String language, String size, int hour, int people, String form, String description) {
        return datasetDao.insertDataset(datasetName, language, size, hour, people, form, description);
    }

    @Override
    public void insertDatasetUploadHistory(String name, Date date) {
        datasetDao.insertDatasetUploadHistory(name, date);
    }

    @Override
    public List<DatasetHistory> getDatasetHistories() {
        return datasetDao.getDatasetHistories();
    }

    @Override
    public void deleteHistory(String name) {
        datasetDao.deleteHistory(name);
    }

    @Override
    public void clearHistory() {
        datasetDao.clearHistory();
    }
}
