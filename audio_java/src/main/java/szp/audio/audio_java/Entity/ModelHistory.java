package szp.audio.audio_java.Entity;

import lombok.Data;

import java.io.Serializable;
import java.util.Date;

/**
 * @author Nakano Miku
 */
@Data
public class ModelHistory implements Serializable {

    private int id;
    private String name;
    private Date time;
}
