package szp.audio.audio_java;


import cn.hutool.core.date.DateField;
import cn.hutool.core.date.DateUtil;
import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTCreator;
import com.auth0.jwt.algorithms.Algorithm;
import org.junit.jupiter.api.Test;

import java.util.Date;

public class TokenTest {
    @Test
    public void createUserToken() {
        Date expireDay = DateUtil.offset(new Date(), DateField.DAY_OF_YEAR, 7);
        Algorithm algorithm = Algorithm.HMAC512("szp061210");
        JWTCreator.Builder builder = JWT.create();
        System.out.println(builder.withClaim("userName", "szp").withClaim("password", "061210")
                .withExpiresAt(expireDay)
                .sign(algorithm));
    }
}
