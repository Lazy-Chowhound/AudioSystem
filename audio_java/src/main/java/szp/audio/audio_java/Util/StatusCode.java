package szp.audio.audio_java.Util;

/**
 * @author Nakano Miku
 */

public enum StatusCode {
    /**
     * 成功
     */
    SUCCESS("success", 200),
    /**
     * 失败
     */
    FAIL("fail", 400);

    /**
     * 状态信息
     */
    private final String status;
    /**
     * 状态码
     */
    private final int code;

    StatusCode(String status, int code) {
        this.status = status;
        this.code = code;
    }

    public String getStatus() {
        return status;
    }

    public int getCode() {
        return code;
    }
}
