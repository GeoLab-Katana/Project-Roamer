'use strict';

/*global L */

var map = L.map('map').setView([0, 0], 2);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var isHeatMap = false
var markers = getMarkers();

console.log(map);

var worker = new Worker('/static/demo/worker.js');
var ready = false;

worker.onmessage = function (e) {
    if (e.data.ready) {
        ready = true;
        update();
    } else {
        updateMarkers(e.data);
    }
};

function update() {
    if (!ready) return;
    var bounds = map.getBounds();
    worker.postMessage({
        bbox: [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()],
        zoom: map.getZoom()
    });
}

map.on('moveend', update);

function createClusterIcon(feature, latlng) {
    if (!feature.properties.cluster) return L.marker(latlng);

    var count = feature.properties.point_count;
    var size =
        count < 100 ? 'small' :
            count < 1000 ? 'medium' : 'large';
    var icon = L.divIcon({
        html: '<div><span>' + feature.properties.point_count_abbreviated + '</span></div>',
        className: 'marker-cluster marker-cluster-' + size,
        iconSize: L.point(40, 40)
    });
    return L.marker(latlng, {icon: icon});
}

function getMarkers() {
    if (markers) {
        map.removeLayer(markers);
    }
    if (!isHeatMap) {
        return L.geoJson(null, {
            pointToLayer: createClusterIcon
        }).addTo(map);
    }
    return L.heatLayer([], {
        radius: 25,
        blur: 20,
        minZoom: 0,
        maxZoom: 16
    }).addTo(map);
}

function updateMarkers(data) {
    if (!isHeatMap) {
        markers.clearLayers();
        markers.addData(data);
    } else {
        data.forEach(function (entry) {
            var num = entry.properties.cluster ? Math.pow(entry.properties.point_count, 1 / 3) : 1;
            for (var i = 0; i < num; i++) {
                var cord = entry.geometry.coordinates;
                markers.addLatLng([cord[1], cord[0]]);
            }
        })
    }
}
