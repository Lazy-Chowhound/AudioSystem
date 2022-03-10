package szp.audio.audio_java.Util;

import com.auth0.jwt.exceptions.TokenExpiredException;
import org.apache.shiro.authc.AuthenticationException;
import org.apache.shiro.authc.IncorrectCredentialsException;
import org.apache.shiro.authc.UnknownAccountException;
import org.apache.shiro.authc.pam.UnsupportedTokenException;
import org.apache.shiro.authz.AuthorizationException;
import org.apache.shiro.authz.UnauthenticatedException;
import org.apache.shiro.authz.UnauthorizedException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * @author Nakano Miku
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ResponseBody
    @ExceptionHandler(AuthenticationException.class)
    public Result authenticationExceptionHandler() {
        return Result.fail(StatusCode.FAIL.getStatus(), "登录异常");
    }

    @ResponseBody
    @ExceptionHandler(UnauthenticatedException.class)
    public Result unauthenticatedExceptionHandler() {
        return Result.fail(StatusCode.FAIL.getStatus(), "您没有登录，请先登录");
    }

    @ResponseBody
    @ExceptionHandler(UnauthorizedException.class)
    public Result unauthorizedExceptionHandler() {
        return Result.fail(StatusCode.FAIL.getStatus(), "没有相关权限");
    }

    @ResponseBody
    @ExceptionHandler(AuthorizationException.class)
    public Result authorizationExceptionHandler() {
        return Result.fail(StatusCode.FAIL.getStatus(), "您没有权限");
    }

    @ResponseBody
    @ExceptionHandler(UnsupportedTokenException.class)
    public Result unsupportedTokenExceptionHandler() {
        return Result.fail(StatusCode.FAIL.getStatus(), "处于未登录状态");
    }

    @ResponseBody
    @ExceptionHandler(UnknownAccountException.class)
    public Result unknownAccountExceptionHandler() {
        return Result.fail(StatusCode.FAIL.getStatus(), "账户不存在");
    }

    @ResponseBody
    @ExceptionHandler(IncorrectCredentialsException.class)
    public Result incorrectCredentialsExceptionHandler() {
        return Result.fail(StatusCode.FAIL.getStatus(), "密码错误");
    }

    @ResponseBody
    @ExceptionHandler(TokenExpiredException.class)
    public Result tokenExpiredExceptionHandler() {
        return Result.fail(StatusCode.FAIL.getStatus(), "登录已失效，请重新登录");
    }
}

