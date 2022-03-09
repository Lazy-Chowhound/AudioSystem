package szp.audio.audio_java.ShiroConfig;

import org.apache.shiro.authc.AuthenticationToken;

/**
 * @author Nakano Miku
 */
public class AccessToken implements AuthenticationToken {

    private final String token;

    private final JwtUtil jwtUtil;

    public AccessToken(String token) {
        this.token = token;
        jwtUtil = new JwtUtil();
    }

    @Override
    public Object getPrincipal() {
        return jwtUtil.getUserName(token);
    }

    @Override
    public Object getCredentials() {
        return jwtUtil.getUserPassword(token);
    }
}

