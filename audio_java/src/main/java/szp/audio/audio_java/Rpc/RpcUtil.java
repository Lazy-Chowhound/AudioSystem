package szp.audio.audio_java.Rpc;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
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

    public JSONObject sendRequest(String functionName, String... params) throws XmlRpcException {
        return (JSONObject) JSON.toJSON(xmlRpcClient.execute(functionName, params));
    }
}
