package szp.audio.audio_java.ShiroConfig;

import org.apache.shiro.authc.*;
import org.apache.shiro.authc.pam.UnsupportedTokenException;
import org.apache.shiro.authz.AuthorizationInfo;
import org.apache.shiro.authz.SimpleAuthorizationInfo;
import org.apache.shiro.realm.AuthorizingRealm;
import org.apache.shiro.subject.PrincipalCollection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import szp.audio.audio_java.Entity.Permission;
import szp.audio.audio_java.Entity.Role;
import szp.audio.audio_java.Entity.User;
import szp.audio.audio_java.Service.UserService;

import java.util.Set;
import java.util.stream.Collectors;

/**
 * @author Nakano Miku
 */
@Component
public class UserRealm extends AuthorizingRealm {

    @Autowired
    private UserService userService;

    @Override
    public boolean supports(AuthenticationToken token) {
        return token instanceof AccessToken;
    }

    /**
     * 认证
     * subject.login()时调用
     */
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken authenticationToken)
            throws AuthenticationException {
        if (authenticationToken == null) {
            throw new UnsupportedTokenException("token为空");
        }
        String userName = (String) authenticationToken.getPrincipal();
        User userInfo = userService.getUserInfoByName(userName);
        if (userInfo == null) {
            throw new UnknownAccountException("没有帐户信息");
        }
        String password = (String) authenticationToken.getCredentials();
        if (!password.equals(userInfo.getPassword())) {
            throw new IncorrectCredentialsException("密码错误");
        }
        return new SimpleAuthenticationInfo(userName, password, getName());
    }

    /**
     * 授权
     * 调用 @RequiresPermissions @RequiresRoles subject.hasRole subject.isPermitted等需要角色权限时调用
     */
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principalCollection) {
        SimpleAuthorizationInfo authorizationInfo = new SimpleAuthorizationInfo();
        // 这里取出的是上面SimpleAuthenticationInfo第一个参数
        String userName = (String) principalCollection.getPrimaryPrincipal();
        // 获取用户权限
        Set<Permission> permissions = userService.getUserPermissions(userName);
        Set<String> perms = permissions.stream().map(Permission::getPermissionName).collect(Collectors.toSet());
        authorizationInfo.setStringPermissions(perms);

        // 获取用户角色
        Set<Role> userRoles = userService.getUserRoles(userName);
        Set<String> roles = userRoles.stream().map(Role::getRoleName).collect(Collectors.toSet());
        authorizationInfo.setRoles(roles);
        return authorizationInfo;
    }
}

