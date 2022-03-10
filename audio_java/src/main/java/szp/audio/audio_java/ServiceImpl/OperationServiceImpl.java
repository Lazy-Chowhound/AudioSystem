package szp.audio.audio_java.ServiceImpl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import szp.audio.audio_java.Dao.OperationDao;
import szp.audio.audio_java.Entity.OperationHistory;
import szp.audio.audio_java.Service.OperationService;

import java.util.Date;
import java.util.List;

/**
 * @author Nakano Miku
 */
@Service
public class OperationServiceImpl implements OperationService {

    @Autowired
    private OperationDao operationDao;

    @Override
    public void insertOperationHistory(String dataset, String audioName, String formerType, String latterType, Date date, String userName) {
        operationDao.insertOperationHistory(dataset, audioName, formerType, latterType, date, userName);
    }

    @Override
    public List<OperationHistory> getOperationHistories(String userName) {
        return operationDao.getOperationHistories(userName);
    }

    @Override
    public void deleteHistory(String dataset, String audioName, String formerType, String latterType, Date date, String userName) {
        operationDao.deleteHistory(dataset, audioName, formerType, latterType, date, userName);
    }

    @Override
    public void clearHistory(String userName) {
        operationDao.clearHistory(userName);
    }
}
