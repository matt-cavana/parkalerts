$(document).ready(function () {
    console.log('Document is ready');

    const bothButton = $('#bothButton');
    const mapButton = $('#mapButton');
    const listButton = $('#listButton');

    if (bothButton.length) {
        bothButton.on('click', function () {
            window.location.href = bothButton.data('url');
        });
    }

    if (mapButton.length) {
        mapButton.on('click', function () {
            window.location.href = mapButton.data('url');
        });
    }

    if (listButton.length) {
        listButton.on('click', function () {
            window.location.href = listButton.data('url');
        });
    }

    const currentPage = window.location.pathname;
    if (currentPage.includes('/map/')) {
        if (mapButton.length) mapButton.addClass('active');
    } else if (currentPage.includes('/list/')) {
        if (listButton.length) listButton.addClass('active');
    } else {
        if (bothButton.length) bothButton.addClass('active');
    }

    const mapElement = $('#map');
    let geojson;

    if (mapElement.length) {
        mapboxgl.accessToken = 'pk.eyJ1IjoibWF0dC1jYXZhbmEiLCJhIjoiY2xna3AyeTdnMHVpZTNvbHZ5dnJmbzg1dSJ9.W4ztKJK-2kSbtsjsRZ-srw';
        const map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v12?events=false',
            center: [122.298333, -25.328056],
            zoom: 5
        });

        map.on('load', function () {
            map.resize();

            // Load GeoJSON data
            const alertsDataElement = $('#alerts-data');
            if (alertsDataElement.length) {
                const alerts = JSON.parse(alertsDataElement.text());

                geojson = {
                    type: 'FeatureCollection',
                    features: alerts.map(alert => ({
                        type: 'Feature',
                        properties: {
                            title: alert.title,
                            details: alert.details,
                            affected_sites: alert.affected_sites || 'N/A',
                            website_link: alert.website_link ? $('<div>').html(alert.website_link).text() : 'N/A',
                            icon_url: alert.icon_url,
                            location: alert.location,
                            start_date: alert.start_date,
                            end_date: alert.end_date,
                            time_elapsed: alert.time_elapsed,
                            attachment: alert.attachment,
                            attachment_name: alert.attachment_name,
                            kml_file_url: alert.kml_file_url
                        },
                        geometry: {
                            type: 'Point',
                            coordinates: [alert.longitude, alert.latitude]
                        }
                    }))
                };

                // Add Geoserver Layer
                map.addSource('wms-source', {
                    'type': 'raster',
                    'tiles': [
                        'https://kmi.dbca.wa.gov.au/geoserver/public/wms?service=WMS&version=1.1.0&request=GetMap&layers=public%3Adbca_trails_public&bbox={bbox-epsg-3857}&width=256&height=256&srs=EPSG%3A3857&styles=&format=image/png&transparent=true'
                    ],
                    'tileSize': 256
                });

                map.addLayer({
                    'id': 'wms-layer',
                    'type': 'raster',
                    'source': 'wms-source',
                    'paint': {}
                });

                // Toggle switch for WMS layer
                $('#wmsToggle').on('change', function () {
                    const visibility = this.checked ? 'visible' : 'none';
                    map.setLayoutProperty('wms-layer', 'visibility', visibility);
                });

                // Add KML layers for each alert with KML file URL
                alerts.forEach(alert => {
                    if (alert.kml_file_url) {
                        const kmlSourceId = `kml-${alert.title}`;
                        if (!map.getSource(kmlSourceId)) {
                            fetch(alert.kml_file_url)
                                .then(response => response.text())
                                .then(kmlText => {
                                    const parser = new DOMParser();
                                    const kml = parser.parseFromString(kmlText, 'text/xml');
                                    const kmlGeoJson = toGeoJSON.kml(kml);
                                    map.addSource(kmlSourceId, {
                                        type: 'geojson',
                                        data: kmlGeoJson,
                                    });
                                    map.addLayer({
                                        id: kmlSourceId,
                                        type: 'line',
                                        source: kmlSourceId,
                                        paint: {
                                            'line-color': '#FF0000',
                                            'line-width': 3
                                        }
                                    });
                                })
                                .catch(error => console.error('Error loading KML:', error));
                        }
                    }
                });

                // Add the geojson source and layers for alerts
                map.addSource('alerts', {
                    type: 'geojson',
                    data: geojson,
                    cluster: true,
                    clusterMaxZoom: 14,
                    clusterRadius: 50
                });

                map.addLayer({
                    id: 'clusters',
                    type: 'circle',
                    source: 'alerts',
                    filter: ['has', 'point_count'],
                    paint: {
                        'circle-color': [
                            'step',
                            ['get', 'point_count'],
                            '#51bbd6',
                            100,
                            '#f1f075',
                            750,
                            '#f28cb1'
                        ],
                        'circle-radius': [
                            'step',
                            ['get', 'point_count'],
                            20,
                            100,
                            30,
                            750,
                            40
                        ]
                    }
                });

                map.addLayer({
                    id: 'cluster-count',
                    type: 'symbol',
                    source: 'alerts',
                    filter: ['has', 'point_count'],
                    layout: {
                        'text-field': '{point_count_abbreviated}',
                        'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                        'text-size': 12
                    }
                });

                alerts.forEach(alert => {
                    const iconUrl = alert.icon_url;
                    map.loadImage(iconUrl, function (error, image) {
                        if (error) throw error;
                        if (!map.hasImage(iconUrl)) {
                            map.addImage(iconUrl, image);
                        }
                    });
                });

                map.addLayer({
                    id: 'unclustered-point',
                    type: 'symbol',
                    source: 'alerts',
                    filter: ['!', ['has', 'point_count']],
                    layout: {
                        'icon-image': ['concat', ['get', 'icon_url']],
                        'icon-size': 0.75
                    }
                });

                // Add popup for unclustered points
                map.on('click', 'unclustered-point', function (e) {
                    console.log("Unclustered point clicked");

                    const coordinates = e.features[0].geometry.coordinates.slice();
                    const properties = e.features[0].properties;

                    console.log("Coordinates:", coordinates);
                    console.log("Properties:", properties);

                    const attachmentLink = properties.attachment ? `<p><strong>Attachment:</strong> <a href="${properties.attachment}" target="_blank">${properties.attachment_name}</a></p>` : '';
                    const affectedSitesContent = properties.affected_sites !== 'N/A' ? `<p><strong>Affected Sites:</strong> ${properties.affected_sites}</p>` : '';
                    const websiteLinkContent = properties.website_link !== 'N/A' ? `<p><strong>Website:</strong> <a href="${properties.website_link}" target="_blank">${properties.website_link}</a></p>` : '';

                    const modalContent = `
                        <h2 class="text-base font-medium text-type-primary xs:text-xl alert-title">
                            <img src="${properties.icon_url}" alt="Icon" style="vertical-align: middle; margin-right: 10px;">
                            ${properties.title}
                        </h2>
                        <p><strong>Location:</strong> ${properties.location}</p>
                        <p><strong>Start Date:</strong> ${properties.start_date}</p>
                        <p><strong>End Date:</strong> ${properties.end_date || 'N/A'}</p>
                        <p>${properties.details}</p>
                        ${affectedSitesContent}
                        ${websiteLinkContent}
                        ${attachmentLink}
                        `;

                    $('#modalDetails').html(modalContent);
                    $('#alertModal').show().css('z-index', '1000');
                    console.log("Modal Content:", modalContent);
                    console.log("Modal shown");
                });

                // Change the cursor to a pointer when the mouse is over the clusters or unclustered points layer
                map.on('mouseenter', 'clusters', function () {
                    map.getCanvas().style.cursor = 'pointer';
                });
                map.on('mouseleave', 'clusters', function () {
                    map.getCanvas().style.cursor = '';
                });
                map.on('mouseenter', 'unclustered-point', function () {
                    map.getCanvas().style.cursor = 'pointer';
                });
                map.on('mouseleave', 'unclustered-point', function () {
                    map.getCanvas().style.cursor = '';
                });

                // Zoom into the cluster when clicked
                map.on('click', 'clusters', function (e) {
                    const features = map.queryRenderedFeatures(e.point, {
                        layers: ['clusters']
                    });
                    const clusterId = features[0].properties.cluster_id;
                    map.getSource('alerts').getClusterExpansionZoom(clusterId, function (err, zoom) {
                        if (err) return;
                        map.easeTo({
                            center: features[0].geometry.coordinates,
                            zoom: zoom
                        });
                    });
                });

                // Add the event listener for the 'expand' button
                const expandButton = $('#expand');
                if (expandButton.length) {
                    expandButton.on('click', function () {
                        map.flyTo({ center: [122.298333, -25.328056], zoom: 5 });
                    });
                }
            }
        });

        $(window).on('resize', function () {
            map.resize();
        });

        // Search box functionality
        $('#searchBox').on('input', function () {
            var searchTerm = $(this).val().toLowerCase();

            // Filter alert items
            $('.alert-item').each(function () {
                var title = $(this).data('title').toLowerCase();
                var location = $(this).data('location').toLowerCase();
                var details = $(this).data('details').toLowerCase();

                if (title.includes(searchTerm) || location.includes(searchTerm) || details.includes(searchTerm)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });

            // Filter alert list items
            $('tbody tr').each(function () {
                var title = $(this).find('td:nth-child(2)').text().toLowerCase();
                var details = $(this).find('td:nth-child(3)').text().toLowerCase();
                var startDate = $(this).find('td:nth-child(4)').text().toLowerCase();
                var endDate = $(this).find('td:nth-child(5)').text().toLowerCase();
                var published = $(this).find('td:nth-child(6)').text().toLowerCase();

                if (title.includes(searchTerm) || details.includes(searchTerm) || startDate.includes(searchTerm) || endDate.includes(searchTerm) || published.includes(searchTerm)) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });

            // Filter map markers and clusters
            const filteredGeojson = {
                type: 'FeatureCollection',
                features: geojson.features.filter(feature => {
                    const title = feature.properties.title.toLowerCase();
                    const location = feature.properties.location.toLowerCase();
                    const details = feature.properties.details.toLowerCase();
                    return title.includes(searchTerm) || location.includes(searchTerm) || details.includes(searchTerm);
                })
            };

            map.getSource('alerts').setData(filteredGeojson);
        });
    }

    // Close the modal when clicking the close button
    $('.close').on('click', function () {
        $('#alertModal').hide();
    });

    // Close modal when clicking outside
    $(document).on('click', function (event) {
        if ($(event.target).is('#alertModal')) {
            $('#alertModal').hide();
        }
    });

    // Alert item click event
    $('.alert-item').on('click', function () {
        var title = $(this).data('title');
        var location = $(this).data('location');
        var startDate = $(this).data('start-date');
        var endDate = $(this).data('end-date');
        var details = $(this).data('details');
        var affectedSites = $(this).data('affected-sites');
        var websiteLink = $(this).data('website-link');
        var iconUrl = $(this).data('icon-url');
        var attachment = $(this).data('attachment');
        var attachmentName = $(this).data('attachment-name');

        var attachmentLink = attachment ? `<p><strong>Attachment:</strong> <a href="${attachment}" target="_blank">${attachmentName}</a></p>` : '';

        var affectedSitesContent = affectedSites !== 'N/A' ? `<p><strong>Affected Sites:</strong> ${affectedSites}</p>` : '';
        var websiteLinkContent = websiteLink !== 'N/A' ? `<p><strong>Website:</strong> <a href="${$('<div>').html(websiteLink).text()}" target="_blank">${$('<div>').html(websiteLink).text()}</a></p>` : '';

        var modalContent = `
            <h2 class="text-base font-medium text-type-primary xs:text-xl alert-title">
                <img src="${iconUrl}" alt="Icon" style="vertical-align: middle; margin-right: 10px;">
                ${title}
            </h2>
            <p><strong>Location:</strong> ${location}</p>
            <p><strong>Start Date:</strong> ${startDate}</p>
            <p><strong>End Date:</strong> ${endDate}</p>
            <p>${details}</p>
            ${affectedSitesContent}
            ${websiteLinkContent}
            ${attachmentLink}
        `;

        $('#modalDetails').html(modalContent);
        $('#alertModal').show().css('z-index', '1000');
    });
});
