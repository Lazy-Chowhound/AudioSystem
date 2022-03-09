package szp.audio.audio_java.Util;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletRequestWrapper;

/**
 * @author Nakano Miku
 */
public class HttpServletWrapper extends HttpServletRequestWrapper {

    String token;

    public HttpServletWrapper(HttpServletRequest request, String token) {
        super(request);
        this.token = token;
    }

    /**
     * 重写请求头token字段
     * 并非真正的重写，原来的token字段值并未改变，只是在调用的时候，如果
     * 获取的是token这个字段，则把我们指定的值返回
     */
    @Override
    public String getHeader(String name) {
        if ("token".equals(name)) {
            return this.token;
        }
        return super.getParameter(name);
    }
}
