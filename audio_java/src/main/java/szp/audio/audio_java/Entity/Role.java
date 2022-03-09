package szp.audio.audio_java.Entity;

import lombok.Data;

import java.util.Set;

/**
 * @author Nakano Miku
 */
@Data
public class Role {

    private int id;

    private String roleName;

    private Set<Permission> permissions;

    @Override
    public String toString() {
        return "Role{" +
                "id=" + id +
                ", roleName='" + roleName + '\'' +
                ", permissions=" + permissions +
                '}';
    }
}