/** 
 * Special python-js bridge function.
 * Fakes the api if it's missing.
 */
var get_bridge = function() {
  if (!window.bridge) {
    window.bridge = {
      'ajax' : function(url, callback) {
        jQuery.ajax({
          type: "GET",
          url: url,
          dataType: "html",
          success: function(data) {
            try {
              callback(data);
            }
            catch(e) {
              alert("Failed to invoke callback: " + e.toString());
            }
          },
          error: function (xhr, ajaxOptions, thrownError) {
            alert("Failed to invoke native ajax");
            alert(xhr.status);
            alert(thrownError);
          }
        });
      },
      'quit' : function() {
        alert("Quit mock");
      },
      'trigger' : function(id, value) {
        alert("Trigger mock: " + id + " --> " + value);
        return "{}";
      },
    };
  }
  else {
    window.bridge.ajax = function(url, callback) {
      callback(window.bridge._ajax(url));
    };
  }
  return window.bridge;
};

/** 
 * JS-app bridge helper.
 * Usage: var result = trigger("id", { "Data" : 10 });
 */
var trigger = function(id, data) {
  if (!data)
    data = {}
  var rtn = {}
  try {
    var bridge = get_bridge();
    raw = bridge.trigger(id, JSON.stringify(data));
    try {
      if (raw == "")
        rtn = ""
      else
        rtn = $.parseJSON(raw);
    }
    catch(e) {
      alert("Failed to parse JSON: '" + raw + "': " + e.toString());
    }
  }
  catch(e) {
    alert("Failed to invoke bridge.trigger: " + e.toString());
  }
  return rtn;
};

/** Set / get pref helpers */
var preference = function(key) {
  return trigger("Utils.get_preference", key).value;
};

/** 
 * Customized ajax helper 
 * Usage: ajax("target", function(data) { ... });
 */
var ajax = function(url, callback) {
  try {
    var bridge = get_bridge();
    bridge.ajax(url, callback);
  }
  catch(e) {
    alert("Failed to invoke bridge.ajax: " + e.toString());
  }
};

/** 
 * Template helper
 *
 * Loads the given template url into the preceeding element.
 *
 * Use like:
 *
 *   <div>Content to replace</div>
 *   <script>template("/inc/header.html")</script>
 */
var template = function(url) {
  var target = $('script').last().prev();
  ajax(url, function(data) {
    target.html(data);
  });
};

/**
 * Helpers to fetch flash notices and display them.
 */
var flash_update = function() {
  try {
    message = trigger("Utils.flash")
    if (message.result) {
      e = document.createElement("div");
      if (message.level == "FAILURE")
        e.className = "alert alert-error";
      else if (message.level == "SUCCESS")
        e.className = "alert alert-success";
      else
        e.className = "alert";
      html = "<button type='button' class='close' data-dismiss='alert'>&times;</button>";
      if (message.level == "FAILURE")
        html += "<strong>Warning!</strong> ";
      html += message.result;
      $(e).html(html);
      $("#alerts").append(e);
      setTimeout(flash_update, 100);
    }
    else {
      setTimeout(flash_update, 1000);
    }
  }
  catch(e) {
    alert("Failed while trying to fetch flash messages: " + e.toString())
  }
};
setTimeout(flash_update, 1000);
