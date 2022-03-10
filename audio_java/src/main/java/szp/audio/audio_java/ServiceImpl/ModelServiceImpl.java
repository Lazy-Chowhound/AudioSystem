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
    public void insertModelUploadHistory(String name, Date date, String userName) {
        modelDao.insertModelUploadHistory(name, date, userName);
    }

    @Override
    public List<ModelHistory> getModelHistories(String userName) {
        return modelDao.getModelHistories(userName);
    }

    @Override
    public void deleteHistory(String name, String userName) {
        modelDao.deleteHistory(name, userName);
    }

    @Override
    public void clearHistory(String userName) {
        modelDao.clearHistory(userName);
    }


}
