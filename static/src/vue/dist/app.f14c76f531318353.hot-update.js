"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(typeof self !== 'undefined' ? self : this)["webpackHotUpdatefrontend"]("app",{

/***/ "./node_modules/@vue/vue-loader-v15/lib/index.js??vue-loader-options!./src/App.vue?vue&type=script&lang=js&":
/*!******************************************************************************************************************!*\
  !*** ./node_modules/@vue/vue-loader-v15/lib/index.js??vue-loader-options!./src/App.vue?vue&type=script&lang=js& ***!
  \******************************************************************************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

eval("__webpack_require__.r(__webpack_exports__);\n\n/* harmony default export */ __webpack_exports__[\"default\"] = ({\n  mounted() {\n    this.initGoogleAuth();\n    this.renderGoogleAuthButton();\n  },\n\n  data() {\n    return {\n      profile: null\n    };\n  },\n\n  methods: {\n    onSignIn(user) {\n      const profile = user.getBasicProfile();\n      const fullName = profile.getName();\n      const email = profile.getEmail();\n      const imageUrl = profile.getImageUrl();\n      this.profile = { fullName, email, imageUrl };\n    },\n\n    signOut() {\n      var auth2 = window.gapi.auth2.getAuthInstance();\n      auth2.signOut().then(() => {\n        console.log(\"User signed out\");\n        this.profile = null;\n      });\n    },\n\n    initGoogleAuth() {\n      window.gapi.load(\"auth2\", function () {\n        window.gapi.auth2.init();\n      });\n    },\n\n    renderGoogleAuthButton() {\n      window.gapi.signin2.render(\"g-signin2\", {\n        onsuccess: this.onSignIn\n      });\n    }\n  }\n});\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9ub2RlX21vZHVsZXMvQHZ1ZS92dWUtbG9hZGVyLXYxNS9saWIvaW5kZXguanM/P3Z1ZS1sb2FkZXItb3B0aW9ucyEuL3NyYy9BcHAudnVlP3Z1ZSZ0eXBlPXNjcmlwdCZsYW5nPWpzJi5qcyIsIm1hcHBpbmdzIjoiOztBQVNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9mcm9udGVuZC9zcmMvQXBwLnZ1ZT8xMWM0Il0sInNvdXJjZXNDb250ZW50IjpbIjx0ZW1wbGF0ZT5cbiAgPGRpdiB2LXNob3c9XCIhcHJvZmlsZVwiIGlkPVwiZy1zaWduaW4yXCI+PC9kaXY+XG4gIDxkaXYgdi1pZj1cInByb2ZpbGVcIj5cbiAgICA8cHJlPnt7IHByb2ZpbGUgfX08L3ByZT5cbiAgICA8YnV0dG9uIEBjbGljaz1cInNpZ25PdXRcIj5TaWduIE91dDwvYnV0dG9uPlxuICA8L2Rpdj5cbjwvdGVtcGxhdGU+XG5cbjxzY3JpcHQ+XG5leHBvcnQgZGVmYXVsdCB7XG4gIG1vdW50ZWQoKSB7XG4gICAgdGhpcy5pbml0R29vZ2xlQXV0aCgpO1xuICAgIHRoaXMucmVuZGVyR29vZ2xlQXV0aEJ1dHRvbigpO1xuICB9LFxuXG4gIGRhdGEoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHByb2ZpbGU6IG51bGxcbiAgICB9O1xuICB9LFxuXG4gIG1ldGhvZHM6IHtcbiAgICBvblNpZ25Jbih1c2VyKSB7XG4gICAgICBjb25zdCBwcm9maWxlID0gdXNlci5nZXRCYXNpY1Byb2ZpbGUoKTtcbiAgICAgIGNvbnN0IGZ1bGxOYW1lID0gcHJvZmlsZS5nZXROYW1lKCk7XG4gICAgICBjb25zdCBlbWFpbCA9IHByb2ZpbGUuZ2V0RW1haWwoKTtcbiAgICAgIGNvbnN0IGltYWdlVXJsID0gcHJvZmlsZS5nZXRJbWFnZVVybCgpO1xuICAgICAgdGhpcy5wcm9maWxlID0geyBmdWxsTmFtZSwgZW1haWwsIGltYWdlVXJsIH07XG4gICAgfSxcblxuICAgIHNpZ25PdXQoKSB7XG4gICAgICB2YXIgYXV0aDIgPSB3aW5kb3cuZ2FwaS5hdXRoMi5nZXRBdXRoSW5zdGFuY2UoKTtcbiAgICAgIGF1dGgyLnNpZ25PdXQoKS50aGVuKCgpID0+IHtcbiAgICAgICAgY29uc29sZS5sb2coXCJVc2VyIHNpZ25lZCBvdXRcIik7XG4gICAgICAgIHRoaXMucHJvZmlsZSA9IG51bGw7XG4gICAgICB9KTtcbiAgICB9LFxuXG4gICAgaW5pdEdvb2dsZUF1dGgoKSB7XG4gICAgICB3aW5kb3cuZ2FwaS5sb2FkKFwiYXV0aDJcIiwgZnVuY3Rpb24gKCkge1xuICAgICAgICB3aW5kb3cuZ2FwaS5hdXRoMi5pbml0KCk7XG4gICAgICB9KTtcbiAgICB9LFxuXG4gICAgcmVuZGVyR29vZ2xlQXV0aEJ1dHRvbigpIHtcbiAgICAgIHdpbmRvdy5nYXBpLnNpZ25pbjIucmVuZGVyKFwiZy1zaWduaW4yXCIsIHtcbiAgICAgICAgb25zdWNjZXNzOiB0aGlzLm9uU2lnbkluXG4gICAgICB9KTtcbiAgICB9XG4gIH1cbn07XG48L3NjcmlwdD5cblxuXG48c3R5bGU+XG4jYXBwIHtcbiAgZm9udC1mYW1pbHk6IEF2ZW5pciwgSGVsdmV0aWNhLCBBcmlhbCwgc2Fucy1zZXJpZjtcbiAgLXdlYmtpdC1mb250LXNtb290aGluZzogYW50aWFsaWFzZWQ7XG4gIC1tb3otb3N4LWZvbnQtc21vb3RoaW5nOiBncmF5c2NhbGU7XG4gIHRleHQtYWxpZ246IGNlbnRlcjtcbiAgY29sb3I6ICMyYzNlNTA7XG59XG5cbm5hdiB7XG4gIHBhZGRpbmc6IDMwcHg7XG59XG5cbm5hdiBhIHtcbiAgZm9udC13ZWlnaHQ6IGJvbGQ7XG4gIGNvbG9yOiAjMmMzZTUwO1xufVxuXG5uYXYgYS5yb3V0ZXItbGluay1leGFjdC1hY3RpdmUge1xuICBjb2xvcjogIzQyYjk4Mztcbn1cbjwvc3R5bGU+XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///./node_modules/@vue/vue-loader-v15/lib/index.js??vue-loader-options!./src/App.vue?vue&type=script&lang=js&\n");

/***/ }),

/***/ "./node_modules/@vue/vue-loader-v15/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/@vue/vue-loader-v15/lib/index.js??vue-loader-options!./src/App.vue?vue&type=template&id=7ba5bd90&":
/*!**************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/@vue/vue-loader-v15/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/@vue/vue-loader-v15/lib/index.js??vue-loader-options!./src/App.vue?vue&type=template&id=7ba5bd90& ***!
  \**************************************************************************************************************************************************************************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"render\": function() { return /* binding */ render; },\n/* harmony export */   \"staticRenderFns\": function() { return /* binding */ staticRenderFns; }\n/* harmony export */ });\nvar render = function () {}\nvar staticRenderFns = []\n\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9ub2RlX21vZHVsZXMvQHZ1ZS92dWUtbG9hZGVyLXYxNS9saWIvbG9hZGVycy90ZW1wbGF0ZUxvYWRlci5qcz8/cnVsZVNldFsxXS5ydWxlc1syXSEuL25vZGVfbW9kdWxlcy9AdnVlL3Z1ZS1sb2FkZXItdjE1L2xpYi9pbmRleC5qcz8/dnVlLWxvYWRlci1vcHRpb25zIS4vc3JjL0FwcC52dWU/dnVlJnR5cGU9dGVtcGxhdGUmaWQ9N2JhNWJkOTAmLmpzIiwibWFwcGluZ3MiOiI7Ozs7O0FBQUE7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZnJvbnRlbmQvLi9zcmMvQXBwLnZ1ZT8xMzlhIl0sInNvdXJjZXNDb250ZW50IjpbInZhciByZW5kZXIgPSBmdW5jdGlvbiAoKSB7fVxudmFyIHN0YXRpY1JlbmRlckZucyA9IFtdXG5cbmV4cG9ydCB7IHJlbmRlciwgc3RhdGljUmVuZGVyRm5zIH0iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///./node_modules/@vue/vue-loader-v15/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/@vue/vue-loader-v15/lib/index.js??vue-loader-options!./src/App.vue?vue&type=template&id=7ba5bd90&\n");

/***/ })

},
/******/ function(__webpack_require__) { // webpackRuntimeModules
/******/ /* webpack/runtime/getFullHash */
/******/ !function() {
/******/ 	__webpack_require__.h = function() { return "a7261e9ff622af05"; }
/******/ }();
/******/ 
/******/ }
);