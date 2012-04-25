// Generated by CoffeeScript 1.3.1
var __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

define(['chaplin/view', 'text!templates/navigation.hbs'], function(View, template) {
  'use strict';

  var NavigationView;
  return NavigationView = (function(_super) {

    __extends(NavigationView, _super);

    NavigationView.name = 'NavigationView';

    function NavigationView() {
      return NavigationView.__super__.constructor.apply(this, arguments);
    }

    NavigationView.prototype.id = 'navigation';

    NavigationView.prototype.tagName = 'ul';

    NavigationView.prototype.className = "nav nav-pills";

    NavigationView.prototype.containerSelector = '#navigation-wrapper';

    NavigationView.prototype.autoRender = true;

    NavigationView.template = template;

    NavigationView.prototype.initialize = function() {
      NavigationView.__super__.initialize.apply(this, arguments);
      this.subscribeEvent('startupController', this.render);
      this.modelBind('change:routes', this.render);
      return this.delegate('click', '.n-signin a', this.showLoginDialog);
    };

    NavigationView.prototype.showLoginDialog = function(ev) {
      console.log(ev);
      return $("#dialogs #login").modal({
        show: true
      });
    };

    return NavigationView;

  })(View);
});