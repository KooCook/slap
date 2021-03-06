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
import SongMetricsChart from './SongMetricsChart';
import SongMetricsRepetition from './SongMetricsRepetition';

/**
 * The SongMetrics model module.
 * @module model/SongMetrics
 * @version 1.0.0
 */
class SongMetrics {
    /**
     * Constructs a new <code>SongMetrics</code>.
     * @alias module:model/SongMetrics
     */
    constructor() { 
        
        SongMetrics.initialize(this);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj) { 
    }

    /**
     * Constructs a <code>SongMetrics</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:model/SongMetrics} obj Optional instance to populate.
     * @return {module:model/SongMetrics} The populated <code>SongMetrics</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new SongMetrics();

            if (data.hasOwnProperty('repetition')) {
                obj['repetition'] = SongMetricsRepetition.constructFromObject(data['repetition']);
            }
            if (data.hasOwnProperty('chart')) {
                obj['chart'] = SongMetricsChart.constructFromObject(data['chart']);
            }
        }
        return obj;
    }


}

/**
 * @member {module:model/SongMetricsRepetition} repetition
 */
SongMetrics.prototype['repetition'] = undefined;

/**
 * @member {module:model/SongMetricsChart} chart
 */
SongMetrics.prototype['chart'] = undefined;






export default SongMetrics;

