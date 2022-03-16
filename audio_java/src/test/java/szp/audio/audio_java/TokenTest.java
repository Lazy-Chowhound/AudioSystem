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
    public void creatWrongUserToken() {
        System.out.println(createUserToken("szp", "0", DateField.DAY_OF_YEAR));
    }

    @Test
    public void creatWrongTimeToken() {
        System.out.println(createUserToken("szp", "061210", DateField.SECOND));
    }

    public String createUserToken(String userName, String password, DateField dateField) {
        Date expireDay = DateUtil.offset(new Date(), dateField, 7);
        Algorithm algorithm = Algorithm.HMAC512("szp061210");
        JWTCreator.Builder builder = JWT.create();
        return builder.withClaim("userName", userName).withClaim("password", password)
                .withExpiresAt(expireDay)
                .sign(algorithm);
    }
}
