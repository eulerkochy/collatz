package collatz.chaincode;

import com.google.gson.JsonObject;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.hyperledger.fabric.shim.ChaincodeBase;
import org.hyperledger.fabric.shim.ChaincodeStub;
import org.hyperledger.fabric.shim.ledger.KeyModification;
import org.hyperledger.fabric.shim.ledger.QueryResultsIterator;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.IntStream;

public class CollatzChaincode extends ChaincodeBase {


    private static Log LOG = LogFactory.getLog(CollatzChaincode.class);

    public static final String INVOKE_FUNCTION = "invoke";
    public static final String QUERY_FUNCTION = "query";
    public static final String QUERY_HISTORY_FUNCTION = "queryHistory";

    @Override
    public Response init(ChaincodeStub chaincodeStub) {
        return newSuccessResponse();
    }

    @Override
    public Response invoke(ChaincodeStub chaincodeStub) {

        String functionName = chaincodeStub.getFunction();
        LOG.info("function name: "+ functionName);


        List<String> paramList = chaincodeStub.getParameters();
        IntStream.range(0,paramList.size()).forEach(idx -> LOG.info("value of param: " + idx  + " is: "+paramList.get(idx)));

        if (INVOKE_FUNCTION.equalsIgnoreCase(functionName)) {
            return performInvokeOperation(chaincodeStub, paramList);
        } else if (QUERY_FUNCTION.equalsIgnoreCase(functionName)) {
            return performQueryOperation(chaincodeStub, paramList);
        }   else if (QUERY_HISTORY_FUNCTION.equalsIgnoreCase(functionName)){
                return performQueryByHistoryFunction(chaincodeStub, paramList);
            }
         else return newErrorResponse(functionName + " function is currently not supported");
    }

    private Response performQueryByHistoryFunction(ChaincodeStub chaincodeStub, List<String> paramList) {
        if (listHasDifferentSizeThen(paramList, 1)) {
            return newErrorResponse("incorrect number of arguments");
        }
        QueryResultsIterator<KeyModification> queryResultsIterator = chaincodeStub.getHistoryForKey(paramList.get(0));
        return newSuccessResponse(buildJsonFromQueryResult(queryResultsIterator));

    }

    private String buildJsonFromQueryResult(QueryResultsIterator<KeyModification> queryResultsIterator) {

        JSONArray jsonArray = new JSONArray();
        queryResultsIterator.forEach(keyModification -> {
            Map<String, Object> map = new LinkedHashMap<>();
            map.put("transactionId", keyModification.getTxId());
            map.put("timestamp", keyModification. getTimestamp().toString());
            map.put("value", keyModification.getStringValue());
            map.put("isDeleted", keyModification.isDeleted());
            jsonArray.put(map);
        });

        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.accumulate("transactions", jsonArray);
        } catch (JSONException e) {
            throw new RuntimeException("exception while generating json object");
        }
        return jsonObject.toString();
    }

    private Response performQueryOperation(ChaincodeStub chaincodeStub, List<String> paramList) {
        if (listHasDifferentSizeThen(paramList, 1)) {
            return newErrorResponse("incorrect number of arguments");
        }
        String product_id = chaincodeStub.getStringState(paramList.get(0));

        if (Objects.isNull(pr)) {
            return newErrorResponse("product_id of provided fabric not found");
        }
        return newSuccessResponse(product_id);
    }

    private Response performInvokeOperation(ChaincodeStub chaincodeStub, List<String> paramList) {
        if (listHasDifferentSizeThen(paramList, 2)) {
            return newErrorResponse("incorrect number of arguments");
        }
        String product_id = paramList.get(0);
        String sustainabilityToUpdate = paramList.get(1);

        if (!StringUtils.isNumeric(sustainabilityToUpdate)) {
            return newErrorResponse("provided sustainability is not numeric value !");
        }

        String sustainabilityFromLedger = chaincodeStub.getStringState(product_id);

        if (StringUtils.isEmpty(sustainabilityFromLedger)) {
            chaincodeStub.putStringState(product_id, sustainabilityToUpdate);
        } else {
            // if (Float.valueOf(sustainabilityFromLedger).compareTo(Float.valueOf(sustainabilityToUpdate)) >= 0) {
            //     return newErrorResponse("incorrect value");
            // }
            chaincodeStub.putStringState(product_id, sustainabilityToUpdate);
        }
        return newSuccessResponse();
    }

    private boolean listHasDifferentSizeThen(List<String> list, int expectedElementsNumber) {
        return list.size() != expectedElementsNumber;

    }

    public static void main(String [] args){
        new CollatzChaincode().start(args);
    }


}
