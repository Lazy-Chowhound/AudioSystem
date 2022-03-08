package szp.audio.audio_java.Entity;

import lombok.Data;

import java.util.Date;

/**
 * @author Nakano Miku
 */
@Data
public class OperationHistory {
    private int id;
    private String formerType;
    private String latterType;
    private Date time;
}
