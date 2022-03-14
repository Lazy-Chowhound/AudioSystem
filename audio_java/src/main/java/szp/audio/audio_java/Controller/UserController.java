package szp.audio.audio_java.Controller;

import com.auth0.jwt.exceptions.TokenExpiredException;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.pam.UnsupportedTokenException;
import org.apache.shiro.subject.Subject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import szp.audio.audio_java.Entity.User;
import szp.audio.audio_java.Service.UserService;
import szp.audio.audio_java.ShiroConfig.AccessToken;
import szp.audio.audio_java.ShiroConfig.JwtUtil;
import szp.audio.audio_java.Util.Result;
import szp.audio.audio_java.Util.StatusCode;

import java.util.concurrent.TimeUnit;

/**
 * @author Nakano Miku
 */
@RestController
public class UserController {

    @Autowired
    private JwtUtil jwtUtil;

    @Value("${jwt.token.refreshTime}")
    private int refreshTime;

    @Autowired
    private UserService userService;

    @Autowired
    private RedisTemplate<String, String> redisTemplate;

    @RequestMapping("/register")
    public Result register(@RequestParam("userName") String userName, @RequestParam("password") String password) {
        User user = userService.getUserInfoByName(userName);
        if (user != null) {
            return Result.fail(StatusCode.FAIL.getStatus(), "用户名已存在");
        }
        userService.register(userName, password);
        return Result.success(StatusCode.SUCCESS.getStatus(), "注册成功");
    }

    @RequestMapping("/login")
    public Result login(@RequestParam("userName") String userName, @RequestParam("password") String password) {
        Subject subject = SecurityUtils.getSubject();
        String token = jwtUtil.createUserToken(userName, password);
        String refreshToken = jwtUtil.createRefreshToken(userName, password);
        AccessToken accessToken = new AccessToken(token);
        subject.login(accessToken);
        // token存入redis
        redisTemplate.opsForValue().set(userName, refreshToken, refreshTime, TimeUnit.DAYS);
        return Result.success(StatusCode.SUCCESS.getStatus(), token);
    }

    @RequestMapping("/logout")
    public Result logout() {
        Subject currentUser = SecurityUtils.getSubject();
        currentUser.logout();
        return Result.success(StatusCode.SUCCESS.getStatus(), "登出成功");
    }

    @RequestMapping("/verifyToken")
    public Result verifyToken(@RequestParam(value = "token", required = false) String token) {
        if (token == null) {
            throw new UnsupportedTokenException();
        }
        String userName = jwtUtil.getUserName(token);
        String password = jwtUtil.getUserPassword(token);
        try {
            jwtUtil.verifyToken(token);
        } catch (TokenExpiredException expiredException) {
            // 双token均过期
            if (Boolean.FALSE.equals(redisTemplate.hasKey(userName))) {
                throw new TokenExpiredException("token已过期");
            } else {
                // 用户token过期但refresh token没有，则刷新两个token，然后将新的token返回给用户
                String newUserToken = jwtUtil.createUserToken(userName, password);
                String newRefreshToken = jwtUtil.createRefreshToken(userName, password);
                redisTemplate.delete(userName);
                redisTemplate.opsForValue().set(userName, newRefreshToken, refreshTime, TimeUnit.DAYS);
                Subject subject = SecurityUtils.getSubject();
                subject.login(new AccessToken(newUserToken));
                return Result.success(StatusCode.SUCCESS.getStatus(), newUserToken + " " + userName);
            }
        } catch (Exception exception) {
            throw new UnsupportedTokenException();
        }
        Subject subject = SecurityUtils.getSubject();
        subject.login(new AccessToken(token));
        return Result.success(StatusCode.SUCCESS.getStatus(), token + " " + userName);
    }
}
