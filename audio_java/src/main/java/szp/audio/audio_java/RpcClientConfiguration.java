package szp.audio.audio_java;

import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.net.MalformedURLException;
import java.net.URL;

/**
 * @author Nakano Miku
 */
@Configuration
public class RpcClientConfiguration {

    @Value("${rpc.server.address}")
    private String rpcServerUrl;

    @Bean
    public XmlRpcClientConfigImpl xmlRpcClientConfig() throws MalformedURLException {
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL(rpcServerUrl));
        return config;
    }

    @Bean
    public XmlRpcClient xmlRpcClient() throws MalformedURLException {
        XmlRpcClient xmlRpcClient = new XmlRpcClient();
        xmlRpcClient.setConfig(xmlRpcClientConfig());
        return xmlRpcClient;
    }
}
