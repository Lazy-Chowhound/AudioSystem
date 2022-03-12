package szp.audio.audio_java.Dao;

import org.apache.ibatis.annotations.Mapper;
import szp.audio.audio_java.Entity.Permission;
import szp.audio.audio_java.Entity.Role;
import szp.audio.audio_java.Entity.User;

import java.util.Set;

/**
 * @author Nakano Miku
 */
@Mapper
public interface UserDao {

    /**
     * 获取用户信息
     *
     * @param userName 用户名
     * @return
     */
    User getUserInfoByName(String userName);

    /**
     * 获取用户权限
     *
     * @param userName 用户名
     * @return
     */
    Set<Permission> getUserPermissions(String userName);

    /**
     * 获取用户角色
     *
     * @param userName 用户名
     * @return
     */
    Set<Role> getUserRoles(String userName);

    /**
     * 插入用户信息
     *
     * @param userName 用户名
     * @param password 密码
     */
    void insertUserInfo(String userName, String password, String role);
}
