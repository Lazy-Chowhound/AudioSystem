package szp.audio.audio_java.ShiroConfig;

import cn.hutool.core.date.DateField;
import cn.hutool.core.date.DateUtil;
import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTCreator;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.Date;

/**
 * @author Nakano Miku
 */
@Component
public class JwtUtil {

    @Value("${jwt.token.secretKey}")
    private String secretKey;

    @Value("${jwt.token.expireTime}")
    private int expireTime;

    @Value("${jwt.token.refreshTime}")
    private int refreshTime;

    public String createUserToken(String userName, String password) {
        Date expireDay = DateUtil.offset(new Date(), DateField.DAY_OF_YEAR, expireTime);
        Algorithm algorithm = Algorithm.HMAC512(secretKey);
        JWTCreator.Builder builder = JWT.create();
        return builder.withClaim("userName", userName).withClaim("password", password)
                .withExpiresAt(expireDay)
                .sign(algorithm);
    }

    public String createRefreshToken(String userName, String password) {
        Date expireDay = DateUtil.offset(new Date(), DateField.DAY_OF_YEAR, refreshTime);
        Algorithm algorithm = Algorithm.HMAC512(secretKey);
        JWTCreator.Builder builder = JWT.create();
        return builder.withClaim("userName", userName).withClaim("password", password)
                .withExpiresAt(expireDay)
                .sign(algorithm);
    }

    public String getUserName(String token) {
        DecodedJWT decodedJWT = JWT.decode(token);
        return decodedJWT.getClaim("userName").asString();
    }

    public String getUserPassword(String token) {
        DecodedJWT decodedJWT = JWT.decode(token);
        return decodedJWT.getClaim("password").asString();
    }

    public void verifyToken(String token) {
        Algorithm algorithm = Algorithm.HMAC512(secretKey);
        JWTVerifier jwtVerifier = JWT.require(algorithm).build();
        jwtVerifier.verify(token);
    }
}
