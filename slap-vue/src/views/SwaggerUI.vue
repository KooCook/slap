<template>
    <div class="container-fluid" id="myDomId">

    </div>
</template>
<script>
    import SwaggerUI from 'swagger-ui'
    import 'swagger-ui/dist/swagger-ui.css'
    const SongLyricsPopularitySlap = require("slap-client");
    const SwaggerUIBundle = require('swagger-ui-dist').SwaggerUIBundle
    export default {
        name: "SwaggerUI",
        mounted() {
            const api = new SongLyricsPopularitySlap.DefaultApi();
            api.listSwaggerSpecs((error, data) => {
                if (error) {
                    console.error(error);
                } else {
                    SwaggerUI({
                        dom_id: '#myDomId',
                        spec: data,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIBundle.SwaggerUIStandalonePreset
                        ],
                        layout: "BaseLayout"
                    })
                }
            })

        }
    }
</script>

<style scoped>

</style>
