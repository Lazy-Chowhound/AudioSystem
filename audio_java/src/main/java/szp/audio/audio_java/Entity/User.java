package szp.audio.audio_java.Entity;

import lombok.Data;

import java.util.Set;

/**
 * @author Nakano Miku
 */
@Data
public class User {

    private int id;

    private String name;

    private String password;

    private Set<Role> roles;

}

