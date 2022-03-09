package szp.audio.audio_java.Controller;

import org.apache.shiro.SecurityUtils;
import org.apache.shiro.subject.Subject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.*;
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
        if (subject.isAuthenticated()) {
            return Result.fail(StatusCode.FAIL.getStatus(), "已经登录，请先退出当前帐号再登录");
        }
        String token = jwtUtil.createUserToken(userName, password);
        String refreshToken = jwtUtil.createRefreshToken(userName, password);
        // token存入redis
        redisTemplate.opsForValue().set(userName, refreshToken, refreshTime, TimeUnit.DAYS);
        AccessToken accessToken = new AccessToken(token);
        subject.login(accessToken);
        return Result.success(StatusCode.SUCCESS.getStatus(), token);
    }

    @RequestMapping("/logout")
    public Result logout() {
        Subject currentUser = SecurityUtils.getSubject();
        currentUser.logout();
        return Result.success(StatusCode.SUCCESS.getStatus(), "登出成功");
    }
}
