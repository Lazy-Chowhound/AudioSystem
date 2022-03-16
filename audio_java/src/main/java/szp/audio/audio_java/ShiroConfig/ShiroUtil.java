package szp.audio.audio_java.ShiroConfig;

import org.apache.shiro.SecurityUtils;
import org.apache.shiro.subject.Subject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * @author Nakano Miku
 */
@Component
public class ShiroUtil {

    @Autowired
    private JwtUtil jwtUtil;

    public void verifyUserToken(String token) {
        jwtUtil.verifyToken(token);
        Subject subject = SecurityUtils.getSubject();
        subject.login(new AccessToken(token));
    }
}
