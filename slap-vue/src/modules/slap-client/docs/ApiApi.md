# SlapClient.ApiApi

All URIs are relative to *http://localhost:8000/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**listWordFrequencys**](ApiApi.md#listWordFrequencys) | **GET** /api/songs/{song_id}/word-frequency | 



## listWordFrequencys

> [AnyType] listWordFrequencys(songId, opts)



### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.ApiApi();
let songId = "songId_example"; // String | 
let opts = {
  'vizFormat': "vizFormat_example" // String | The selected data format for visualization
};
apiInstance.listWordFrequencys(songId, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **songId** | **String**|  | 
 **vizFormat** | **String**| The selected data format for visualization | [optional] 

### Return type

[**[AnyType]**](AnyType.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

