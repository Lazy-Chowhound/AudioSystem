package szp.audio.audio_java.ServiceImpl;

import cn.hutool.json.JSONArray;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import szp.audio.audio_java.Dao.UserDao;
import szp.audio.audio_java.Entity.Permission;
import szp.audio.audio_java.Entity.Role;
import szp.audio.audio_java.Entity.User;
import szp.audio.audio_java.Service.UserService;

import java.util.Set;

/**
 * @author Nakano Miku
 */
@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserDao userDao;

    @Override
    public User getUserInfoByName(String userName) {
        return userDao.getUserInfoByName(userName);
    }

    @Override
    public Set<Permission> getUserPermissions(String userName) {
        return userDao.getUserPermissions(userName);
    }

    @Override
    public Set<Role> getUserRoles(String userName) {
        return userDao.getUserRoles(userName);
    }

    @Override
    public void register(String userName, String password) {
        userDao.insertUserInfo(userName, password, "[2]");
    }
}
