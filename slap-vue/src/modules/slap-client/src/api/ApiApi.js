/**
 * Song Lyrics & Popularity (SLAP)
 * This API provides the metrics and the metadata of songs in order to analyze Lyrics & Popularity
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */


import ApiClient from "../ApiClient";
import AnyType from '../model/AnyType';

/**
* Api service.
* @module api/ApiApi
* @version 1.0.0
*/
export default class ApiApi {

    /**
    * Constructs a new ApiApi. 
    * @alias module:api/ApiApi
    * @class
    * @param {module:ApiClient} [apiClient] Optional API client implementation to use,
    * default to {@link module:ApiClient#instance} if unspecified.
    */
    constructor(apiClient) {
        this.apiClient = apiClient || ApiClient.instance;
    }


    /**
     * Callback function to receive the result of the listWordFrequencys operation.
     * @callback module:api/ApiApi~listWordFrequencysCallback
     * @param {String} error Error message, if any.
     * @param {Array.<module:model/AnyType>} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * @param {String} songId 
     * @param {Object} opts Optional parameters
     * @param {String} opts.vizFormat The selected data format for visualization
     * @param {module:api/ApiApi~listWordFrequencysCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link Array.<module:model/AnyType>}
     */
    listWordFrequencys(songId, opts, callback) {
      opts = opts || {};
      let postBody = null;
      // verify the required parameter 'songId' is set
      if (songId === undefined || songId === null) {
        throw new Error("Missing the required parameter 'songId' when calling listWordFrequencys");
      }

      let pathParams = {
        'song_id': songId
      };
      let queryParams = {
        'viz_format': opts['vizFormat']
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = [];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = [AnyType];
      return this.apiClient.callApi(
        '/api/songs/{song_id}/word-frequency', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }


}
