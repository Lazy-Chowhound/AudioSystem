package szp.audio.audio_java.Rpc;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * @author Nakano Miku
 */
@Component
public class RpcUtil {

    @Autowired
    private XmlRpcClient xmlRpcClient;

    public String sendRequest(String functionName, String... params) throws XmlRpcException {
        return String.valueOf(xmlRpcClient.execute(functionName, params));
    }
}
