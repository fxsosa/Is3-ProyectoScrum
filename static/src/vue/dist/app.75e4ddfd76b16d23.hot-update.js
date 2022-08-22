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

eval("__webpack_require__.r(__webpack_exports__);\n\n/* harmony default export */ __webpack_exports__[\"default\"] = ({\n  mounted() {\n    this.initGoogleAuth();\n    this.renderGoogleAuthButton();\n  },\n\n  data() {\n    return {\n      profile: null\n    };\n  },\n\n  methods: {\n    onSignIn(user) {\n      const profile = user.getBasicProfile();\n      const fullName = profile.getName();\n      const email = profile.getEmail();\n      const imageUrl = profile.getImageUrl();\n      this.profile = { fullName, email, imageUrl };\n    },\n\n    signOut() {\n      var auth2 = window.gapi.auth2.getAuthInstance();\n      auth2.signOut().then(() => {\n        console.log(\"User signed out\");\n        this.profile = null;\n      });\n    },\n\n    initGoogleAuth() {\n      window.gapi.load(\"auth2\", function () {\n        window.gapi.auth2.init();\n      });\n    },\n\n    renderGoogleAuthButton() {\n      window.gapi.signin2.render(\"g-signin2\", {\n        onsuccess: this.onSignIn\n      });\n    }\n  }\n});\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiLi9ub2RlX21vZHVsZXMvQHZ1ZS92dWUtbG9hZGVyLXYxNS9saWIvaW5kZXguanM/P3Z1ZS1sb2FkZXItb3B0aW9ucyEuL3NyYy9BcHAudnVlP3Z1ZSZ0eXBlPXNjcmlwdCZsYW5nPWpzJi5qcyIsIm1hcHBpbmdzIjoiOztBQVdBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9mcm9udGVuZC9zcmMvQXBwLnZ1ZT8xMWM0Il0sInNvdXJjZXNDb250ZW50IjpbIjx0ZW1wbGF0ZT5cbiAgPGRpdj5cbiAgICAgIDxkaXYgdi1zaG93PVwiIXByb2ZpbGVcIiBpZD1cImctc2lnbmluMlwiPjwvZGl2PlxuICAgICAgPGRpdiB2LWlmPVwicHJvZmlsZVwiPlxuICAgICAgICA8cHJlPnt7IHByb2ZpbGUgfX08L3ByZT5cbiAgICAgICAgPGJ1dHRvbiBAY2xpY2s9XCJzaWduT3V0XCI+U2lnbiBPdXQ8L2J1dHRvbj5cbiAgICAgIDwvZGl2PlxuICAgIDwvZGl2PlxuPC90ZW1wbGF0ZT5cblxuPHNjcmlwdD5cbmV4cG9ydCBkZWZhdWx0IHtcbiAgbW91bnRlZCgpIHtcbiAgICB0aGlzLmluaXRHb29nbGVBdXRoKCk7XG4gICAgdGhpcy5yZW5kZXJHb29nbGVBdXRoQnV0dG9uKCk7XG4gIH0sXG5cbiAgZGF0YSgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgcHJvZmlsZTogbnVsbFxuICAgIH07XG4gIH0sXG5cbiAgbWV0aG9kczoge1xuICAgIG9uU2lnbkluKHVzZXIpIHtcbiAgICAgIGNvbnN0IHByb2ZpbGUgPSB1c2VyLmdldEJhc2ljUHJvZmlsZSgpO1xuICAgICAgY29uc3QgZnVsbE5hbWUgPSBwcm9maWxlLmdldE5hbWUoKTtcbiAgICAgIGNvbnN0IGVtYWlsID0gcHJvZmlsZS5nZXRFbWFpbCgpO1xuICAgICAgY29uc3QgaW1hZ2VVcmwgPSBwcm9maWxlLmdldEltYWdlVXJsKCk7XG4gICAgICB0aGlzLnByb2ZpbGUgPSB7IGZ1bGxOYW1lLCBlbWFpbCwgaW1hZ2VVcmwgfTtcbiAgICB9LFxuXG4gICAgc2lnbk91dCgpIHtcbiAgICAgIHZhciBhdXRoMiA9IHdpbmRvdy5nYXBpLmF1dGgyLmdldEF1dGhJbnN0YW5jZSgpO1xuICAgICAgYXV0aDIuc2lnbk91dCgpLnRoZW4oKCkgPT4ge1xuICAgICAgICBjb25zb2xlLmxvZyhcIlVzZXIgc2lnbmVkIG91dFwiKTtcbiAgICAgICAgdGhpcy5wcm9maWxlID0gbnVsbDtcbiAgICAgIH0pO1xuICAgIH0sXG5cbiAgICBpbml0R29vZ2xlQXV0aCgpIHtcbiAgICAgIHdpbmRvdy5nYXBpLmxvYWQoXCJhdXRoMlwiLCBmdW5jdGlvbiAoKSB7XG4gICAgICAgIHdpbmRvdy5nYXBpLmF1dGgyLmluaXQoKTtcbiAgICAgIH0pO1xuICAgIH0sXG5cbiAgICByZW5kZXJHb29nbGVBdXRoQnV0dG9uKCkge1xuICAgICAgd2luZG93LmdhcGkuc2lnbmluMi5yZW5kZXIoXCJnLXNpZ25pbjJcIiwge1xuICAgICAgICBvbnN1Y2Nlc3M6IHRoaXMub25TaWduSW5cbiAgICAgIH0pO1xuICAgIH1cbiAgfVxufTtcbjwvc2NyaXB0PlxuXG5cbjxzdHlsZT5cbiNhcHAge1xuICBmb250LWZhbWlseTogQXZlbmlyLCBIZWx2ZXRpY2EsIEFyaWFsLCBzYW5zLXNlcmlmO1xuICAtd2Via2l0LWZvbnQtc21vb3RoaW5nOiBhbnRpYWxpYXNlZDtcbiAgLW1vei1vc3gtZm9udC1zbW9vdGhpbmc6IGdyYXlzY2FsZTtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICBjb2xvcjogIzJjM2U1MDtcbn1cblxubmF2IHtcbiAgcGFkZGluZzogMzBweDtcbn1cblxubmF2IGEge1xuICBmb250LXdlaWdodDogYm9sZDtcbiAgY29sb3I6ICMyYzNlNTA7XG59XG5cbm5hdiBhLnJvdXRlci1saW5rLWV4YWN0LWFjdGl2ZSB7XG4gIGNvbG9yOiAjNDJiOTgzO1xufVxuPC9zdHlsZT5cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///./node_modules/@vue/vue-loader-v15/lib/index.js??vue-loader-options!./src/App.vue?vue&type=script&lang=js&\n");

/***/ })

},
/******/ function(__webpack_require__) { // webpackRuntimeModules
/******/ /* webpack/runtime/getFullHash */
/******/ !function() {
/******/ 	__webpack_require__.h = function() { return "a35bf5fc20269e35"; }
/******/ }();
/******/ 
/******/ }
);