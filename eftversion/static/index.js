(function() {
  var ajax = function(method, url, success, error) {
    var request = new XMLHttpRequest();
    request.open(method, url, true);

    request.onload = function() {
      if (request.status >= 200 && request.status < 400) {
        success(JSON.parse(request.responseText));
      } else {
        error(request);
      }
    };

    request.send();
  };

  // JSON API functions
  var API = {
    get_version: function(success, error) {
      ajax("GET", "/versions.json", success, error);
    }
  };

  var request_delay = 30 * 1000; // 30 seconds
  var game_version = document.getElementById("game-version");
  var launcher_version = document.getElementById("launcher-version");

  setInterval(function() {
    API.get_version(function(data) {
      game_version.textContent = data.client;
      launcher_version.textContent = data.launcher;
    });
  }, request_delay);
})()
