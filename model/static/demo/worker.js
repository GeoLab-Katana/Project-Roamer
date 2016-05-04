'use strict';

// generate supercluster.js from the repo root with:
// browserify index.js -s supercluster > demo/supercluster.js

importScripts('supercluster.js');

var now = Date.now();

var index;

var updateUrl = '/data/json';
var updateUrlBase = '/data/json';
var updateCallback = function (geojson) {
    console.log('loaded ' + geojson.length + ' points JSON in ' + ((Date.now() - now) / 1000) + 's');

    index = supercluster({
        log: true,
        radius: 60,
        extent: 256,
        maxZoom: 17
    }).load(geojson.features);

    console.log(index.getTile(0, 0, 0));

    postMessage({ready: true});
};

getJSON(updateUrl, updateCallback);

self.onmessage = function (e) {
    if (e.data) {
        if (e.data.url || e.data.url == ''){
            updateUrlBase = updateUrl+e.data.url;
            getJSON(updateUrlBase, updateCallback);
        }
        var zoom = e.data.heatmap ? 16 : e.data.zoom;
        postMessage(index.getClusters(e.data.bbox, zoom));
    }
};

function getJSON(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.open('GET', url, true);
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.onload = function () {
        if (xhr.readyState === 4 && xhr.status >= 200 && xhr.status < 300 && xhr.response) {
            callback(xhr.response);
        }
    };
    xhr.send();
}
