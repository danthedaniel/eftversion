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

  // Render a favicon image
  var set_favicon = function(version) {
    var text = version.split(".").slice(0, 2).join(".");
    var char_width = 3;
    var x_pos = Math.floor((16 - text.length * char_width) / 2);

    var canvas = document.createElement("canvas");
    canvas.width = 16;
    canvas.height = 16;

    // Fill in background
    var ctx = canvas.getContext("2d");
    ctx.fillStyle = "#222";
    ctx.fillRect(0, 0, 16, 16);

    // Render text
    ctx.fillStyle = '#FFF';
    ctx.font = "bold 8px sans-serif";
    ctx.fillText(text, x_pos, 11);

    // Update favicon
    var favicon = document.getElementById("favicon");
    favicon.href = canvas.toDataURL("image/x-icon");
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
  set_favicon(game_version.textContent);

  setInterval(function() {
    API.get_version(function(data) {
      game_version.textContent = data.client;
      launcher_version.textContent = data.launcher;
      set_favicon(data.client);
    });
  }, request_delay);
})()
