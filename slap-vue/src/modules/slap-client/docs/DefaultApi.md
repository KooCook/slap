# SlapClient.DefaultApi

All URIs are relative to *http://localhost:8000/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**listSongWordFrequencyPlots**](DefaultApi.md#listSongWordFrequencyPlots) | **GET** /songs/{song_id}/word-frequency/plot | 
[**listWordRandomizations**](DefaultApi.md#listWordRandomizations) | **GET** /songs/words/randomize | 
[**listWords**](DefaultApi.md#listWords) | **GET** /songs/{song_id}/words | 
[**retrieveRepetitionMatrixPlot**](DefaultApi.md#retrieveRepetitionMatrixPlot) | **GET** /plot/rep-matrix/{song_id} | 
[**retrieveSong**](DefaultApi.md#retrieveSong) | **GET** /songs/{id}/ | 
[**slapFlaskPublicControllersSongsGetParameterizedWordPopularitySingle**](DefaultApi.md#slapFlaskPublicControllersSongsGetParameterizedWordPopularitySingle) | **GET** /song/{song_id}/word_popularity | 
[**slapFlaskPublicControllersSongsGetSong**](DefaultApi.md#slapFlaskPublicControllersSongsGetSong) | **GET** /song | 
[**slapFlaskPublicControllersSongsGetSongGenres**](DefaultApi.md#slapFlaskPublicControllersSongsGetSongGenres) | **GET** /song/genres | 
[**slapFlaskPublicControllersSongsGetSongMetrics**](DefaultApi.md#slapFlaskPublicControllersSongsGetSongMetrics) | **GET** /song/{song_id}/metrics | 
[**slapFlaskPublicControllersSongsGetSongs**](DefaultApi.md#slapFlaskPublicControllersSongsGetSongs) | **GET** /songs | 
[**slapListRepetitionPopularityPlots**](DefaultApi.md#slapListRepetitionPopularityPlots) | **GET** /plot/rep-pop | 



## listSongWordFrequencyPlots

> Object listSongWordFrequencyPlots(songId)



### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
let songId = "songId_example"; // String | 
apiInstance.listSongWordFrequencyPlots(songId, (error, data, response) => {
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

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listWordRandomizations

> InlineResponse2003 listWordRandomizations()



### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
apiInstance.listWordRandomizations((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listWords

> InlineResponse2001 listWords(songId)



A list of words in the given song lyrics

### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
let songId = "songId_example"; // String | 
apiInstance.listWords(songId, (error, data, response) => {
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

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## retrieveRepetitionMatrixPlot

> String retrieveRepetitionMatrixPlot(songId)



View to list all users in the system.  * Requires token authentication. * Only admin users are able to access this view.

### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
let songId = "songId_example"; // String | 
apiInstance.retrieveRepetitionMatrixPlot(songId, (error, data, response) => {
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

### Return type

**String**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: text/csv


## retrieveSong

> Song retrieveSong(id)



An API endpoint that allows songs to be viewed.

### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
let id = "id_example"; // String | A unique integer value identifying this song.
apiInstance.retrieveSong(id, (error, data, response) => {
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
 **id** | **String**| A unique integer value identifying this song. | 

### Return type

[**Song**](Song.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## slapFlaskPublicControllersSongsGetParameterizedWordPopularitySingle

> [InlineResponse2002] slapFlaskPublicControllersSongsGetParameterizedWordPopularitySingle(songId, wordCountWeight, popularityWeight, opts)



Returns word popularity index

### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
let songId = 519; // String | The ID of the song
let wordCountWeight = 12; // Number | The given weight of word count
let popularityWeight = 12; // Number | The given popularity index of word count
let opts = {
  'popularityIndicator': youtube_views // String | The given popularity indicator
};
apiInstance.slapFlaskPublicControllersSongsGetParameterizedWordPopularitySingle(songId, wordCountWeight, popularityWeight, opts, (error, data, response) => {
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
 **songId** | **String**| The ID of the song | 
 **wordCountWeight** | **Number**| The given weight of word count | 
 **popularityWeight** | **Number**| The given popularity index of word count | 
 **popularityIndicator** | **String**| The given popularity indicator | [optional] 

### Return type

[**[InlineResponse2002]**](InlineResponse2002.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## slapFlaskPublicControllersSongsGetSong

> [Song] slapFlaskPublicControllersSongsGetSong(title, artist)



Returns a song matching the query

### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
let title = Begin Again; // String | The title of a song
let artist = Taylor Swift; // String | The artist of a song
apiInstance.slapFlaskPublicControllersSongsGetSong(title, artist, (error, data, response) => {
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
 **title** | **String**| The title of a song | 
 **artist** | **String**| The artist of a song | 

### Return type

[**[Song]**](Song.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## slapFlaskPublicControllersSongsGetSongGenres

> [Genre] slapFlaskPublicControllersSongsGetSongGenres()



Returns all genres

### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
apiInstance.slapFlaskPublicControllersSongsGetSongGenres((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**[Genre]**](Genre.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## slapFlaskPublicControllersSongsGetSongMetrics

> [SongMetrics] slapFlaskPublicControllersSongsGetSongMetrics(songId, opts)



Returns song metrics

### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
let songId = 12; // String | The ID of the song
let opts = {
  'forGraph': true // Boolean | Whether to return additional parameters for making a graph
};
apiInstance.slapFlaskPublicControllersSongsGetSongMetrics(songId, opts, (error, data, response) => {
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
 **songId** | **String**| The ID of the song | 
 **forGraph** | **Boolean**| Whether to return additional parameters for making a graph | [optional] 

### Return type

[**[SongMetrics]**](SongMetrics.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## slapFlaskPublicControllersSongsGetSongs

> InlineResponse200 slapFlaskPublicControllersSongsGetSongs(opts)



Returns all songs

### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
let opts = {
  'page': 1, // Number | The page number
  'title': "title_example" // String | The partial title of this song
};
apiInstance.slapFlaskPublicControllersSongsGetSongs(opts, (error, data, response) => {
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
 **page** | **Number**| The page number | [optional] 
 **title** | **String**| The partial title of this song | [optional] 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## slapListRepetitionPopularityPlots

> Object slapListRepetitionPopularityPlots(opts)



Return a list of all users.

### Example

```javascript
import SlapClient from 'slap-client';

let apiInstance = new SlapClient.DefaultApi();
let opts = {
  'popFacet': youtube_view, // Number | The page number
  'repFacet': compressibility // Number | The page number
};
apiInstance.slapListRepetitionPopularityPlots(opts, (error, data, response) => {
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
 **popFacet** | **Number**| The page number | [optional] 
 **repFacet** | **Number**| The page number | [optional] 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

