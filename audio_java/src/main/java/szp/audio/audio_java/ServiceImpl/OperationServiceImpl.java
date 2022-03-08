package szp.audio.audio_java.ServiceImpl;

import org.springframework.beans.factory.annotation.Autowired;
import szp.audio.audio_java.Dao.OperationDao;
import szp.audio.audio_java.Entity.OperationHistory;
import szp.audio.audio_java.Service.OperationService;

import java.util.Date;
import java.util.List;

/**
 * @author Nakano Miku
 */
public class OperationServiceImpl implements OperationService {
    @Autowired
    private OperationDao operationDao;

    @Override
    public void insertOperationHistory(String formerType, String latterType, Date date) {
        operationDao.insertOperationHistory(formerType, latterType, date);
    }

    @Override
    public List<OperationHistory> getOperationHistories() {
        return operationDao.getOperationHistories();
    }

    @Override
    public void deleteHistory(String formerType, String latterType, Date date) {
        operationDao.deleteHistory(formerType, latterType, date);
    }

    @Override
    public void clearHistory() {
        operationDao.clearHistory();
    }
}
