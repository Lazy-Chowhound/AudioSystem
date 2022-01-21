package szp.audio.audio_java.Util;

import lombok.Data;

/**
 * @author Nakano Miku
 */
@Data
public class Result {

    private int code;
    private String message;
    private Object data;

    public Result(int code, String message, Object data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    public static Result success(String message, Object data) {
        return new Result(StatusCode.SUCCESS.getCode(), message, data);
    }

    public static Result fail(String message, Object data) {
        return new Result(StatusCode.FAIL.getCode(), message, data);
    }
}
