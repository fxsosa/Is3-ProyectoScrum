"use strict";(self["webpackChunksso_google"]=self["webpackChunksso_google"]||[]).push([[988],{7149:function(t,e,s){s.d(e,{Z:function(){return _}});var i=s(998),a=function(){var t=this,e=t._self._c;return e(i.Z,[e("NavDefault"),e("main",{staticClass:"layoutDefault__main"},[t._t("default")],2),e("FooterDefault")],1)},r=[],n=s(6232),l=s(6190),o=s(5495),h=s(3687),u=function(){var t=this,e=t._self._c;return e(n.Z,{attrs:{app:"",absolute:"",color:"#683bce",src:s(2381),height:"50",dark:""},scopedSlots:t._u([{key:"img",fn:function({props:s}){return[e(o.Z,t._b({attrs:{gradient:"to top left, rgba(78, 221, 68, 0.8), rgba(62, 66, 244, 0.8)"}},"v-img",s,!1))]}}])},[e("div",{staticClass:"ml-4"},[e("h3",{staticClass:"title"},[t._v(" ScrumLAB ")])]),e(h.Z),t.$store.getters["usuario/esAdministrador"]?e(l.Z,{staticClass:"mr-2",attrs:{to:"/administracion",outlined:"",color:"white"}},[t._v(" Administración ")]):t._e(),e(l.Z,{staticClass:"mr-2",attrs:{outlined:"",color:"white",to:"/proyectos"}},[t._v(" Proyectos ")]),e(l.Z,{staticClass:"mr-2",attrs:{outlined:"",color:"white"},on:{click:t.logout}},[t._v(" Cerrar sesión ")])],1)},d=[],c={methods:{async logout(){await this.$store.dispatch("usuario/logout"),this.$router.push("/")}}},p=c,m=s(1001),v=(0,m.Z)(p,u,d,!1,null,"290ece1e",null),g=v.exports,f=s(9168),y={components:{NavDefault:g,FooterDefault:f.Z}},b=y,C=(0,m.Z)(b,a,r,!1,null,"65002767",null),_=C.exports},988:function(t,e,s){s.r(e),s.d(e,{default:function(){return H}});var i=s(9286),a=s(6190),r=s(9582),n=s(4886),l=s(2118),o=s(4324),h=s(5495),u=s(6878),d=s(8860),c=s(3037),p=s(6669),m=s(1444),v=s(7069),g=s(5352),f=s(4101),y=s(7678);const b=(0,y.Z)(u.Z,d.Z,p.Z,(0,c.d)("listItemGroup"),(0,m.d)("inputValue"));var C=b.extend().extend({name:"v-list-item",directives:{Ripple:v.Z},inject:{isInGroup:{default:!1},isInList:{default:!1},isInMenu:{default:!1},isInNav:{default:!1}},inheritAttrs:!1,props:{activeClass:{type:String,default(){return this.listItemGroup?this.listItemGroup.activeClass:""}},dense:Boolean,inactive:Boolean,link:Boolean,selectable:{type:Boolean},tag:{type:String,default:"div"},threeLine:Boolean,twoLine:Boolean,value:null},data:()=>({proxyClass:"v-list-item--active"}),computed:{classes(){return{"v-list-item":!0,...d.Z.options.computed.classes.call(this),"v-list-item--dense":this.dense,"v-list-item--disabled":this.disabled,"v-list-item--link":this.isClickable&&!this.inactive,"v-list-item--selectable":this.selectable,"v-list-item--three-line":this.threeLine,"v-list-item--two-line":this.twoLine,...this.themeClasses}},isClickable(){return Boolean(d.Z.options.computed.isClickable.call(this)||this.listItemGroup)}},created(){this.$attrs.hasOwnProperty("avatar")&&(0,f.Jk)("avatar",this)},methods:{click(t){t.detail&&this.$el.blur(),this.$emit("click",t),this.to||this.toggle()},genAttrs(){const t={"aria-disabled":!!this.disabled||void 0,tabindex:this.isClickable&&!this.disabled?0:-1,...this.$attrs};return this.$attrs.hasOwnProperty("role")||this.isInNav||(this.isInGroup?(t.role="option",t["aria-selected"]=String(this.isActive)):this.isInMenu?(t.role=this.isClickable?"menuitem":void 0,t.id=t.id||`list-item-${this._uid}`):this.isInList&&(t.role="listitem")),t},toggle(){this.to&&void 0===this.inputValue&&(this.isActive=!this.isActive),this.$emit("change")}},render(t){let{tag:e,data:s}=this.generateRouteLink();s.attrs={...s.attrs,...this.genAttrs()},s[this.to?"nativeOn":"on"]={...s[this.to?"nativeOn":"on"],keydown:t=>{this.disabled||(t.keyCode===g.Do.enter&&this.click(t),this.$emit("keydown",t))}},this.inactive&&(e="div"),this.inactive&&this.to&&(s.on=s.nativeOn,delete s.nativeOn);const i=this.$scopedSlots.default?this.$scopedSlots.default({active:this.isActive,toggle:this.toggle}):this.$slots.default;return t(e,this.isActive?this.setTextColor(this.color,s):s,i)}}),_=s(3423),Z=_.Z,I=Z.extend({name:"v-list-item-avatar",props:{horizontal:Boolean,size:{type:[Number,String],default:40}},computed:{classes(){return{"v-list-item__avatar--horizontal":this.horizontal,...Z.options.computed.classes.call(this),"v-avatar--tile":this.tile||this.horizontal}}},render(t){const e=Z.options.render.call(this,t);return e.data=e.data||{},e.data.staticClass+=" v-list-item__avatar",e}}),x=s(7423),$=(x.Z.extend().extend({name:"v-list",provide(){return{isInList:!0,list:this}},inject:{isInMenu:{default:!1},isInNav:{default:!1}},props:{dense:Boolean,disabled:Boolean,expand:Boolean,flat:Boolean,nav:Boolean,rounded:Boolean,subheader:Boolean,threeLine:Boolean,twoLine:Boolean},data:()=>({groups:[]}),computed:{classes(){return{...x.Z.options.computed.classes.call(this),"v-list--dense":this.dense,"v-list--disabled":this.disabled,"v-list--flat":this.flat,"v-list--nav":this.nav,"v-list--rounded":this.rounded,"v-list--subheader":this.subheader,"v-list--two-line":this.twoLine,"v-list--three-line":this.threeLine}}},methods:{register(t){this.groups.push(t)},unregister(t){const e=this.groups.findIndex((e=>e._uid===t._uid));e>-1&&this.groups.splice(e,1)},listClick(t){if(!this.expand)for(const e of this.groups)e.toggle(t)}},render(t){const e={staticClass:"v-list",class:this.classes,style:this.styles,attrs:{role:this.isInNav||this.isInMenu?void 0:"list",...this.attrs$}};return t(this.tag,this.setBackgroundColor(this.color,e),[this.$slots.default])}}),s(2240)),k=s(538),A=k.ZP.extend({name:"v-list-item-icon",functional:!0,render(t,{data:e,children:s}){return e.staticClass=`v-list-item__icon ${e.staticClass||""}`.trim(),t("div",e,s)}}),B=s(2500),S=s(8223),V=s(4712),w=s(7394);const P=(0,y.Z)(B.Z,S.Z,u.Z,(0,V.f)("list"),m.Z);P.extend().extend({name:"v-list-group",directives:{ripple:v.Z},props:{activeClass:{type:String,default:""},appendIcon:{type:String,default:"$expand"},color:{type:String,default:"primary"},disabled:Boolean,group:[String,RegExp],noAction:Boolean,prependIcon:String,ripple:{type:[Boolean,Object],default:!0},subGroup:Boolean},computed:{classes(){return{"v-list-group--active":this.isActive,"v-list-group--disabled":this.disabled,"v-list-group--no-action":this.noAction,"v-list-group--sub-group":this.subGroup}}},watch:{isActive(t){!this.subGroup&&t&&this.list&&this.list.listClick(this._uid)},$route:"onRouteChange"},created(){this.list&&this.list.register(this),this.group&&this.$route&&null==this.value&&(this.isActive=this.matchRoute(this.$route.path))},beforeDestroy(){this.list&&this.list.unregister(this)},methods:{click(t){this.disabled||(this.isBooted=!0,this.$emit("click",t),this.$nextTick((()=>this.isActive=!this.isActive)))},genIcon(t){return this.$createElement($.Z,t)},genAppendIcon(){const t=!this.subGroup&&this.appendIcon;return t||this.$slots.appendIcon?this.$createElement(A,{staticClass:"v-list-group__header__append-icon"},[this.$slots.appendIcon||this.genIcon(t)]):null},genHeader(){return this.$createElement(C,{staticClass:"v-list-group__header",attrs:{"aria-expanded":String(this.isActive),role:"button"},class:{[this.activeClass]:this.isActive},props:{inputValue:this.isActive},directives:[{name:"ripple",value:this.ripple}],on:{...this.listeners$,click:this.click}},[this.genPrependIcon(),this.$slots.activator,this.genAppendIcon()])},genItems(){return this.showLazyContent((()=>[this.$createElement("div",{staticClass:"v-list-group__items",directives:[{name:"show",value:this.isActive}]},(0,g.z9)(this))]))},genPrependIcon(){const t=this.subGroup&&null==this.prependIcon?"$subgroup":this.prependIcon;return t||this.$slots.prependIcon?this.$createElement(A,{staticClass:"v-list-group__header__prepend-icon"},[this.$slots.prependIcon||this.genIcon(t)]):null},onRouteChange(t){if(!this.group)return;const e=this.matchRoute(t.path);e&&this.isActive!==e&&this.list&&this.list.listClick(this._uid),this.isActive=e},toggle(t){const e=this._uid===t;e&&(this.isBooted=!0),this.$nextTick((()=>this.isActive=e))},matchRoute(t){return null!==t.match(this.group)}},render(t){return t("div",this.setTextColor(this.isActive&&this.color,{staticClass:"v-list-group",class:this.classes}),[this.genHeader(),t(w.Fx,this.genItems())])}});var L=s(6174),z=s(3457);const D=(0,y.Z)(L.Z,z.Z,p.Z).extend({name:"base-item-group",props:{activeClass:{type:String,default:"v-item--active"},mandatory:Boolean,max:{type:[Number,String],default:null},multiple:Boolean,tag:{type:String,default:"div"}},data(){return{internalLazyValue:void 0!==this.value?this.value:this.multiple?[]:void 0,items:[]}},computed:{classes(){return{"v-item-group":!0,...this.themeClasses}},selectedIndex(){return this.selectedItem&&this.items.indexOf(this.selectedItem)||-1},selectedItem(){if(!this.multiple)return this.selectedItems[0]},selectedItems(){return this.items.filter(((t,e)=>this.toggleMethod(this.getValue(t,e))))},selectedValues(){return null==this.internalValue?[]:Array.isArray(this.internalValue)?this.internalValue:[this.internalValue]},toggleMethod(){if(!this.multiple)return t=>this.valueComparator(this.internalValue,t);const t=this.internalValue;return Array.isArray(t)?e=>t.some((t=>this.valueComparator(t,e))):()=>!1}},watch:{internalValue:"updateItemsState",items:"updateItemsState"},created(){this.multiple&&!Array.isArray(this.internalValue)&&(0,f.Kd)("Model must be bound to an array if the multiple property is true.",this)},methods:{genData(){return{class:this.classes}},getValue(t,e){return void 0===t.value?e:t.value},onClick(t){this.updateInternalValue(this.getValue(t,this.items.indexOf(t)))},register(t){const e=this.items.push(t)-1;t.$on("change",(()=>this.onClick(t))),this.mandatory&&!this.selectedValues.length&&this.updateMandatory(),this.updateItem(t,e)},unregister(t){if(this._isDestroyed)return;const e=this.items.indexOf(t),s=this.getValue(t,e);this.items.splice(e,1);const i=this.selectedValues.indexOf(s);if(!(i<0)){if(!this.mandatory)return this.updateInternalValue(s);this.multiple&&Array.isArray(this.internalValue)?this.internalValue=this.internalValue.filter((t=>t!==s)):this.internalValue=void 0,this.selectedItems.length||this.updateMandatory(!0)}},updateItem(t,e){const s=this.getValue(t,e);t.isActive=this.toggleMethod(s)},updateItemsState(){this.$nextTick((()=>{if(this.mandatory&&!this.selectedItems.length)return this.updateMandatory();this.items.forEach(this.updateItem)}))},updateInternalValue(t){this.multiple?this.updateMultiple(t):this.updateSingle(t)},updateMandatory(t){if(!this.items.length)return;const e=this.items.slice();t&&e.reverse();const s=e.find((t=>!t.disabled));if(!s)return;const i=this.items.indexOf(s);this.updateInternalValue(this.getValue(s,i))},updateMultiple(t){const e=Array.isArray(this.internalValue)?this.internalValue:[],s=e.slice(),i=s.findIndex((e=>this.valueComparator(e,t)));this.mandatory&&i>-1&&s.length-1<1||null!=this.max&&i<0&&s.length+1>this.max||(i>-1?s.splice(i,1):s.push(t),this.internalValue=s)},updateSingle(t){const e=this.valueComparator(this.internalValue,t);this.mandatory&&e||(this.internalValue=e?void 0:t)}},render(t){return t(this.tag,this.genData(),this.$slots.default)}});D.extend({name:"v-item-group",provide(){return{itemGroup:this}}}),(0,y.Z)(D,u.Z).extend({name:"v-list-item-group",provide(){return{isInGroup:!0,listItemGroup:this}},computed:{classes(){return{...D.options.computed.classes.call(this),"v-list-item-group":!0}}},methods:{genData(){return this.setTextColor(this.color,{...D.options.methods.genData.call(this),attrs:{role:"listbox"}})}}}),k.ZP.extend({name:"v-list-item-action",functional:!0,render(t,{data:e,children:s=[]}){e.staticClass=e.staticClass?`v-list-item__action ${e.staticClass}`:"v-list-item__action";const i=s.filter((t=>!1===t.isComment&&" "!==t.text));return i.length>1&&(e.staticClass+=" v-list-item__action--stack"),t("div",e,s)}});(0,g.Ji)("v-list-item__action-text","span");const O=(0,g.Ji)("v-list-item__content","div"),M=(0,g.Ji)("v-list-item__title","div"),G=(0,g.Ji)("v-list-item__subtitle","div");var E=function(){var t=this,e=t._self._c;return e("LayoutDefault",[e("div",{staticClass:"container"},[e(i.Z,{attrs:{items:t.items},scopedSlots:t._u([{key:"divider",fn:function(){return[e(o.Z,[t._v("mdi-forward")])]},proxy:!0}])})],1),e(l.Z,[e("h3",[t._v("LISTA DE MIS PROYECTOS")]),t._l(t.listaProyectos,(function(s,i){return e("div",{key:i},[e(r.Z,{staticClass:"mx-auto",attrs:{"max-width":"344",outlined:""}},[e(C,{attrs:{"three-line":""}},[e(O,[e("div",{staticClass:"text-overline mb-4"},[t._v(" Proyecto Scrum ")]),e(M,{staticClass:"text-h5 mb-1"},[t._v(" "+t._s(s.fields.nombre)+" ")]),e(G,[t._v(t._s(s.fields.descripcion))])],1),e(I,{attrs:{tile:"",size:"80",color:"grey"}},[e(h.Z,{attrs:{src:"https://source.unsplash.com/random/900x900?sig="+100*Math.random()}})],1)],1),e(n.h7,[e(a.Z,{attrs:{outlined:"",rounded:"",text:""},on:{click:function(e){return t.irAProyecto(s.pk)}}},[t._v(" Ir al proyecto ")])],1)],1)],1)}))],2)],1)},R=[],T=s(7149),j=s(1725),N={name:"",data(){return{listaProyectos:[],items:[{text:"Inicio",disabled:!1,href:"/inicio"},{text:"Proyectos",disabled:!0,href:"/proyectos"}]}},components:{LayoutDefault:T.Z},async mounted(){let t=this.$store.state.usuario.idToken,e={headers:{"Content-Type":"application/json",Authorization:`Bearer ${t}`}},s=await j.Z.get("/usuario/proyectos",e);this.listaProyectos=s.data,console.log(this.listaProyectos)},methods:{async irAProyecto(t){this.$router.push(`/proyecto/${t}`)}}},J=N,F=s(1001),W=(0,F.Z)(J,E,R,!1,null,null,null),H=W.exports},1884:function(){},3423:function(t,e,s){s.d(e,{Z:function(){return o}});var i=s(6878),a=s(8846),r=s(2637),n=s(5352),l=s(7678),o=(0,l.Z)(i.Z,a.Z,r.Z).extend({name:"v-avatar",props:{left:Boolean,right:Boolean,size:{type:[Number,String],default:48}},computed:{classes(){return{"v-avatar--left":this.left,"v-avatar--right":this.right,...this.roundedClasses}},styles(){return{height:(0,n.kb)(this.size),minWidth:(0,n.kb)(this.size),width:(0,n.kb)(this.size),...this.measurableStyles}}},render(t){const e={staticClass:"v-avatar",class:this.classes,style:this.styles,on:this.$listeners};return t("div",this.setBackgroundColor(this.color,e),this.$slots.default)}})},9286:function(t,e,s){s.d(e,{Z:function(){return h}});var i=s(8860),a=s(7678),r=(0,a.Z)(i.Z).extend({name:"v-breadcrumbs-item",props:{activeClass:{type:String,default:"v-breadcrumbs__item--disabled"},ripple:{type:[Boolean,Object],default:!1}},computed:{classes(){return{"v-breadcrumbs__item":!0,[this.activeClass]:this.disabled}}},render(t){const{tag:e,data:s}=this.generateRouteLink();return t("li",[t(e,{...s,attrs:{...s.attrs,"aria-current":this.isActive&&this.isLink?"page":void 0}},this.$slots.default)])}}),n=s(5352),l=(0,n.Ji)("v-breadcrumbs__divider","li"),o=s(6669),h=(0,a.Z)(o.Z).extend({name:"v-breadcrumbs",props:{divider:{type:String,default:"/"},items:{type:Array,default:()=>[]},large:Boolean},computed:{classes(){return{"v-breadcrumbs--large":this.large,...this.themeClasses}}},methods:{genDivider(){return this.$createElement(l,this.$slots.divider?this.$slots.divider:this.divider)},genItems(){const t=[],e=!!this.$scopedSlots.item,s=[];for(let i=0;i<this.items.length;i++){const a=this.items[i];s.push(a.text),e?t.push(this.$scopedSlots.item({item:a})):t.push(this.$createElement(r,{key:s.join("."),props:a},[a.text])),i<this.items.length-1&&t.push(this.genDivider())}return t}},render(t){const e=this.$slots.default||this.genItems();return t("ul",{staticClass:"v-breadcrumbs",class:this.classes},e)}})},2118:function(t,e,s){s.d(e,{Z:function(){return n}});s(9027),s(1884);var i=s(538);function a(t){return i.ZP.extend({name:`v-${t}`,functional:!0,props:{id:String,tag:{type:String,default:"div"}},render(e,{props:s,data:i,children:a}){i.staticClass=`${t} ${i.staticClass||""}`.trim();const{attrs:r}=i;if(r){i.attrs={};const t=Object.keys(r).filter((t=>{if("slot"===t)return!1;const e=r[t];return t.startsWith("data-")?(i.attrs[t]=e,!1):e||"string"===typeof e}));t.length&&(i.staticClass+=` ${t.join(" ")}`)}return s.id&&(i.domProps=i.domProps||{},i.domProps.id=s.id),e(s.tag,i,a)}})}var r=s(1767),n=a("container").extend({name:"v-container",functional:!0,props:{id:String,tag:{type:String,default:"div"},fluid:{type:Boolean,default:!1}},render(t,{props:e,data:s,children:i}){let a;const{attrs:n}=s;return n&&(s.attrs={},a=Object.keys(n).filter((t=>{if("slot"===t)return!1;const e=n[t];return t.startsWith("data-")?(s.attrs[t]=e,!1):e||"string"===typeof e}))),e.id&&(s.domProps=s.domProps||{},s.domProps.id=e.id),t(e.tag,(0,r.ZP)(s,{staticClass:"container",class:Array({"container--fluid":e.fluid}).concat(a||[])}),i)}})},2240:function(t,e,s){var i=s(4324);e["Z"]=i.Z},8223:function(t,e,s){var i=s(4101),a=s(538);e["Z"]=a.ZP.extend().extend({name:"bootable",props:{eager:Boolean},data:()=>({isBooted:!1}),computed:{hasContent(){return this.isBooted||this.eager||this.isActive}},watch:{isActive(){this.isBooted=!0}},created(){"lazy"in this.$attrs&&(0,i.Jk)("lazy",this)},methods:{showLazyContent(t){return this.hasContent&&t?t():[this.$createElement()]}}})},6174:function(t,e,s){var i=s(538),a=s(5352);e["Z"]=i.ZP.extend({name:"comparable",props:{valueComparator:{type:Function,default:a.vZ}}})}}]);
//# sourceMappingURL=988.js.33a4b867ba8a.map