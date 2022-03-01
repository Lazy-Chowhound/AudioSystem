package szp.audio.audio_java.ServiceImpl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import szp.audio.audio_java.Dao.ModelDao;
import szp.audio.audio_java.Entity.ModelHistory;
import szp.audio.audio_java.Service.ModelService;

import java.util.Date;
import java.util.List;

/**
 * @author Nakano Miku
 */
@Service
public class ModelServiceImpl implements ModelService {

    @Autowired
    private ModelDao modelDao;

    @Override
    public void insertModelUploadHistory(String name, Date date) {
        modelDao.insertModelUploadHistory(name, date);
    }

    @Override
    public List<ModelHistory> getModelHistories() {
        return modelDao.getModelHistories();
    }

    @Override
    public void deleteHistory(String name) {
        modelDao.deleteHistory(name);
    }

    @Override
    public void clearHistory() {
        modelDao.clearHistory();
    }


}
