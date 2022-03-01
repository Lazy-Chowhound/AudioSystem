package szp.audio.audio_java.Config;


import org.springframework.boot.web.servlet.MultipartConfigFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.util.unit.DataSize;

import javax.servlet.MultipartConfigElement;

/**
 * @author Nakano Miku
 */
@Configuration
public class UploadConfig {

    @Bean
    public MultipartConfigElement multipartConfigElement() {
        MultipartConfigFactory factory = new MultipartConfigFactory();
        DataSize dataSize = DataSize.ofGigabytes(2);
        factory.setMaxRequestSize(dataSize);
        factory.setMaxFileSize(dataSize);
        return factory.createMultipartConfig();
    }

}
