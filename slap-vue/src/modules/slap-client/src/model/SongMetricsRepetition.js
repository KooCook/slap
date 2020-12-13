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

import ApiClient from '../ApiClient';
import SongMetricsRepetitionBow from './SongMetricsRepetitionBow';

/**
 * The SongMetricsRepetition model module.
 * @module model/SongMetricsRepetition
 * @version 1.0.0
 */
class SongMetricsRepetition {
    /**
     * Constructs a new <code>SongMetricsRepetition</code>.
     * @alias module:model/SongMetricsRepetition
     */
    constructor() { 
        
        SongMetricsRepetition.initialize(this);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj) { 
    }

    /**
     * Constructs a <code>SongMetricsRepetition</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/SongMetricsRepetition} obj Optional instance to populate.
     * @return {module:model/SongMetricsRepetition} The populated <code>SongMetricsRepetition</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new SongMetricsRepetition();

            if (data.hasOwnProperty('bow')) {
                obj['bow'] = SongMetricsRepetitionBow.constructFromObject(data['bow']);
            }
        }
        return obj;
    }


}

/**
 * @member {module:model/SongMetricsRepetitionBow} bow
 */
SongMetricsRepetition.prototype['bow'] = undefined;






export default SongMetricsRepetition;
