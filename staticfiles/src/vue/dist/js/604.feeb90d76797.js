"use strict";(self["webpackChunksso_google"]=self["webpackChunksso_google"]||[]).push([[604],{5604:function(e,t,i){i.r(t),i.d(t,{default:function(){return D}});var n=i(6190),s=i(266),a=i(9223),l=i(5495),o=i(1713),r=function(){var e=this,t=e._self._c;return t("LayoutGuest",[t("div",{staticClass:"contenedor_inicio container"},[t("div",{staticClass:"text-center"},[t("h1",{staticClass:"title_presentation"},[e._v("Login With Google")]),t("div",{staticClass:"container ml-5 mt-5 mb-15"},[e.$store.getters["usuario/estaAutenticado"]?t(n.Z,{attrs:{color:"#3e41f4","x-large":"",outlined:"",text:"",to:"/inicio"}},[e._v(" Comenzar ")]):t("div",{attrs:{id:"signInDiv"}})],1)]),t(a.Z,{staticClass:"my-15"}),e._l(e.items,(function(i){return t(o.Z,{key:i.id,staticClass:"contenedor_informacion"},[2===i.type?t(s.Z,{attrs:{cols:"12",md:"6"}},[t(l.Z,{attrs:{src:i.img}})],1):e._e(),t(s.Z,{attrs:{cols:"12",md:"6"}},[t("h2",{style:e.getColorTitulo(i)},[e._v(" "+e._s(i.title)+" ")]),t(a.Z,{staticClass:"mb-8"}),t("p",[e._v(" "+e._s(i.description)+" ")])],1),1===i.type?t(s.Z,{attrs:{cols:"12",md:"6"}},[t(l.Z,{attrs:{src:i.img}})],1):e._e()],1)}))],2)])},u=[],c=i(998),d=function(){var e=this,t=e._self._c;return t(c.Z,[t("NavGuest"),t("main",{staticClass:"layoutDefault__main"},[e._t("default")],2),t("FooterDefault")],1)},g=[],m=i(6232),p=i(3687),f=function(){var e=this,t=e._self._c;return t(m.Z,{attrs:{app:"",absolute:"",color:"#683bce",src:i(2381),height:"80",dark:""},scopedSlots:e._u([{key:"img",fn:function({props:i}){return[t(l.Z,e._b({attrs:{gradient:"to top left, rgba(78, 221, 68, 0.8), rgba(62, 66, 244, 0.8)"}},"v-img",i,!1))]}}])},[t("div",{staticClass:"ml-4"},[t("h3",{staticClass:"title"},[e._v(" ScrumLAB ")])]),t(p.Z),e.$store.getters["usuario/estaAutenticado"]?t(n.Z,{staticClass:"white--text",attrs:{outlined:"",to:"/inicio"}},[e._v(" Comenzar ")]):e._e()],1)},v=[],y={},b=y,h=i(1001),C=(0,h.Z)(b,f,v,!1,null,"85c3f498",null),_=C.exports,S=i(9168),Z={components:{NavGuest:_,FooterDefault:S.Z}},x=Z,j=(0,h.Z)(x,d,g,!1,null,"4e51c08c",null),L=j.exports;const k={GOOGLE_CLIENT_ID:"619211861447-4ct17vkmnl8v694j8c7pb61a2rniurrb.apps.googleusercontent.com"};var w=k,q={name:"HomeView",data(){return{client:null,items:[{type:1,title:"Lorem ipsum dolor sit amet",description:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nec mi felis. \n            Praesent vitae congue mi. Sed efficitur ante sapien, eget tristique sapien \n            sollicitudin vitae. Aliquam vel tellus id diam pulvinar hendrerit eget \n            quis mi. Cras magna ligula, volutpat quis massa in, gravida laoreet magna. \n            In id nisi risus. Vestibulum bibendum maximus maximus. Sed porta mauris \n            eget dolor scelerisque feugiat. Ut odio mi, eleifend sed malesuada eu, \n            fringilla et urna. Donec luctus ex sed ligula auctor sagittis. Suspendisse \n            sit amet risus nibh. ",img:i(7018)},{type:2,title:"Lorem ipsum dolor sit amet",description:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nec mi felis. \n            Praesent vitae congue mi. Sed efficitur ante sapien, eget tristique sapien \n            sollicitudin vitae. Aliquam vel tellus id diam pulvinar hendrerit eget \n            quis mi. Cras magna ligula, volutpat quis massa in, gravida laoreet magna. \n            In id nisi risus. Vestibulum bibendum maximus maximus. Sed porta mauris \n            eget dolor scelerisque feugiat. Ut odio mi, eleifend sed malesuada eu, \n            fringilla et urna. Donec luctus ex sed ligula auctor sagittis. Suspendisse \n            sit amet risus nibh. ",img:i(7018)},{type:1,title:"Lorem ipsum dolor sit amet",description:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nec mi felis. \n            Praesent vitae congue mi. Sed efficitur ante sapien, eget tristique sapien \n            sollicitudin vitae. Aliquam vel tellus id diam pulvinar hendrerit eget \n            quis mi. Cras magna ligula, volutpat quis massa in, gravida laoreet magna. \n            In id nisi risus. Vestibulum bibendum maximus maximus. Sed porta mauris \n            eget dolor scelerisque feugiat. Ut odio mi, eleifend sed malesuada eu, \n            fringilla et urna. Donec luctus ex sed ligula auctor sagittis. Suspendisse \n            sit amet risus nibh. ",img:i(7018)}]}},components:{LayoutGuest:L},methods:{getColorTitulo(e){return 1===e.type?"color: #3e42f4;":2===e.type?"color: #4edd44;":"#000000"},async callbackLogin(e){console.log("response",e);const t=e.credential;await this.$store.dispatch("usuario/login",{idToken:t}),this.$router.push("/inicio")},initClient(){console.log("google",google),this.client=google.accounts.id.initialize({client_id:w.GOOGLE_CLIENT_ID,callback:e=>this.callbackLogin(e)})}},created(){this.initClient()},mounted(){const e={theme:"filled_blue",size:"large",shape:"pill",text:"continue_with",width:"50"};google.accounts.id.prompt(),google.accounts.id.renderButton(document.getElementById("signInDiv"),e)}},$=q,G=(0,h.Z)($,r,u,!1,null,"04dcea76",null),D=G.exports},1884:function(){},266:function(e,t,i){i(1884);var n=i(538),s=i(1767),a=i(5352);const l=["sm","md","lg","xl"],o=(()=>l.reduce(((e,t)=>(e[t]={type:[Boolean,String,Number],default:!1},e)),{}))(),r=(()=>l.reduce(((e,t)=>(e["offset"+(0,a.jC)(t)]={type:[String,Number],default:null},e)),{}))(),u=(()=>l.reduce(((e,t)=>(e["order"+(0,a.jC)(t)]={type:[String,Number],default:null},e)),{}))(),c={col:Object.keys(o),offset:Object.keys(r),order:Object.keys(u)};function d(e,t,i){let n=e;if(null!=i&&!1!==i){if(t){const i=t.replace(e,"");n+=`-${i}`}return"col"!==e||""!==i&&!0!==i?(n+=`-${i}`,n.toLowerCase()):n.toLowerCase()}}const g=new Map;t["Z"]=n.ZP.extend({name:"v-col",functional:!0,props:{cols:{type:[Boolean,String,Number],default:!1},...o,offset:{type:[String,Number],default:null},...r,order:{type:[String,Number],default:null},...u,alignSelf:{type:String,default:null,validator:e=>["auto","start","end","center","baseline","stretch"].includes(e)},tag:{type:String,default:"div"}},render(e,{props:t,data:i,children:n,parent:a}){let l="";for(const s in t)l+=String(t[s]);let o=g.get(l);if(!o){let e;for(e in o=[],c)c[e].forEach((i=>{const n=t[i],s=d(e,i,n);s&&o.push(s)}));const i=o.some((e=>e.startsWith("col-")));o.push({col:!i||!t.cols,[`col-${t.cols}`]:t.cols,[`offset-${t.offset}`]:t.offset,[`order-${t.order}`]:t.order,[`align-self-${t.alignSelf}`]:t.alignSelf}),g.set(l,o)}return e(t.tag,(0,s.ZP)(i,{class:o}),n)}})},1713:function(e,t,i){i(1884);var n=i(538),s=i(1767),a=i(5352);const l=["sm","md","lg","xl"],o=["start","end","center"];function r(e,t){return l.reduce(((i,n)=>(i[e+(0,a.jC)(n)]=t(),i)),{})}const u=e=>[...o,"baseline","stretch"].includes(e),c=r("align",(()=>({type:String,default:null,validator:u}))),d=e=>[...o,"space-between","space-around"].includes(e),g=r("justify",(()=>({type:String,default:null,validator:d}))),m=e=>[...o,"space-between","space-around","stretch"].includes(e),p=r("alignContent",(()=>({type:String,default:null,validator:m}))),f={align:Object.keys(c),justify:Object.keys(g),alignContent:Object.keys(p)},v={align:"align",justify:"justify",alignContent:"align-content"};function y(e,t,i){let n=v[e];if(null!=i){if(t){const i=t.replace(e,"");n+=`-${i}`}return n+=`-${i}`,n.toLowerCase()}}const b=new Map;t["Z"]=n.ZP.extend({name:"v-row",functional:!0,props:{tag:{type:String,default:"div"},dense:Boolean,noGutters:Boolean,align:{type:String,default:null,validator:u},...c,justify:{type:String,default:null,validator:d},...g,alignContent:{type:String,default:null,validator:m},...p},render(e,{props:t,data:i,children:n}){let a="";for(const s in t)a+=String(t[s]);let l=b.get(a);if(!l){let e;for(e in l=[],f)f[e].forEach((i=>{const n=t[i],s=y(e,i,n);s&&l.push(s)}));l.push({"no-gutters":t.noGutters,"row--dense":t.dense,[`align-${t.align}`]:t.align,[`justify-${t.justify}`]:t.justify,[`align-content-${t.alignContent}`]:t.alignContent}),b.set(a,l)}return e(t.tag,(0,s.ZP)(i,{staticClass:"row",class:l}),n)}})},7018:function(e,t,i){e.exports=i.p+"img/trabajo_en_equipo.jpg"}}]);
//# sourceMappingURL=604.js.def6b18cbf60.map